format: 
	uv run isort ./src/

check:
	uv run ruff check ./src/

update_requirements:
	uv pip freeze > requirements.txt
