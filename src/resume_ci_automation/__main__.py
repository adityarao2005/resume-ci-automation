from pathlib import Path
import sys

PACKAGE_DIR = Path(__file__).resolve().parent
SRC_DIR = PACKAGE_DIR.parent
PROJECT_ROOT = SRC_DIR.parent

if __package__ in {None, ""}:
    if str(SRC_DIR) not in sys.path:
        sys.path.insert(0, str(SRC_DIR))
    from resume_ci_automation.pdf_generator import generate_pdf
else:
    from .pdf_generator import generate_pdf

if __name__ == "__main__":
    generate_pdf()