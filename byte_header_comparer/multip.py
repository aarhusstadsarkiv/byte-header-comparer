from pathlib import Path
import time
import concurrent.futures
import argparse
from typing import Generator


def read_bytes(filename: Path, nBytes: int) -> Generator:
    """Reads one byte at the time.

    Args:
        filename: file to be read.
        nBytes: how many bytes to be read.
    Returns:
        1 byte

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


def read_files_binary(filenames: list[Path], header_size: int = 1024) -> list[list[str]]:
    """Read the files to a list of strings in binary representation.

    Args:
        list of Path: the path to the files to be read.
        header size: the size of the header to be compared.
    Returns:
        list[str]: A list of strings in binary format ie. 0b10100101.
    """
    print("")
    print("Header size is " + str(header_size))

    allfiles: list[list[str]] = []

    for x in range(len(filenames)):
        filecontent = []

        for b in read_bytes(filenames[x], header_size):
            i = int.from_bytes(b, byteorder="big")
            filecontent.append(bin(i))

        allfiles.append(filecontent)

    print("")
    print("Number of files: " + str(len(allfiles)))
    print("")
    return allfiles


def hexify_binary_file(allfiles) -> list[str]:
    """Takes a file in binary string format and returns the hex equivalent.

    Args:
        list[str]: the files to input.
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
    """Finds the longest common substring of two strings.

    Core dynamic programming algorithm.

    Args:
        string1: First string to be compared.
        string2: Second string to be compared.

    Returns:
        LCS: Longest common substring.
    """
    matrix = []

    for _ in range(len(string1)):
        matrix.append([0] * len(string2))

    max_number = 0
    number_row = 0
    # number_col = 0

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
                # matrix[row][col-1] = 1 + upper_left

                if matrix[row][col] > max_number:
                    max_number = matrix[row][col]
                    number_row = row
                    # number_col = col

            else:
                matrix[row][col] = 0

    start_of_substring = number_row - max_number + 1

    return string1[start_of_substring : start_of_substring + max_number]  # noqa


def rotate_string_list(string_files: list[str]) -> list[str]:
    to_back = string_files.pop(0)
    string_files.append(to_back)

    return string_files


def get_version() -> str:
    version: str = "Ukendt version"
    with open(Path(__file__).absolute().parent.parent / "pyproject.toml") as i:
        for line in i.readlines():
            if line.startswith("version"):
                version = line[line.index('"') + 1 : -2]  # noqa
    return version


def main(args=None):
    """
    Main...
    """
    parser = argparse.ArgumentParser(
        description=(
            "Compares the first 1024 bytes of each file with the other "
            "files and finds longest common substrings"
        )
    )
    parser.add_argument(
        "folder",
        metavar="files_home",
        type=Path,
        help="Home of files to compare.",
    )
    parser.add_argument(
        "header_size",
        nargs="?",
        default=1024,
        metavar="header_size",
        type=int,
        help="Optional size of header to compare.",
    )

    parser.add_argument("--version", action="version", version=get_version())

    args = parser.parse_args(args)

    if not Path(args.folder).exists():
        exit("Input directory doesn't exists.")

    filenames: list[Path] = [f for f in Path(args.folder).iterdir() if f.is_file()]

    histogram: dict[str, int] = {}
    histogram_files: dict[str, list[str]] = {}

    allfiles = read_files_binary(filenames, args.header_size)
    hex_files = hexify_binary_file(allfiles)

    start = time.perf_counter()

    futures_list: list[concurrent.futures.Future] = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for i, file_1 in enumerate(hex_files):
            for file_2 in hex_files[i + 1 :]:
                future = executor.submit(longest_common_hex_substring, file_1, file_2)
                futures_list.append(future)

    for i in range(len(hex_files)):
        lcs = futures_list[i].result()

        try:
            histogram[lcs] = histogram[lcs] + 1
        except KeyError:
            histogram[lcs] = 1

        try:
            fn0_bool = str(filenames[0].absolute()) not in histogram_files[lcs]
            fn1_bool = str(filenames[1].absolute()) not in histogram_files[lcs]

            if fn0_bool:
                histogram_files[lcs].append(str(filenames[0].absolute()))
            if fn1_bool:
                histogram_files[lcs].append(str(filenames[1].absolute()))
        except KeyError:
            histogram_files[lcs] = [
                str(filenames[0].absolute()),
                str(filenames[1].absolute()),
            ]

    finish = time.perf_counter()
    # Find the smallest byte header by smallest length of string
    lenght_of_keys = [len(k) for k in histogram_files.keys()]

    # A common substring can also be nothing, therefore we remove any zero from the list.
    lenght_of_keys.remove(0)

    value = lenght_of_keys.index(min(lenght_of_keys))
    smallest_byte_header = list(histogram_files.keys())[value]

    seen_count = 0
    for file_1 in hex_files:
        if smallest_byte_header in file_1:
            seen_count += 1

    if seen_count == len(hex_files):
        print("Succes!")
        print(
            "The smallest of the longest common substring between all given files have been found."
        )
        print(f"The byte header is: {smallest_byte_header}")
    else:
        print("Warning!")
        print(
            f"The smallest of the longest common substring have only"
            f" been seen in {seen_count} out of {len(hex_files)}"
        )
        print(f"The byte header is: {smallest_byte_header}")
    print("\n")
    print(f"Finished multiprocessing in {round(finish-start, 2)} second(s)")


if __name__ == "__main__":
    main()
