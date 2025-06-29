from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np

from .clip_service import ClipService


@dataclass
class Group:
    name: str
    paths: list[Path]


def compute_centroid(group: Group, service: ClipService) -> np.ndarray:
    """Return the unit-normalised average embedding for a group."""
    if not group.paths:
        return np.zeros(512, dtype=np.float32)

    embeddings = [service.embed(path) for path in group.paths]
    arr = np.vstack(embeddings).astype(np.float32)
    centroid = arr.mean(axis=0)
    norm = np.linalg.norm(centroid)
    if norm == 0:
        return centroid
    return centroid / norm
