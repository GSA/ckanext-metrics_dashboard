CKAN_VERSION ?= 2.10
COMPOSE_FILE ?= docker-compose.yml

build: ## Build the  docker containers
	CKAN_VERSION=$(CKAN_VERSION) docker-compose -f $(COMPOSE_FILE) build

clean: ## Clean workspace and containers
	find . -name *.pyc -delete
	CKAN_VERSION=$(CKAN_VERSION) docker-compose -f $(COMPOSE_FILE) down -v --remove-orphans

lint: ## Lint the code
	CKAN_VERSION=$(CKAN_VERSION) docker-compose -f $(COMPOSE_FILE) run --rm app flake8 ckanext --count --show-source --statistics --exclude ckan

test: ## Run extension tests
	CKAN_VERSION=$(CKAN_VERSION) docker-compose -f $(COMPOSE_FILE) run --rm app ./test.sh

up: ## Start the containers
	CKAN_VERSION=$(CKAN_VERSION) docker-compose -f $(COMPOSE_FILE) up app

debug: ## Start the containers but don't start CKAN. This allows us to run ipdb.
	CKAN_VERSION=$(CKAN_VERSION) docker-compose -f $(COMPOSE_FILE) run -p 5000:5000 -v ./ckanext:/srv/app/ckanext -v ./test.sh:/srv/app/test.sh -v ./test.ini:/srv/app/test.ini -v ./setup.py:/srv/app/setup.py -v ./docker-entrypoint.d/:/docker-entrypoint.d/ -v ./seed.py:/srv/app/seed.py -v /etc/timezone:/etc/timezone:ro --rm app bash

upd: ## Start the containers in the background
	CKAN_VERSION=$(CKAN_VERSION) docker-compose -f $(COMPOSE_FILE) run --rm app ckan search-index rebuild -i -o -e
	CKAN_VERSION=$(CKAN_VERSION) docker-compose -f $(COMPOSE_FILE) up -d

seed: ## Seed some data into container
	CKAN_VERSION=$(CKAN_VERSION) docker-compose -f $(COMPOSE_FILE) run app python3 seed.py
	CKAN_VERSION=$(CKAN_VERSION) docker-compose -f $(COMPOSE_FILE) run app ckan search-index rebuild

.DEFAULT_GOAL := help
.PHONY: build clean help lint test up upd seed

# Output documentation for top-level targets
# Thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help: ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-10s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
