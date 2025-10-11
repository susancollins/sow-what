# Makefile for linting, testing, building, deploying

# -----------------------------------------------------------------------------
# Variables
# -----------------------------------------------------------------------------

VERSION = 0.1.0
PROJECT_NAME = sow_what
PROJECT_HOME ?= /usr/src/sow_what

TODAY = $(shell date "+%Y-%m-%d")

# CI variables
CI_COMMIT_SHORT_SHA ?= $(shell git rev-parse --short=8 HEAD)
BUILD_IMAGE ?= sow_what:latest
CLI ?= sow-what


# -----------------------------------------------------------------------------
# Targets
# -----------------------------------------------------------------------------

.PHONY: help build shell clean clean-build clean-pyc lint test repl lock install

help:  ## Show this help
	@echo "$(PROJECT_NAME) v$(VERSION) - Make invocations"
	@echo
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)


# -----------------------------------------------------------------------------
# Run
# -----------------------------------------------------------------------------

run: build ## Run the application
	docker run -v $(CURDIR):/app -w /app $(BUILD_IMAGE) \
		pixi run $(CLI)
# -----------------------------------------------------------------------------
# Project Management
# -----------------------------------------------------------------------------

install: ## Install dev environment via Pixi
	pixi install -e dev

lock pixi.lock: ## Lock environment dependencies
	@echo Rebuilding pixi.lock...
	pixi lock

build: lock ## Build Docker image
	docker buildx build --tag $(BUILD_IMAGE) .

shell: ## Open a shell inside the container
	docker run -it -v $(CURDIR):/app -v /app/.pixi -w /app $(BUILD_IMAGE) bash

# -----------------------------------------------------------------------------
# Code Quality
# -----------------------------------------------------------------------------

lint: ## Lint code, outside container. Requires pre-commit. Install dev dependencies if you have not already.
	@echo Running pre-commit --------------------------------------------------
	pre-commit run --all-files -v

# -----------------------------------------------------------------------------
# Testing
# -----------------------------------------------------------------------------

test: build ## Run tests inside container
	docker run -v $(CURDIR):/app -w /app $(BUILD_IMAGE)
		pixi run -e dev pytest -vv -s tests -m "not remote_integration"

test-integration: build ## Run integration tests inside container
	docker run -v $(CURDIR):/app -w /app $(BUILD_IMAGE)
		pixi run -e dev pytest -vv -s tests


# -----------------------------------------------------------------------------
# Cleanup
# -----------------------------------------------------------------------------

clean: clean-build clean-docs clean-pyc ## Remove all temp files

clean-build: ## Remove cached Python package builds and distributions
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info

clean-docs:
	rm -rf docs/source/generated
	rm -rf docs/build

clean-pyc: ## Remove cached Python bytecode
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

# -----------------------------------------------------------------------------
# Dev Utils
# -----------------------------------------------------------------------------

repl: ## Python shell with project loaded
	python3 -i -c 'import sow_what'


# -----------------------------------------------------------------------------
# Docs
# -----------------------------------------------------------------------------

docs: build
	docker run -v $(CURDIR):/app -v /app/.pixi -w /app $(BUILD_IMAGE) \
		pixi run -e docs make html

html:
	pixi run -e docs sphinx-apidoc -M -e -o docs/source/generated sow_what/
	pixi run -e docs sphinx-build -b html docs/source docs/build