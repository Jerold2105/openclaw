import json
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRUTH = ROOT / "engine_step1_truth" / "truth_profile.json"

def load_truth():
    return json.loads(TRUTH.read_text(encoding="utf-8"))

def make_map(job_id: int):
    truth = load_truth()

    evidence = {
        "job_id": job_id,
        "sources": {
            "truth_profile": str(TRUTH)
        },
        "claims": []
    }

    # experience bullets
    for exp in truth.get("experience", []):
        for a in exp.get("achievements", []):
            evidence["claims"].append({
                "claim": a,
                "evidence_path": "experience.achievements",
                "source": "truth_profile.json"
            })

    # project bullets
    for proj in truth.get("projects", []):
        for d in proj.get("details", []):
            evidence["claims"].append({
                "claim": f"{proj.get('name')}: {d}",
                "evidence_path": "projects.details",
                "source": "truth_profile.json"
            })

    out = ROOT / "engine_step2_tailor" / "outputs" / "jobs" / f"job_{job_id}" / "evidence_map.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(evidence, indent=2), encoding="utf-8")
    print("OK:", out)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--job", type=int, required=True)
    a = p.parse_args()
    make_map(a.job)