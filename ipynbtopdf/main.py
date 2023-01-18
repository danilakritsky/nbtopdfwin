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
    latex_body: str
    resources: dict

    latex_body, resources = exporter.from_notebook_node(notebook_node)
    return latex_body, resources


def save_outputs(outputs: dict[str, bytes], dir: str | Path = '.') -> None:
    "Save each output to a file."
    cur_output: str
    for cur_output in outputs:
        with open(Path(dir) / cur_output, 'wb') as f:
            f.write(outputs[cur_output])
