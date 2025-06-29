from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import Qt, Slot, QSize
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QInputDialog,
    QFileDialog,
    QListWidgetItem,
    QMainWindow,
)

from ..domain.clip_service import ClipService
from ..domain.grouping import Group
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
        self.assign_button = self.ui.assignButton
        self.add_group_button.clicked.connect(self._add_group)
        self.assign_button.clicked.connect(self._assign_selected)
        self.list_widget.itemSelectionChanged.connect(self._highlight_membership)
        self.clip = ClipService()
        self.groups: dict[str, Group] = {}
        self.GROUPS_ROLE = Qt.ItemDataRole.UserRole + 1

    def create_group(self, name: str) -> None:
        if name and name not in self.groups:
            self.groups[name] = Group(name, [])
            self.group_list.addItem(name)

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

    @Slot()
    def _assign_selected(self) -> None:
        items = self.list_widget.selectedItems()
        groups = [item.text() for item in self.group_list.selectedItems()]
        for group_name in groups:
            group = self.groups.setdefault(group_name, Group(group_name, []))
            for it in items:
                path = it.data(Qt.ItemDataRole.UserRole)
                if path not in group.paths:
                    group.paths.append(path)
                memberships = set(it.data(self.GROUPS_ROLE) or [])
                memberships.add(group_name)
                it.setData(self.GROUPS_ROLE, list(memberships))
                it.setToolTip(", ".join(sorted(memberships)))
        self._highlight_membership()

    @Slot()
    def _open(self) -> None:
        folder = QFileDialog.getExistingDirectory(self.window, "Select images")
        if folder:
            self._load_images(Path(folder))

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
                _ = self.clip.embed(img)  # preload embedding

    def run(self) -> None:
        self.window.show()
        sys.exit(self.app.exec())
