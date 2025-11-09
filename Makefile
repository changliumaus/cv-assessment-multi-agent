.PHONY: install install-dev test lint format clean run-example help

help:
	@echo "CV Assessment Agent - Development Commands"
	@echo ""
	@echo "Available commands:"
	@echo "  make install       - Install package"
	@echo "  make install-dev   - Install with development dependencies"
	@echo "  make test          - Run tests"
	@echo "  make test-cov      - Run tests with coverage"
	@echo "  make lint          - Run linters (ruff, mypy)"
	@echo "  make format        - Format code (black, ruff)"
	@echo "  make run-example   - Run example assessment"
	@echo "  make clean         - Clean build artifacts"
	@echo ""

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"
	pre-commit install

test:
	pytest

test-cov:
	pytest --cov=src/cv_assessment --cov-report=html --cov-report=term-missing

lint:
	ruff check src/ tests/
	mypy src/

format:
	black src/ tests/ examples/
	ruff check src/ tests/ examples/ --fix

run-example:
	python examples/run_example.py

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
