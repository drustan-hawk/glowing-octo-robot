from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import Qt, Slot, QSize
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QListWidgetItem,
    QMainWindow,
)

from ..domain.clip_service import ClipService
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
        self.clip = ClipService()

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
                item.setSizeHint(QSize(110, 120))
                self.list_widget.addItem(item)
                _ = self.clip.embed(img)  # preload embedding

    def run(self) -> None:
        self.window.show()
        sys.exit(self.app.exec())
