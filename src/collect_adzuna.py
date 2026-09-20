"""Collect current UK analytics vacancies from the Adzuna API.

Raw extracts should be kept local and are ignored by Git.
"""

from __future__ import annotations

import os
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

COUNTRY = "gb"
RESULTS_PER_PAGE = 50
PAGES_PER_ROLE = 4

SEARCH_TERMS = [
    "data analyst",
    "business intelligence analyst",
    "BI analyst",
    "reporting analyst",
    "data scientist",
]

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)


def fetch_page(term: str, page: int) -> dict:
    if not APP_ID or not APP_KEY:
        raise RuntimeError(
            "Missing Adzuna credentials. Copy .env.example to .env and add "
            "ADZUNA_APP_ID and ADZUNA_APP_KEY."
        )

    url = f"https://api.adzuna.com/v1/api/jobs/{COUNTRY}/search/{page}"
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "results_per_page": RESULTS_PER_PAGE,
        "what": term,
        "content-type": "application/json",
        "sort_by": "date",
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def flatten_job(job: dict, search_term: str, extracted_at: str) -> dict:
    location = job.get("location") or {}
    company = job.get("company") or {}
    category = job.get("category") or {}

    return {
        "job_id": job.get("id"),
        "search_term": search_term,
        "title": job.get("title"),
        "company": company.get("display_name"),
        "location": location.get("display_name"),
        "location_area": " > ".join(location.get("area") or []),
        "latitude": job.get("latitude"),
        "longitude": job.get("longitude"),
        "category": category.get("label"),
        "salary_min": job.get("salary_min"),
        "salary_max": job.get("salary_max"),
        "contract_type": job.get("contract_type"),
        "contract_time": job.get("contract_time"),
        "created": job.get("created"),
        "description": job.get("description"),
        "redirect_url": job.get("redirect_url"),
        "extracted_at": extracted_at,
    }


def main() -> None:
    extracted_at = datetime.now(timezone.utc).isoformat()
    rows = []

    for term in SEARCH_TERMS:
        print(f"Collecting {term!r}")
        for page in range(1, PAGES_PER_ROLE + 1):
            payload = fetch_page(term, page)
            rows.extend(
                flatten_job(job, term, extracted_at)
                for job in payload.get("results", [])
            )
            time.sleep(0.5)

    df = pd.DataFrame(rows)
    if df.empty:
        raise RuntimeError("No jobs were returned by the API.")

    df = df.drop_duplicates(subset=["job_id"], keep="first")
    stamp = datetime.now().strftime("%Y%m%d")
    path = RAW_DIR / f"adzuna_uk_analytics_jobs_{stamp}.csv"
    df.to_csv(path, index=False)
    print(f"Saved {len(df):,} unique adverts to {path}")


if __name__ == "__main__":
    main()
