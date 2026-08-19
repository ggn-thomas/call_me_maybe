default:
        @echo "Commandes disponibles :"
        @echo "  make install       - Install project dependencies using pip, uv, pipx, or any other package manager of your choice."
        @echo "  make run           - Execute the main script"
        @echo "  make debug         - Run the main script in debug mode using Python’s built-in debugger"
        @echo "  make clean         - Remove temporary files or cache"
        @echo "  make lint          - Execute the commands flake8 . and mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs"
		@echo "  make lint-strict   - Execute the commands flake8 . and mypy . --strict"

install: 
	pip install

run:

debug:

clean:

lint:

lint-strict: