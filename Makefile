format: 
	uv run isort src && uv run pyink src

check:
	uv run ruff check ./src/

up:
	docker compose up --build

down: 
	docker compose down
