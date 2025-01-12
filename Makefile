VENV := $(PWD)/.venv

export PATH := $(VENV)/bin:$(PATH)

ifeq ($(filter undefine,$(value .FEATURES)),)
SHELL = env PATH="$(PATH)" /bin/bash
endif

.PHONY: .venv
.venv:
	python3 -m venv $(VENV)
	pip install --upgrade pip

install: .venv
	pip install -r requirements.txt

lint:
	ruff check
	ruff format --check

format:
	ruff check --select I --fix
	ruff format

clean:
	rm -rf .ruff_cache
	find . -name __pycache__ | xargs rm -rf
