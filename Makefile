install:
	pip install .

run:
	python3 a_maze_ing.py config.txt

clean:
	rm -rf __pycache__ mazegen/__pycache__ .mypy_cache
	rm -f maze.txt

lint:
	python3 -m flake8 . --exclude=.venv
	python3 -m mypy . --ignore-missing-imports --exclude='.venv'

build:
	python3 -m pip install --upgrade build
	python3 -m build
	cp dist/mazegen-1.0.0-py3-none-any.whl .
	cp dist/mazegen-1.0.0.tar.gz .

.PHONY: install run clean lint build