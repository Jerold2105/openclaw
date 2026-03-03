import argparse
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "engine_step3_approval" / "outputs" / "review_queue.md"
APPROVED = ROOT / "engine_step3_approval" / "outputs" / "approved_log.md"
REJECTED = ROOT / "engine_step3_approval" / "outputs" / "rejected_log.md"
REVISIONS = ROOT / "engine_step3_approval" / "outputs" / "revision_log.md"

def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.exists() else ""

def write_text(p: Path, s: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding="utf-8")

def append_text(p: Path, s: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(s)

def next_job_id(queue_text: str) -> int:
    ids = [int(m.group(1)) for m in re.finditer(r"^## Job (\d+)\b", queue_text, flags=re.M)]
    return (max(ids) + 1) if ids else 1

def get_job_block(queue_text: str, job_id: int) -> str:
    pat = re.compile(rf"(## Job {job_id}\b.*?)(?=^## Job \d+\b|\Z)", flags=re.M | re.S)
    m = pat.search(queue_text)
    if not m:
        raise SystemExit(f"Job {job_id} not found in review_queue.md")
    return m.group(1)

def replace_job_block(queue_text: str, job_id: int, new_block: str) -> str:
    pat = re.compile(rf"(## Job {job_id}\b.*?)(?=^## Job \d+\b|\Z)", flags=re.M | re.S)
    m = pat.search(queue_text)
    if not m:
        raise SystemExit(f"Job {job_id} not found in review_queue.md")
    return queue_text[:m.start(1)] + new_block + queue_text[m.end(1):]

def set_decision(job_id: int, decision: str) -> None:
    decision = decision.strip().upper()
    if decision not in {"APPROVED", "REJECTED", "REVISE", "PENDING", "WITHDRAWN"}:
        raise SystemExit("Decision must be one of: APPROVED, REJECTED, REVISE, PENDING, WITHDRAWN")

    qt = read_text(QUEUE)
    block = get_job_block(qt, job_id)

    if re.search(r"^Decision:\s*.*$", block, flags=re.M):
        block2 = re.sub(r"^Decision:\s*.*$", f"Decision: {decision}", block, flags=re.M)
    else:
        block2 = re.sub(r"^(Status:.*)$", r"\1\nDecision: " + decision, block, flags=re.M)

    qt2 = replace_job_block(qt, job_id, block2)
    write_text(QUEUE, qt2)
    print(f"OK: Job {job_id} Decision -> {decision}")

def log_decision(job_id: int) -> None:
    qt = read_text(QUEUE)
    block = get_job_block(qt, job_id)

    m = re.search(r"^Decision:\s*(.+)$", block, flags=re.M)
    if not m:
        raise SystemExit("No Decision line found in job block")
    decision = m.group(1).strip().upper()

    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"\n[{ts}] Job {job_id} Decision: {decision}\n{block}\n"

    if decision == "APPROVED":
        append_text(APPROVED, entry)
        print(f"OK: logged to {APPROVED}")
    elif decision == "REJECTED":
        append_text(REJECTED, entry)
        print(f"OK: logged to {REJECTED}")
    elif decision == "REVISE":
        append_text(REVISIONS, entry)
        print(f"OK: logged to {REVISIONS}")
    else:
        raise SystemExit("Decision must be APPROVED, REJECTED, or REVISE to log")

def add_job(company: str, role: str, link: str) -> None:
    qt = read_text(QUEUE)
    jid = next_job_id(qt)
    block = (
        f"## Job {jid}\n"
        f"Company: {company}\n"
        f"Role: {role}\n"
        f"Job Link: {link}\n"
        f"Status: JD_NOT_ADDED\n"
        f"Decision: PENDING\n\n"
        f"Resume PDF:\n"
        f"Cover Letter:\n"
        f"Autofill Answers:\n\n"
        f"Missing Info:\n\n"
        f"Actions:\n"
        f"- APPROVE\n"
        f"- REVISE\n"
        f"- REJECT\n\n"
        f"Notes:\n\n"
        f"---\n\n"
    )
    write_text(QUEUE, qt + ("" if qt.endswith("\n") or qt == "" else "\n") + block)
    print(f"OK: Added Job {jid}")

def main():
    ap = argparse.ArgumentParser(prog="openclaw")
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add")
    a.add_argument("--company", required=True)
    a.add_argument("--role", required=True)
    a.add_argument("--link", required=True)

    d = sub.add_parser("decision")
    d.add_argument("--job", type=int, required=True)
    d.add_argument("--set", required=True)

    l = sub.add_parser("log")
    l.add_argument("--job", type=int, required=True)

    args = ap.parse_args()

    if args.cmd == "add":
        add_job(args.company, args.role, args.link)
    elif args.cmd == "decision":
        set_decision(args.job, args.set)
    elif args.cmd == "log":
        log_decision(args.job)

if __name__ == "__main__":
    main()