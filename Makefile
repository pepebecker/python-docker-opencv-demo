LOCAL_PATH = $(shell pwd)
DOCKER_PATH = /usr/src/app

IMAGE = ekazakov/python-opencv

init:
	@mkdir data

enter:
	@docker run -w $(DOCKER_PATH) --rm -it -v $(LOCAL_PATH):$(DOCKER_PATH) $(IMAGE) bash

run:
	@python main.py video/input.webm data/output.webm