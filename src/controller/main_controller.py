from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import QFile, QIODevice, Slot
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
)
from typing import cast

from ..domain.clip_service import ClipService


class MainController:
    """Application controller connecting UI and domain."""

    def __init__(self) -> None:
        self.app = QApplication(sys.argv)
        self.window = self._load_ui()
        main = cast(QMainWindow, self.window.findChild(QMainWindow))
        assert main is not None
        main.setWindowTitle("Image Partitioner")
        main.resize(640, 480)
        main.actionOpen.triggered.connect(self._open)  # type: ignore[attr-defined]
        main.actionExit.triggered.connect(self.app.quit)  # type: ignore[attr-defined]
        widget = cast(QListWidget, self.window.findChild(QListWidget, "listWidget"))
        assert widget is not None
        self.list_widget = widget
        self.clip = ClipService()

    def _load_ui(self) -> QMainWindow:
        loader = QUiLoader()
        path = Path(__file__).resolve().parents[1] / "ui" / "main_window.ui"
        file = QFile(str(path))
        file.open(QIODevice.ReadOnly)  # type: ignore[attr-defined]
        ui = loader.load(file)
        file.close()
        return cast(QMainWindow, ui)

    @Slot()
    def _open(self) -> None:
        folder = QFileDialog.getExistingDirectory(self.window, "Select images")
        if folder:
            self._load_images(Path(folder))

    def _load_images(self, folder: Path) -> None:
        self.list_widget.clear()
        for img in folder.iterdir():
            if img.suffix.lower() in {".png", ".jpg", ".jpeg"}:
                item = QListWidgetItem(img.name)
                self.list_widget.addItem(item)
                _ = self.clip.embed(img)  # preload embedding

    def run(self) -> None:
        self.window.show()
        sys.exit(self.app.exec())
