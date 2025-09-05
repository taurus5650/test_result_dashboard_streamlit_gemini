DEPLOYMENT_PATH := ./deployment/
DOCKER_COMPOSE_FILE := $(DEPLOYMENT_PATH)docker-compose-prod.yml
DOCKER_COMPOSE_FILE_DEV := $(DEPLOYMENT_PATH)docker-compose-dev.yml
DOCKER_SERVICE_NAME := automation_test_result_dashboard_service
DOCKER_IMAGE_TAG := $(DOCKER_SERVICE_NAME):latest


.PHONY: run-prod
run-prod:
	@echo "========== Starting Docker Compose Process =========="
	@echo "========== 1. Stopping and removing containers, and cleaning up unused images =========="
	docker-compose -f $(DOCKER_COMPOSE_FILE) down --remove-orphans
	docker image prune -f
	@echo "========== 2. Building and starting the Docker service ($(DOCKER_SERVICE_NAME)) =========="
	docker-compose -f $(DOCKER_COMPOSE_FILE) build --no-cache
	docker-compose -f $(DOCKER_COMPOSE_FILE) up -d
	@echo "========== 3. Checking the status of the Docker service ($(DOCKER_SERVICE_NAME)) =========="
	docker-compose -f $(DOCKER_COMPOSE_FILE) ps
	docker image prune -f
	docker rmi $(DOCKER_IMAGE_TAG) || echo "⚠️ Image not found or in use"
	@echo "========== Docker Compose Process Complete =========="

.PHONY: run-dev
run-dev:
	@echo "========== Starting Docker Compose Process =========="
	@echo "========== 1. Stopping and removing containers, and cleaning up unused images =========="
	docker-compose -f $(DOCKER_COMPOSE_FILE_DEV) down --remove-orphans
	docker image prune -f
	@echo "========== 2. Building and starting the Docker service ($(DOCKER_SERVICE_NAME)) =========="
	docker-compose -f $(DOCKER_COMPOSE_FILE_DEV) build --no-cache
	docker-compose -f $(DOCKER_COMPOSE_FILE_DEV) up -d
	@echo "========== 3. Checking the status of the Docker service ($(DOCKER_SERVICE_NAME)) =========="
	docker-compose -f $(DOCKER_COMPOSE_FILE_DEV) ps
	docker image prune -f
	docker rmi $(DOCKER_IMAGE_TAG) || echo "⚠️ Image not found or in use"
	@echo "========== Docker Compose Process Complete =========="