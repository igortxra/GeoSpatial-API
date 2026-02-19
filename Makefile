format: 
	uv run isort src && uv run pyink src

check:
	uv run ruff check ./src/

up:
	docker compose up --build --detach

down: 
	docker compose down

notebook:
	# Install Jupyter Notebook dependencies
	uv sync --group=notebook
	
	# Start Jupyter Notebook server
	uv run jupyter notebook ./jupyter_notebook/original.ipynb
	
	# Uninstall Jupyter Notebook dependencies
	uv sync --no-group=notebook

ingestion:
	# Install ingestion script dependencies
	uv sync --group=ingestion
	# Run ingestion script
	uv run python ./ingestion_script/ingestion.py
	# Uninstall ingestion script dependencies
	uv sync --no-group=ingestion
