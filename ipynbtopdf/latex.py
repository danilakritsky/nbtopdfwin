from pathlib import Path
from typing import Iterable, Literal

import nbformat
from nbconvert import LatexExporter


class Latex:
    def __init__(self, text: str, resources: [str, dict]):
        self.text: str = text
        self.resources = resources
        # https://github.com/python/typing/issues/157
        self.outputs: dict[str, Path] = {
            output: Path(output)
            for output in self.resources['outputs']
        }
        self.outputs_saved: bool = False
        self.path: Path | None = None


    @classmethod
    def from_notebook(cls, notebook_path: str | Path) -> 'Latex':
        """
        Convert notebook to latex and return its content and additional data.
        """

        notebook_node = nbformat.read(
            notebook_path,
            as_version=4
        )
        exporter: LatexExporter = LatexExporter()
        text: str
        resources: dict

        text, resources = exporter.from_notebook_node(notebook_node)
        
        return Latex(text, resources)
    

    def set_cyrillic_friendly_fonts(
            self,
            main_font: str = "Calibri",
            mono_font: str = "Courier New"
    ) -> None:
        """
        Add lines to the latex text that would set a document font that
        supports cyrillic characters. Defaults to 'Calibri' for main font
        and 'Courier New' for monospaced font.
        """

        # https://tex.stackexchange.com/questions/164520/cyrillic-font-for-xelatex-in-os-x
        # https://tex.stackexchange.com/questions/352804/setmainfont-vs-fontspec
        DOCUMENT_BEGIN_SECTION: str = "\\begin{document}\n"
        updated_latex: str = self.text.replace(
            DOCUMENT_BEGIN_SECTION,
            # mono spaced font that supports cyrillic characters
            # https://tex.stackexchange.com/questions/264544/courier-font-just-not-working
            DOCUMENT_BEGIN_SECTION + (
                f"{chr(32) * 4} \\setmainfont{{{main_font}}}\n"
                f"{chr(32) * 4} \\setmonofont{{{mono_font}}}\n"
            )
        )

        self.text = updated_latex


    def save_outputs(self, outputs_dir: str | Path | None = None) -> None:
        "Save each output to a file."
        if outputs_dir is None:
            outputs_dir = Path('.')
        cur_output: str
        for cur_output in self.outputs:
            if outputs_dir:
                self.outputs[cur_output] = Path(outputs_dir) / cur_output
            with open(self.outputs[cur_output], 'wb') as f:
                f.write(self.resources['outputs'][cur_output])
        self.outputs_saved = True

    
    def delete_outputs(self) -> None:
        "Delete all saved outputs."
        cur_output: str
        output_file: Path
        for cur_output, output_file in self.outputs.items():
            output_file.unlink()
            self.outputs[cur_output] = Path(cur_output)
        self.outputs_saved = False


    def add_full_path_to_outputs(self) -> None:
        """Replace each output filename in latex text with its full path."""

        updated_text: str = self.text
        cur_filename: Path
        for cur_file, cur_file_path in self.outputs.items():
            updated_text = updated_text.replace(
                f'{{{cur_file}}}',
                # NOTE: replace forward slashes with backslashes
                # since xelatex will not work if there are pathes with back slashes
                # in files on Windows
                f'{{{cur_file_path.as_posix()}}}'
            )

        return updated_text


    def save_to_file(self, path: str | Path) -> None:
        """Save latex text to file."""
        
        if isinstance(path, str):
            path = Path(path)

        if not self.outputs_saved:
            self.save_outputs()
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(self.add_full_path_to_outputs())
        
        self.path = path

       
    def delete_file(self) -> None:
        """Save latex text to file."""
        if self.path:
            self.path.unlink()
            self.path = None