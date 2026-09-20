# Data Dictionary

## Public Indeed outputs

### `uk_market_trend.csv`
| Field | Meaning |
|---|---|
| date | observation date |
| uk_job_postings_index | seasonally adjusted UK posting index |

### `latest_sector_index.csv`
| Field | Meaning |
|---|---|
| sector | Indeed occupational sector |
| date | latest available date for the sector |
| job_postings_index | sector posting index |

### `latest_region_index.csv`
| Field | Meaning |
|---|---|
| region | UK region |
| date | latest available date |
| indeed_job_postings_index | regional posting index |

### `latest_city_index.csv`
| Field | Meaning |
|---|---|
| city | UK city |
| date | latest available date |
| indeed_job_postings_index | city posting index |

## Optional Adzuna processed data

Key analytical fields include:

| Field | Meaning |
|---|---|
| job_id | source advert identifier |
| title | vacancy title |
| company | employer / advertiser name |
| location | source location text |
| salary_min / salary_max | advertised salary bounds where available |
| salary_mid_clean | midpoint after plausibility filter |
| role_group | derived analytics role category |
| seniority | derived title-based seniority |
| region | derived broad region |
| skill_* | binary mention flag for named skill |
| skills_count | total tracked skill mentions |
