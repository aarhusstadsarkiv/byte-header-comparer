### Imports
# Standard library
import argparse
from pathlib import Path
from typing import Optional

# Third-party libraries
from byte_header_comparer.multip import byte_header_comparer

# Local files


def get_version() -> str:
    """
    Get version number from pyproject.toml.

    Args:
        None

    Returns:
        str: The version number.
    """
    version: str = "Ukendt version"
    with open(Path(__file__).absolute().parent.parent / "pyproject.toml") as i:
        for line in i.readlines():
            if line.startswith("version"):
                version = line[line.index('"') + 1 : -2]
    return f"version {version}"


def cli(args: Optional[None] = None) -> None:
    """
    Comparer byte header of given folder.

    Args:
        args: Something something

    Returns:
        None
    """
    parser = argparse.ArgumentParser(
        description=(
            "Compares the first 1024 bytes of each file with the other "
            "files and finds longest common substrings"
        ),
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=get_version(),
        help="Display version number",
    )
    parser.add_argument(
        "-f",
        "--folder",
        metavar="folder",
        type=Path,
        required=True,
        help="Folder of files to compare.",
    )
    parser.add_argument(
        "-hs",
        "--header_size",
        nargs="?",
        default=1024,
        metavar="header_size",
        type=int,
        help="Optional size of header to compare.",
    )
    args = parser.parse_args(args)

    byte_header_comparer(args.folder, args.header_size)


if __name__ == "__main__":
    cli()
