"""Tests for qgc4qgis plugin initialization and metadata verification."""

import configparser
from pathlib import Path

import qgc4qgis


def test_import_qgc4qgis():
    """Verify qgc4qgis package can be imported without QGIS running."""
    assert qgc4qgis is not None


def test_plugin_metadata_file():
    """Verify metadata.txt exists, is valid INI, and contains required metadata fields."""
    plugin_dir = Path(qgc4qgis.__file__).parent
    metadata_path = plugin_dir / "metadata.txt"

    assert metadata_path.exists(), f"metadata.txt not found at {metadata_path}"

    config = configparser.ConfigParser()
    config.optionxform = str  # Preserve option case
    config.read(metadata_path, encoding="utf-8")

    assert "general" in config
    general = config["general"]

    required_keys = [
        "name",
        "qgisMinimumVersion",
        "description",
        "about",
        "version",
        "author",
        "repository",
        "hasProcessingProvider",
    ]

    for key in required_keys:
        assert key in general, f"Missing required metadata key: {key}"

    assert general["name"] == "QGC4QGIS"
    assert general["version"] == "0.1.0"
    assert general["qgisMinimumVersion"] == "3.34"
    assert general["hasProcessingProvider"] == "yes"
