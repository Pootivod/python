# DevOps

Little windows on tkInter

## Installing

Install VcXsrv
https://sourceforge.net/projects/vcxsrv/

```bash
docker build devops-app .
```
## Running

Run VcXsrv 

```bash
winpty docker run -it --rm -e DISPLAY=host.docker.internal:0.0 devops-app
