# Interview Guide

## 30-second explanation
"I wanted a portfolio project that was directly relevant to the market I was applying into. I built a UK data-analytics job-market pipeline that combines public labour-market time series with optional live vacancy data. I used Python for data ingestion and transformation, SQL for analysis, and created Power BI-ready output tables. I also added testing and CI so it is reproducible."

## Why use two data sources?
The public posting index provides a stable market-level trend, while live vacancy data adds job-level detail such as titles, salaries, companies and skills.

## Why not call the Indeed index a vacancy count?
Because it is an indexed measure of job postings relative to a baseline. Job postings and vacancies are related but conceptually different.

## Why regex skill extraction?
It is transparent, easy to audit and appropriate for a portfolio pipeline. A future version could compare it with NLP/entity extraction.

## What would you improve next?
- scheduled monthly snapshots
- a warehouse layer
- dbt transformations
- NLP skill extraction
- salary modelling
- Streamlit dashboard
- richer ONS occupation comparisons
