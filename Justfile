format:
    uv run ruff format .

lint:
    uv run ruff check .

test:
    uv run pytest

check:
    uv run ruff check .
    uv run ruff format --check .
    uv run pytest

run:
    uv run frameshift --help

scan media_path:
    uv run frameshift scan "{{media_path}}"

fix:
    uv run ruff check --fix .
    uv run ruff format .

library:
    uv run frameshift library