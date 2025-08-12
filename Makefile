.PHONY: install run run-main lint tests

install:
	pip install -r requirements.txt

run:
	python -m uvicorn app.main:app --reload --port 8888

lint:
	python -m ruff check .

tests:
	python -m pytest tests