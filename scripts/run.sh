#!/usr/bin/env bash

set -e

if [[ ! -d dev_env ]]; then
	python3 -m venv dev_env
	source dev_env/bin/activate
	pip3 install pyyaml
	pip3 install click
	pip3 install yamlcore
fi

source dev_env/bin/activate
python3 scripts/run.py
