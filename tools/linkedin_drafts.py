import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRUTH = ROOT / "engine_step1_truth" / "truth_profile.json"
OUT = ROOT / "engine_step2_tailor" / "outputs" / "linkedin_drafts.md"

def load_truth():
    return json.loads(TRUTH.read_text(encoding="utf-8"))

def main():
    t = load_truth()
    name = t.get("name", "Me")
    projects = t.get("projects", [])
    exp = t.get("experience", [])

    lines = []
    lines.append(f"# LinkedIn Drafts ({datetime.now().strftime('%Y-%m-%d')})\n")

    # Draft 1: project spotlight
    if projects:
        p = projects[0]
        lines.append("## Draft 1 — Project Spotlight\n")
        lines.append(f"Sharing a quick update on {p['name']}.\n")
        for d in p.get("details", [])[:2]:
            lines.append(f"- {d}\n")
        lines.append("\nIf you're working on SOC operations or phishing defense, I'd love to connect.\n")
        lines.append(f"\n— {name}\n\n---\n")

    # Draft 2: experience highlight
    if exp:
        e = exp[0]
        lines.append("## Draft 2 — Experience Highlight\n")
        lines.append(f"In my previous role at {e['company']}, I focused on security assurance work that improved release readiness.\n")
        for a in e.get("achievements", [])[:2]:
            lines.append(f"- {a}\n")
        lines.append(f"\nNow I’m building hands-on security projects while finishing my M.S. (expected May 2026).\n")
        lines.append(f"\n— {name}\n\n---\n")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("".join(lines), encoding="utf-8")
    print("OK:", OUT)

if __name__ == "__main__":
    main()