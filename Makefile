FILES := $(shell find . -maxdepth 1 -name '*.py')
PYRIGHT := uvx basedpyright
RUFF := uvx ruff
EC := uvx --from editorconfig-checker ec
PYTHON3 := uv run python3


.PHONY: check fix test prepare format

prepare:
	uv sync --all-extras

check:
	$(EC)
	$(PYRIGHT) $(FILES)
	$(RUFF) check $(FILES)

fix:
	$(RUFF) check $(FILES) --unsafe-fixes --fix

test:
	$(PYTHON3) -m unittest discover

format:
	$(RUFF) format $(FILES)
