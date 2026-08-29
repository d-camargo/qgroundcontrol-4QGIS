"""Réplica local do portão de segurança (passo 117, decisão D61).

Mesma semântica do `_scan_seguranca` do planexec.py — o scanner da família
Bandit que o plugins.qgis.org roda no upload — restrito às duas regras que
atingem o plugin:

- **B110/B112**: ``ExceptHandler`` cujo corpo é um único ``pass``/``continue``
  *e* cujo tipo é ausente ou genérico (``Exception``/``BaseException``).
  Handler tipado com corpo mudo PASSA (``check_typed_exception=False``).
- **B405**: ``import`` cujo nome é ``xml`` ou começa com ``xml.etree``.

Varre apenas os ``.py`` de ``qgc4qgis/`` — o que entra no ZIP do plugin;
``tests/`` não é escaneado pelo portão real e pode importar ``xml.etree``
livremente (é o oráculo do ``test_xmlwrite.py``).
"""

import ast
from pathlib import Path

_MUDOS = (ast.Pass, ast.Continue)
_GENERICAS = ("Exception", "BaseException")


def _scan(codigo: str) -> list[str]:
    """Devolver os achados (REGRA — trecho) de um fonte Python.

    :param codigo: Conteúdo do arquivo .py.
    :return: Lista de strings `REGRA — trecho` (vazia = passa).
    """
    achados: list[str] = []
    linhas = codigo.splitlines()
    for no in ast.walk(ast.parse(codigo)):
        if isinstance(no, ast.ExceptHandler):
            if (
                len(no.body) == 1
                and isinstance(no.body[0], _MUDOS)
                and (
                    no.type is None
                    or (isinstance(no.type, ast.Name) and no.type.id in _GENERICAS)
                )
            ):
                regra = "B110" if isinstance(no.body[0], ast.Pass) else "B112"
                trecho = linhas[no.lineno - 1].strip() if 0 < no.lineno <= len(linhas) else ""
                achados.append(
                    f"{no.lineno}: {regra} try/except/{type(no.body[0]).__name__.lower()} — {trecho[:110]}"
                )
        elif isinstance(no, (ast.Import, ast.ImportFrom)):
            nomes = (
                [a.name for a in no.names] if isinstance(no, ast.Import) else [no.module or ""]
            )
            if any(n.startswith("xml.etree") or n == "xml" for n in nomes):
                trecho = linhas[no.lineno - 1].strip() if 0 < no.lineno <= len(linhas) else ""
                achados.append(f"{no.lineno}: B405 xml.etree — {trecho[:110]}")
    return achados


def test_scan_seguranca_sem_handler_mudo_nem_xml_etree():
    """qgc4qgis/ não pode ter handler genérico mudo nem import xml.etree."""
    pacote = Path(__file__).resolve().parent.parent / "qgc4qgis"
    problemas: list[str] = []
    for py in sorted(pacote.rglob("*.py")):
        for achado in _scan(py.read_text(encoding="utf-8")):
            problemas.append(f"{py.relative_to(pacote.parent)}:{achado}")
    assert not problemas, "Achados do scanner (arquivo:linha: REGRA — trecho):\n" + "\n".join(
        problemas
    )


def test_semantica_do_scanner():
    """A semântica replica o _scan_seguranca: tipado passa, genérico mudo acusa."""
    # Handler tipado com pass: PASSA (fluxo de controle legítimo).
    assert _scan("try:\n    f()\nexcept AttributeError:\n    pass\n") == []
    # Handler genérico que registra: PASSA (corpo não é só pass/continue).
    assert _scan("try:\n    f()\nexcept Exception as e:\n    log(e)\n") == []
    # B110: genérico + corpo só pass.
    assert _scan("try:\n    f()\nexcept Exception:\n    pass\n") == [
        "3: B110 try/except/pass — except Exception:"
    ]
    # B112: sem tipo + corpo só continue.
    assert _scan("for i in x:\n    try:\n        f()\n    except:\n        continue\n") == [
        "4: B112 try/except/continue — except:"
    ]
    # B405: import xml.etree (direto e from).
    assert _scan("import xml.etree.ElementTree as ET\n") == [
        "1: B405 xml.etree — import xml.etree.ElementTree as ET"
    ]
    assert _scan("from xml.etree import ElementTree\n") == [
        "1: B405 xml.etree — from xml.etree import ElementTree"
    ]
