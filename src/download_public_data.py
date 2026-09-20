"""Download public UK labour-market time-series data from Indeed Hiring Lab."""

from __future__ import annotations

from pathlib import Path
import requests

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

FILES = {
    "aggregate_job_postings_gb.csv":
        "https://raw.githubusercontent.com/hiring-lab/job_postings_tracker/master/GB/aggregate_job_postings_gb.csv",
    "job_postings_by_sector_gb.csv":
        "https://raw.githubusercontent.com/hiring-lab/job_postings_tracker/master/GB/job_postings_by_sector_gb.csv",
    "regional_postings_gb.csv":
        "https://raw.githubusercontent.com/hiring-lab/job_postings_tracker/master/GB/regional_postings_gb.csv",
    "city_postings_gb.csv":
        "https://raw.githubusercontent.com/hiring-lab/job_postings_tracker/master/GB/city_postings_gb.csv",
}


def download_file(url: str, path: Path) -> None:
    response = requests.get(
        url,
        timeout=60,
        headers={"User-Agent": "uk-data-analytics-job-market/1.0"},
    )
    response.raise_for_status()
    path.write_bytes(response.content)


def main() -> None:
    for filename, url in FILES.items():
        path = RAW_DIR / filename
        print(f"Downloading {filename}...")
        download_file(url, path)
        print(f"Saved {path} ({path.stat().st_size:,} bytes)")

    print("\nSource: Indeed Hiring Lab job_postings_tracker (CC BY 4.0).")


if __name__ == "__main__":
    main()
