import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JD_PATH = ROOT / "engine_step2_tailor" / "inputs" / "job_description.txt"
QUEUE = ROOT / "engine_step3_approval" / "outputs" / "review_queue.md"

def read(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.exists() else ""

def write(p: Path, s: str):
    p.write_text(s, encoding="utf-8")

def attach(job_id: int):
    jd = read(JD_PATH).strip()
    if not jd:
        raise SystemExit("job_description.txt is empty")

    q = read(QUEUE)
    marker = f"## Job {job_id}"
    if marker not in q:
        raise SystemExit(f"Job {job_id} not found")

    jobs_dir = ROOT / "engine_step2_tailor" / "outputs" / "jobs" / f"job_{job_id}"
    jobs_dir.mkdir(parents=True, exist_ok=True)

    out_jd = jobs_dir / "job_description.txt"
    write(out_jd, jd + "\n")

    # update status line
    lines = q.splitlines(True)
    out = []
    inside = False
    for line in lines:
        if line.startswith(marker):
            inside = True
        elif inside and line.startswith("## Job "):
            inside = False

        if inside and line.startswith("Status:"):
            out.append("Status: JD_ADDED\n")
        else:
            out.append(line)

    write(QUEUE, "".join(out))
    print("OK: attached JD to", out_jd)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--job", type=int, required=True)
    a = p.parse_args()
    attach(a.job)