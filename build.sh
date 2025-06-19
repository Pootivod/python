#!/bin/bash
set -euo pipefail

docker build -t amelzzi/devops-python:main -f .dockerbuild .

docker push amelzzi/devops-python:main