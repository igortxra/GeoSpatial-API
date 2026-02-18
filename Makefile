format: 
	uv run isort ./src/

check:
	uv run ruff check ./src/

up:
	docker compose up --build

down: 
	docker compose down
