# DevOps

Little windows on tkInter

## Installing

Install VcXsrv
https://sourceforge.net/projects/vcxsrv/

```bash
docker build -t amelzzi/devops-python .
```
--build-arg CYBERPUNK=true # sets my prompth

## Running

Run VcXsrv with 'Disable access control' ON.

```bash
docker run -itd --name devops-python --rm -v .:/app -e DISPLAY=host.docker.internal:0.0 amelzzi/devops-python sleep infinity
```

## Using

In order to enter virtaul os, you should use

```bash
docker exec -it devops-python /bin/bash
```
