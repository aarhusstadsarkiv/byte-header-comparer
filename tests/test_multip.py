from src import multip
from pathlib import Path
from typing import Generator

filenames: list[Path] = [Path("tests/1st_file.bin")]


def test_read_bytes():

    filename = Path("tests/1st_file.bin")

    for b in multip.read_bytes(filename, 1):
        i = int.from_bytes(b, byteorder="big")

        assert bin(i) == bin(0b01001000)


def test_read_bytes_return_type():
    filename = Path("tests/1st_file.bin")

    generator = multip.read_bytes(filename, 1)
    assert isinstance(generator, Generator)


def test_read_files_binary():

    allfiles: list[list[str]] = multip.read_files_binary(filenames, 2)

    assert allfiles[0][0] == bin(0b01001000) and allfiles[0][1] == bin(
        0b01100101
    )


def test_hexify_binary_file():

    allfiles: list[list[str]] = multip.read_files_binary(filenames, 2)

    hex_string_files: list[str] = multip.hexify_binary_file(allfiles)

    assert hex_string_files[0] == "4865"


def test_longest_common_hex_substring():

    lcs = multip.longest_common_hex_substring("abcdef", "mnopcdfg")

    assert lcs == "cd"


def test_rotate_string_list():
    list_rot: list[str] = multip.rotate_string_list(["a", "b", "c"])

    assert list_rot[2] == "a"


def test_rotate_filenames():
    filenames: list[Path] = [
        Path("tests/1st_file.bin"),
        Path("tests/2nd_file.bin"),
        Path("tests/3rd_file.bin"),
    ]

    multip.rotate_filenames(filenames)

    assert filenames[2] == Path("tests/1st_file.bin")
