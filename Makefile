VENV := ./.venv
APPS := fahrraddiebstahl_berlin main
BIN := $(VENV)/bin
PYTHON := $(BIN)/python

.PHONY: help
help: ## Show this help
	@grep -Eh '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: venv
venv: ## Make a new virtual environment
	python3 -m venv .venv

.PHONY: install
install: venv ## Make venv and install requirements
	$(VENV)/bin/pip install -r requirements.txt

.PHONY: run
run: ## Run the server
	$(PYTHON) manage.py runserver

.PHONY: format
format: ## Format code with isort/black
	isort -rc $(APPS)
	black $(APPS)
