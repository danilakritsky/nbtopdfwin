from pathlib import Path

import pytest

from ipynbtopdf import main

@pytest.fixture
def test_dir():
    return Path(__file__).parent


@pytest.fixture
def test_file(test_dir):
    return test_dir / 'test_file.ipynb'


def test_notebook_to_latex(test_file):
    latex_text, resources = main.notebook_to_latex(
        notebook_path=test_file
    )
    assert "Привет" in latex_text
    assert resources['outputs']


def test_save_outputs(test_dir, test_file):
    latex_text, resources = main.notebook_to_latex(test_file)
    outputs = resources['outputs']
    main.save_outputs(
        outputs=outputs,
        outputs_dir=test_dir
    )
    
    output: str
    for output in outputs:
        assert (test_dir  / output).exists
        (test_dir  / output).unlink()


def test_set_cyrillic_friendly_font(test_file):
    latex_text, resources = main.notebook_to_latex(test_file)
    new_latex = main.set_cyrillic_friendly_font(
        latex_text=latex_text, font="Arial"
    )
    
    assert "Arial" in new_latex


def test_add_full_path_to_outputs(test_dir, test_file):
    latex_text, resources = main.notebook_to_latex(test_file)
    main.add_full_path_to_outputs(
        latex_text=latex_text,
        outputs_names=[name for name in resources['output']],
        outputs_dir=test_dir
    )
