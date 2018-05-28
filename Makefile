clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*.~' -exec rm -f {} +
	find . -name '.cache' -exec rm -rf {} +
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.db' -exec rm -rf {} +

build:
	docker-compose build

publish:
	docker-compose push simple_app

install:
	pipenv install
	pipenv run python app/main.py

up:
	docker-compose up

down:
	docker-compose down

rmi:
	docker rmi $(docker images -f dangling=true -q)

exec:
	docker-compose exec --privileged simple_app /bin/bash
