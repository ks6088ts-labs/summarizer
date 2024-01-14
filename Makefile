SOURCE_FILES ?= .

GIT_REVISION ?= $(shell git rev-parse --short HEAD)
GIT_TAG ?= $(shell git describe --tags --abbrev=0 | sed -e s/v//g)

DOCKERHUB_USERNAME ?= ks6088ts
DOCKER_IMAGE_NAME ?= summarizer
DOCKER_PLATFORM ?= linux/amd64
DOCKER_TAG_NAME ?= $(DOCKERHUB_USERNAME)/$(DOCKER_IMAGE_NAME):$(GIT_TAG)

DEBUG ?= false

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
	poetry install --with lint,format,scripts,test,dev --no-root

.PHONY: lint
lint: ## lint codes
	poetry run black $(SOURCE_FILES) --check
	poetry run ruff $(SOURCE_FILES)

.PHONY: format
format: ## format codes
	poetry run black $(SOURCE_FILES)
	poetry run ruff $(SOURCE_FILES) --fix

.PHONY: test
test: ## test codes
	# poetry run pytest $(SOURCE_FILES)

.PHONY: ci-test
ci-test: install-deps lint test ## run CI test

.PHONY: server
server: ## run server
	DEBUG=$(DEBUG) poetry run uvicorn server.main:app --host 0.0.0.0 --port 8888 --reload

.PHONY: jupyterlab
jupyterlab: ## run jupyterlab server
	poetry run jupyter lab --port 8889

.PHONY: docker-build
docker-build: ## docker build
	docker build --platform=$(DOCKER_PLATFORM) -t $(DOCKER_TAG_NAME) .

.PHONY: docker-run
docker-run: ## docker run
	docker run --platform=$(DOCKER_PLATFORM) --rm \
		-p "8888:8888" \
		--env "REVISION=$(GIT_REVISION)" \
		--env "VERSION=$(GIT_TAG)" \
		$(DOCKER_TAG_NAME)
