SHELL := bash
.DEFAULT_GOAL := help

.PHONY: install
install: ## Create the virtual environment with all dependency groups
	@uv sync

.PHONY: lint
lint: ## Lock consistency and ruff
	@uv lock --locked
	@uv run ruff check .
	@uv run ruff format --check .

.PHONY: test
test: ## Tests with coverage
	@uv run pytest --cov --cov-report=term-missing

.PHONY: verify
verify: lint test ## The one gate: run before reporting any change complete

.PHONY: build
build: ## Build sdist and wheel into dist/
	@uv build

symlink-global-docker-env: ## symlink global docker env file for local development
	@DOCKERFILES_SHARE_DIR="$HOME/.local/share/dockerfiles" \
	DOCKER_GLOBAL_ENV_FILENAME=".env.docker" \
	DOCKER_GLOBAL_ENV_FILE="$${DOCKERFILES_SHARE_DIR}/$${DOCKER_GLOBAL_ENV_FILENAME}" \
	[ -f "$${DOCKER_GLOBAL_ENV_FILE}" ] && ln -sf "$${DOCKER_GLOBAL_ENV_FILE}" .env.docker || echo "Global docker env file not found"

docker-login: ## login to docker
	@bash .docker/.docker-scripts/docker-compose.sh login

docker-build-base: ## build the docker base image
	@bash .docker/.docker-scripts/docker-compose.sh build --variant base

docker-build-app: ## build the docker app image
	@bash .docker/.docker-scripts/docker-compose.sh build --variant app

docker-config-base: ## show the docker base config
	@bash .docker/.docker-scripts/docker-compose.sh config --variant base

docker-config-app: ## show the docker app config
	@bash .docker/.docker-scripts/docker-compose.sh config --variant app

docker-push-base: ## push the docker base image
	@bash .docker/.docker-scripts/docker-compose.sh push --variant base

docker-push-app: ## push the docker app image
	@bash .docker/.docker-scripts/docker-compose.sh push --variant app

docker-run-base: ## run the docker base image
	@bash .docker/.docker-scripts/docker-compose.sh run --variant base

docker-run-app: ## run the docker app image
	@bash .docker/.docker-scripts/docker-compose.sh run --variant app

docker-up-app: ## launch the docker app image
	@bash .docker/.docker-scripts/docker-compose.sh up --variant app

docker-up-app-detach: ## launch the docker app image in detached mode
	@bash .docker/.docker-scripts/docker-compose.sh up --variant app --detach

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-28s\033[0m %s\n", $$1, $$2}'
