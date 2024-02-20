### Imports
# Standard library
import concurrent.futures
import os
import time
from pathlib import Path
from textwrap import wrap
from typing import Generator

# Local files
from exceptions import OnlyOneFileError

# Third-party libraries
from rich.console import Console
from rich.table import Table


def read_bytes(filename: Path, nBytes: int) -> Generator:
    """Read one byte at the time.

    Args:
        filename: (Path) File to be read.
        nBytes: (int) How many bytes to be read.

    Returns:
        Generator: 1 byte
    """
    with open(filename, "rb") as file:
        while True:
            byte = file.read(1)
            if byte:
                yield byte
            else:
                break

            if nBytes > 0:
                nBytes -= 1
                if nBytes == 0:
                    break


def read_files_binary(filenames: list[Path], header_size: int) -> list[list[str]]:
    """
    Read the files to a list of strings in binary representation.

    Args:
        filenames: (list[Path]) The path to the files to be read.
        header_size: (int) The size of the header to be compared.

    Returns:
        list[str]: A list of strings in binary format ie. 0b10100101.
    """
    allfiles: list[list[str]] = []

    for x in range(len(filenames)):
        filecontent = []

        for b in read_bytes(filenames[x], header_size):
            i = int.from_bytes(b, byteorder="big")
            filecontent.append(bin(i))

        allfiles.append(filecontent)

    print(
        f"Header size is {header_size}",
        f"\nNumber of files: {len(allfiles)!s}",
    )
    return allfiles


def hexify_binary_file(allfiles: list[list[str]]) -> list[str]:
    """
    Take a file in binary string format and returns the hex equivalent.

    Args:
        allfiles: (list[str]) The files to input.

    Returns:
        list[str]: A list of strings in hex format without the 0x prefix.
    """
    hex_string_files: list[str] = []

    for file_number in range(len(allfiles)):
        fullString = ""
        for i in range(len(allfiles[file_number])):
            token = hex(int(allfiles[file_number][i], 2)).replace("0x", "")

            if len(token) == 1:
                token = "0" + token

            fullString = fullString + token

        hex_string_files.append(fullString)

    return hex_string_files


def longest_common_hex_substring(string1: str, string2: str) -> str:
    """
    Find the longest common substring of two strings.

    Core dynamic programming algorithm.

    Args:
        string1: (str) First string to be compared.
        string2: (str) Second string to be compared.

    Returns:
        str: Longest common substring.
    """
    matrix = []

    for _ in range(len(string1)):
        matrix.append([0] * len(string2))

    max_number = 0
    number_row = 0

    for row in range(0, len(string1), 1):
        for col in range(0, len(string2), 1):
            if (
                row > 0
                and col > 0
                and string1[row] == string2[col]
                and string1[row - 1] == string2[col - 1]
                and col % 2 == 1
            ):
                matrix[row - 1][col - 1] = matrix[row - 2][col - 2] + 1
                upper_left = 0

                if row > 0 and col > 0:
                    upper_left = matrix[row - 1][col - 1]

                matrix[row][col] = 1 + upper_left

                if matrix[row][col] > max_number:
                    max_number = matrix[row][col]
                    number_row = row

            else:
                matrix[row][col] = 0

    start_of_substring = number_row - max_number + 1

    return string1[start_of_substring : start_of_substring + max_number]


def print_table(data: list[list[str]]) -> None:
    """
    Print the data in a table with Rich.

    Args:
        data: (list[list[str]]) A list of lists with the given data.

    Returns:
        None
    """
    table = Table(title="Byte Header Comparer")

    table.add_column("Seen in", justify="right")
    table.add_column("Longest common substring")
    table.add_column("Filenames", justify="right")

    for i, d in enumerate(data):
        if i % 2 == 0:
            table.add_row(*d, style="#808080")
        else:
            table.add_row(*d)

    console = Console()
    console.print(table)


def wrap_text(string: str, lenght: int = 100) -> str:
    """
    Wrap too long strings around to a max lenght.

    Args:
        string: (str) The string which will be wrap around.
        lenght: (int) The lenght of the string for each wrap. Default is a lenght on 100.

    Returns:
        str: The wrap around string.
    """
    s = wrap(string, 100)
    return "\n".join(s)


def byte_header_comparer(folder: Path, header_size: int = 1024) -> None:
    """
    Main.

    Args:
        folder: (Path) Path to folder which files are location.
        header_size: (int) The size of the header to be compared.

    Raise:
        OnlyOneFileError: If there is only one file to comparer byte headers.
    """
    if not Path(folder).exists():
        exit("Input directory doesn't exists.")

    filenames: list[Path] = [f for f in Path(folder).iterdir() if f.is_file()]

    # We need to raise an OnlyOneFileError error, when there is only one file.
    # It doesn't give sense to comparer byte headers between only one file.
    if len(filenames) == 1:
        raise OnlyOneFileError

    allfiles = read_files_binary(filenames, header_size)
    hex_files = hexify_binary_file(allfiles)

    start = time.perf_counter()

    futures_list: list[concurrent.futures.Future] = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for i, file_1 in enumerate(hex_files):
            for file_2 in hex_files[i + 1 :]:
                future = executor.submit(longest_common_hex_substring, file_1, file_2)
                futures_list.append(future)

    results_list = []
    for result in futures_list:
        results_list.append(result.result())
    results_dict = {}
    for key in set(results_list):
        results_dict[key] = []

    for key in results_dict:
        for hex_file, filename in zip(hex_files, filenames):
            if key in hex_file:
                file_name = os.path.basename(filename)
                results_dict[key].append(file_name)

    d = []
    for key, values in results_dict.items():
        d.append(
            [
                f"{len(values)}/{len(filenames)}",
                wrap_text(key),
                "\n".join(values),
            ],
        )

    print_table(d)

    finish = time.perf_counter()

    print(f"Finished multiprocessing in {round(finish-start, 2)} second(s)")
