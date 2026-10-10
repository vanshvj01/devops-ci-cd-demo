# Base image is a build argument: python:3.12-slim by default.
# The lab machine has no Docker Hub access, so Jenkins passes a locally imported Ubuntu 24.04 image that already contains Python 3.12.
ARG BASE_IMAGE=python:3.12-slim
FROM ${BASE_IMAGE}
WORKDIR /app
COPY app.py .
EXPOSE 8000
CMD ["python3", "app.py", "serve"]
