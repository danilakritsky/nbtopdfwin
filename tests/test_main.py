from pathlib import Path

import pytest

from ipynbtopdf import main

@pytest.fixture
def test_dir():
    return Path(__file__).parent

@pytest.fixture
def test_notebook(test_dir):
    return test_dir / 'test_notebook.ipynb'

@pytest.fixture()
def test_latex(test_dir):
    return test_dir / 'test_latex.tex'

def test_notebook_to_latex(test_notebook):
    latex_text, resources = main.notebook_to_latex(
        notebook_path=test_notebook
    )
    assert "Привет" in latex_text
    assert resources['outputs']


def test_save_outputs(test_dir, test_notebook):
    latex_text, resources = main.notebook_to_latex(test_notebook)
    outputs = resources['outputs']
    main.save_outputs(
        outputs=outputs,
        outputs_dir=test_dir
    )
    
    output: str
    for output in outputs:
        assert (test_dir  / output).exists
        (test_dir  / output).unlink()


def test_set_cyrillic_friendly_font(test_notebook):
    latex_text, _ = main.notebook_to_latex(test_notebook)
    new_latex = main.set_cyrillic_friendly_font(
        latex_text=latex_text, main_font="Arial"
    )

    assert "Arial" in new_latex


def test_add_full_path_to_outputs(test_dir, test_notebook):
    latex_text, resources = main.notebook_to_latex(test_notebook)
    updated_latex = main.add_full_path_to_outputs(
        latex_text=latex_text,
        outputs_names=[name for name in resources['outputs']],
        outputs_dir=test_dir
    )
    assert test_dir.as_posix() in updated_latex


def test_save_latex(test_latex, test_notebook, test_dir):
    latex_text, resources = main.notebook_to_latex(test_notebook)
    latex_text = main.set_cyrillic_friendly_font(latex_text)
    latex_text = main.add_full_path_to_outputs(
        latex_text=latex_text,
        outputs_names=[name for name in resources['outputs']],
        outputs_dir=test_dir
    )
    main.save_outputs(
        outputs=resources['outputs'],
        outputs_dir=test_dir
    )
    main.save_latex_to_file(
        latex_text=latex_text,
        path=test_latex
    )
    
    assert Path(test_latex).exists
    Path(test_latex).unlink()
