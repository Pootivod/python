#!/bin/bash

set -euo pipefail

docker build -t amelzzi/devops-python:base -f ./build/Dockerfile.base .

docker push amelzzi/devops-python:base