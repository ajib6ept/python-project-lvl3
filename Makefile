install:
	poetry install

build:
	poetry build

package-install:
	python3 -m pip install --user dist/*.whl

lint:
	@poetry run flake8 page_loader

test:
	poetry run coverage run --source=page_loader -m pytest tests
	
test-coverage:
	poetry run coverage xml

.PHONY: test
