"""PyFly To-Do entry point script."""

from aviation.cli import app


def main():
    print("starting main..")
    app(prog_name="pyfly")


if __name__ == "__main__":
    main()