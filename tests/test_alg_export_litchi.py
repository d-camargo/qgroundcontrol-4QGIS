"""End-to-end headless processing tests for ExportLitchiAlgorithm via processing.run."""

import csv
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


def test_export_litchi_processing_run_end_to_end(tmp_path):
    """Verify end-to-end execution of Litchi export algorithm using processing.run.

    Tests memory layer input -> processing.run -> CSV file read back -> row count and
    coordinate containment verification within the polygon.
    """
    input_layer = create_sample_polygon_layer()
    output_csv = str(tmp_path / "litchi_mission_end_to_end.csv")

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
        "OUTPUT": output_csv,
    }

    result = processing.run("qgc4qgis:exportar_litchi_csv", params)
    assert "OUTPUT" in result
    assert result["OUTPUT"] == output_csv

    csv_path = Path(output_csv)
    assert csv_path.exists()
    assert csv_path.stat().st_size > 0

    # Read back the CSV file and check headers, row count, and coordinates
    with open(output_csv, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        rows = list(reader)

    # Check headers
    expected_headers = [
        "latitude",
        "longitude",
        "altitude(m)",
        "heading(deg)",
        "curvesize(m)",
        "rotationdir",
        "gimbalmode",
        "gimbalpitchangle",
        "altitudemode",
        "speed(m/s)",
        "poi_latitude",
        "poi_longitude",
        "poi_altitude(m)",
        "poi_altitudemode",
        "photo_timeinterval",
        "photo_distinterval",
    ]
    for h in expected_headers:
        assert h in headers

    # Row count verification
    assert len(rows) > 0

    # Polygon geometry for containment checks
    input_feat = next(input_layer.getFeatures())
    poly_geom = input_feat.geometry()
    # Add small buffer tolerance (~1m in degrees, 1e-5) for boundary floating point precision
    buffered_poly = poly_geom.buffer(1e-5, 8)

    # Check waypoint coordinates inside polygon
    for row in rows:
        lat = float(row["latitude"])
        lon = float(row["longitude"])
        alt = float(row["altitude(m)"])

        assert alt == 100.0
        pt = QgsPointXY(lon, lat)
        assert buffered_poly.contains(QgsGeometry.fromPointXY(pt)), (
            f"Waypoint coordinate ({lat}, {lon}) is outside the polygon envelope"
        )


def test_export_litchi_processing_run_options(tmp_path):
    """Verify Litchi export processing.run with refly, waypoint wait, and turnaround."""
    input_layer = create_sample_polygon_layer()
    output_csv = str(tmp_path / "litchi_mission_options.csv")

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
        "TRIGGER_MODE": 0,
        "SPEED": 6.0,
        "GIMBAL_PITCH": -90.0,
        "WAYPOINT_WAIT": 2.5,
        "OUTPUT": output_csv,
    }

    result = processing.run("qgc4qgis:exportar_litchi_csv", params)
    assert result["OUTPUT"] == output_csv

    with open(output_csv, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) > 0
    first_row = rows[0]
    assert float(first_row["altitude(m)"]) == 120.0
    assert float(first_row["speed(m/s)"]) == 6.0
    assert first_row["actiontype1"] == "0"
    assert float(first_row["actionparam1"]) == 2500.0
