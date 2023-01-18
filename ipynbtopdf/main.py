from pathlib import Path

import nbformat
from nbconvert import LatexExporter

def notebook_to_latex(notebook: str | Path) -> tuple[str, dict]:
    "Convert notebook to latex and return its content and additional data."
    notebook_node = nbformat.read(
        notebook,
        as_version=4
    )
    exporter: LatexExporter = LatexExporter()
    latex_text: str
    resources: dict

    latex_text, resources = exporter.from_notebook_node(notebook_node)
    return latex_text, resources


def save_outputs(outputs: dict[str, bytes], dir: str | Path = '.') -> None:
    "Save each output to a file."
    cur_output: str
    for cur_output in outputs:
        with open(Path(dir) / cur_output, 'wb') as f:
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
