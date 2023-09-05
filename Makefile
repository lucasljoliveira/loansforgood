update-precommit:
	poetry run pre-commit install && poetry run pre-commit autoupdate

lint:
	poetry run pre-commit run

test:
	poetry run pytest -s loansforgood --cov=loansforgood/apps -l

dc-project-up:
	docker-compose up app celery react

dc-project-test:
	docker-compose up test
