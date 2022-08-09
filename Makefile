install:
	poetry install

build:
	poetry build

package-install:
	python3 -m pip install --user dist/*.whl

lint:
	@poetry run flake8 page_loader tests

page_loader:
	@poetry run page_loader

test:
	poetry run pytest -vvs
	
test-coverage:
	poetry run coverage run --source=page_loader -m pytest tests
	poetry run coverage xml

.PHONY: test, page_loader
