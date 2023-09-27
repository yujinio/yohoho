.DEFAULT_GOAL := help

.PHONY: help
help: ## Display this help screen
	@grep -E '^[a-z.A-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

format-frontend:
	@echo "--- Formatting frontend ---"
	@cd frontend/yohoho && yarn run format
	@echo "--- Finished formatting frontend ---"

build-frontend: format-frontend ## Build frontend
	@echo "--- Building frontend ---"
	@cd frontend/yohoho && yarn run build
	@echo "--- Finished building frontend ---"
