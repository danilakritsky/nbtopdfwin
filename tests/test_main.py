from pathlib import Path

import pytest

from ipynbtopdf import main

@pytest.fixture
def test_folder():
    return Path(__file__).parent


@pytest.fixture
def test_file(test_folder):
    return test_folder / 'test_file.ipynb'


def test_notebook_to_latex(test_file):
    body, resources = main.notebook_to_latex(test_file)
    assert "Привет" in body
    assert resources['outputs']


def test_save_outputs(test_folder, test_file):
    body, resources = main.notebook_to_latex(test_file)
    main.save_outputs(resources['outputs'], dir=test_folder)
    
    output: str
    for output in resources['outputs']:
        assert (test_folder  / output).exists
        (test_folder  / output).unlink()
