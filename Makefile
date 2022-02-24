install:
	poetry install
	make build
	make package-install

build:
	poetry build

package-install:
	poetry run python -m pip install --force-reinstall dist/*.whl

lint:
	@poetry run flake8 page_loader

page_loader:
	@poetry run page_loader

test:
	poetry run coverage run --source=page_loader -m pytest tests
	
test-coverage:
	poetry run coverage xml

.PHONY: test, page_loader
