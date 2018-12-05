PWD:= $(shell pwd)

build:
	docker build  web-service

run: 
	docker-compose up --build

run-test-against-running-docker:
	DOCKER_RUN=1 python3 -m pytest test_api.py -s
