import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "engine_step3_approval" / "outputs" / "review_queue.md"

def run(cmd):
    print("\n>>", " ".join(cmd))
    subprocess.run(cmd, check=True)

def next_job_id():
    text = QUEUE.read_text(encoding="utf-8") if QUEUE.exists() else ""
    ids = [int(m.group(1)) for m in re.finditer(r"^## Job (\d+)", text, re.M)]
    return (max(ids) + 1) if ids else 1

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--company", required=True)
    p.add_argument("--role", required=True)
    p.add_argument("--url", required=True)
    args = p.parse_args()

    # Step 1: Add job
    run([
        sys.executable,
        "tools/openclaw.py",
        "add",
        "--company", args.company,
        "--role", args.role,
        "--link", args.url
    ])

    job_id = next_job_id() - 1
    print(f"\nDetected Job ID: {job_id}")

    # Step 2: Scrape JD
    run([
        sys.executable,
        "tools/scrape_jd.py",
        "--job", str(job_id),
        "--url", args.url
    ])

    # Step 3: Run full pipeline
    run([
        sys.executable,
        "tools/pipeline.py",
        "--job", str(job_id),
        "--company", args.company,
        "--role", args.role
    ])

    print("\nFULL AUTO PIPELINE COMPLETE — READY_FOR_REVIEW")