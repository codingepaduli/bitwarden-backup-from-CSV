#!/bin/bash

# PYTHONDONTWRITEBYTECODE=1 -> don't create the folder __pycache__ running python3
# pyyaml --no-cache-dir -> don't create the folder __pycache__ running pip3
# mypy --cache-dir=/dev/null -> don't create the folder __mypy_cache__ running mypy

# BUG: bash pipe '|' and bash evaluation '$()' don't work with docker when 
# execute 'docker run -it'. Fix the bug using 'docker run -i'
# echo piped content | docker run -i  ubuntu:16.04 cat - # works
# echo piped content | docker run -it ubuntu:16.04 cat - # error: unable to setup input stream

FOLDER_TO_CHECK="$HOME/Sviluppo/SVN/javing/appunti/backups/bitwarden_backup_from_csv_file"

CSV_FILE="bitwarden_export_20221229120953.csv"

echo "making CSV printable: "

docker run -it --rm --name makePintableListFromCSV -v "$PWD":/usr/src/myapp -v "$FOLDER_TO_CHECK":"$FOLDER_TO_CHECK" -e PYTHONDONTWRITEBYTECODE=1 -w /usr/src/myapp python:3.10-slim /bin/bash -c "pip3.10 install --no-cache-dir pyyaml && python /usr/src/myapp/makePintableListFromCSV.py --input-file $FOLDER_TO_CHECK/$CSV_FILE"
