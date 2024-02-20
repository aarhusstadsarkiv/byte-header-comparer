### Imports
# Standard library
from pathlib import Path

# Third-party libraries
import pytest

# Local files


@pytest.fixture()
def path_to_1st_file_bin() -> Path:
    return Path("tests/test_data/1st_file.bin")


@pytest.fixture()
def list_of_path_to_1st_file_bin() -> Path:
    return [Path("tests/test_data/1st_file.bin")]


@pytest.fixture()
def path_to_test_folder_1() -> Path:
    return Path("tests/test_data/test_folder_1")