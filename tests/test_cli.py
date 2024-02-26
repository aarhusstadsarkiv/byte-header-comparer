### Imports
# Standard library
from pathlib import Path

# Third-party libraries
import pytest

# Local files
from byte_header_comparer.cli import cli
from byte_header_comparer.multip import OnlyOneFileError


class TestCli:
    def test_invalid_direcotry(self) -> None:
        """Test if the cli raise SystemExit if the path leads to nothing."""
        with pytest.raises(SystemExit):
           cli(["--folder", "invalid\path\to\nothing"])
    
    def test_OnlyOneFileError(self, path_to_test_folder_1: Path) -> None:
        """Test if the cli/multip raise OnlyOneFileError if the folder only contains one file."""
        with pytest.raises(OnlyOneFileError):
           cli(["--folder", path_to_test_folder_1])

    def test_valid_run(self, capsys, path_to_test_folder_2: Path) -> None:
        """Test if the cli runs without problems given a vaild folder."""
        cli(["--folder", path_to_test_folder_2])
        captured = capsys.readouterr()

        assert "Header size is 1024" in captured.out
        assert "2/2" in captured.out
        assert "626c6120626c6120626c61" in captured.out
    
    def test_valid_run_header_size(self, capsys, path_to_test_folder_2: Path) -> None:
        """Test if the cli runs without problems given a vaild folder and if the header size have been change."""
        cli(["--header_size", "5", "--folder", path_to_test_folder_2])
        captured = capsys.readouterr()

        assert "Header size is 5" in captured.out
        assert "2/2" in captured.out
        assert "626c612062" in captured.out
