#!/bin/bash

echo "Syntax checking..."

# PYTHONDONTWRITEBYTECODE=1  -> don't create the folder __pycache__ running python3
# pip install --no-cache-dir -> don't create the folder __pycache__ running pip3
# mypy --cache-dir=/dev/null -> don't create the folder __mypy_cache__ running mypy

docker run -it --rm --name mypy -v "$PWD":/usr/src/myapp -v "$FOLDER_TO_CHECK":"$FOLDER_TO_CHECK" -e PYTHONDONTWRITEBYTECODE=1 -w /usr/src/myapp python:3.10-slim /bin/bash -c 'pip install --no-cache-dir mypy pyyaml types-PyYAML && python -m mypy --cache-dir=/dev/null --warn-unreachable --strict /usr/src/myapp/config.py /usr/src/myapp/makePintableListFromCSV.py'
