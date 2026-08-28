"""End-to-end headless processing tests for ExportDjiAlgorithm via processing.run."""

import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

import processing
import pytest
from processing.core.Processing import Processing
from qgis.core import (
    QgsApplication,
    QgsFeature,
    QgsGeometry,
    QgsPointXY,
    QgsVectorLayer,
)

from qgc4qgis.core.wpml import KML_NS, WPML_NS
from qgc4qgis.processing.provider import Qgc4QgisProvider


@pytest.fixture(scope="module", autouse=True)
def setup_processing(qgis_app):
    """Initialize QGIS Processing framework and register Qgc4QgisProvider for test module."""
    Processing.initialize()
    registry = QgsApplication.processingRegistry()
    provider = Qgc4QgisProvider()
    registry.addProvider(provider)
    yield provider
    registry.removeProvider(provider)


def create_sample_polygon_layer() -> QgsVectorLayer:
    """Create an in-memory WGS84 polygon layer (~111m x 111m square near lat=0, lon=0)."""
    layer = QgsVectorLayer("Polygon?crs=EPSG:4326", "poly_input", "memory")
    pr = layer.dataProvider()
    poly_pts = [
        QgsPointXY(0.0, 0.0),
        QgsPointXY(0.001, 0.0),
        QgsPointXY(0.001, 0.001),
        QgsPointXY(0.0, 0.001),
    ]
    feat = QgsFeature()
    feat.setGeometry(QgsGeometry.fromPolygonXY([poly_pts]))
    pr.addFeatures([feat])
    layer.updateExtents()
    return layer


def test_export_dji_processing_run_end_to_end(tmp_path):
    """Verify end-to-end execution of DJI export algorithm using processing.run.

    Tests memory layer input -> processing.run -> KMZ output on disk -> ZIP contents
    and XML structure/namespaces verification.
    """
    input_layer = create_sample_polygon_layer()
    output_kmz = str(tmp_path / "dji_mission_end_to_end.kmz")

    params = {
        "INPUT": input_layer,
        "CAMERA": 0,
        "ALTITUDE": 100.0,
        "GSD": 0.0,
        "OVERLAP_SIDE": 70.0,
        "OVERLAP_FRONTAL": 70.0,
        "ANGLE": 0.0,
        "TURNAROUND": 0.0,
        "ENTRY_LOCATION": 0,
        "REFLY": False,
        "TRIGGER_MODE": 0,
        "SPEED": 5.0,
        "GIMBAL_PITCH": -90.0,
        "WAYPOINT_WAIT": 0.0,
        "FINISH_ACTION": 0,
        "RC_LOST_ACTION": 0,
        "TRANSITIONAL_SPEED": 5.0,
        "ZIP_LAYOUT": 0,  # wpmz/ subfolder
        "OUTPUT": output_kmz,
    }

    result = processing.run("qgc4qgis:exportar_dji_kmz", params)
    assert "OUTPUT" in result
    assert result["OUTPUT"] == output_kmz

    kmz_path = Path(output_kmz)
    assert kmz_path.exists()
    assert kmz_path.stat().st_size > 0

    # Open ZIP and verify expected internal structure
    with zipfile.ZipFile(kmz_path, "r") as zf:
        namelist = zf.namelist()
        assert "wpmz/template.kml" in namelist
        assert "wpmz/waylines.wpml" in namelist

        template_bytes = zf.read("wpmz/template.kml")
        waylines_bytes = zf.read("wpmz/waylines.wpml")

    # Validate template.kml XML
    template_root = ET.fromstring(template_bytes)
    assert template_root.tag == f"{{{KML_NS}}}kml"
    template_doc = template_root.find(f"{{{KML_NS}}}Document")
    assert template_doc is not None
    assert template_doc.find(f"{{{WPML_NS}}}author") is not None
    assert template_doc.find(f"{{{WPML_NS}}}missionConfig") is not None

    # Validate waylines.wpml XML
    waylines_root = ET.fromstring(waylines_bytes)
    assert waylines_root.tag == f"{{{KML_NS}}}kml"
    waylines_doc = waylines_root.find(f"{{{KML_NS}}}Document")
    assert waylines_doc is not None

    folder = waylines_doc.find(f"{{{KML_NS}}}Folder")
    assert folder is not None
    assert folder.find(f"{{{WPML_NS}}}templateId") is not None
    assert folder.find(f"{{{WPML_NS}}}executeHeightMode") is not None

    placemarks = folder.findall(f"{{{KML_NS}}}Placemark")
    assert len(placemarks) > 0

    # Verify waypoint placemarks
    for pm in placemarks:
        idx_elem = pm.find(f"{{{WPML_NS}}}index")
        assert idx_elem is not None
        coords_elem = pm.find(f"{{{KML_NS}}}Point/{f'{{{KML_NS}}}coordinates'}")
        assert coords_elem is not None
        height_elem = pm.find(f"{{{WPML_NS}}}executeHeight")
        assert height_elem is not None
        assert float(height_elem.text) == 100.0


