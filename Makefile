format: 
	uv run isort ./src/

check:
	uv run ruff check ./src/
