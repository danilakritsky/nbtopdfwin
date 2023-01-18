from pathlib import Path

import nbformat
from nbconvert import LatexExporter

def notebook_to_latex(notebook: str | Path) -> tuple[str, dict]:
    notebook_node = nbformat.read(
        notebook,
        as_version=4
    )
    exporter: LatexExporter = LatexExporter()
    latex_body: str
    resources: dict

    latex_body, resources = exporter.from_notebook_node(notebook_node)
    return latex_body, resources
