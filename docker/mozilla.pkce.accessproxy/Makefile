IMAGE_NAME	:= "mozilla.pkce.accessproxy"
PORTS		:= "8080:80"
COMPOSE_CMD	:= "up"

all: help

help:
	@echo "Makefile configuration and targets:"
	@echo
	@grep '^[^#[:space:]].*:' Makefile

build: Dockerfile
	docker build -t $(IMAGE_NAME) .

compose: compose/docker-compose.yml
	touch compose/local.env
	docker-compose -f compose/docker-compose.yml $(COMPOSE_CMD)

run: Dockerfile
	docker run -i -p $(PORTS)  -t $(IMAGE_NAME)

.PHONY: help build run awslogin compose compose-detach compose-staging compose-production
