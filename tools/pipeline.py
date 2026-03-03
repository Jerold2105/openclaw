import argparse
import subprocess
import sys

def run(cmd):
    print("\n>>", " ".join(cmd))
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--job", type=int, required=True)
    p.add_argument("--company", required=True)
    p.add_argument("--role", required=True)
    args = p.parse_args()

    # 1. Attach JD
    run([sys.executable, "tools/attach_jd.py", "--job", str(args.job)])

    # 2. Generate Resume
    run([sys.executable, "tools/generate_resume.py"])

    # 3. Convert Resume PDF
    run([sys.executable, "tools/convert_to_pdf.py"])

    # 4. Generate Cover Letter
    run([
        sys.executable,
        "tools/generate_cover_letter.py",
        "--job", str(args.job),
        "--company", args.company,
        "--role", args.role
    ])

    # 5. Convert Cover Letter PDF
    run([
        sys.executable,
        "tools/convert_cover_letter.py",
        "--job", str(args.job)
    ])

    # 6. Score Job
    run([sys.executable, "tools/score_job.py", "--job", str(args.job)])

    # 7. Generate Evidence Map
    run([sys.executable, "tools/evidence_map.py", "--job", str(args.job)])

    print("\nPIPELINE COMPLETE — READY_FOR_REVIEW")