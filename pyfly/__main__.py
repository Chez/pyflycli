"""RP To-Do entry point script."""

from pyfly import cli, __app_name__

from sqlmodel import create_engine, SQLModel, Session, Field, select


def main():
    print("starting main..")
    cli.app(prog_name=__app_name__)


if __name__ == "__main__":
    main()