### Imports
# Standard library
import os
from pathlib import Path

# Third-party libraries
import pytest
from click.testing import CliRunner

# Local files


@pytest.fixture()
def cli_run():
    """
    Fixture used in
        test_cli
            test_invalid_direcotry
            test_OnlyOneFileError
            test_valid_run
            test_valid_run_header_size
    """
    return CliRunner()


@pytest.fixture()
def root_path() -> Path:
    """
    Fixture used in another fixture
        conftest
            path_to_test_folder_1
            path_to_test_folder_2
    """
    return Path(__file__).parent.parent


@pytest.fixture()
def path_to_1st_file_bin() -> Path:
    """
    Fixture used in
        test_multip
            test_read_bytes
            test_read_bytes_return_type
    """
    return Path("tests/test_data/1st_file.bin")


@pytest.fixture()
def list_of_path_to_1st_file_bin() -> list[Path]:
    """
    Fixture used in
        test_multip
            test_read_files_binary
            test_hexify_binary_file
    """
    return [Path("tests/test_data/1st_file.bin")]


@pytest.fixture()
def path_to_test_folder_1(root_path: Path) -> str:
    """
    Fixture used in
        test_cli
            test_OnlyOneFileError
        test_multip
            test_invalid_folder
    """
    return os.path.join(str(root_path), "tests\\test_data\\test_folder_1")


@pytest.fixture()
def path_to_test_folder_2(root_path: Path) -> str:
    """
    Fixture used in
        test_cli
            test_valid_run
            test_valid_run_header_size
    """
    return os.path.join(str(root_path), "tests\\test_data\\test_folder_2")
