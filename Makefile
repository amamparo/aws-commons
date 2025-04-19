install:
	poetry install --no-root

lint:
	poetry run pylint src tests infrastructure

types:
	poetry run mypy src tests infrastructure

test:
	poetry run python -m unittest discover -s 'tests' -p '*.py'

check: lint types test

diff:
	cdk diff --fail

deploy:
	cdk deploy --require-approval never