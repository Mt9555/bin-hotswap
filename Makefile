PYTHON = python
VENV_DIR = bin_hotswap_env
PACKAGE_NAME = binary_relauncher

# Create VE
venv:
	$(PYTHON) -m venv $(VENV_DIR)

# Activate VE
activate:
ifeq ($(OS),Windows_NT)
	.\$(VENV_DIR)\Scripts\activate.bat
else
	source $(VENV_DIR)/bin/activate
endif

install:
	$(PYTHON) -m pip install -r requirements.txt

run:
	$(PYTHON) -m $(PACKAGE_NAME)

# Clean up generated files
clean:
	rm -rf $(VENV_DIR)

.PHONY: venv activate install run clean
