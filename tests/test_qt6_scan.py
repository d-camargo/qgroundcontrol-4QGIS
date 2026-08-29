"""Guarda de regressão Qt6 / QGIS 4.x (passo 129, decisão D71).

Réplica local do scanner de compatibilidade Qt6 do plugins.qgis.org, restrita
às 7 famílias de enum não-escopado reportadas na 0.7.0 (106 achados): no
PyQt6/Qt6 todo enum vive no escopo da sua enum-class —
``Qt.RightDockWidgetArea`` vira ``Qt.DockWidgetArea.RightDockWidgetArea``.

Varre estaticamente os ``.py`` de ``qgc4qgis/`` (o que entra no ZIP do plugin;
``tests/`` não é escaneado). As formas escopadas não casam porque após o ponto
vem o nome da enum-class. Sem isenções por comentário ou bloco ``except``: a
linha do fallback é exatamente a que o checker oficial acusa — foi assim que a
0.7.0 foi reprovada.

``QVariant.Type.*`` (que o checker aceita, mas o PyQt6 não expõe em runtime)
não é deny-list aqui: vive apenas no branch Qt5 das constantes ``FIELD_*`` dos
algoritmos, e o que guarda o runtime Qt6 é a suíte rodando no container qgis4.
"""

import re
from pathlib import Path

_DENY = [
    (
        re.compile(r"\bQgsProcessingParameterNumber\.(?:Double|Integer)\b"),
        "QgsProcessingParameterNumber.Type.<N>",
    ),
    (
        re.compile(r"\bQVariant\.(?:Double|Int|String|Bool|Map|List|UserType)\b"),
        "forma escopada (Qt5: QVariant.Type.<T>; Qt6: QMetaType.Type.<T>)",
    ),
    (
        re.compile(r"\bQgsProcessing\.TypeVector(?:Polygon|Line|Point)\b"),
        "QgsProcessing.SourceType.<Tipo>",
    ),
    (
        re.compile(r"\bQgsMapLayerProxyModel\.(?:PolygonLayer|RasterLayer)\b"),
        "QgsMapLayerProxyModel.Filter.<F>",
    ),
    (
        re.compile(r"\bQgsFeatureSink\.FastInsert\b"),
        "QgsFeatureSink.Flag.FastInsert",
    ),
    (
        re.compile(r"\bQgsBlockingNetworkRequest\.NoError\b"),
        "QgsBlockingNetworkRequest.ErrorCode.NoError",
    ),
    (
        re.compile(r"\bQt\.RightDockWidgetArea\b"),
        "Qt.DockWidgetArea.RightDockWidgetArea",
    ),
    (
        re.compile(r"\bQgis\.(?:Warning|Critical|Info|Success)\b"),
        "Qgis.MessageLevel.<Level>",
    ),
    (
        re.compile(r"\bQFrame\.NoFrame\b"),
        "QFrame.Shape.NoFrame",
    ),
]


def _scan_lines(linhas: list[str]) -> list[tuple[int, str, str]]:
    """Varra as linhas e devolva (lineno, achado, forma correta) de cada negado."""
    achados: list[tuple[int, str, str]] = []
    for lineno, linha in enumerate(linhas, start=1):
        for padrao, forma in _DENY:
            for m in padrao.finditer(linha):
                achados.append((lineno, m.group(0), forma))
    return achados


def test_scan_qt6_compat():
    """qgc4qgis/ não pode conter nenhuma das 7 famílias não-escopadas."""
    pacote = Path(__file__).resolve().parent.parent / "qgc4qgis"
    problemas: list[str] = []

    for py in sorted(pacote.rglob("*.py")):
        if "__pycache__" in py.parts:
            continue
        rel = py.relative_to(pacote.parent)
        for lineno, achado, forma in _scan_lines(py.read_text(encoding="utf-8").splitlines()):
            problemas.append(f"{rel}:{lineno}: '{achado}' não-escopado (use {forma})")

    assert not problemas, "Enums Qt5 não-escopados em qgc4qgis/:\n" + "\n".join(problemas)


def test_semantica_do_scanner_qt6():
    """Forma escopada passa; forma nua e fallback Qgis.Warning reproduzem."""
    # Formas escopadas (as que o plugin usa) passam.
    assert _scan_lines(
        [
            "from qgis.PyQt.QtCore import QVariant\n",
            "area = Qt.DockWidgetArea.RightDockWidgetArea\n",
            "lvl = Qgis.MessageLevel.Warning\n",
            "frame = QFrame.Shape.NoFrame\n",
            "n = QgsProcessingParameterNumber.Type.Double\n",
            "t = QgsProcessing.SourceType.TypeVectorPolygon\n",
            "sink.addFeature(f, QgsFeatureSink.Flag.FastInsert)\n",
            "    FIELD_INT = QVariant.Type.Int\n",
        ]
    ) == []

    # Forma nua reproduz.
    assert _scan_lines(["x = QVariant.Int\n"]) == [(1, "QVariant.Int", "forma escopada (Qt5: QVariant.Type.<T>; Qt6: QMetaType.Type.<T>)")]
    assert _scan_lines(["n = QgsProcessingParameterNumber.Double()\n"]) == [
        (1, "QgsProcessingParameterNumber.Double", "QgsProcessingParameterNumber.Type.<N>")
    ]
    assert _scan_lines(["t = QgsProcessing.TypeVectorPolygon\n"]) == [
        (1, "QgsProcessing.TypeVectorPolygon", "QgsProcessing.SourceType.<Tipo>")
    ]

    # Fallback Qt5 (try/except AttributeError) também reproduz: a linha do
    # fallback é a que o checker oficial acusa.
    fallback = [
        "try:\n",
        "    _WARNING = Qgis.MessageLevel.Warning\n",
        "except AttributeError:\n",
        "    _WARNING = Qgis.Warning\n",
    ]
    assert _scan_lines(fallback) == [(4, "Qgis.Warning", "Qgis.MessageLevel.<Level>")]
