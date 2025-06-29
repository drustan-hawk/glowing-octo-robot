from pathlib import Path

import numpy as np
from PIL import Image

from image_partition.domain.clip_service import ClipService


def test_clip_service_embed(tmp_path: Path) -> None:
    img = Image.new("RGB", (10, 10))
    path = tmp_path / "img.jpg"
    img.save(path)
    service = ClipService()
    emb1 = service.embed(path)
    emb2 = service.embed(path)
    assert emb1.shape == (512,)
    assert np.allclose(emb1, emb2)
    assert service is ClipService()
