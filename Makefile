FILES := $(shell find . -maxdepth 1 -name '*.py')
MYPY := uvx mypy
RUFF := uvx ruff
EC := uvx --from editorconfig-checker ec
PYTHON3 := uv run python3

.PHONY: check check! test


check:
	$(EC)
	$(MYPY) $(FILES)
	$(RUFF) check $(FILES)

check!:
	$(RUFF) check $(FILES) --unsafe-fixes --fix

test:
	$(PYTHON3) -m unittest discover
