"""Analyse public UK Indeed Hiring Lab job-posting index data."""

from __future__ import annotations

from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw")
OUT_DIR = Path("outputs")
OUT_DIR.mkdir(exist_ok=True)


def _read(name: str) -> pd.DataFrame:
    path = RAW_DIR / name
    if not path.exists():
        raise FileNotFoundError(
            f"{path} was not found. Run `python src/download_public_data.py` first."
        )
    df = pd.read_csv(path)
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df


def latest_rows(df: pd.DataFrame, group_col: str, value_col: str) -> pd.DataFrame:
    clean = df.dropna(subset=["date", group_col, value_col]).copy()
    idx = clean.groupby(group_col)["date"].idxmax()
    return (
        clean.loc[idx, [group_col, "date", value_col]]
        .sort_values(value_col, ascending=False)
        .reset_index(drop=True)
    )


def main() -> None:
    aggregate = _read("aggregate_job_postings_gb.csv")
    sectors = _read("job_postings_by_sector_gb.csv")
    regions = _read("regional_postings_gb.csv")
    cities = _read("city_postings_gb.csv")

    # Aggregate: prefer total postings if a variable column is present.
    agg = aggregate.copy()
    if "variable" in agg.columns:
        total_mask = agg["variable"].astype(str).str.lower().str.contains("total")
        if total_mask.any():
            agg = agg[total_mask]

    sa_col = next(
        (c for c in ["indeed_job_postings_index_SA", "indeed_job_postings_index"] if c in agg.columns),
        None,
    )
    if not sa_col:
        raise ValueError("No seasonally adjusted aggregate index column found.")

    agg_out = (
        agg.dropna(subset=["date", sa_col])
        .sort_values("date")[["date", sa_col]]
        .rename(columns={sa_col: "uk_job_postings_index"})
    )
    agg_out.to_csv(OUT_DIR / "uk_market_trend.csv", index=False)

    # Latest sector values.
    sector_value = "indeed_job_postings_index"
    if {"display_name", sector_value}.issubset(sectors.columns):
        sec = sectors.copy()
        if "variable" in sec.columns:
            mask = sec["variable"].astype(str).str.lower().str.contains("total")
            if mask.any():
                sec = sec[mask]
        latest_rows(sec, "display_name", sector_value).rename(
            columns={"display_name": "sector", sector_value: "job_postings_index"}
        ).to_csv(OUT_DIR / "latest_sector_index.csv", index=False)

    # Latest region values.
    if {"region", "indeed_job_postings_index"}.issubset(regions.columns):
        latest_rows(regions, "region", "indeed_job_postings_index").to_csv(
            OUT_DIR / "latest_region_index.csv", index=False
        )

    # Latest city values.
    if {"cities", "indeed_job_postings_index"}.issubset(cities.columns):
        latest_rows(cities, "cities", "indeed_job_postings_index").rename(
            columns={"cities": "city"}
        ).to_csv(OUT_DIR / "latest_city_index.csv", index=False)

    # Monthly UK trend for dashboard.
    monthly = agg_out.set_index("date").resample("MS").last().dropna().reset_index()
    monthly.to_csv(OUT_DIR / "uk_market_trend_monthly.csv", index=False)

    print("Generated:")
    for p in sorted(OUT_DIR.glob("*.csv")):
        print(f" - {p}")


if __name__ == "__main__":
    main()
