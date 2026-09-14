"""Pytest setup and fixtures for qgc4qgis plugin tests."""

import gc
import os
import sys

import pytest

# Ensure headless Qt environment
os.environ["QT_QPA_PLATFORM"] = "offscreen"

# Ensure QGIS plugins path is in sys.path for processing module
QGIS_PLUGIN_PATHS = ["/usr/share/qgis/python", "/usr/share/qgis/python/plugins"]
for path in QGIS_PLUGIN_PATHS:
    if os.path.exists(path) and path not in sys.path:
        sys.path.insert(0, path)

# Ensure repository root directory is in sys.path
PLUGIN_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PLUGIN_DIR not in sys.path:
    sys.path.insert(0, PLUGIN_DIR)


@pytest.fixture(autouse=True)
def _collect_widget_cycles():
    """Coleta ciclos de referência (dock widgets órfãos) ENTRE testes.

    ``QgcPlanningDockWidget`` sem parent fica preso num ciclo PyQt (sinal do
    filho → bound method → dock) e só morre no GC. Se um dock zumbi sobrevive
    até um ``removeAllMapLayers()`` de teste posterior, o slot
    ``layerChanged`` roda sobre camada já deletada, a RuntimeError escapa por
    um slot disparado de dentro do C++ e o PyQt5/Qt6 aborta o processo
    (``qFatal``) ANTES de o pytest reportar. Coletar o GC num ponto quiescente
    (fim de cada teste) destrói os docks deterministicamente e elimina a
    janela de crash — medido no container qgis3 3.44/Qt5 em 2026-09-14.
    """
    yield
    gc.collect()


@pytest.fixture(scope="session", autouse=True)
def qgis_app():
    """Initialize QgsApplication in headless mode for test suite execution.

    ``qgis.testing.start_app`` (mesmo utilitário do smoke do gate) registra o
    ``exitQgis`` via ``atexit``: chamá-lo aqui na finalização da fixture aborta
    (Qt6) ou segfaulta (Qt5) ANTES de o pytest imprimir o resumo da suíte.
    """
    from qgis.testing import start_app

    app = start_app()
    yield app
