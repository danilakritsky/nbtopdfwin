import pytest

from pathlib import Path

from ipynbtopdf.latex import Latex
import ipynbtopdf.pdf as pdf


def test_convert_latex_to_pdf_saved_file(
    test_dir, test_notebook, test_latex_file
):
    pdf_file = test_dir / f'{test_latex_file.stem}.pdf'

    latex = Latex.from_notebook(
        notebook_path=test_notebook
    )

    latex.set_cyrillic_friendly_fonts()
    latex.save_outputs(test_dir)
    latex.save_to_file(path=test_latex_file)
    pdf.convert_latex_to_pdf(
        latex=latex,
        pdf_dir=test_dir,
        clear_autogen_files=True,
        clear_outputs=True,
    )

    
    assert pdf_file.exists()
    assert not (test_dir / f'{test_latex_file.stem}.out').exists()
    
    latex.delete_file()
    pdf_file.unlink()
    

def test_convert_latex_to_pdf_no_file(
    test_dir, test_notebook, test_latex_file
):
    latex = Latex.from_notebook(
        notebook_path=test_notebook
    )
    pdf.convert_latex_to_pdf(
        latex=latex,
        pdf_dir=test_dir
    )
    pdfs =  Path(test_dir).glob('*tmp*.pdf')
    assert pdfs
    for pdf_file in pdfs:
        pdf_file.unlink()

    assert Path(test_dir).glob('*.tex')
