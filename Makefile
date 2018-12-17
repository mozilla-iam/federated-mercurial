.PHONY: all
all:
	@echo 'Available make targets:'
	@grep '^[^#[:space:]^\.].*:' Makefile


.PHONY: lint
lint: ## check style with flake8
	flake8 federated_mercurial tests

.PHONY: test
test: ## run tests quickly with the default Python
	py.test

.PHONY: docker-build
docker-build:
	cd docker/hgweb && \
	docker build -t mozillaiam/federated-mercurial-hgweb:latest .

.PHONY: docker-run
docker-run:
	docker run --rm -ti -p 8000:8000 mozillaiam/federated-mercurial-hgweb:latest

.PHONY: compose-run
compose-run:
	cd docker && \
	  docker-compose -f compose.yml up
