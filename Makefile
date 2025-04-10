.PHONY: format lint check all

format:
	poetry run black .

lint:
	poetry run flake8 .

check:
	poetry run pre-commit run --all-files

all: format lint check
