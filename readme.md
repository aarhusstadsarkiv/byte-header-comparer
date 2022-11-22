# Multiprocessing of longest common substring
This program takes a folder with the files which byte headers is to be compared. For 3 files and a byte header of 1024, this takes around 1 second. The program is based on dynamic programming.
## Argument 1:
The path to the folder which contains the files.

## Argument 2:
Optional argument which sets the size of the byte header, default is 1024.
```
usage: multip.py [-h] [--version] files_home [header_size]

Compares the first 1024 bytes of each file with the other files and finds longest common substrings

positional arguments:
  files_home   Home of files to compare.
  header_size  Optional size of header to compare.

options:
  -h, --help   show this help message and exit
  --version    show program's version number and exit
```