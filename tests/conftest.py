from pathlib import Path

import pytest

from ipynbtopdf.latex import Latex
import ipynbtopdf.pdf as pdf

@pytest.fixture
def test_dir():
    return Path(__file__).parent

@pytest.fixture
def test_notebook(test_dir):
    return test_dir / 'test_notebook.ipynb'

@pytest.fixture()
def test_latex_file(test_dir):
    return test_dir / 'test_latex.tex'