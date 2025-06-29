# Image Partitioner

A small PySide6 application that groups images by visual similarity using CLIP embeddings.

## Development

After editing `src/ui/main_window.ui`, regenerate the Python class:

```bash
uv run pyside6-uic src/ui/main_window.ui -o src/ui/main_window_ui.py
```
