[![test](https://github.com/ks6088ts-labs/summarizer/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/ks6088ts-labs/summarizer/actions/workflows/test.yml?query=branch%3Amain)
[![release](https://github.com/ks6088ts-labs/summarizer/workflows/release/badge.svg)](https://github.com/ks6088ts-labs/summarizer/actions/workflows/release.yml)

# summarizer

A summarizer service using Azure OpenAI Service

## Prerequisites

- [Python (3.10+)](https://www.python.org/downloads/) as a primary language
- [Poetry](https://python-poetry.org/docs/#installation) as a package manager
- [GNU Make](https://www.gnu.org/software/make/) as a task runner

## Usage

All tasks are defined in [Makefile](./Makefile).  
To see all tasks, run the following command.

```shell
$ make
ci-test                        run CI test
docker-build                   docker build
docker-run                     docker run
format                         format codes
info                           show info
install-deps                   install dependencies
jupyterlab                     run jupyterlab server
lint                           lint codes
server                         run server
test                           test codes
```

### Install dependencies

To install dependencies, just run the following command.

```shell
$ make install-deps
```

### Run CI test

To make sure that your code is working as expected, you should run CI test before committing your code.
To run the whole CI test, just run the following command.

```shell
$ make ci-test
```

This task is also executed on GitHub Actions (see [test.yml](./.github/workflows/test.yml)).

### Run API server

To run API server, you need to set environment variables.

Create `*.env` files with reference to `*.env.sample` files.  
For example, just copy [azure_ai_search.env.sample](./azure_ai_search.env.sample) to `azure_ai_search.env` and edit it to fit your environment.

Then, run the following command to start API server.

```shell
$ make server
```

Playground for each API is live at `/FEATURE/playground` (e.g. `/search/playground`).

### Run notebook

To run notebook, run the following command.

```shell
$ make jupyterlab
```

### Run scripts

To run scripts, run the following command.

```shell
$ poetry run python scripts/TAGET_SCRIPT.py
```