def test_export_dji_processing_run_root_zip_layout(tmp_path):
    """Verify DJI export processing.run with root ZIP layout option."""
    input_layer = create_sample_polygon_layer()
    output_kmz = str(tmp_path / "dji_mission_root_layout.kmz")

    params = {
        "INPUT": input_layer,
        "CAMERA": 0,
        "ALTITUDE": 80.0,
        "GSD": 0.0,
        "OVERLAP_SIDE": 75.0,
        "OVERLAP_FRONTAL": 75.0,
        "ANGLE": 45.0,
        "TURNAROUND": 5.0,
        "ENTRY_LOCATION": 1,
        "REFLY": False,
        "TRIGGER_MODE": 0,
        "SPEED": 6.0,
        "GIMBAL_PITCH": -90.0,
        "WAYPOINT_WAIT": 0.0,
        "FINISH_ACTION": 0,
        "RC_LOST_ACTION": 0,
        "TRANSITIONAL_SPEED": 5.0,
        "ZIP_LAYOUT": 1,  # Root layout
        "OUTPUT": output_kmz,
    }

    result = processing.run("qgc4qgis:exportar_dji_kmz", params)
    assert result["OUTPUT"] == output_kmz

    kmz_path = Path(output_kmz)
    assert kmz_path.exists()
    assert kmz_path.stat().st_size > 0

    with zipfile.ZipFile(kmz_path, "r") as zf:
        namelist = zf.namelist()
        assert "template.kml" in namelist
        assert "waylines.wpml" in namelist
        assert "wpmz/template.kml" not in namelist

        template_bytes = zf.read("template.kml")
        waylines_bytes = zf.read("waylines.wpml")

    t_root = ET.fromstring(template_bytes)
    w_root = ET.fromstring(waylines_bytes)
    assert t_root.tag == f"{{{KML_NS}}}kml"
    assert w_root.tag == f"{{{KML_NS}}}kml"


def test_export_dji_processing_run_custom_options(tmp_path):
    """Verify DJI export processing.run with custom options (refly, finish action, waypoint wait)."""
    input_layer = create_sample_polygon_layer()
    output_kmz = str(tmp_path / "dji_mission_custom_options.kmz")

    params = {
        "INPUT": input_layer,
        "CAMERA": 0,
        "ALTITUDE": 120.0,
        "GSD": 0.0,
        "OVERLAP_SIDE": 70.0,
        "OVERLAP_FRONTAL": 70.0,
        "ANGLE": 0.0,
        "TURNAROUND": 10.0,
        "ENTRY_LOCATION": 0,
        "REFLY": True,
        "TRIGGER_MODE": 1,  # POR_TEMPO
        "SPEED": 7.0,
        "GIMBAL_PITCH": -45.0,
        "WAYPOINT_WAIT": 3.0,
        "FINISH_ACTION": 1,  # noAction
        "RC_LOST_ACTION": 1,  # landing
        "TRANSITIONAL_SPEED": 8.0,
        "ZIP_LAYOUT": 0,
        "OUTPUT": output_kmz,
    }

    result = processing.run("qgc4qgis:exportar_dji_kmz", params)
    assert result["OUTPUT"] == output_kmz

    kmz_path = Path(output_kmz)
    assert kmz_path.exists()

    with zipfile.ZipFile(kmz_path, "r") as zf:
        template_bytes = zf.read("wpmz/template.kml")
        waylines_bytes = zf.read("wpmz/waylines.wpml")

    t_root = ET.fromstring(template_bytes)
    mc = t_root.find(f"{{{KML_NS}}}Document/{f'{{{WPML_NS}}}missionConfig'}")
    assert mc is not None
    assert mc.find(f"{{{WPML_NS}}}finishAction").text == "noAction"
    assert mc.find(f"{{{WPML_NS}}}executeRCLostAction").text == "landing"
    assert mc.find(f"{{{WPML_NS}}}globalTransitionalSpeed").text == "8.0"

    w_root = ET.fromstring(waylines_bytes)
    folder = w_root.find(f"{{{KML_NS}}}Document/{f'{{{KML_NS}}}Folder'}")
    assert folder is not None
    placemarks = folder.findall(f"{{{KML_NS}}}Placemark")
    assert len(placemarks) > 0
