# itoyparser
Simple python parser program from Yatahay poker format to IPoker.

## Requirements
Before you install the binaries, you need a couple additional libraries installed:
- [PyInstaller for Python 3][pyexe] 
- make

###### NOTE! You need Python3 in order to run this program!

## Installation
To install, simply run 
```sh
$ make
````
This will initialize the required folders and will run `pyinstaller` to create the binary executable. 
The available `make` commands are:
```sh
    # Remove temporary and distribution files
    $ make clean
    # Initialize 
    $ make init
    # Build the project
    $ make build
```
The resulting binary file is located inside `dist` directory.

### Note! I've written this program originally on Windows machine, using [`GNUWIN`][gnuwin] environment and [`LiClipse IDE`][liclipse]. The build process as written in makefile will not find the necessary python modules if you use the `GNUWIN` terminal, as `pwd()` command returns the Linux-like location of the file, and not the actual Windows location!

## Usage

You need to have `ITOYINPUT` and `ITOYOUTPUT` folders in your root directory, otherwise the program will fail. Follow the Installation procedure above to create them.

Put your `Yatahay`-formatted logs inside the input folder and run the program:
```sh
# For Windows
$ itoyparser.exe
```

The results are written to the output folder, converted to IPoker format.

License
----
[GPL3][license]

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [pyexe]: http://www.abv.bg
   [gnuwin]: http://gnuwin32.sourceforge.net/
   [liclipse]: http://liclipse.com
   [license]: https://github.com/vanxa/itoyparser/blob/master/LICENSE
