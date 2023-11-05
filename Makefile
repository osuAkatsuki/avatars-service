#!/usr/bin/env make

build:
	docker build -t avatars-service:latest .

run:
	docker run --network=host --env-file=.env -it avatars-service:latest

run-bg:
	docker run --network=host --env-file=.env -d avatars-service:latest
