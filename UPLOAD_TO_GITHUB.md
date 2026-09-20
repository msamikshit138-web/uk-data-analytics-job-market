# Upload This Project to GitHub

## Easiest method — GitHub website

1. Create a new **public** repository named:
   `uk-data-analytics-job-market`

2. Do **not** create an extra README, licence, or `.gitignore` on GitHub.

3. Extract the ZIP provided by ChatGPT.

4. Open the extracted `uk-data-analytics-job-market-final` folder.

5. Upload **all files and folders inside it** to the new GitHub repository.

6. Commit with:
   `Initial UK data analytics job market portfolio project`

## Better method — Git command line

From inside the extracted project folder:

```bash
git init
git add .
git commit -m "Initial UK data analytics job market portfolio project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/uk-data-analytics-job-market.git
git push -u origin main
```

## Before publishing

- Do not add your `.env` file.
- Do not add Adzuna API credentials.
- Raw Adzuna vacancy extracts are intentionally ignored by Git.
- Replace only the author/profile details you want to personalise.

## After upload

Run the public pipeline locally:

```bash
pip install -r requirements.txt
python src/run_pipeline.py --public
```

This downloads the public Indeed Hiring Lab UK time-series data and creates the analysis outputs.
