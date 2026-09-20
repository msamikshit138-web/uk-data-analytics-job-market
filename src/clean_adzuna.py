"""Clean Adzuna analytics-vacancy data and extract skill flags."""

from __future__ import annotations

import re
from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
OUT_DIR = Path("outputs")

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
OUT_DIR.mkdir(parents=True, exist_ok=True)

SKILLS = {
    "sql": [r"\bsql\b"],
    "python": [r"\bpython\b"],
    "r": [r"(?<![a-z])r(?![a-z])", r"\br programming\b"],
    "power_bi": [r"\bpower\s*bi\b", r"\bpowerbi\b"],
    "tableau": [r"\btableau\b"],
    "excel": [r"\bexcel\b", r"\bmicrosoft excel\b"],
    "looker": [r"\blooker\b"],
    "aws": [r"\baws\b", r"\bamazon web services\b"],
    "azure": [r"\bazure\b"],
    "gcp": [r"\bgcp\b", r"\bgoogle cloud\b"],
    "snowflake": [r"\bsnowflake\b"],
    "databricks": [r"\bdatabricks\b"],
    "spark": [r"\bspark\b", r"\bpyspark\b"],
    "dbt": [r"\bdbt\b"],
    "power_query": [r"\bpower query\b"],
    "dax": [r"\bdax\b"],
    "sas": [r"\bsas\b"],
    "alteryx": [r"\balteryx\b"],
    "statistics": [r"\bstatistics?\b", r"\bstatistical\b"],
    "machine_learning": [r"\bmachine learning\b"],
    "git": [r"\bgit\b", r"\bgithub\b"],
}


def contains_any(text: str, patterns: list[str]) -> int:
    return int(any(re.search(p, text, flags=re.I) for p in patterns))


def classify_role(title: str) -> str:
    t = title.lower()
    if "data scientist" in t:
        return "Data Scientist"
    if "business intelligence" in t or re.search(r"\bbi\b", t):
        return "BI Analyst"
    if "reporting" in t:
        return "Reporting Analyst"
    if "data analyst" in t:
        return "Data Analyst"
    if "analytics" in t or "analyst" in t:
        return "Other Analytics"
    return "Other"


def classify_seniority(title: str) -> str:
    t = title.lower()
    if any(x in t for x in ["graduate", "junior", "entry level", "trainee", "apprentice"]):
        return "Junior"
    if any(x in t for x in ["senior", "lead", "principal", "manager", "head of"]):
        return "Senior"
    return "Mid / Unspecified"


def extract_region(location_area: str) -> str:
    if pd.isna(location_area):
        return "Unknown"
    parts = [x.strip() for x in str(location_area).split(">") if x.strip()]
    if len(parts) >= 2 and parts[0].lower() in {"uk", "united kingdom"}:
        return parts[1]
    return parts[0] if parts else "Unknown"


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    if "job_id" in out.columns:
        out = out.drop_duplicates(subset=["job_id"], keep="first")

    out["title"] = out["title"].fillna("").str.strip()
    out["description"] = out["description"].fillna("")
    out["company"] = out["company"].fillna("Unknown")
    out["location"] = out["location"].fillna("Unknown")

    out["created"] = pd.to_datetime(out["created"], errors="coerce", utc=True)
    out["extracted_at"] = pd.to_datetime(out["extracted_at"], errors="coerce", utc=True)
    out["posting_date"] = out["created"].dt.date

    for col in ["salary_min", "salary_max"]:
        out[col] = pd.to_numeric(out[col], errors="coerce")

    out["salary_mid"] = out[["salary_min", "salary_max"]].mean(axis=1)
    out["salary_available"] = out["salary_mid"].notna().astype(int)
    out["salary_mid_clean"] = out["salary_mid"].where(
        out["salary_mid"].between(12000, 250000)
    )

    out["role_group"] = out["title"].apply(classify_role)
    out["seniority"] = out["title"].apply(classify_seniority)
    out["region"] = out.get("location_area", pd.Series(index=out.index, dtype="object")).apply(extract_region)

    combined = (out["title"] + " " + out["description"]).str.lower()

    for skill, patterns in SKILLS.items():
        out[f"skill_{skill}"] = combined.apply(lambda x: contains_any(x, patterns))

    skill_cols = [f"skill_{s}" for s in SKILLS]
    out["skills_count"] = out[skill_cols].sum(axis=1)
    return out


def build_outputs(df: pd.DataFrame) -> None:
    skill_cols = [c for c in df.columns if c.startswith("skill_")]
    skills = (
        df[skill_cols].sum()
        .sort_values(ascending=False)
        .rename("job_count")
        .reset_index()
        .rename(columns={"index": "skill"})
    )
    skills["skill"] = skills["skill"].str.replace("skill_", "", regex=False)
    skills["share_of_jobs_pct"] = (100 * skills["job_count"] / len(df)).round(1)
    skills.to_csv(OUT_DIR / "adzuna_skill_demand.csv", index=False)

    role = (
        df.groupby("role_group", dropna=False)
        .agg(
            jobs=("job_id", "count"),
            median_salary=("salary_mid_clean", "median"),
            salary_disclosure_rate=("salary_available", "mean"),
        )
        .reset_index()
        .sort_values("jobs", ascending=False)
    )
    role["salary_disclosure_rate"] = (100 * role["salary_disclosure_rate"]).round(1)
    role.to_csv(OUT_DIR / "adzuna_role_summary.csv", index=False)

    region = (
        df.groupby("region", dropna=False)
        .agg(
            jobs=("job_id", "count"),
            median_salary=("salary_mid_clean", "median"),
        )
        .reset_index()
        .sort_values("jobs", ascending=False)
    )
    region.to_csv(OUT_DIR / "adzuna_region_summary.csv", index=False)


def main() -> None:
    files = sorted(RAW_DIR.glob("adzuna_uk_analytics_jobs_*.csv"))
    if not files:
        raise FileNotFoundError(
            "No Adzuna raw dataset found. Run `python src/collect_adzuna.py` first."
        )

    df = pd.read_csv(files[-1])
    clean = clean_dataframe(df)

    # Full local analytical file (contains advert descriptions).
    clean.to_csv(PROCESSED_DIR / "adzuna_full_local.csv", index=False)

    # Public-safe derived file: no full description / redirect URL.
    public_cols = [c for c in clean.columns if c not in {"description", "redirect_url"}]
    clean[public_cols].to_csv(PROCESSED_DIR / "adzuna_public.csv", index=False)

    build_outputs(clean)
    print(f"Processed {len(clean):,} unique adverts.")


if __name__ == "__main__":
    main()
