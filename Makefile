run-server:
	@echo "Running server..."
	@python -m server.server

lint-server:
	@echo "Linting server..."
	@ruff check server

format-server:
	@echo "Formatting server..."
	@ruff format server
