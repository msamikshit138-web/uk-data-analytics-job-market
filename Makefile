install:
	pip install -r requirements.txt

public:
	python src/run_pipeline.py --public

adzuna:
	python src/run_pipeline.py --adzuna

test:
	pytest -q
