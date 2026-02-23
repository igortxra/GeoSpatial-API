format: 
	uv run isort src alembic && uv run pyink src alembic

check:
	uv run ruff check ./src/

up:
	docker compose up --build --detach

down: 
	docker compose down

clean:
	docker compose down --volumes --remove-orphans

migration:
	uv run alembic upgrade head

notebook:
	# Install Jupyter Notebook dependencies
	uv sync --group=notebook
	
	# Start Jupyter Notebook server
	uv run jupyter notebook ./utils/original.ipynb
	
	# Uninstall Jupyter Notebook dependencies
	uv sync --no-group=notebook

ingestion:
	# Install ingestion script dependencies
	uv sync --group=ingestion
	# Run ingestion script
	uv run python ./utils/ingestion.py
	# Uninstall ingestion script dependencies
	uv sync --no-group=ingestion

sql:
	uv run alembic upgrade dba20e7e5d18:head --sql > ./setup.sql
