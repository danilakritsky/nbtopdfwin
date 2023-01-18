import nbformat
from nbconvert import LatexExporter

notebook = nbformat.read(
    './test_latex.ipynb',
    as_version=4
)
exporter = LatexExporter()
body: str
resources: dict

body, resources = exporter.from_notebook_node(notebook)

outputs: dict[str, bytes]
outputs = resources['outputs']
print(outputs['output_2_1.png'])

with open('output_2_1.png', 'wb') as f:
    f.write(outputs['output_2_1.png'])
# a font that supports cyrillic character should be set for the document
# https://tex.stackexchange.com/questions/164520/cyrillic-font-for-xelatex-in-os-x


DOCUMENT_START_SECTION: str = r"\begin{document}"

fontname: str = "Calibri"
body = body.replace(
    DOCUMENT_START_SECTION,
    DOCUMENT_START_SECTION + (
        "\n" + chr(32) * 4 + r"\setmainfont" + "{" + fontname + "}" + "\n"
    )
)

with open("test.tex", 'w', encoding='utf-8') as f:
    f.write(body)

# import subprocess

# subprocess.run(f"xelatex test.tex")

# TODO pdf from string without saving to a file

# TODO save images