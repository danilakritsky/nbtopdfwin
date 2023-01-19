# nbtopdfwin

Convert IPython notebooks to pdf files on Windows.
Supports Cyrillic characters.

NOTE: Pandoc and MiKTeX must be isntalled on your Windows system for conversion to work:
1. download and install [pandoc](https://pandoc.org/installing.html)
    - default installation path: `C:\Users\USERNAME\AppData\Local\Pandoc`
    - add to PATH: `export PATH=$PATH:/c/Users/USERNAME/AppData/Local/Pandoc/`

2. download and install [MiKTeX](https://miktex.org/download)
    - default installation path: `C:\Users\USERNAME\AppData\Local\Programs\MiKTeX`
    - add to PATH: `export PATH=$PATH:/c/Users/USERNAME/AppData/Local/Programs/MiKTeX/`
    - Reboot the PC!

The package includes 2 modules:

- `latex` module contains `Latex` class that reads a notebook file, converts it to LaTeX via `nbconvert` and modifies its contents for proper pdf conversion.

 - `pdf` module contains a single `convert_latex_to_pdf` function that is used to convert a `Latex` instance to a pdf file.

Additonally you can convert files on the spot via command line command:
`python -m nbtopdfwin NOTEBOOK_PATH [OUTPUT_PDF_NAME] [OUTPUT_PDF_DIR]`
