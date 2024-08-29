# import config.
ifneq ($(wildcard .make.env),)
    include .make.env
endif
include .envs/.local/.postgres
DOCKER_COMPOSE ?= docker compose -f docker-compose.local.yml
DJANGO_SERVICE ?= django_wiki_local

# ANSI escape code for colors
BLUE := \033[34m
RESET := \033[0m

help: ## This help
	@awk 'BEGIN {FS = ":.*?## "; printf "Usage:\n  make $(BLUE)<target>\n"} \
    /^[a-zA-Z_-]+:.*?## / {printf "$(BLUE)%-30s$(RESET) %s\n", $$1, $$2}' $(MAKEFILE_LIST)

runserver:  ## Run project
	@$(DOCKER_COMPOSE) up -d --build

stop: ## Stop running containers
	@$(DOCKER_COMPOSE) stop

migrations: ## Make migrations
	@$(DOCKER_COMPOSE) run --rm $(DJANGO_SERVICE) ./manage.py makemigrations

migrate: ## Migrate
	@$(DOCKER_COMPOSE) run --rm $(DJANGO_SERVICE) ./manage.py migrate

pytest: ## Run tests
	@$(DOCKER_COMPOSE) run --rm $(DJANGO_SERVICE) pytest

pytest_opensearch: ## Run tests for opensearch
	@$(DOCKER_COMPOSE) run --rm $(DJANGO_SERVICE) pytest -m opensearch

pytest_repeat: ## Run repeat test
	@$(DOCKER_COMPOSE) run --rm $(DJANGO_SERVICE) pytest -x -vv --count=$(filter-out $@,$(MAKECMDGOALS))

coverage: ## Run tests with coverage
	@$(DOCKER_COMPOSE) run --rm $(DJANGO_SERVICE) coverage run -m pytest
	@$(DOCKER_COMPOSE) run --rm $(DJANGO_SERVICE) coverage report
	@$(DOCKER_COMPOSE) run --rm $(DJANGO_SERVICE) coverage html

ruff: ## Run ruff fix
	@$(DOCKER_COMPOSE) run --rm $(DJANGO_SERVICE) ruff format .
	@$(DOCKER_COMPOSE) run --rm $(DJANGO_SERVICE) ruff check --fix .

mypy: ## Run mypy check
	@$(DOCKER_COMPOSE) run --rm $(DJANGO_SERVICE) mypy --disallow-untyped-defs --exclude \
	"/(test_.*\\.py$$|conftest_plugins/.*|conftest.py)" .

check: ## Run all checks
	@$(DOCKER_COMPOSE) run --rm $(DJANGO_SERVICE) ruff check .
	@$(DOCKER_COMPOSE) run --rm $(DJANGO_SERVICE) ruff format --check .
	@$(DOCKER_COMPOSE) run --rm $(DJANGO_SERVICE) mypy .
	@$(DOCKER_COMPOSE) run --rm $(DJANGO_SERVICE) pytest -n auto

manage: ## Run manage command. Use quotes for commands with -flags or special symbols
	@$(DOCKER_COMPOSE) run --rm $(DJANGO_SERVICE) ./manage.py $(filter-out $@,$(MAKECMDGOALS))

run: ## Run command within the container. Use quotes for commands with -flags or special symbols
	@$(DOCKER_COMPOSE) run --rm $(DJANGO_SERVICE) $(filter-out $@,$(MAKECMDGOALS))
