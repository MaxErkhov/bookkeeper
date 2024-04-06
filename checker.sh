#!/bin/bash
# Silly way to execute checks.

poetry run pytest --cov
poetry run mypy --strict bookkeeper
poetry run pylint bookkeeper  --extension-pkg-whitelist=PySide6
poetry run flake8 bookkeeper

