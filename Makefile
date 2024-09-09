FILES := $(shell find . -maxdepth 1 -name '*.py')
MYPY := uvx mypy
RUFF := uvx ruff
.PHONY: check check!


check:
	$(MYPY) $(FILES)
	$(RUFF) check $(FILES)

check!:
	$(RUFF) check $(FILES) --unsafe-fixes --fix
