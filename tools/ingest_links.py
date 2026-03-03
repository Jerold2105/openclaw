import argparse
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
LINKS = ROOT / "engine_step2_tailor" / "inputs" / "job_links.txt"

def read_links():
    if not LINKS.exists():
        return []
    raw = LINKS.read_text(encoding="utf-8", errors="ignore")
    urls = re.findall(r"https?://\S+", raw)
    # de-dup preserve order
    seen = set()
    out = []
    for u in urls:
        u = u.strip().rstrip(").,;")
        if u not in seen:
            out.append(u)
            seen.add(u)
    return out

def write_remaining(remaining):
    LINKS.write_text("\n".join(remaining) + ("\n" if remaining else ""), encoding="utf-8")

def run(cmd):
    subprocess.run(cmd, check=True)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--company", required=True)
    p.add_argument("--role", required=True)
    args = p.parse_args()

    urls = read_links()
    if not urls:
        print("No links found in job_links.txt")
        return

    # ingest ALL links using same company/role label (fast MVP)
    for u in urls:
        run([sys.executable, "tools/openclaw.py", "add", "--company", args.company, "--role", args.role, "--link", u])

    # clear inbox after ingest
    write_remaining([])
    print("OK: ingested links and cleared job_links.txt")

if __name__ == "__main__":
    main()