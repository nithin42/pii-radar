.PHONY: install test lint format typecheck clean

install:
	pip install -e ".[dev]"
	pre-commit install

test:
	pytest --cov=pii_radar --cov-report=term-missing

lint:
	flake8 src/ tests/ --max-line-length=88 --extend-ignore=E203,W503

format:
	black src/ tests/

typecheck:
	mypy src/pii_radar/

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf build/ dist/ *.egg-info .pytest_cache htmlcov coverage.xml

all: format lint typecheck test
