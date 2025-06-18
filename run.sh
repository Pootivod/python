#!/bin/bash
set -euo pipefail


if docker ps --filter "name=devops-python" --format "{{.Names}}" | grep -wq "devops-python"; then
    docker kill devops-python
    echo "Killed existing devops-python container."
fi

echo "Starting a new amelzzi/devops-python container."

docker build --build-arg CYBERPUNK=true -t amelzzi/devops-python .

docker run -itd --name devops-python --rm -v .:/app -e DISPLAY=host.docker.internal:0.0 amelzzi/devops-python sleep infinity

clear
echo "Container devops-python is running and you are now inside the container's shell."
echo "To exit the container, type 'exit' or press Ctrl+D."

docker exec -it devops-python /bin/bash

yes | docker image prune