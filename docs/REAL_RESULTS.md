# Real Results — UK Data Analytics Job Market

## Analysis scope

The API extraction contains **798 unique job records**. For the main portfolio analysis, the sample is restricted to:

- postings created within 30 days of extraction;
- `Data Analyst`, `BI Analyst`, `Reporting Analyst`, and `Data Scientist` role groups.

This produces a cleaner **297-posting core analytics sample**.

Extraction timestamp in the supplied dataset: **20 September 2026 01:07 UTC**.

## Headline findings

### Role mix

| Role | Jobs | Share |
|---|---:|---:|
| Data Analyst | 127 | 42.8% |
| Reporting Analyst | 76 | 25.6% |
| BI Analyst | 71 | 23.9% |
| Data Scientist | 23 | 7.7% |

`Data Analyst` is the largest core role category in this 30-day sample.

### Geography

London accounts for **107 postings (36.0%)** of the core sample.

Top regions are reported in `outputs/region_summary_30d.csv`.

### Salary field

The median cleaned salary field across the core sample is approximately **£52,604**.

Median salary field by role:

- **Data Scientist**: £60,000
- **Data Analyst**: £53,288
- **BI Analyst**: £52,500
- **Reporting Analyst**: £51,095

**Important:** the current collector did not preserve Adzuna's `salary_is_predicted` field. Therefore these values should be described as **Adzuna salary fields**, not automatically as employer-disclosed salaries. Future API runs should store `salary_is_predicted`.

### Skill mentions

The most frequently detected skills in the core sample are:

- **Power Bi**: 51 postings (17.2%)
- **Sql**: 27 postings (9.1%)
- **Excel**: 11 postings (3.7%)
- **Python**: 8 postings (2.7%)
- **Tableau**: 6 postings (2.0%)
- **Machine Learning**: 6 postings (2.0%)
- **Statistics**: 5 postings (1.7%)
- **R**: 4 postings (1.3%)

SQL and Python are both detected in **6 postings (2.0%)**.

**Important:** Adzuna's search API provides only a snippet of each job description. These numbers are therefore **skill mentions detected in API snippets**, not the true proportion of employers requiring each skill.

## Data-quality decisions

The raw search results include many roles classified as `Other` or `Other Analytics`. They are retained in the full dataset for transparency but excluded from the headline role-market analysis.

The 30-day window is used to reduce the influence of stale postings.

Salary observations outside the pipeline's plausibility range are excluded from the cleaned salary measure.

## Recommended portfolio wording

> Analysed a 30-day sample of UK analytics job postings retrieved through the Adzuna API, focusing on Data Analyst, BI Analyst, Reporting Analyst and Data Scientist roles. Built reproducible Python transformations to compare role mix, geography, salary fields and technology mentions, while documenting API limitations and data-quality controls.

## Files

- `outputs/core_analytics_jobs_30d.csv`
- `outputs/role_summary_30d.csv`
- `outputs/region_summary_30d.csv`
- `outputs/skill_mentions_30d.csv`
- `outputs/skill_by_role_30d.csv`
- `outputs/seniority_summary_30d.csv`
- `outputs/top_employers_30d.csv`
- `charts/jobs_by_role.png`
- `charts/jobs_by_region.png`
- `charts/skill_mentions.png`
- `charts/median_salary_by_role.png`
