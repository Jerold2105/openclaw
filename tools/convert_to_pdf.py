from docx2pdf import convert
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
docx_path = ROOT / "engine_step2_tailor" / "outputs" / "generated_resume.docx"
pdf_path = ROOT / "engine_step2_tailor" / "outputs" / "generated_resume.pdf"

convert(str(docx_path), str(pdf_path))

print("PDF generated:", pdf_path)