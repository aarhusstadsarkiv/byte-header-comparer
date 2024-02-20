### Imports
# Standard library
from pathlib import Path
from typing import Generator

# Third-party libraries
import pytest

# Local files
from byte_header_comparer.multip import (
    read_bytes, 
    read_files_binary, 
    hexify_binary_file, 
    longest_common_hex_substring, 
    byte_header_comparer,
    OnlyOneFileError
)


class TestMultip:
    def test_read_bytes(self, path_to_1st_file_bin: Path) -> None:
        for b in read_bytes(path_to_1st_file_bin, 1):
            i = int.from_bytes(b, byteorder="big")

            assert bin(i) == bin(0b01001000)
    
    def test_read_bytes_return_type(self, path_to_1st_file_bin: Path) -> None:
        generator = read_bytes(path_to_1st_file_bin, 1)

        assert isinstance(generator, Generator)

    def test_read_files_binary(self, list_of_path_to_1st_file_bin: list[Path]) -> None:
        allfiles = read_files_binary(list_of_path_to_1st_file_bin, 2)

        assert allfiles[0][0] == bin(0b01001000)
        assert allfiles[0][1] == bin(0b01100101)
    
    def test_hexify_binary_file(self, list_of_path_to_1st_file_bin: list[Path]) -> None:
        allfiles = read_files_binary(list_of_path_to_1st_file_bin, 2)

        hex_string_files = hexify_binary_file(allfiles)

        assert hex_string_files[0] == "4865"
    
    def test_longest_common_hex_substring(self) -> None:
        lcs = longest_common_hex_substring("abcdef", "mnopcdfg")

        assert lcs == "cd"
    
    def test_invalide_folder(self, path_to_test_folder_1: Path) -> None:
        with pytest.raises(OnlyOneFileError):
            byte_header_comparer(path_to_test_folder_1)