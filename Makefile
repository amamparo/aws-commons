install:
	poetry install --no-root

lint:
	poetry run pylint src

types:
	poetry run mypy src

synth:
	cdk synth -q

check: lint types synth

diff:
	cdk diff

deploy:
	cdk deploy --require-approval never