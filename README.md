# UK Data Analytics Job Market

An end-to-end data analytics portfolio project examining UK hiring demand for data and analytics professionals using **Python, SQL, Power BI-ready outputs, public labour-market data, and an optional live jobs API**.

## Project Question

> **How is the UK data and analytics job market changing, where is demand concentrated, and which skills appear in live analytics vacancies?**

## What this repository demonstrates

- API / public-data ingestion
- reproducible data pipelines
- data cleaning and validation
- SQL analysis
- Python exploratory analysis
- text-based skill extraction
- time-series analysis
- geographic analysis
- dashboard design
- data ethics and source attribution
- automated testing with GitHub Actions

## Data Sources

### 1. Indeed Hiring Lab — public UK job-posting index
The public `job_postings_tracker` repository provides daily seasonally adjusted UK job-posting indices and is refreshed weekly.

Used for:
- UK job-posting trend
- occupational-sector trend
- regional trend
- city trend

Source:
https://github.com/hiring-lab/job_postings_tracker

Indeed Hiring Lab states that these data are available under **CC BY 4.0** and may be reused with attribution.

### 2. Office for National Statistics (ONS) — UK labour demand
ONS publishes **Labour demand volumes by Standard Occupation Classification (SOC 2020), UK**, containing online job-advert counts by local authority and occupation.

Dataset page:
https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/datasets/labourdemandvolumesbystandardoccupationclassificationsoc2020uk

The edition available when this project was prepared was released **21 August 2026** and covered January 2017 to July 2026.

### 3. Adzuna API — optional live analytics vacancy detail
The optional Adzuna collector can retrieve current UK vacancies for searches such as:
- Data Analyst
- BI Analyst
- Business Intelligence Analyst
- Reporting Analyst
- Data Scientist

It enables:
- advertised salary analysis
- employer analysis
- skill extraction from descriptions
- seniority analysis
- role-level comparisons

API documentation:
https://developer.adzuna.com/

**API credentials are never committed to GitHub.**

---

## Architecture

```text
PUBLIC DATA                         OPTIONAL LIVE DATA
Indeed Hiring Lab                  Adzuna API
       |                               |
       v                               v
download_public_data.py          collect_adzuna.py
       |                               |
       v                               v
analyse_public_market.py         clean_adzuna.py
       |                               |
       +---------------+---------------+
                       |
                       v
                  CSV outputs
                       |
              +--------+---------+
              |                  |
              v                  v
             SQL              Power BI
              |                  |
              +--------+---------+
                       |
                       v
              Portfolio insights
```

## Repository Structure

```text
uk-data-analytics-job-market/
|
|-- .github/workflows/
|   `-- ci.yml
|
|-- dashboard/
|   |-- POWER_BI_BUILD_GUIDE.md
|   `-- dashboard_wireframe.png
|
|-- data/
|   |-- raw/
|   `-- processed/
|
|-- docs/
|   |-- DATA_DICTIONARY.md
|   |-- METHODOLOGY.md
|   |-- PORTFOLIO_RESUME_COPY.md
|   `-- PROJECT_INTERVIEW_GUIDE.md
|
|-- notebooks/
|   `-- 01_market_analysis.ipynb
|
|-- outputs/
|   `-- README.md
|
|-- sql/
|   |-- adzuna_schema.sql
|   `-- analysis_queries.sql
|
|-- src/
|   |-- analyse_public_market.py
|   |-- clean_adzuna.py
|   |-- collect_adzuna.py
|   |-- download_public_data.py
|   `-- run_pipeline.py
|
|-- tests/
|   |-- fixtures/
|   `-- test_pipeline.py
|
|-- .env.example
|-- .gitignore
|-- CITATION.cff
|-- LICENSE
|-- Makefile
|-- requirements.txt
`-- README.md
```

## Quick Start — public-data version (no API key required)

### 1. Create an environment

```bash
python -m venv .venv
```

macOS / Linux:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Download the public UK market data

```bash
python src/download_public_data.py
```

### 4. Run analysis

```bash
python src/analyse_public_market.py
```

or run both steps:

```bash
python src/run_pipeline.py --public
```

Generated analytical CSVs will appear in `outputs/`.

## Optional: add current analytics vacancies with Adzuna

Create an Adzuna developer account and copy `.env.example` to `.env`.

```text
ADZUNA_APP_ID=your_app_id
ADZUNA_APP_KEY=your_app_key
```

Then:

```bash
python src/collect_adzuna.py
python src/clean_adzuna.py
```

or:

```bash
python src/run_pipeline.py --adzuna
```

## Questions Answered

### Market trend
1. How has the UK job-posting index changed relative to the February 2020 baseline?
2. Which UK regions are above or below the national pattern?
3. Which cities show stronger or weaker posting activity?
4. How does the relevant data/analytics occupational sector compare with other sectors?

### Live analytics vacancies
5. Which analytics roles appear most often?
6. What share of adverts disclose salary?
7. What is the median advertised salary by role?
8. Which skills are most frequently mentioned?
9. How often are SQL and Python requested together?
10. How does Power BI compare with Tableau?
11. Which cloud/data-platform skills appear most often?
12. Which employers appear most often in the collected sample?

## Power BI Dashboard

The dashboard plan is in:

`dashboard/POWER_BI_BUILD_GUIDE.md`

Suggested pages:

1. **UK Market Overview**
2. **Analytics Skills**
3. **Salary Intelligence**
4. **Geography & Employers**

A layout wireframe is included in `dashboard/dashboard_wireframe.png`.

## Important Interpretation Note

The Indeed Hiring Lab series is an **index**, not a raw vacancy count. A value above 100 means postings are above the 1 February 2020 baseline; below 100 means they are below that baseline.

Online job adverts are also not identical to official vacancies. ONS explicitly distinguishes online job adverts from vacancies because some vacancies are advertised through channels other than online job boards.

## Data Ethics

- `.env` is excluded from Git.
- Raw Adzuna descriptions are excluded from public Git commits.
- No synthetic observations are presented as real market findings.
- Test fixtures are explicitly marked synthetic and are used only for automated tests.
- Source licences and limitations are documented.

## How to present this project in an interview

> I built a reproducible UK labour-market analytics pipeline using public job-posting data and an optional live-vacancy API. I used Python for ingestion, cleaning and analysis; SQL for business questions; and designed a Power BI dashboard covering market trends, geography, salaries and technical skill demand. I also added tests and CI so the project is reproducible rather than being a one-off notebook.

## Author

**Sam**  
MSc Data Analytics

---

### Attribution

Indeed Hiring Lab job-posting index data:  
https://github.com/hiring-lab/job_postings_tracker

Office for National Statistics labour-demand data:  
https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/datasets/labourdemandvolumesbystandardoccupationclassificationsoc2020uk
