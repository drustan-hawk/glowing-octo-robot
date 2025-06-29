from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import Qt, Slot, QSize
from PySide6.QtGui import QIcon, QPixmap, QColor
from PySide6.QtWidgets import (
    QApplication,
    QInputDialog,
    QDoubleSpinBox,
    QFileDialog,
    QListWidgetItem,
    QMainWindow,
    QTreeWidgetItem,
)

from ..domain.clip_service import ClipService
from ..domain.grouping import Group, compute_centroid
import numpy as np
from ..ui.main_window_ui import Ui_MainWindow


class MainController:
    """Application controller connecting UI and domain."""

    def __init__(self) -> None:
        self.app = QApplication(sys.argv)
        self.window = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.window)
        self.window.setWindowTitle("Image Partitioner")
        self.window.resize(640, 480)
        self.ui.actionOpen.triggered.connect(self._open)
        self.ui.actionExit.triggered.connect(self.app.quit)
        self.list_widget = self.ui.listWidget
        self.group_list = self.ui.groupListWidget
        self.add_group_button = self.ui.addGroupButton
        self.threshold_spinbox: QDoubleSpinBox = self.ui.thresholdSpinBox
        self.assign_button = self.ui.assignButton
        self.partition_button = self.ui.partitionButton
        self.result_tree = self.ui.resultTreeWidget
        self.add_group_button.clicked.connect(self._add_group)
        self.assign_button.clicked.connect(self._assign_selected)
        self.partition_button.clicked.connect(self._partition_images)
        self.list_widget.itemSelectionChanged.connect(self._highlight_membership)
        self.clip = ClipService()
        self.groups: dict[str, Group] = {}
        self.group_colors: dict[str, QColor] = {}
        self._color_index = 0
        self.GROUPS_ROLE = Qt.ItemDataRole.UserRole + 1

    def create_group(self, name: str, threshold: float | None = None) -> None:
        if name and name not in self.groups:
            if threshold is None:
                threshold = float(self.threshold_spinbox.value())
            self.groups[name] = Group(name, [], threshold)
            item = QListWidgetItem(name)
            color = QColor.fromHsv((self._color_index * 60) % 360, 160, 255)
            self.group_colors[name] = color
            self._color_index += 1
            item.setBackground(color)
            self.group_list.addItem(item)

    @Slot()
    def _add_group(self) -> None:
        name, ok = QInputDialog.getText(self.window, "Add Group", "Group name:")
        if ok:
            self.create_group(name)

    @Slot()
    def _highlight_membership(self) -> None:
        selected = self.list_widget.selectedItems()
        if not selected:
            self.group_list.clearSelection()
            self.window.statusBar().clearMessage()
            return
        memberships: set[str] = set()
        for it in selected:
            memberships.update(it.data(self.GROUPS_ROLE) or [])
        for i in range(self.group_list.count()):
            grp_item = self.group_list.item(i)
            grp_item.setSelected(grp_item.text() in memberships)
        if memberships:
            self.window.statusBar().showMessage(", ".join(sorted(memberships)))

    def _update_item_visual(self, item: QListWidgetItem) -> None:
        groups = item.data(self.GROUPS_ROLE) or []
        if not groups:
            item.setBackground(QColor())
            return
        color = self.group_colors.get(groups[0])
        if color:
            item.setBackground(color)

    @Slot()
    def _assign_selected(self) -> None:
        items = self.list_widget.selectedItems()
        groups = [item.text() for item in self.group_list.selectedItems()]
        for group_name in groups:
            group = self.groups.setdefault(
                group_name, Group(group_name, [], float(self.threshold_spinbox.value()))
            )
            for it in items:
                path = it.data(Qt.ItemDataRole.UserRole)
                if path not in group.paths:
                    group.paths.append(path)
                memberships = set(it.data(self.GROUPS_ROLE) or [])
                memberships.add(group_name)
                it.setData(self.GROUPS_ROLE, list(memberships))
                it.setToolTip(", ".join(sorted(memberships)))
                self._update_item_visual(it)
        self._highlight_membership()

    @Slot()
    def _open(self) -> None:
        folder = QFileDialog.getExistingDirectory(self.window, "Select images")
        if folder:
            self._load_images(Path(folder))

    @Slot()
    def _partition_images(self) -> None:
        if not self.groups:
            return
        centroids = {
            name: compute_centroid(g, self.clip) for name, g in self.groups.items()
        }
        self.result_tree.clear()
        group_nodes: dict[str, QTreeWidgetItem] = {}
        for name in self.groups:
            node = QTreeWidgetItem([name])
            self.result_tree.addTopLevelItem(node)
            group_nodes[name] = node
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item.data(self.GROUPS_ROLE):
                continue
            path = item.data(Qt.ItemDataRole.UserRole)
            emb = self.clip.embed(path)
            best_name = None
            best_score = float("-inf")
            for name, centroid in centroids.items():
                if not centroid.any():
                    continue
                score = float(
                    np.dot(emb, centroid)
                    / (np.linalg.norm(emb) * np.linalg.norm(centroid))
                )
                if score >= self.groups[name].threshold and score > best_score:
                    best_score = score
                    best_name = name
            if best_name is None:
                continue
            memberships = [best_name]
            item.setData(self.GROUPS_ROLE, memberships)
            item.setToolTip(best_name)
            self.groups[best_name].paths.append(path)
            QTreeWidgetItem(group_nodes[best_name], [path.name])
            self._update_item_visual(item)
        self.result_tree.expandAll()

    def _load_images(self, folder: Path) -> None:
        self.list_widget.clear()
        for img in folder.iterdir():
            if img.suffix.lower() in {".png", ".jpg", ".jpeg"}:
                pixmap = QPixmap(str(img))
                if not pixmap.isNull():
                    thumb = pixmap.scaled(
                        100,
                        100,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation,
                    )
                    icon = QIcon(thumb)
                else:
                    icon = QIcon()
                item = QListWidgetItem(icon, img.name)
                item.setData(Qt.ItemDataRole.UserRole, img)
                item.setData(self.GROUPS_ROLE, [])
                item.setSizeHint(QSize(110, 120))
                self.list_widget.addItem(item)
                self._update_item_visual(item)
                _ = self.clip.embed(img)  # preload embedding

    def run(self) -> None:
        self.window.show()
        sys.exit(self.app.exec())
