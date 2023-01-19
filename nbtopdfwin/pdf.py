import subprocess
from pathlib import Path
from tempfile import NamedTemporaryFile

from .latex import Latex


def convert_latex_to_pdf(
    latex: Latex,
    pdf_dir: str | Path = Path("."),
    clear_autogen_files: bool = True,
    clear_outputs: bool = False,
    cyrillic_support: bool = True,
) -> None:
    """Convert a latex file to pdf via xelatex."""

    if not isinstance(pdf_dir, Path):
        pdf_dir = Path(pdf_dir)

    if cyrillic_support:
        latex.set_cyrillic_friendly_fonts()

    drop_later: bool = False
    if not latex.path:
        if not latex.outputs_saved:
            latex.save_outputs()

        latex_tempfile = NamedTemporaryFile(
            mode="w", dir=pdf_dir, suffix=".tex", delete=False
        )
        latex_tempfile.close()
        latex.save_to_file(pdf_dir / Path(latex_tempfile.name))
        drop_later = True

    cmd: str = f"xelatex -output-directory {pdf_dir} {latex.path}"

    subprocess.run(cmd)

    if clear_autogen_files:
        for file in pdf_dir.glob(f"*{latex.path.stem}*"):
            if file.suffix in (".aux", ".log", ".out"):
                file.unlink()

    if clear_outputs or drop_later:
        latex.delete_outputs()

    if drop_later:
        latex.delete_file()
