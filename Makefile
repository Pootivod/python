.PHONY: run build enter

all: help

enter:
	@test "$$(pwd)" != "/app" || (echo "Already in virtual environment"; exit 1)
	bash scripts/enter.sh

build:
	bash scripts/build-base.sh

run:
	@test "$$(pwd)" = "/app" || (echo "You must run this command from the virtual environment."; exit 1)
	python src/main.py

clean:
	rm -rf __pycache__ build dist *.pyc

help:
	@echo "Available targets:"
	@echo "  enter     Enetrs in the virtual environment by docker"
	@echo "  run       Run the main application"
	@echo "  build     Build base image and push it to Docker Hub"
	@echo "  clean     Clean up build and cache files"