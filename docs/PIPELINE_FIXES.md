# Pipeline Fixes for the Next API Run

## 1. Preserve Adzuna salary prediction status

The Adzuna search response includes a `salary_is_predicted` field. Add this to `flatten_job()`:

```python
"salary_is_predicted": job.get("salary_is_predicted"),
```

This lets the project separate advertised salary values from Adzuna-predicted salary values.

## 2. Keep a current-window field

After parsing dates:

```python
df["age_days"] = (
    df["extracted_at"] - df["created"]
).dt.total_seconds() / 86400
```

Create a current core sample using:

```python
CORE_ROLES = [
    "Data Analyst",
    "BI Analyst",
    "Reporting Analyst",
    "Data Scientist",
]

portfolio_df = df[
    df["role_group"].isin(CORE_ROLES)
    & (df["age_days"] <= 30)
].copy()
```

## 3. Describe skills correctly

The Adzuna search documentation says only a snippet of the job description is returned. Label these metrics:

**Skill mentions in API snippets**

not:

**Percentage of employers requiring each skill**

## 4. Avoid calling the salary field 'salary disclosure rate'

Because the current dataset does not preserve `salary_is_predicted`, `salary_available` cannot reliably be interpreted as an employer salary-disclosure indicator.
