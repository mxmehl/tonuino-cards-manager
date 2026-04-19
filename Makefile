# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2025 Max Mehl

.DEFAULT_GOAL := help
.PHONY: help check-uv setup pytest ruff-lint ruff-format ty reuse test-all


help: ## Show help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

PYTHON = python3
UV = uv

check-requirements: ## Check if Python and uv are installed
	@command -v $(PYTHON) >/dev/null 2>&1 || { \
		echo "Python 3 is not installed. Please install it from https://www.python.org/downloads/"; \
		exit 1; \
	}
	@command -v $(UV) >/dev/null 2>&1 || { \
		echo "uv is not installed. Please install it from https://docs.astral.sh/uv/getting-started/installation/"; \
		exit 1; \
	}

setup: check-requirements ## Install dependencies: install dependencies via uv
	$(UV) sync -q

pytest: ## Run pytest: unit tests
	$(UV) run pytest --cov=tonuino_cards_manager

ruff-lint: ## Run ruff: linting
	$(UV) run ruff check

ruff-format: ## Run ruff: formatting check
	$(UV) run ruff format --check

ty: ## Run ty: type checking
	$(UV) run ty check

reuse: ## Run reuse: license and copyright best practices
	$(UV) run reuse lint

test-all: setup pytest ruff-lint ruff-format ty reuse ## Run all tests
	@echo
	@echo "--------------------------------"
	@echo "All tests passed!"
