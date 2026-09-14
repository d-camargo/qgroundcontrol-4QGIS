"""Tests for documentation site integrity and quality gates (D76)."""

import ast
import configparser
import re
from pathlib import Path
from urllib.parse import urlparse

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
MKDOCS_PATH = REPO_ROOT / "mkdocs.yml"
METADATA_PATH = REPO_ROOT / "qgc4qgis" / "metadata.txt"
PROCESSING_DIR = REPO_ROOT / "qgc4qgis" / "processing"

EXPECTED_DOCS_DIR = "docs-qgc4qgis"
EXPECTED_SITE_URL = "https://qgr4qgis.dcamargo.com.br/"
EXPECTED_ALG_COUNT = 7


def _returned_string(py_path: Path, func_name: str) -> str:
    """Return the literal string returned by `def func_name` in py_path."""
    tree = ast.parse(py_path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            for stmt in ast.walk(node):
                if (
                    isinstance(stmt, ast.Return)
                    and isinstance(stmt.value, ast.Constant)
                    and isinstance(stmt.value.value, str)
                ):
                    return stmt.value.value
    raise AssertionError(
        f"{py_path.name}: não achei `def {func_name}` retornando string literal"
    )


def _provider_alg_ids() -> list[str]:
    """Full algorithm ids read from source: provider id() + each alg name()."""
    provider_id = _returned_string(PROCESSING_DIR / "provider.py", "id")
    ids = []
    for alg_path in sorted(PROCESSING_DIR.glob("alg_*.py")):
        ids.append(f"{provider_id}:{_returned_string(alg_path, 'name')}")
    return ids


def _load_mkdocs_config() -> dict:
    assert MKDOCS_PATH.exists(), f"mkdocs.yml: arquivo não encontrado em {MKDOCS_PATH}"
    try:
        with open(MKDOCS_PATH, encoding="utf-8") as f:
            config = yaml.safe_load(f)
    except Exception as exc:
        assert False, f"mkdocs.yml: erro ao carregar YAML: {exc}"
    assert isinstance(config, dict), "mkdocs.yml: conteúdo do arquivo YAML não é um dicionário"
    return config


def _extract_nav_files(nav_item) -> list[str]:
    files = []
    if isinstance(nav_item, str):
        files.append(nav_item)
    elif isinstance(nav_item, dict):
        for val in nav_item.values():
            files.extend(_extract_nav_files(val))
    elif isinstance(nav_item, list):
        for item in nav_item:
            files.extend(_extract_nav_files(item))
    return files


def test_gate1_config_yaml_safe_load():
    """Gate 1: mkdocs.yml loads cleanly with yaml.safe_load."""
    config = _load_mkdocs_config()
    assert config, "mkdocs.yml: arquivo YAML está vazio"


def test_gate2_docs_dir_and_site_url():
    """Gate 2: docs_dir is docs-qgc4qgis (never docs/) and site_url is exact."""
    config = _load_mkdocs_config()
    docs_dir = config.get("docs_dir")
    site_url = config.get("site_url")

    assert docs_dir == EXPECTED_DOCS_DIR, (
        f"mkdocs.yml: docs_dir deve ser '{EXPECTED_DOCS_DIR}' "
        f"(docs/ pertence ao QGC upstream), achei '{docs_dir}'"
    )
    assert site_url == EXPECTED_SITE_URL, (
        f"mkdocs.yml: site_url deve ser '{EXPECTED_SITE_URL}' "
        f"(domínio real do site), achei '{site_url}'"
    )

    docs_path = REPO_ROOT / docs_dir
    assert docs_path.is_dir(), f"mkdocs.yml: diretório docs_dir '{docs_dir}' não encontrado"


def test_gate3_cname_matches_site_url_host():
    """Gate 3: CNAME content matches site_url hostname."""
    config = _load_mkdocs_config()
    docs_dir = config["docs_dir"]
    site_url = config["site_url"]

    parsed = urlparse(site_url)
    expected_host = parsed.hostname or parsed.netloc.split(":")[0]
    assert expected_host, f"mkdocs.yml: falha ao extrair hostname de site_url '{site_url}'"

    cname_path = REPO_ROOT / docs_dir / "CNAME"
    assert cname_path.exists(), f"{docs_dir}/CNAME: arquivo CNAME não encontrado"

    cname_content = cname_path.read_text(encoding="utf-8").strip()
    assert cname_content == expected_host, (
        f"{docs_dir}/CNAME: conteúdo do CNAME '{cname_content}' "
        f"diverge do host de site_url '{expected_host}'"
    )


def test_gate4_nav_files_bidirectional():
    """Gate 4: Nav entries match doc files in both directions."""
    config = _load_mkdocs_config()
    docs_dir = config["docs_dir"]
    docs_path = REPO_ROOT / docs_dir
    nav = config.get("nav", [])

    assert nav, "mkdocs.yml: nav ausente ou vazia"
    nav_files = _extract_nav_files(nav)

    # Direction 1: Nav -> Files
    for nav_file in nav_files:
        target_path = docs_path / nav_file
        assert target_path.exists(), (
            f"mkdocs.yml: arquivo '{nav_file}' listado na nav não existe em '{docs_dir}'"
        )

    # Direction 2: Files -> Nav
    for md_file in docs_path.rglob("*.md"):
        if md_file.name.endswith(".pt.md"):
            continue
        rel_path = md_file.relative_to(docs_path).as_posix()
        assert rel_path in nav_files, (
            f"{docs_dir}/{rel_path}: arquivo .md não está listado na nav de mkdocs.yml"
        )


def test_gate5_pt_md_parity():
    """Gate 5: Parity between .md and .pt.md documentation files."""
    config = _load_mkdocs_config()
    docs_dir = config["docs_dir"]
    docs_path = REPO_ROOT / docs_dir

    all_md_files = list(docs_path.rglob("*.md"))

    # For every base .md, check .pt.md exists
    for md_file in all_md_files:
        if md_file.name.endswith(".pt.md"):
            continue
        rel_path = md_file.relative_to(docs_path).as_posix()
        stem = md_file.name[:-3]
        pt_file = md_file.parent / f"{stem}.pt.md"
        assert pt_file.exists(), (
            f"{docs_dir}/{rel_path}: arquivo de tradução {pt_file.name} não encontrado"
        )

    # For every .pt.md, check base .md exists
    for pt_file in all_md_files:
        if not pt_file.name.endswith(".pt.md"):
            continue
        rel_path = pt_file.relative_to(docs_path).as_posix()
        stem = pt_file.name[:-6]
        base_file = pt_file.parent / f"{stem}.md"
        assert base_file.exists(), (
            f"{docs_dir}/{rel_path}: arquivo original {base_file.name} não encontrado"
        )


def _metadata_general():
    assert METADATA_PATH.exists(), f"qgc4qgis/metadata.txt: arquivo não encontrado em {METADATA_PATH}"

    parser = configparser.ConfigParser(interpolation=None)
    parser.optionxform = str
    parser.read(METADATA_PATH, encoding="utf-8")

    assert "general" in parser, "qgc4qgis/metadata.txt: seção [general] não encontrada"
    return parser["general"]


def _h2_headings(text: str) -> list[str]:
    return [m.group(1).strip() for m in re.finditer(r"^##\s+(.+?)\s*$", text, re.MULTILINE)]


def test_gate6_changelog_tied_to_metadata():
    """Gate 6: Changelog is tied to version and changelog in metadata.txt."""
    general = _metadata_general()

    version = general.get("version", "").strip()
    changelog_val = general.get("changelog", "").strip()

    assert version, "qgc4qgis/metadata.txt: campo 'version' ausente ou vazio"
    assert changelog_val, "qgc4qgis/metadata.txt: campo 'changelog' ausente ou vazio"

    metadata_versions = re.findall(r"(?m)^\s*(\d+\.\d+\.\d+)\s*:", changelog_val)
    assert metadata_versions, (
        "qgc4qgis/metadata.txt: campo 'changelog' não lista versões no formato 'X.Y.Z:'"
    )
    assert version in metadata_versions, (
        f"qgc4qgis/metadata.txt: campo 'changelog' não contém a versão '{version}'"
    )

    config = _load_mkdocs_config()
    docs_dir = config["docs_dir"]
    docs_path = REPO_ROOT / docs_dir

    for changelog_name in ("changelog.md", "changelog.pt.md"):
        changelog_path = docs_path / changelog_name
        assert changelog_path.exists(), (
            f"{docs_dir}/{changelog_name}: arquivo não encontrado"
        )

        headings = _h2_headings(changelog_path.read_text(encoding="utf-8"))
        assert headings, f"{docs_dir}/{changelog_name}: nenhuma seção '## ' encontrada"
        assert headings[0] == version, (
            f"{docs_dir}/{changelog_name}: a primeira seção é '{headings[0]}', "
            f"mas a versão atual do metadata.txt é '{version}'"
        )
        for metadata_version in metadata_versions:
            assert metadata_version in headings, (
                f"{docs_dir}/{changelog_name}: a versão {metadata_version} do "
                "changelog= do metadata.txt não aparece como seção '## '"
            )


def test_gate7_provider_ids_and_installation_mentions():
    """Gate 7: provider IDs (read from source) in algorithm pages; install mentions."""
    config = _load_mkdocs_config()
    docs_dir = config["docs_dir"]
    docs_path = REPO_ROOT / docs_dir

    alg_ids = _provider_alg_ids()
    assert len(alg_ids) == EXPECTED_ALG_COUNT, (
        f"qgc4qgis/processing/alg_*.py: o provider registra {len(alg_ids)} "
        f"algoritmos (esperados {EXPECTED_ALG_COUNT}); se a contagem mudou de "
        "propósito, atualize algorithms.md/algorithms.pt.md e EXPECTED_ALG_COUNT"
    )

    alg_en = docs_path / "algorithms.md"
    alg_pt = docs_path / "algorithms.pt.md"

    assert alg_en.exists(), f"{docs_dir}/algorithms.md: arquivo não encontrado"
    assert alg_pt.exists(), f"{docs_dir}/algorithms.pt.md: arquivo não encontrado"

    alg_en_text = alg_en.read_text(encoding="utf-8")
    alg_pt_text = alg_pt.read_text(encoding="utf-8")

    for alg_id in alg_ids:
        assert alg_id in alg_en_text, (
            f"{docs_dir}/algorithms.md: ID do algoritmo '{alg_id}' não encontrado"
        )
        assert alg_id in alg_pt_text, (
            f"{docs_dir}/algorithms.pt.md: ID do algoritmo '{alg_id}' não encontrado"
        )

    inst_en = docs_path / "installation.md"
    inst_pt = docs_path / "installation.pt.md"

    assert inst_en.exists(), f"{docs_dir}/installation.md: arquivo não encontrado"
    assert inst_pt.exists(), f"{docs_dir}/installation.pt.md: arquivo não encontrado"

    inst_en_text = inst_en.read_text(encoding="utf-8")
    inst_pt_text = inst_pt.read_text(encoding="utf-8")

    required_mentions = ["3.34", "4.x", "Qt6"]
    for mention in required_mentions:
        assert mention in inst_en_text, (
            f"{docs_dir}/installation.md: menção a '{mention}' não encontrada"
        )
        assert mention in inst_pt_text, (
            f"{docs_dir}/installation.pt.md: menção a '{mention}' não encontrada"
        )


def test_gate8_installation_urls():
    """Gate 8: installation pages contain QGIS plugin repository and GitHub release URLs."""
    config = _load_mkdocs_config()
    docs_dir = config["docs_dir"]
    docs_path = REPO_ROOT / docs_dir

    plugin_url = "plugins.qgis.org/plugins/qgc4qgis"
    release_url = "github.com/d-camargo/qgroundcontrol-4QGIS/releases"

    for filename in ("installation.md", "installation.pt.md"):
        filepath = docs_path / filename
        assert filepath.exists(), f"{docs_dir}/{filename}: arquivo não encontrado"
        text = filepath.read_text(encoding="utf-8")
        assert plugin_url in text, (
            f"{docs_dir}/{filename}: URL '{plugin_url}' não encontrada"
        )
        assert release_url in text, (
            f"{docs_dir}/{filename}: URL '{release_url}' não encontrada"
        )

