from pathlib import Path

import pytest

from nbtopdfwin.latex import Latex


def test_from_notebook(test_notebook):
    print(test_notebook)
    latex = Latex.from_notebook(
        notebook_path=test_notebook
    )
    assert "Привет" in latex.text
    assert latex.resources


def test_set_cyrillic_friendly_fonts(test_notebook):
    latex = Latex.from_notebook(
        notebook_path=test_notebook
    )
    latex.set_cyrillic_friendly_fonts(
        main_font="Arial",
    )

    assert "Arial" in latex.text


def test_add_full_path_to_outputs(test_notebook):
    latex = Latex.from_notebook(
        notebook_path=test_notebook
    )
    text_with_full_paths = latex.add_full_path_to_outputs()
    for output_path in latex.outputs.values():
        assert output_path.as_posix() in text_with_full_paths


def test_save_outputs(test_dir, test_notebook):
    latex = Latex.from_notebook(
        notebook_path=test_notebook
    )

    latex.save_outputs(
        outputs_dir=test_dir
    )
    
    output_file: Path
    for output_file in latex.outputs.values():
        assert output_file.exists()

    assert latex.outputs_saved == True
        
    
def test_delete_outputs(test_dir, test_notebook):
    latex = Latex.from_notebook(
        notebook_path=test_notebook
    )

    latex.save_outputs(
        outputs_dir=test_dir
    )
    assert latex.outputs_saved == True
    
    latex.delete_outputs()
    
    output_file: Path
    for output_file in latex.outputs.values():
        assert not output_file.exists()

    assert latex.outputs_saved == False


def test_save_to_file(test_latex_file, test_notebook, test_dir):
    latex = Latex.from_notebook(
        notebook_path=test_notebook
    )
    latex.set_cyrillic_friendly_fonts()
    latex.save_outputs(test_dir)
    latex.save_to_file(path=test_latex_file)

    assert latex.path.exists()
    latex.path.unlink()

    file: Path
    for file in latex.outputs.values():
        file.unlink()


def test_delete_file(test_latex_file, test_notebook, test_dir):
    latex = Latex.from_notebook(
        notebook_path=test_notebook
    )
    latex.save_outputs(test_dir)
    latex.save_to_file(path=test_latex_file)
    assert latex.path.exists()
    
    latex.delete_outputs()
    latex.delete_file()

    assert not latex.path
