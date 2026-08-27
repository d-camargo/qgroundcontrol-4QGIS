QGIS_PLUGIN_DIR ?= $(HOME)/.local/share/QGIS/QGIS3/profiles/default/python/plugins
PLUGIN_NAME = qgc4qgis
TARGET_DIR = $(QGIS_PLUGIN_DIR)/$(PLUGIN_NAME)
SRC_DIR = $(CURDIR)/$(PLUGIN_NAME)

.PHONY: all install uninstall test

all: install

install:
	mkdir -p $(QGIS_PLUGIN_DIR)
	rm -rf $(TARGET_DIR)
	ln -s $(SRC_DIR) $(TARGET_DIR)

uninstall:
	rm -rf $(TARGET_DIR)

test:
	python3 -m compileall $(PLUGIN_NAME)
	pytest || [ $$? -eq 5 ]
