.PHONY: run install install-uv install-pip clean check-uv setup check-deps find-python

# Find Python 3.10+
find-python:
	@for version in 12 11 10; do \
		if command -v python3.$$version > /dev/null 2>&1; then \
			PYTHON_VERSION=$$(python3.$$version --version 2>&1 | awk '{print $$2}'); \
			MAJOR=$$(echo $$PYTHON_VERSION | cut -d. -f1); \
			MINOR=$$(echo $$PYTHON_VERSION | cut -d. -f2); \
			if [ "$$MAJOR" -eq 3 ] && [ "$$MINOR" -ge 10 ]; then \
				echo "python3.$$version"; \
				exit 0; \
			fi; \
		fi; \
	done; \
	if command -v python3 > /dev/null 2>&1; then \
		PYTHON_VERSION=$$(python3 --version 2>&1 | awk '{print $$2}'); \
		MAJOR=$$(echo $$PYTHON_VERSION | cut -d. -f1); \
		MINOR=$$(echo $$PYTHON_VERSION | cut -d. -f2); \
		if [ "$$MAJOR" -eq 3 ] && [ "$$MINOR" -ge 10 ]; then \
			echo "python3"; \
			exit 0; \
		fi; \
	fi; \
	echo "python3"

# Check if dependencies are installed
check-deps:
	@PYTHON_CMD=$$($(MAKE) -s find-python); \
	$$PYTHON_CMD -c "import PySide6" 2>/dev/null || (echo "Dependencies not installed. Running setup..." && $(MAKE) setup)

# Auto-setup dependencies (system + Python)
setup:
	@chmod +x setup.sh
	@./setup.sh

# Check if uv is available, fallback to python -m pip
check-uv:
	@which uv > /dev/null 2>&1 || (echo "Warning: uv not found. Install with: curl -LsSf https://astral.sh/uv/install.sh | sh" && exit 1)

# Run with auto-setup
run: check-deps
	@PYTHON_CMD=$$($(MAKE) -s find-python); \
	if command -v uv > /dev/null 2>&1; then \
		if [ ! -d ".venv" ]; then \
			echo "Creating virtual environment with uv..."; \
			uv venv; \
		fi; \
		uv run $$PYTHON_CMD -m pide; \
	else \
		$$PYTHON_CMD -m pide; \
	fi

install-uv: check-uv
	uv pip install -r requirements.txt

install-pip:
	pip3 install --user -r requirements.txt || pip install --user -r requirements.txt

install: setup

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true