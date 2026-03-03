import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINKS = ROOT / "engine_step2_tailor" / "inputs" / "job_links.txt"
QUEUE = ROOT / "engine_step3_approval" / "outputs" / "review_queue.md"

def run(cmd):
    print("\n>>", " ".join(cmd))
    subprocess.run(cmd, check=True)

def read_links():
    if not LINKS.exists():
        return []
    raw = LINKS.read_text(encoding="utf-8", errors="ignore")
    urls = re.findall(r"https?://\S+", raw)
    seen, out = set(), []
    for u in urls:
        u = u.strip().rstrip(").,;")
        if u not in seen:
            out.append(u)
            seen.add(u)
    return out

def clear_links():
    LINKS.write_text("", encoding="utf-8")

def next_job_id():
    text = QUEUE.read_text(encoding="utf-8") if QUEUE.exists() else ""
    ids = [int(m.group(1)) for m in re.finditer(r"^## Job (\d+)", text, re.M)]
    return (max(ids) + 1) if ids else 1

if __name__ == "__main__":
    urls = read_links()
    if not urls:
        print("No links in job_links.txt")
        raise SystemExit(0)

    start_id = next_job_id()

    company = input("Company label: ").strip()
    role = input("Role label: ").strip()

    jid = start_id
    for u in urls:
        run([sys.executable, "tools/openclaw.py", "add", "--company", company, "--role", role, "--link", u])
        print(f"Added as Job {jid} (JD attach + pipeline is manual per job for now)")
        jid += 1

    clear_links()
    print("\nOK: links ingested + cleared inbox")