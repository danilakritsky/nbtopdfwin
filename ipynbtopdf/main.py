from pathlib import Path
from typing import Iterable

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
        latex_text: str, font: str = "Calibri"
) -> str:
    """
    Add a line to the latex text that would set a document font that
    supports cyrillic characters. Defaults to 'Calibri'.
    """
    # https://tex.stackexchange.com/questions/164520/cyrillic-font-for-xelatex-in-os-x
    
    DOCUMENT_BEGIN_SECTION: str = r"\begin{document}"
    return latex_text.replace(
        DOCUMENT_BEGIN_SECTION,
        DOCUMENT_BEGIN_SECTION + (
            "\n" + chr(32) * 4 + r"\setmainfont" + "{" + font + "}" + "\n"
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
            f'{{{str(outputs_dir / cur_filename)}}}'
        )
    return latex_text


def save_latex(latex_text: str, path: str | Path) -> None:
    "Save latex text to file."
    with open(path, 'w', encoding='utf-8') as f:
        f.write(latex_text)
