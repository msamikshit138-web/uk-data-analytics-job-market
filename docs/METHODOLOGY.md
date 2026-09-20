# Methodology

## 1. Research objective
The project investigates UK labour-market demand with two complementary layers:

1. **Macro market trend** using public job-posting indices.
2. **Role-level analytics detail** using an optional live vacancy API.

## 2. Public market layer
Indeed Hiring Lab publishes daily UK series that are seasonally adjusted and indexed to a February 2020 baseline. The project downloads:

- national UK posting index
- sector posting index
- UK regional posting index
- UK city posting index

The latest observation for each geography/sector is extracted, and the national series is also resampled monthly for dashboard readability.

## 3. Vacancy-detail layer
Adzuna is queried for several analytics-related search terms.

Because overlapping search terms can return the same vacancy, observations are deduplicated using `job_id`.

## 4. Role classification
Job titles are classified into:

- Data Analyst
- BI Analyst
- Reporting Analyst
- Data Scientist
- Other Analytics
- Other

This classification is deterministic and keyword based.

## 5. Seniority classification
Titles containing terms such as `junior`, `graduate`, or `trainee` are classified as Junior.
Titles containing terms such as `senior`, `lead`, `principal`, or `manager` are classified as Senior.
All others are Mid / Unspecified.

## 6. Skill extraction
A controlled dictionary and regular expressions detect technologies in job title + description text.

Examples:
- SQL
- Python
- Power BI
- Tableau
- Excel
- Azure
- AWS
- Snowflake
- Databricks
- dbt

The method identifies mentions, not proficiency level or whether a skill is mandatory.

## 7. Salary
`salary_mid` is the midpoint of advertised minimum and maximum salary where available.
`salary_mid_clean` excludes values outside £12,000–£250,000 to reduce obvious unit/data-entry anomalies.

This is a transparent rule rather than a claim that all excluded values are errors.

## 8. Limitations
- Job adverts are not equivalent to official vacancies.
- Search APIs are samples of the online market and may not cover all employers.
- Duplicate detection depends on the source identifier.
- Keyword extraction can create false positives/negatives.
- Salary disclosure is incomplete.
- Regional classifications depend on source location fields.
- A posting index shows change relative to baseline, not raw number of vacancies.
