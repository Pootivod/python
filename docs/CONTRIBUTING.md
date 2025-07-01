# Notes for developers 

## Build

The purpose of .dockerbuild is creating main build of Python container.

In order to build and push new image use those comands

```bash

docker build -t amelzzi/devops-python:main -f .dockerbuild .

docker push amelzzi/devops-python:main

```