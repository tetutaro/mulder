.PHONY: clean
clean: clean-python clean-tests clean-system

.PHONY: clean-python
clean-python:
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*.pyd' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -fr {} +
	@uv cache clean

.PHONY: clean-tests
clean-tests:
	@rm -rf .mypy_cache/ .pytest_cache/ .ruff_cache/ htmlcov/ .coverage

.PHONY: clean-system
clean-system:
	@find . -name '*~' -exec rm -f {} +
	@find . -name '.DS_Store' -exec rm -f {} +

.PHONY: update-requirements
update-requirements:
	uv pip compile requirements/requirements-dev.in --universal \
		--output-file requirements/requirements-dev.txt
	uv pip compile requirements/requirements-vim.in --universal \
		--output-file requirements/requirements-vim.txt

.PHONY: setup-environment
setup-environment:
	uv python pin 3.11.10
	uv venv
	. .venv/bin/activate
	uv pip sync \
		requirements/requirements-dev.txt \
		requirements/requirements-vim.txt

.PHONY: sync-environment
sync-environment:
	uv pip sync \
		requirements/requirements-dev.txt \
		requirements/requirements-vim.txt

.PHONY: update-html
update-html:
	pandoc -f markdown -t html --standalone --embed-resources --metadata title="README" -c readme.css README.md > README.html

.PHONY: deliverable
deliverable:
	@git checkout-index -a -f --prefix=deliverable/
	@zip -r deliverable.zip deliverable/
	@rm -rf deliverable

.PHONY: lint
lint:
	@echo "Running mypy"
	uvx mypy mulder/ tests/ --explicit-package-bases
	@echo "Running ruff"
	uvx ruff check mulder/ tests/

.PHONY: format
format:
	@echo "Running black"
	uvx black src/ tests/
	@echo "Running isort"
	uvx isort src/ tests/

.PHONY: check
check:
	@echo "Checking lint & format"
	.venv/bin/python3 -m pytest -v --black --ruff --mypy --isort ./mulder/

.PHONY: tests
tests:
	@echo "Running pytest"
	coverage run -m pytest ./tests/
	coverage html --ignore-errors
	coverage report --ignore-errors
