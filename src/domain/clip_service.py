from __future__ import annotations

from pathlib import Path
from typing import Any, ClassVar

import numpy as np
from PIL import Image

try:  # optional heavy deps
    import open_clip  # type: ignore
    import torch  # type: ignore
except Exception:  # pragma: no cover - fallback when deps missing
    open_clip = None
    from typing import cast

    torch = cast(Any, None)


class ClipService:
    """Singleton wrapper around OpenCLIP for image embeddings."""

    _instance: ClassVar["ClipService" | None] = None

    def __new__(cls) -> "ClipService":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_model()
        return cls._instance

    def _init_model(self) -> None:
        if open_clip is None or torch is None:
            self.model: Any | None = None
            self.preprocess: Any | None = None
        else:
            model, _, preprocess = open_clip.create_model_and_transforms("ViT-B-32")
            self.model = model.eval()
            self.preprocess = preprocess

    def embed(self, image_path: Path) -> np.ndarray:
        if self.model is None or self.preprocess is None:
            return np.zeros(512, dtype=np.float32)
        img = Image.open(image_path).convert("RGB")
        tensor = self.preprocess(img).unsqueeze(0)
        if torch is None:
            return np.zeros(512, dtype=np.float32)
        with torch.no_grad():
            emb = self.model.encode_image(tensor)[0]
        return emb.cpu().numpy()
