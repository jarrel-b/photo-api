PROJECT_NAME = photocatalog

black: 
	black .

black-diff:
	black --check --diff .

flake:
	flake8 . --exclude=*/settings.py,*/admin.py
 
isort:
	isort -rc .

isort-diff:
	isort -rc . --diff --check-only

format: isort black

coverage-report:
	coverage report -m

pylint:
	pylint $(PROJECT_NAME)

mypy:
	find . -name '*.py' | xargs mypy --ignore-missing-imports

test: black-diff isort-diff flake
	coverage run --source='.' -m pytest . -v

run-local:
	python manage.py runserver
