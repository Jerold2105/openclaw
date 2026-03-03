import argparse
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]

def scrape(job_id: int, url: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)
        page.wait_for_timeout(5000)

        text = page.inner_text("body")
        browser.close()

    out_dir = ROOT / "engine_step2_tailor" / "outputs" / "jobs" / f"job_{job_id}"
    out_dir.mkdir(parents=True, exist_ok=True)

    out_file = out_dir / "job_description.txt"
    out_file.write_text(text, encoding="utf-8")

    print("OK: scraped JD →", out_file)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--job", type=int, required=True)
    p.add_argument("--url", required=True)
    a = p.parse_args()
    scrape(a.job, a.url)