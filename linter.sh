#!/bin/bash
xrun() {
    echo "********************** $*"
    vpy3 $*
}

xrun bandit --recursive --skip B101 .  # B101 is assert statements
xrun black --check . || true
xrun codespell --quiet-level=2 --skip=./examples/* # --ignore-words-list="" --skip=""
xrun flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
xrun isort --check-only --profile black --skip examples . || true
xrun mypy --ignore-missing-imports --exclude=examples/* . || true
#xrun pytest || true
#xrun pytest --doctest-modules || true
#xrun safety check
