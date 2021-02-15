.DEFAULT_GOAL := all
isort = isort arkbreeder
black = black arkbreeder
autoflake = autoflake -ir --remove-all-unused-imports --ignore-init-module-imports --remove-unused-variables arkbreeder
mypy = mypy arkbreeder

.PHONY: install
install:
	pip install -e .

.PHONY: format
format:
	$(autoflake)
	$(isort)
	$(black)
	$(mypy)

.PHONY: lint
lint:
	$(isort) --check-only
	$(black) --check

.PHONY: mypy
mypy:
	mypy arkbreeder

.PHONY: test
test:
	pytest -v --cov=arkbreeder/
