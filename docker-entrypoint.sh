#!/bin/bash
set -e

pip install --editable /usr/src/cc/
pip install --editable /usr/src/keras-ocr/

exec "$@"
