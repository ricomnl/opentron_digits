PROJECT_NAME = "opentrons_digits"

env: pyproject.toml
	poetry install

kernel: env
	poetry run python -m ipykernel install --user --name ${PROJECT_NAME}