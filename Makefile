SHELL:=/usr/bin/env bash

.PHONY: lint
lint:
	poetry run mypy mypy_extras tests/*.py
	poetry run flake8 .
	poetry run doc8 -q docs

.PHONY: unit
unit:
	poetry run pytest

.PHONY: package
package:
	poetry check
	poetry run pip check
	poetry run safety check --full-report

.PHONY: typetests
typetests:
	@# We do this to speed up the build:
	poetry run pytest typesafety -p no:cov -o addopts="" --mypy-ini-file=setup.cfg

.PHONY: test
test: lint unit package typetests

