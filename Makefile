.DEFAULT_GOAL := help

base_python := python3
py := poetry run
python := $(py) python

reports_dir := reports


help:
	@echo "aiogram_cli"


# =================================================================================================
# Environment
# =================================================================================================

.PHONY: clean
clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -rf `find . -name .pytest_cache`
	rm -rf *.egg-info
	rm -f .coverage
	rm -f report.html
	rm -f .coverage.*
	rm -rf {build,dist,site,.cache,.mypy_cache,reports}


# =================================================================================================
# Code quality
# =================================================================================================

.PHONY: isort
isort:
	$(py) isort -rc aiogram_cli tests

.PHONY: black
black:
	$(py) black aiogram_cli tests

.PHONY: flake8
flake8:
	$(py) flake8 aiogram_cli test

.PHONY: flake8-report
flake8-report:
	mkdir -p $(reports_dir)/flake8
	$(py) flake8 --format=html --htmldir=$(reports_dir)/flake8 aiogram_cli test

.PHONY: mypy
mypy:
	$(py) mypy aiogram_cli

.PHONY: mypy-report
mypy-report:
	$(py) mypy aiogram_cli --html-report $(reports_dir)/typechecking

.PHONY: lint
lint: isort black flake8 mypy

# =================================================================================================
# Tests
# =================================================================================================

.PHONY: test
test:
	$(py) pytest --cov=aiogram_cli --cov-config .coveragerc tests/

.PHONY: test-coverage
test-coverage:
	mkdir -p $(reports_dir)/tests/
	$(py) pytest --cov=aiogram_cli --cov-config .coveragerc --html=$(reports_dir)/tests/index.html tests/
	$(py) coverage html -d $(reports_dir)/coverage

.PHONY: test-coverage-report
test-coverage-report:
	python -c "import webbrowser; webbrowser.open('file://$(shell pwd)/reports/coverage/index.html')"

# =================================================================================================
# Project
# =================================================================================================

.PHONY: build
build: clean flake8-report mypy-report test-coverage docs docs-copy-reports
	mkdir -p site/simple
	poetry build
	mv dist site/simple/aiogram_cli
