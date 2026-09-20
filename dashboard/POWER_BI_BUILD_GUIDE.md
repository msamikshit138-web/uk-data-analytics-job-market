# Power BI Build Guide

## Data to import

Public pipeline:
- `outputs/uk_market_trend_monthly.csv`
- `outputs/latest_sector_index.csv`
- `outputs/latest_region_index.csv`
- `outputs/latest_city_index.csv`

Optional Adzuna pipeline:
- `data/processed/adzuna_public.csv`
- `outputs/adzuna_skill_demand.csv`
- `outputs/adzuna_role_summary.csv`
- `outputs/adzuna_region_summary.csv`

## Page 1 — UK Market Overview
Cards:
- Latest UK posting index
- Change versus previous month
- Highest regional index
- Highest city index

Visuals:
- Line: UK monthly posting index
- Bar: latest regional indices
- Bar: selected occupational-sector indices
- Table: latest cities

## Page 2 — Analytics Skills
Requires Adzuna detail layer.

Visuals:
- Top skills
- SQL vs Python
- Power BI vs Tableau
- Cloud/platform skills
- Skills by role

Slicers:
- role group
- seniority
- region

## Page 3 — Salary Intelligence
Requires Adzuna detail layer.

Visuals:
- median salary by role
- median salary by seniority
- median salary by region
- salary disclosure rate
- salary by selected skill

## Page 4 — Geography & Employers
Requires Adzuna detail layer.

Visuals:
- map of jobs
- top regions
- top employers
- role mix by region

## Suggested calculated measures

```DAX
Total Jobs =
COUNTROWS(adzuna_public)

Median Salary =
MEDIAN(adzuna_public[salary_mid_clean])

Salary Disclosure % =
DIVIDE(
    SUM(adzuna_public[salary_available]),
    COUNTROWS(adzuna_public)
)

SQL Jobs =
CALCULATE(
    [Total Jobs],
    adzuna_public[skill_sql] = 1
)

Python Jobs =
CALCULATE(
    [Total Jobs],
    adzuna_public[skill_python] = 1
)
```

## Storytelling rule
Every visual should answer a question. Avoid adding charts simply because a field exists.
