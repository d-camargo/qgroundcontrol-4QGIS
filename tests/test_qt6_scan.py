"""Guarda de regressão Qt6 / QGIS 4.x (passo 129, decisão D71).

Varre estaticamente todos os arquivos .py de `qgc4qgis/` em busca de sintaxes
legadas do Qt5 / PyQt5 / QGIS 3.x que causam incompatibilidades no Qt6 / QGIS 4.x.

Semântica de isenção por linha / bloco:
- Linhas de comentário puras (iniciando com `#`) são ignoradas.
- Linhas que contêm `# qt6-compat:` (com justificativa), `# Qt5` ou `# PyQt5` são
  isentas.
- Linhas inseridas em handlers `except AttributeError:` (blocos de fallback Qt5
  para quando os atributos do Qt6 não existem no módulo) são isentas.
"""

import ast
import re
from pathlib import Path

# Membros Qt não qualificados: Qt.<Membro> fora da forma qualificada Qt.<Enum>.<Membro>
_QT_MEMBER_RE = re.compile(r"\bQt\.[A-Za-z0-9_]+(?:\.[A-Za-z0-9_]+)?\b")

# Padrões legados do Qt5/QGIS 3.x com respectivas sugestões de correção
_LEGACY_PATTERNS = [
    (
        re.compile(r"\b(?:from|import)\s+PyQt[456]\b"),
        "qgis.PyQt (wrapper independente de versão)",
    ),
    (
        re.compile(r"\bQVariant\.(?:String|Int|Double|Bool|Map|List|UserType)\b"),
        "QMetaType.Type.<Tipo> (QVariant.Type não existe no PyQt6)",
    ),
    (
        re.compile(r"\bQgis\.(?:Critical|Info|Warning|Success)\b"),
        "Qgis.MessageLevel.<Level>",
    ),
    (
        re.compile(r"\bQgsTask\.CanCancel\b"),
        "QgsTask.Flag.CanCancel",
    ),
    (
        re.compile(r"\bQMessageBox\.(?:Yes|No|Ok|Cancel|Save|Close)\b"),
        "QMessageBox.StandardButton.<Button>",
    ),
    (
        re.compile(r"\bQPainter\.Antialiasing\b"),
        "QPainter.RenderHint.Antialiasing",
    ),
    (
        re.compile(r"\bQImage\.Format_\w*"),
        "QImage.Format.Format_<...>",
    ),
    (
        re.compile(r"\bQFrame\.(?:StyledPanel|Raised|NoFrame|Box|Panel|Plain)\b"),
        "QFrame.Shape / QFrame.Shadow",
    ),
    (
        re.compile(r"\bQNetworkReply\.(?!NetworkError\b)[A-Z]\w*Error\b"),
        "QNetworkReply.NetworkError.<...>",
    ),
    (
        re.compile(r"\bQgsVectorLayerDirector\.(?!Direction\b)Direction\w+\b"),
        "QgsVectorLayerDirector.Direction.<...>",
    ),
    (
        re.compile(r"\.exec_\("),
        ".exec() (PyQt6 removeu o alias exec_)",
    ),
]

_EXEMPT_RE = re.compile(r"#\s*(?:qt6-compat|Qt5|PyQt5)", re.IGNORECASE)


def _is_exempt(line: str) -> bool:
    """Verifica se a linha é isenta por comentário de cabeçalho ou tag pragma."""
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return True
    if _EXEMPT_RE.search(line):
        return True
    return False


