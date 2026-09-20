from pathlib import Path
import sys
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from clean_adzuna import clean_dataframe


def test_adzuna_cleaning():
    fixture = Path(__file__).parent / "fixtures" / "adzuna_sample.csv"
    df = pd.read_csv(fixture)
    clean = clean_dataframe(df)

    assert len(clean) == 3
    assert clean.loc[clean["job_id"] == 1, "skill_sql"].iloc[0] == 1
    assert clean.loc[clean["job_id"] == 1, "skill_power_bi"].iloc[0] == 1
    assert clean.loc[clean["job_id"] == 2, "seniority"].iloc[0] == "Senior"
    assert clean.loc[clean["job_id"] == 1, "seniority"].iloc[0] == "Junior"
    assert clean["salary_mid_clean"].notna().all()
