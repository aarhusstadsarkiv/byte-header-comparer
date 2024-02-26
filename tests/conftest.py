### Imports
# Standard library
from pathlib import Path

# Third-party libraries
import pytest
from click.testing import CliRunner

# Local files


CONST_PATH_TO_MODULE = Path(".")


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
def path_to_1st_file_bin() -> Path:
    """
    Fixture used in
        test_multip
            test_read_bytes
            test_read_bytes_return_type
    """
    return Path("./tests/test_data/1st_file.bin")


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
def path_to_test_folder_1() -> str:
    """
    Fixture used in
        test_cli
            test_OnlyOneFileError
        test_multip
            test_invalid_folder
    """
    return "tests\\test_data\\test_folder_1"


@pytest.fixture()
def path_to_test_folder_2() -> Path:
    """
    Fixture used in
        test_cli
            test_valid_run
            test_valid_run_header_size
    """
    return CONST_PATH_TO_MODULE / "tests/test_data/test_folder_2"
