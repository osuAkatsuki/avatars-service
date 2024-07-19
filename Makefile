#!/usr/bin/env make

build:
	docker build -t assets-service:latest .

run:
	docker run --network=host --env-file=.env -it assets-service:latest

run-bg:
	docker run --network=host --env-file=.env -d assets-service:latest
