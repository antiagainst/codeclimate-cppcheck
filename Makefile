.PHONY: image

IMAGE_NAME ?= codeclimate/codeclimate-cppcheck

image:
	docker build --rm -t $(IMAGE_NAME) .
