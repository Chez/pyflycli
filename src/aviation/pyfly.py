"""PyFly To-Do entry point script."""

from aviation.cli import app


def pyfly():
    print("starting main..")
    app(prog_name="pyfly")


if __name__ == "__main__":
    pyfly()