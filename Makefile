FILES := $(shell find . -maxdepth 1 -name '*.py')
MYPY := uvx mypy
RUFF := uvx ruff
EC := uvx --from editorconfig-checker ec
.PHONY: check check!


check:
	$(EC)
	$(MYPY) $(FILES)
	$(RUFF) check $(FILES)

check!:
	$(RUFF) check $(FILES) --unsafe-fixes --fix
