import pytest

try:  # pragma: no cover - optional Qt runtime
    from PySide6.QtWidgets import QApplication, QMainWindow
except Exception:  # pragma: no cover - skip when Qt unavailable
    pytest.skip("PySide6 not available", allow_module_level=True)

from image_partition.ui.main_window_ui import Ui_MainWindow
from image_partition.controller.main_controller import MainController
from PIL import Image


def test_main_window_ui_setup(qtbot):
    _ = QApplication.instance() or QApplication([])
    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    qtbot.addWidget(window)
    # if setupUi fails, the test will raise


def test_load_images_thumbnail(qtbot, tmp_path):
    folder = tmp_path / "imgs"
    folder.mkdir()
    img = Image.new("RGB", (10, 10))
    path = folder / "sample.png"
    img.save(path)

    _ = QApplication.instance() or QApplication([])
    controller = MainController()
    controller._load_images(folder)
    qtbot.addWidget(controller.window)

    item = controller.list_widget.item(0)
    assert item.text() == "sample.png"
    assert not item.icon().isNull()
