# Multiprocessing of longest common substring
This program takes a folder with the files which byte headers is to be compared.


### Command line
Optional argument which sets the size of the byte header, default is 1024.
```
Usage: cli.py [OPTIONS] COMMAND [ARGS]...

Options:
  --version                   Show the version and exit.
  -f, --folder TEXT           Folder of files to compare.        
  -hs, --header_size INTEGER  Optional size of header to compare.
  --help                      Show this message and exit.
```