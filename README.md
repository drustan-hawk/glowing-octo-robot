# Image Partitioner

A small PySide6 application that groups images by visual similarity using CLIP embeddings.

## Development

After editing a `.ui` file, regenerate the Python module:

```bash
uv run pyside6-uic path/to/file.ui -o path/to/file_ui.py
```

To launch the application after installing dependencies, run:

```bash
uv run image-partitioner
```