def _scan_lines(lines: list[str]) -> list[tuple[int, str, str]]:
    """Varre as linhas fornecidas e devolve uma lista de (lineno, trecho, sugestao)."""
    violations: list[tuple[int, str, str]] = []

    # Identifica linhas que pertencem a blocos except AttributeError: (fallback Qt5)
    except_attribute_error_lines: set[int] = set()
    try:
        content = "".join(lines) if lines and lines[0].endswith("\n") else "\n".join(lines)
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler):
                if isinstance(node.type, ast.Name) and node.type.id == "AttributeError":
                    for child in ast.walk(node):
                        if hasattr(child, "lineno"):
                            except_attribute_error_lines.add(child.lineno)
    except Exception:
        pass

    for lineno, line in enumerate(lines, start=1):
        if _is_exempt(line) or lineno in except_attribute_error_lines:
            continue

        # 1. Verifica uso de Qt.<Membro> desescopado (ex: Qt.RightDockWidgetArea)
        for match in _QT_MEMBER_RE.finditer(line):
            text = match.group(0)
            if text.count(".") < 2:
                parts = text.split(".", 1)
                member = parts[1]
                if member not in (
                    "DockWidgetArea",
                    "AlignmentFlag",
                    "WindowType",
                    "Orientation",
                    "ItemFlag",
                    "CheckState",
                ):
                    violations.append((lineno, text, f"Qt.<Enum>.{member}"))

        # 2. Verifica padrões legados conhecidos
        for pattern, fix in _LEGACY_PATTERNS:
            for match in pattern.finditer(line):
                violations.append((lineno, match.group(0), fix))

    return violations


def _scan_file(path: Path) -> list[tuple[int, str, str]]:
    """Lê o arquivo e retorna as violações encontradas."""
    code = path.read_text(encoding="utf-8")
    return _scan_lines(code.splitlines(keepends=True))


def test_scan_qt6_compat():
    """Varre qgc4qgis/**/*.py para garantir compatibilidade com Qt6 / QGIS 4.x."""
    pacote = Path(__file__).resolve().parent.parent / "qgc4qgis"
    problemas: list[str] = []

    for py_path in sorted(pacote.rglob("*.py")):
        if "__pycache__" in py_path.parts:
            continue
        rel_path = py_path.relative_to(pacote.parent)
        for lineno, achado, fix in _scan_file(py_path):
            problemas.append(
                f"{rel_path}:{lineno}: '{achado}' não é a forma qualificada do Qt6 (use {fix})"
            )

    assert not problemas, "Encontradas incompatibilidades Qt6/QGIS 4.x em qgc4qgis:\n" + "\n".join(
        problemas
    )


def test_semantica_do_scanner_qt6():
    """Valida a semântica do scanner com casos positivos, negativos e isenções."""
    # Código Qt6 válido passa sem violações
    codigo_valido = [
        "from qgis.PyQt.QtCore import Qt\n",
        "area = Qt.DockWidgetArea.RightDockWidgetArea\n",
        "level = Qgis.MessageLevel.Warning\n",
        "dialog.exec()\n",
    ]
    assert _scan_lines(codigo_valido) == []

    # Import direto de PyQt5 acusa
    assert _scan_lines(["from PyQt5 import QtCore\n"]) == [
        (1, "from PyQt5", "qgis.PyQt (wrapper independente de versão)")
    ]

    # Exec legado (.exec_()) acusa
    assert _scan_lines(["dlg.exec_()\n"]) == [
        (1, ".exec_(", ".exec() (PyQt6 removeu o alias exec_)")
    ]

    # Qgis.Warning desescopado acusa
    assert _scan_lines(["lvl = Qgis.Warning\n"]) == [
        (1, "Qgis.Warning", "Qgis.MessageLevel.<Level>")
    ]

    # Linha com comentário de isenção Qt5 ou qt6-compat passa
    assert _scan_lines(["area = Qt.RightDockWidgetArea  # Qt5 (PyQt5)\n"]) == []
    assert _scan_lines(["lvl = Qgis.Warning  # qt6-compat: fallback QGIS<3.24\n"]) == []

    # Linhas dentro de except AttributeError: passam por serem fallback
    codigo_fallback = [
        "try:\n",
        "    _WARNING = Qgis.MessageLevel.Warning\n",
        "except AttributeError:\n",
        "    _WARNING = Qgis.Warning\n",
    ]
    assert _scan_lines(codigo_fallback) == []

    # Linhas de comentários puros são ignoradas
    assert _scan_lines(["# Qgis.Warning é usado em QGIS antigo\n"]) == []
