import numpy as np
import pytest
from pathlib import Path

try:  # pragma: no cover - skip if Qt unavailable
    from PySide6.QtWidgets import QApplication
    from PySide6.QtCore import Qt
except Exception:
    pytest.skip("PySide6 not available", allow_module_level=True)

from image_partition.controller.main_controller import MainController
from image_partition.domain.clip_service import ClipService


def test_partition_images_assigns_best_group(qtbot, tmp_path, monkeypatch):
    folder = tmp_path / "imgs"
    folder.mkdir()
    g1 = folder / "g1.png"
    g2 = folder / "g2.png"
    u = folder / "u.png"
    for p in (g1, g2, u):
        p.write_bytes(b"\x00")

    def fake_embed(self, path: Path) -> np.ndarray:
        if path == g1:
            return np.ones(512, dtype=np.float32)
        if path == g2:
            return -np.ones(512, dtype=np.float32)
        if path == u:
            return np.full(512, 0.8, dtype=np.float32)
        return np.zeros(512, dtype=np.float32)

    monkeypatch.setattr(ClipService, "embed", fake_embed, raising=False)

    _ = QApplication.instance() or QApplication([])
    controller = MainController()
    controller._load_images(folder)
    controller.create_group("A")
    controller.create_group("B")

    controller.list_widget.setCurrentRow(0)
    controller.group_list.setCurrentRow(0)
    controller._assign_selected()  # g1 -> A

    controller.list_widget.setCurrentRow(1)
    controller.group_list.setCurrentRow(1)
    controller._assign_selected()  # g2 -> B

    controller.list_widget.clearSelection()
    controller._partition_images()

    item = controller.list_widget.item(2)
    assert item.toolTip() == "A"
    group_items = controller.result_tree.findItems("A", Qt.MatchFlag.MatchExactly)
    assert group_items and group_items[0].childCount() == 1
