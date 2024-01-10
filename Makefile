SOURCE_FILES ?= .

GIT_REVISION ?= $(shell git rev-parse --short HEAD)
GIT_TAG ?= $(shell git describe --tags --abbrev=0 | sed -e s/v//g)

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.DEFAULT_GOAL := help

.PHONY: info
info: ## show info
	@echo "GIT_REVISION: $(GIT_REVISION)"
	@echo "GIT_TAG: $(GIT_TAG)"

.PHONY: install-deps
install-deps: ## install dependencies
	poetry install --with lint,format,test,dev --no-root

.PHONY: lint
lint: ## lint codes
	poetry run black $(SOURCE_FILES) --check
	poetry run ruff $(SOURCE_FILES)

.PHONY: format
format: ## format codes
	poetry run black $(SOURCE_FILES)

.PHONY: test
test: ## test codes
	# poetry run pytest $(SOURCE_FILES)

.PHONY: ci-test
ci-test: install-deps lint test ## run CI test

.PHONY: server
server: ## run server
	poetry run uvicorn server.main:app --host 0.0.0.0 --port 8888 --reload

.PHONY: jupyterlab
jupyterlab: ## run jupyterlab server
	poetry run jupyter lab --port 8889
