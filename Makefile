
build:
	docker-compose build

run:
	docker-compose run --rm app /bin/bash


pre-commit-run:
	pre-commit run --all-files
