default:
		@echo "Commandes disponibles :"
		@echo "  make install       - Install project dependencies using pip, uv, pipx, or any other package manager of your choice."
		@echo "  make run           - Execute the main script"
		@echo "  make debug         - Run the main script in debug mode using Python’s built-in debugger"
		@echo "  make clean         - Remove temporary files or cache"
		@echo "  make lint          - Execute the commands flake8 . and mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs"
		@echo "  make lint-strict   - Execute the commands flake8 . and mypy . --strict"

install:
	uv sync

run: 
	uv run python3 -m src

debug:
	uv run python -m pdb src/__main__.py

clean:
	rm -rf .venv/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	rm -rf dist/ build/ *.egg-info

lint:
	uv run ruff check .

lint-strict: