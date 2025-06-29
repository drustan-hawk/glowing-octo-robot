from pathlib import Path

import numpy as np

from image_partition.domain.grouping import Group, compute_centroid


class DummyService:
    def embed(self, path: Path) -> np.ndarray:  # pragma: no cover - simple stub
        return np.ones(512, dtype=np.float32)


def test_compute_centroid_normalized(tmp_path: Path) -> None:
    img1 = tmp_path / "a.png"
    img2 = tmp_path / "b.png"
    img1.write_bytes(b"\x00")
    img2.write_bytes(b"\x00")
    group = Group("dummy", [img1, img2])
    centroid = compute_centroid(group, DummyService())
    assert centroid.shape == (512,)
    np.testing.assert_allclose(np.linalg.norm(centroid), 1.0, atol=1e-6)
