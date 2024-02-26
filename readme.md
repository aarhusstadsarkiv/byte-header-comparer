# Multiprocessing of longest common substring
This program takes a folder with the files which byte headers is to be compared.


### Command line
Optional argument which sets the size of the byte header, default is 1024.
```
usage: cli.py [-h] [-v] -f folder [-hs [header_size]]

Compares the first 1024 bytes of each file with the other files and finds longest common substrings

options:
  -h, --help            show this help message and exit
  -v, --version         Display version number
  -f folder, --folder folder
                        Folder of files to compare.
  -hs [header_size], --header_size [header_size]
                        Optional size of header to compare.
```