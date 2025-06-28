# AGENTS.md – Image Partitioner (PySide6 + CLIP)

> **Scope**  Root of the repository – governs both human contributors _and_ AI coding agents.  
> **Tooling**  [`uv`](https://astral.sh/uv) for environment & package management (best‑practice workflow, June 2025).

---

## 1  Project Purpose

Build a cross‑platform desktop application that helps users **organise large image collections by semantic similarity**.

**Workflow**  
1. Load a directory of images.  
2. Drag any subset into user‑defined *seed groups*.  
3. Compute each group’s average CLIP embedding (**centroid**).  
4. Compute cosine similarity between every remaining image and each centroid.  
5. Assign each image to the group with the highest similarity (≥ τ).  
6. Iterate: user can tweak seeds, re‑cluster, and export results (CSV or folder tree).

Key technologies: **PySide6** for GUI, **OpenCLIP+Torch** for embeddings.

---

## 2  Quick‑Start‑Start (the 30‑second version)

```bash
# 1. Install uv (if not already) – see docs.astral.sh/uv for other methods
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Clone the repo
git clone https://github.com/drustan-hawk/glowing-octo-robot.git image‑partitioner
cd image‑partitioner

# 3. Generate virtual environment and install dependencies
uv sync
```
---


## 4  Project Structure Structure

```
.
├── src/                  # Python source code
│   ├── main.py           # PySide6 entry‑point
│   ├── ...
├── assets/               # App icon, sample images (read‑only)
├── docs/                 # Design notes, UML, AGENTS.md copies
├── pyproject.toml        # Project metadata & deps
├── .python-version       # '3.13' → uv’s default runtime
├── uv.lock               # **Committed** lockfile for reproducibility
└── .venv/                # Auto‑generated, **never** committed
```
---

## 5  Environment & Dependencies & Dependencies

| Category | Package(s) | Reason |
|----------|------------|--------|
| 🎛 GUI | `PySide6>=6.7` | Qt 6 widgets |
| 🧠 ML | `torch` (`>=2.3`)<br>`open_clip_torch>=2.24` | CLIP embeddings |
| 🔬 Math | `numpy` · `scikit-learn` | cosine similarity |
| ⚡ Accel (opt.) | `faiss-cpu` | large image sets |
| 🛠 Tooling | `black` · `ruff` · `pytest` · `pytest-qt` · `mypy` | enforced in CI |

All dependency declarations live in **`pyproject.toml`** under `[project]` and `[tool.uv.dev-dependencies]`; _never_ edit `uv.lock` by hand.

---

## 6  Command Cheatsheet

```bash
# Tests (headless Qt via xvfb)
uv run -m pytest -q

# Static analysis
uv run -m ruff .
uv run -m mypy src/
uv run -m black --check .
```
---

## 7  Coding Conventions Conventions

* **PEP 8** enforced by `ruff` & `black` (line length = 100).
* **MVC split**: `ui/` (pure `.ui`), `controller/` (signals/slots), `domain/` (logic, no Qt imports).
* All public APIs fully **type‑annotated**; run `mypy --strict`.
* Use `QCoreApplication.translate` for user‑visible strings (future i18n).

---

## 8  Embedding & Clustering Rules & Clustering Rules

1. **CLIP model** loaded once; managed by singleton `ClipService`.
2. Each image → 224×224 preprocess → `float32` embedding stored in cache dir.
3. **Centroid** = mean of group embeddings (unit‑normalised).
4. Assign images to group with highest cosine similarity (≥ τ, default 0).
5. Incremental centroid updates for interactivity.

---

## 9  UI/UX Guidelines/UX Guidelines

* Qt Quick Controls 2 with *Fusion* style.
* Thumbnail grid ↔ group list drag‑and‑drop seeding.
* Overlay similarity score (0–100 %).
* Heavy ops run in `QThreadPool`; progress → status bar.
* Persist last folder in `QSettings`.

---

## 10  Testing Strategy Strategy

| Layer | Goal | Tooling |
|-------|------|---------|
| Domain | deterministic math | `pytest`, `hypothesis` |
| Controller | correct Qt signal flow | `pytest-qt` |
| UI smoke | app launches | `xvfb-run uv run python -m src.main --test` |

Min. coverage ≥ 85 %.

---

## 11  Pull‑Request Checklist‑Request Checklist

1. Target `main`; keep PRs ≤ 300 LOC.
2. Describe user‑visible changes & link issue.
3. GitHub Actions must pass (`uv sync`, tests, linters).
4. UI changes → screenshot.
5. Verify every `.ui` file compiles via `uv run pyside6-uic src/ui/main_window.ui`.
6. After merge, nightly packages via **PyInstaller**.

---

## 12  Agent‑Specific Instructions‑Specific Instructions

* Prioritise **functional correctness**, then perf.
* Prefer composition over inheritance in controllers.
* Don’t regenerate large binaries; reference instead.
* When adding files, update `AUTHORS.md`.

---

## 13  Future Extensions Extensions

* **Multimodal centroids** (text prompt seeding).
* **Hierarchical grouping**.
* **faiss‑gpu** when CUDA present.
* **Export plug‑ins** – Adobe Bridge, JSON manifest.

---

*(End of AGENTS.md ‑ uv best‑practice edition)*

