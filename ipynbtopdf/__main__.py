import sys
from .latex import Latex
from .pdf import convert_latex_to_pdf

module_path, notebook = sys.argv


latex = Latex.from_notebook(notebook)
convert_latex_to_pdf(latex)