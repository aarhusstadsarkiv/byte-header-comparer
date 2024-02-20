### Imports
# Standard library
from pathlib import Path
from typing import Generator

# Third-party libraries
import pytest
from click.testing import CliRunner

# Local files
from byte_header_comparer.cli import cli


@pytest.fixture()
def cli_run():
    return CliRunner()


class TestCli:
    def test_with_valid_input(self, cli_run: CliRunner):
        # Run digiarch on AARS.TEST.
        # test_db: Path = test_data / "AARS.TEST" / "_metadata" / "files.db"
        # print(test_db)
        args = ["--folder" "aaa"]#["--threshold=20", str(test_db_copy), str(test_out), "master"]
        result = cli_run.invoke(cli, args)
        assert result.exit_code == 0