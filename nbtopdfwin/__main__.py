import sys
from pathlib import Path

from .latex import Latex
from .pdf import convert_latex_to_pdf


def convert_notebook():
    notebook_path: str = ""
    output_pdf_name: str = ""
    output_pdf_dir: str = ""

    match len(sys.argv):
        case 1:
            raise SystemExit("Provide a path to a notebook.")
        case 2:
            _, notebook_path = sys.argv
        case 3:
            _, notebook_path, output_pdf_name = sys.argv
        case 4:
            _, notebook_path, output_pdf_name, output_pdf_dir = sys.argv
        case _:
            raise SystemExit(
                "Too many arguments. Only the following arguments are supported:\n"
                "nbtopdfwin NOTEBOOK_PATH [OUTPUT_PDF_NAME] [OUTPUT_PDF_DIR]"
            )

    latex = Latex.from_notebook(notebook_path)
    latex.set_cyrillic_friendly_fonts()
    if output_pdf_name:
        latex.save_to_file(Path(output_pdf_name).stem + ".tex")

    if output_pdf_dir:
        convert_latex_to_pdf(latex, pdf_dir=output_pdf_dir, clear_outputs=True)
    else:
        convert_latex_to_pdf(latex, clear_outputs=True)

    if output_pdf_name:
        latex.delete_file()


if __name__ == "__main__":
    convert_notebook()
