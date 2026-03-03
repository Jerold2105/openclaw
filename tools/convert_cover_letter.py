import argparse
from pathlib import Path
from docx2pdf import convert

ROOT = Path(__file__).resolve().parents[1]

def convert_cl(job_id: int):
    docx_path = ROOT / "engine_step2_tailor" / "outputs" / "jobs" / f"job_{job_id}" / "cover_letter.docx"
    pdf_path = ROOT / "engine_step2_tailor" / "outputs" / "jobs" / f"job_{job_id}" / "cover_letter.pdf"

    if not docx_path.exists():
        raise SystemExit(f"Missing cover letter for job {job_id}")

    convert(str(docx_path), str(pdf_path))
    print("OK:", pdf_path)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--job", type=int, required=True)
    a = p.parse_args()
    convert_cl(a.job)