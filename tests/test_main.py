from pathlib import Path

import pytest

from ipynbtopdf import main

@pytest.fixture
def test_file():
    return Path(__file__).parent / 'test_file.ipynb'

def test_notebook_to_latex(test_file):
    body, resources = main.notebook_to_latex(test_file)
    assert "Привет" in body
    assert resources['outputs']
