from __future__ import annotations

from src.controller.main_controller import MainController


def main() -> None:
    controller = MainController()
    controller.run()


if __name__ == "__main__":
    main()
