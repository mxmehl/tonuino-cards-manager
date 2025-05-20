# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2025 Max Mehl

.DEFAULT_GOAL := help
.PHONY: help check-poetry setup pytest pylint formatting mypy reuse test-all


help: ## Show help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

PYTHON = python3
POETRY = poetry

check-requirements: ## Check if Python and Poetry are installed
	@command -v $(PYTHON) >/dev/null 2>&1 || { \
		echo "Python 3 is not installed. Please install it from https://www.python.org/downloads/"; \
		exit 1; \
	}
	@command -v $(POETRY) >/dev/null 2>&1 || { \
		echo "Poetry is not installed. Please install it from https://python-poetry.org/docs/#installation"; \
		exit 1; \
	}

setup: check-requirements ## Install dependencies: install dependencies via poetry
	$(POETRY) install -q

pytest: ## Run pytest: unit tests
	$(POETRY) run pytest --cov=tonuino_cards_manager

pylint: ## Run pylint: static code analysis
	$(POETRY) run pylint --disable=fixme tonuino_cards_manager/

formatting: ## Run isort and black: format code
	$(POETRY) run isort --check tonuino_cards_manager/
	$(POETRY) run black --check .

mypy: ## Run mypy: type checking
	$(POETRY) run mypy

reuse: ## Run reuse: license and copyright best practices
	$(POETRY) run reuse lint

test-all: setup pytest pylint formatting mypy reuse ## Run all tests
	@echo
	@echo "--------------------------------"
	@echo "All tests passed!"
