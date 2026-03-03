import json
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRUTH = ROOT / "engine_step1_truth" / "truth_profile.json"

def load_truth():
    return json.loads(TRUTH.read_text(encoding="utf-8"))

def load_jd(job_id):
    p = ROOT / "engine_step2_tailor" / "outputs" / "jobs" / f"job_{job_id}" / "job_description.txt"
    if not p.exists():
        raise SystemExit("Missing job_description.txt for that job.")
    return p.read_text(encoding="utf-8").lower()

def flatten_skills(truth):
    skills = []
    for category in truth.get("skills", {}).values():
        skills += category
    return [s.lower() for s in skills]

def score(job_id):
    truth = load_truth()
    jd = load_jd(job_id)
    skills = flatten_skills(truth)

    matched = []
    for skill in skills:
        if skill.lower() in jd:
            matched.append(skill)

    score_pct = round((len(matched) / len(skills)) * 100, 1) if skills else 0

    print("\nMATCHED SKILLS:")
    for m in matched:
        print("-", m)

    print(f"\nSCORE: {score_pct}%")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--job", type=int, required=True)
    args = p.parse_args()
    score(args.job)