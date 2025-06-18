FROM amelzzi/devops-python:main

ARG CYBERPUNK=false

WORKDIR /app 

RUN if [ "$CYBERPUNK" = "true" ]; then \
    apt-get update; \
    yes | apt-get install wget; \
    wget https://raw.githubusercontent.com/git/git/refs/heads/master/contrib/completion/git-prompt.sh; \
    mv git-prompt.sh /root/.git-prompt.sh; \
    echo '. ~/.git-prompt.sh' >> /root/.bashrc; \
    echo 'PROMPT_COMMAND='"'"'PS1_CMD1=$(__git_ps1 " [%s]")'"'"'; PS1='"'"'\[\e[38;5;196;2m\]\H\[\e[0m\] \[\e[38;5;226m\]\u\[\e[0m\] \[\e[38;5;38;1m\]\w\[\e[0;38;5;198m\]${PS1_CMD1}\[\e[38;5;226m\]:\[\e[0m\]'"'"'' >> /root/.bashrc; \
    . /root/.bashrc; \
    fi

COPY . .

CMD ["python", "main.py"]
