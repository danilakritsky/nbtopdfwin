from pathlib import Path
from typing import Iterable
import subprocess

import nbformat
from nbconvert import LatexExporter

def notebook_to_latex(notebook_path: str | Path) -> tuple[str, dict]:
    "Convert notebook to latex and return its content and additional data."
    notebook_node = nbformat.read(
        notebook_path,
        as_version=4
    )
    exporter: LatexExporter = LatexExporter()
    latex_text: str
    resources: dict

    latex_text, resources = exporter.from_notebook_node(notebook_node)
    return latex_text, resources


def save_outputs(outputs: dict[str, bytes], outputs_dir: str | Path = '.') -> None:
    "Save each output to a file."
    cur_output: str
    for cur_output in outputs:
        with open(Path(outputs_dir) / cur_output, 'wb') as f:
            f.write(outputs[cur_output])


def set_cyrillic_friendly_font(
        latex_text: str,
        main_font: str = "Calibri",
        mono_font: str = "Courier New"
) -> str:
    """
    Add a line to the latex text that would set a document font that
    supports cyrillic characters. Defaults to 'Calibri'.
    """
    # https://tex.stackexchange.com/questions/164520/cyrillic-font-for-xelatex-in-os-x
    # https://tex.stackexchange.com/questions/352804/setmainfont-vs-fontspec
    DOCUMENT_BEGIN_SECTION: str = "\\begin{document}\n"
    return latex_text.replace(
        DOCUMENT_BEGIN_SECTION,
        # mono spaced font that supports cyrillic characters
        # https://tex.stackexchange.com/questions/264544/courier-font-just-not-working
        DOCUMENT_BEGIN_SECTION + (
            f"{chr(32) * 4} \\setmainfont{{{main_font}}}\n"
            f"{chr(32) * 4} \\setmonofont{{{mono_font}}}\n"
        )
    )


def add_full_path_to_outputs(
    latex_text: str,
    outputs_names: Iterable[str],
    outputs_dir: str | Path
) -> str:
    "Replace each output filename in latex text with its full path."
    cur_filename: str
    for cur_filename in outputs_names:
        latex_text = latex_text.replace(
            f'{{{cur_filename }}}',
            # NOTE: replace forward slashes with backslashes
            # since xelatex will not work if there are pathes with back slashes
            # in files on Windows
            f'{{{(outputs_dir / cur_filename).as_posix()}}}'
        )
    return latex_text


def save_latex_to_file(latex_text: str, path: str | Path) -> None:
    "Save latex text to file."
    with open(path, 'w', encoding='utf-8') as f:
        f.write(latex_text)


def convert_latex_to_pdf(
    latex_file: str | Path,
    output_dir: str | Path | None = '.',
    clear_files: bool = False
) -> None:
    """Convert a latex file to pdf."""
    cmd: str = "xelatex"
    if not output_dir:
        output_dir = '.'
    cmd = f"{cmd} -output-directory {output_dir} {latex_file}"
    
    subprocess.run(cmd)

    if clear_files:
        for file in output_dir.glob(f"*{latex_file.stem}*"):
            if file.suffix not in ('.tex', '.pdf'):
                file.unlink()