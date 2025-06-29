import pytest

try:  # pragma: no cover - optional Qt runtime
    from PySide6.QtWidgets import QApplication, QMainWindow
except Exception:  # pragma: no cover - skip when Qt unavailable
    pytest.skip("PySide6 not available", allow_module_level=True)

from image_partition.ui.main_window_ui import Ui_MainWindow


def test_main_window_ui_setup(qtbot):
    _ = QApplication.instance() or QApplication([])
    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    qtbot.addWidget(window)
    # if setupUi fails, the test will raise
