### Imports
# Standard library
from pathlib import Path

# Third-party libraries
from click.testing import CliRunner

# Local files
from byte_header_comparer.cli import cli
from byte_header_comparer.multip import OnlyOneFileError


class TestCli:
    def test_invalid_direcotry(self, cli_run: CliRunner) -> None:
        """Test if the cli raise SystemExit if the path leads to nothing."""
        result = cli_run.invoke(cli, ["--folder", "invalid\\path\to\nothing"])
        assert isinstance(result.exception, SystemExit)

    def test_OnlyOneFileError(self, cli_run: CliRunner, path_to_test_folder_1: Path) -> None:
        """Test if the cli/multip raise OnlyOneFileError if the folder only contains one file."""
        result = cli_run.invoke(cli, ["--folder", str(path_to_test_folder_1)])
        assert isinstance(result.exception, OnlyOneFileError)

    def test_valid_run(self, cli_run: CliRunner, path_to_test_folder_2: Path) -> None:
        """Test if the cli runs without problems given a vaild folder."""
        result = cli_run.invoke(cli, ["--folder", str(path_to_test_folder_2)])

        assert result.exit_code == 0
        assert "Header size is 1024" in result.output
        assert "2/2" in result.output
        assert "626c6120626c6120626c61" in result.output

    def test_valid_run_header_size(
        self,
        cli_run: CliRunner,
        path_to_test_folder_2: Path,
    ) -> None:
        """Test if the cli runs without problems given a vaild folder and changes header size."""
        result = cli_run.invoke(cli, ["--header_size", "5", "--folder", str(path_to_test_folder_2)])

        assert result.exit_code == 0
        assert "Header size is 5" in result.output
        assert "2/2" in result.output
        assert "626c612062" in result.output
