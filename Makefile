run-server:
	@echo "Running server..."
	@python -m server.app

lint-server:
	@echo "Linting server..."
	@ruff check server

format-server:
	@echo "Formatting server..."
	@ruff format server
