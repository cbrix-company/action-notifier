# Container image that runs your code
FROM python:3.8-alpine3.13

RUN pip install -r requirements.txt --no-cache-dir

# Copies your code file from your action repository to the filesystem path `/` of the container
COPY entrypoint.sh /entrypoint.sh
COPY main.py .
COPY requirements.txt .

# Code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["/entrypoint.sh"]
