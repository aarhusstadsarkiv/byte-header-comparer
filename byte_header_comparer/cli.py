### Imports
# Standard library
from pathlib import Path

# Third-party libraries
import click
from click.core import Context as ClickContext

# Local files
from byte_header_comparer.multip import byte_header_comparer


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
    return f"{version}"


@click.group(invoke_without_command=True)
@click.version_option(get_version())
@click.option("-f", "--folder", "folder", type=Path, help="Folder of files to compare.")
@click.option("-hs", "--header_size", "header_size", type=int, default=1024, help="Optional size of header to compare.")
@click.pass_context
def cli(ctx: ClickContext, folder: Path, header_size: int):
    byte_header_comparer(folder, header_size)


if __name__ == "__main__":
    cli()
