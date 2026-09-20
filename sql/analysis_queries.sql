-- 1. Overall market summary
SELECT
    COUNT(*) AS total_jobs,
    ROUND(PERCENTILE_CONT(0.5)
          WITHIN GROUP (ORDER BY salary_mid_clean)::numeric, 0) AS median_salary,
    ROUND(100.0 * AVG(salary_available), 1) AS salary_disclosure_pct
FROM uk_analytics_jobs;

-- 2. Jobs and median salary by role
SELECT
    role_group,
    COUNT(*) AS jobs,
    ROUND(PERCENTILE_CONT(0.5)
          WITHIN GROUP (ORDER BY salary_mid_clean)::numeric, 0) AS median_salary
FROM uk_analytics_jobs
GROUP BY role_group
ORDER BY jobs DESC;

-- 3. Jobs by region
SELECT
    region,
    COUNT(*) AS jobs,
    ROUND(PERCENTILE_CONT(0.5)
          WITHIN GROUP (ORDER BY salary_mid_clean)::numeric, 0) AS median_salary
FROM uk_analytics_jobs
GROUP BY region
ORDER BY jobs DESC;

-- 4. Core skill demand
SELECT 'SQL' AS skill, SUM(skill_sql) AS jobs FROM uk_analytics_jobs
UNION ALL SELECT 'Python', SUM(skill_python) FROM uk_analytics_jobs
UNION ALL SELECT 'Power BI', SUM(skill_power_bi) FROM uk_analytics_jobs
UNION ALL SELECT 'Tableau', SUM(skill_tableau) FROM uk_analytics_jobs
UNION ALL SELECT 'Excel', SUM(skill_excel) FROM uk_analytics_jobs
UNION ALL SELECT 'Azure', SUM(skill_azure) FROM uk_analytics_jobs
UNION ALL SELECT 'AWS', SUM(skill_aws) FROM uk_analytics_jobs
UNION ALL SELECT 'Snowflake', SUM(skill_snowflake) FROM uk_analytics_jobs
UNION ALL SELECT 'Databricks', SUM(skill_databricks) FROM uk_analytics_jobs
UNION ALL SELECT 'dbt', SUM(skill_dbt) FROM uk_analytics_jobs
ORDER BY jobs DESC;

-- 5. SQL + Python co-occurrence
SELECT
    COUNT(*) FILTER (WHERE skill_sql = 1 AND skill_python = 1) AS sql_and_python,
    COUNT(*) AS total_jobs,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE skill_sql = 1 AND skill_python = 1)
        / NULLIF(COUNT(*), 0), 1
    ) AS pct_sql_and_python
FROM uk_analytics_jobs;

-- 6. Power BI vs Tableau
SELECT
    SUM(skill_power_bi) AS power_bi_jobs,
    SUM(skill_tableau) AS tableau_jobs,
    SUM(CASE WHEN skill_power_bi = 1 AND skill_tableau = 1 THEN 1 ELSE 0 END)
        AS both_jobs
FROM uk_analytics_jobs;

-- 7. Salary by seniority
SELECT
    seniority,
    COUNT(*) AS jobs,
    ROUND(PERCENTILE_CONT(0.5)
          WITHIN GROUP (ORDER BY salary_mid_clean)::numeric, 0) AS median_salary
FROM uk_analytics_jobs
GROUP BY seniority
ORDER BY median_salary DESC NULLS LAST;

-- 8. Top employers
SELECT
    company,
    COUNT(*) AS jobs
FROM uk_analytics_jobs
GROUP BY company
ORDER BY jobs DESC
LIMIT 20;

-- 9. Salary and selected skills
SELECT
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary_mid_clean)
          FILTER (WHERE skill_sql = 1)::numeric, 0) AS sql_median_salary,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary_mid_clean)
          FILTER (WHERE skill_python = 1)::numeric, 0) AS python_median_salary,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary_mid_clean)
          FILTER (WHERE skill_power_bi = 1)::numeric, 0) AS power_bi_median_salary
FROM uk_analytics_jobs;

-- 10. Posting trend
SELECT posting_date, COUNT(*) AS jobs
FROM uk_analytics_jobs
GROUP BY posting_date
ORDER BY posting_date;
