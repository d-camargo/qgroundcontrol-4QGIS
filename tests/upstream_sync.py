"""Refresh and check the upstream QGC contract that qgc4qgis depends on.

qgc4qgis (src/../qgc4qgis/) is a QGIS plugin derived from a handful of facts
declared by the upstream QGroundControl C++ code: the .plan file format
version, the range of Survey ComplexItem versions the planner accepts, and the
bundled camera metadata catalog. This script fetches those facts straight from
``mavlink/qgroundcontrol`` on GitHub and either checks them against the frozen
contract in ``tests/upstream_contract.json`` (default) or refreshes that
contract file (``--refresh``).

Network access is required for the ``fetch_*`` helpers and the ``cmd_check``/
``cmd_refresh`` CLI commands. ``compatibility_report`` and ``load_contract`` are
network-free and are imported directly by the offline pytest suite (see
``tests/test_upstream_contract.py``); no top-level code in this module performs
network I/O, so importing it never requires a network connection.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import sys
import urllib.request
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError

UPSTREAM_REPO = "mavlink/qgroundcontrol"
UPSTREAM_REF = "master"
RAW_BASE = f"https://raw.githubusercontent.com/{UPSTREAM_REPO}/{UPSTREAM_REF}"
API_COMMITS_URL = f"https://api.github.com/repos/{UPSTREAM_REPO}/commits"
USER_AGENT = "qgc4qgis-upstream-sync"

REPO_ROOT = Path(__file__).resolve().parent.parent
CONTRACT_PATH = REPO_ROOT / "tests" / "upstream_contract.json"
CAMERAS_JSON_PATH = REPO_ROOT / "qgc4qgis" / "data" / "cameras.json"
PLANFILE_PATH = REPO_ROOT / "qgc4qgis" / "core" / "planfile.py"

PLAN_MASTER_CONTROLLER_H = "src/MissionManager/PlanMasterController.h"
SURVEY_COMPLEX_ITEM_CC = "src/MissionManager/SurveyComplexItem.cc"
CAMERA_METADATA_JSON = "src/Camera/CameraMetaData.json"

WATCHED_SOURCES = [
    "src/MissionManager/SurveyComplexItem.cc",
    "src/MissionManager/SurveyComplexItem.h",
    "src/MissionManager/CameraCalc.cc",
    "src/MissionManager/CameraCalc.h",
    "src/MissionManager/TransectStyleComplexItem.cc",
]

PLAN_FILE_VERSION_RE = re.compile(r"kPlanFileVersion\s*=\s*(\d+)")
SURVEY_VERSION_RANGE_RE = re.compile(r"version\s*<\s*(\d+)\s*\|\|\s*version\s*>\s*(\d+)")


def _headers() -> dict[str, str]:
    """Build request headers, adding a GitHub token if available to avoid rate limits."""
    headers = {"User-Agent": USER_AGENT}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _fetch_bytes(url: str) -> bytes:
    """Fetch the raw bytes at *url*, raising a clear error on network failure."""
    request = urllib.request.Request(url, headers=_headers())
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.read()
    except (HTTPError, URLError) as exc:
        raise RuntimeError(f"Failed to fetch {url}: {exc}") from exc


def _fetch_text(url: str) -> str:
    """Fetch *url* and decode it as UTF-8 text."""
    return _fetch_bytes(url).decode("utf-8")


def fetch_upstream_file(path: str) -> str:
    """Fetch the raw text content of *path* at the upstream ref."""
    return _fetch_text(f"{RAW_BASE}/{path}")


def fetch_upstream_bytes(path: str) -> bytes:
    """Fetch the raw bytes of *path* at the upstream ref."""
    return _fetch_bytes(f"{RAW_BASE}/{path}")


def fetch_last_commit_sha(path: str) -> str:
    """Fetch the SHA of the most recent commit that touched *path* on the upstream ref."""
    url = f"{API_COMMITS_URL}?path={path}&per_page=1&sha={UPSTREAM_REF}"
    payload = json.loads(_fetch_text(url))
    if not payload:
        raise RuntimeError(f"No commits found upstream for path {path!r}")
    return str(payload[0]["sha"])


def extract_plan_file_version(content: str) -> int:
    """Extract ``kPlanFileVersion`` from PlanMasterController.h content."""
    match = PLAN_FILE_VERSION_RE.search(content)
    if not match:
        raise RuntimeError(
            f"Could not find 'kPlanFileVersion = <int>' in upstream "
            f"{PLAN_MASTER_CONTROLLER_H}; upstream may have changed its format."
        )
    return int(match.group(1))


def extract_survey_version_range(content: str) -> tuple[int, int]:
    """Extract the accepted Survey version range from SurveyComplexItem.cc content."""
    match = SURVEY_VERSION_RANGE_RE.search(content)
    if not match:
        raise RuntimeError(
            "Could not find 'version < N || version > M' guard in upstream "
            f"{SURVEY_COMPLEX_ITEM_CC}; upstream may have changed its format."
        )
    return int(match.group(1)), int(match.group(2))


def fetch_upstream_facts() -> dict[str, Any]:
    """Fetch the current upstream facts qgc4qgis's contract tracks."""
    plan_master_controller_h = fetch_upstream_file(PLAN_MASTER_CONTROLLER_H)
    survey_complex_item_cc = fetch_upstream_file(SURVEY_COMPLEX_ITEM_CC)
    camera_metadata_bytes = fetch_upstream_bytes(CAMERA_METADATA_JSON)

    plan_file_version = extract_plan_file_version(plan_master_controller_h)
    survey_min, survey_max = extract_survey_version_range(survey_complex_item_cc)
    camera_metadata_sha256 = hashlib.sha256(camera_metadata_bytes).hexdigest()

    watched_sources = {path: fetch_last_commit_sha(path) for path in WATCHED_SOURCES}

    return {
        "plan_file_version": {"path": PLAN_MASTER_CONTROLLER_H, "value": plan_file_version},
        "survey_version_range": {
            "path": SURVEY_COMPLEX_ITEM_CC,
            "min": survey_min,
            "max": survey_max,
        },
        "camera_metadata": {"path": CAMERA_METADATA_JSON, "sha256": camera_metadata_sha256},
        "watched_sources": watched_sources,
        "_camera_metadata_bytes": camera_metadata_bytes,
    }


def load_contract() -> dict[str, Any]:
    """Load the frozen contract from disk."""
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


def _load_planfile_module() -> Any:
    """Load qgc4qgis/core/planfile.py by file path, without importing the qgc4qgis package.

    ``planfile.py`` is pure stdlib (json/pathlib/typing). Loading it by path
    (instead of ``from qgc4qgis.core import planfile``) avoids pulling in the
    ``qgc4qgis`` package's ``__init__.py``, ``tests/conftest.py``'s autouse QGIS
    fixture, and PyQGIS itself -- none of which are available on a plain CI
    runner. This keeps the compatibility gate usable in CI, where the rest of
    the plugin test suite cannot run at all.
    """
    spec = importlib.util.spec_from_file_location("qgc4qgis_planfile_standalone", PLANFILE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module spec for {PLANFILE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def compatibility_report(contract: dict[str, Any]) -> list[str]:
    """Check qgc4qgis's shipped constants and data against *contract*.

    :param contract: An upstream contract dict (either the one on disk or a
        freshly fetched one), in the same shape as ``upstream_contract.json``.
    :return: A list of actionable problem descriptions; an empty list means
        qgc4qgis is still compatible with the upstream facts in *contract*.
    """
    planfile = _load_planfile_module()
    problems: list[str] = []

    upstream_plan_version = contract["plan_file_version"]["value"]
    if upstream_plan_version != planfile.PLAN_VERSION:
        problems.append(
            f"upstream QGC now expects Plan file version {upstream_plan_version} "
            f"(kPlanFileVersion in {contract['plan_file_version']['path']}) but qgc4qgis "
            f"writes PLAN_VERSION={planfile.PLAN_VERSION}; update PLAN_VERSION in "
            "qgc4qgis/core/planfile.py"
        )

    survey_range = contract["survey_version_range"]
    min_version, max_version = survey_range["min"], survey_range["max"]
    if not (min_version <= planfile.SURVEY_VERSION <= max_version):
        problems.append(
            f"upstream now accepts survey versions {min_version}-{max_version} "
            f"({survey_range['path']}); qgc4qgis writes {planfile.SURVEY_VERSION} "
            "-- update SURVEY_VERSION in qgc4qgis/core/planfile.py"
        )

    expected_sha256 = contract["camera_metadata"]["sha256"]
    actual_sha256 = hashlib.sha256(CAMERAS_JSON_PATH.read_bytes()).hexdigest()
    if actual_sha256 != expected_sha256:
        problems.append(
            "qgc4qgis/data/cameras.json no longer matches upstream "
            f"{contract['camera_metadata']['path']} (sha256 mismatch); run "
            "'python tests/upstream_sync.py --refresh' to resync it from upstream"
        )

    return problems


def build_contract(facts: dict[str, Any]) -> dict[str, Any]:
    """Build the contract document (as written to upstream_contract.json) from fetched facts."""
    return {
        "_comment": (
            "Upstream facts qgc4qgis depends on. Refreshed by tests/upstream_sync.py; "
            "asserted by tests/test_upstream_contract.py."
        ),
        "upstream": UPSTREAM_REPO,
        "ref": UPSTREAM_REF,
        "refreshed_at": datetime.now(UTC).strftime("%Y-%m-%d UTC"),
        "camera_metadata": facts["camera_metadata"],
        "plan_file_version": facts["plan_file_version"],
        "survey_version_range": facts["survey_version_range"],
        "watched_sources": facts["watched_sources"],
    }


def diff_contracts(old: dict[str, Any], new: dict[str, Any]) -> list[str]:
    """Return a list of human-readable differences between two contracts.

    Compares only the fact fields (ignores ``_comment`` and ``refreshed_at``).
    """
    diffs: list[str] = []

    if old["plan_file_version"]["value"] != new["plan_file_version"]["value"]:
        diffs.append(
            "plan_file_version: "
            f"{old['plan_file_version']['value']} -> {new['plan_file_version']['value']}"
        )

    old_range = (old["survey_version_range"]["min"], old["survey_version_range"]["max"])
    new_range = (new["survey_version_range"]["min"], new["survey_version_range"]["max"])
    if old_range != new_range:
        diffs.append(f"survey_version_range: {old_range} -> {new_range}")

    if old["camera_metadata"]["sha256"] != new["camera_metadata"]["sha256"]:
        diffs.append(
            "camera_metadata.sha256: "
            f"{old['camera_metadata']['sha256']} -> {new['camera_metadata']['sha256']}"
        )

    old_watched = old.get("watched_sources", {})
    new_watched = new.get("watched_sources", {})
    for path in WATCHED_SOURCES:
        old_sha = old_watched.get(path)
        new_sha = new_watched.get(path)
        if old_sha != new_sha:
            diffs.append(f"watched_sources[{path}]: {old_sha} -> {new_sha}")

    return diffs


def build_pr_body(
    diffs: list[str], new_contract: dict[str, Any], compat_problems: list[str]
) -> str:
    """Build a markdown summary of what changed, for use as a PR body."""
    lines = ["# qgc4qgis upstream sync", ""]
    if not diffs:
        lines.append("No changes detected in the tracked upstream facts.")
    else:
        lines.append("The following upstream facts changed:")
        lines.append("")
        for line in diffs:
            lines.append(f"- {line}")
    lines.append("")
    lines.append(f"Refreshed at: {new_contract['refreshed_at']}")
    lines.append("")
    lines.append("## Compatibility")
    lines.append("")
    if not compat_problems:
        lines.append("✅ plugin constants still match upstream")
    else:
        lines.append("⚠️ qgc4qgis no longer matches upstream:")
        lines.append("")
        for problem in compat_problems:
            lines.append(f"- {problem}")
    lines.append("")
    lines.append(
        "Review `tests/test_upstream_contract.py` failures (if any) and update "
        "`qgc4qgis/core/planfile.py` accordingly before merging."
    )
    return "\n".join(lines) + "\n"


def cmd_check() -> int:
    """Fetch upstream facts and compare them against the contract on disk and qgc4qgis's code.

    This is the gate that must actually catch drift: the offline pytest suite
    (``tests/test_upstream_contract.py``) never runs in CI (it requires PyQGIS,
    which plain runners don't have), so this function -- not pytest -- is what
    ``just qgis-upstream-check`` and the sync workflow rely on to fail loudly.
    """
    old_contract = load_contract()
    facts = fetch_upstream_facts()
    new_contract = build_contract(facts)

    diffs = diff_contracts(old_contract, new_contract)
    compat_problems = compatibility_report(new_contract)

    if not diffs and not compat_problems:
        print("Upstream contract is up to date; no differences found.")
        return 0

    if diffs:
        print("Upstream contract is stale; differences found:")
        for line in diffs:
            print(f"  - {line}")

    if compat_problems:
        print("qgc4qgis is no longer compatible with upstream:")
        for problem in compat_problems:
            print(f"  - {problem}")
        return 2

    return 1


def cmd_refresh(pr_body_path: Path | None) -> int:
    """Fetch upstream facts, rewrite the contract, and sync cameras.json bytes."""
    old_contract = load_contract() if CONTRACT_PATH.exists() else None
    facts = fetch_upstream_facts()
    new_contract = build_contract(facts)

    CONTRACT_PATH.write_text(json.dumps(new_contract, indent=2) + "\n", encoding="utf-8")
    CAMERAS_JSON_PATH.write_bytes(facts["_camera_metadata_bytes"])

    diffs = diff_contracts(old_contract, new_contract) if old_contract else ["initial contract"]
    compat_problems = compatibility_report(new_contract)
    pr_body = build_pr_body(diffs, new_contract, compat_problems)
    print(pr_body)

    if pr_body_path is not None:
        pr_body_path.write_text(pr_body, encoding="utf-8")

    return 2 if compat_problems else 0


def main(argv: list[str] | None = None) -> int:
    """CLI entry point: check (default) or refresh the upstream contract."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Rewrite tests/upstream_contract.json and qgc4qgis/data/cameras.json from upstream.",
    )
    parser.add_argument(
        "--pr-body",
        type=Path,
        default=None,
        help="With --refresh, also write the markdown change summary to this file.",
    )
    args = parser.parse_args(argv)

    if args.pr_body is not None and not args.refresh:
        parser.error("--pr-body requires --refresh")

    if args.refresh:
        return cmd_refresh(args.pr_body)
    return cmd_check()


if __name__ == "__main__":
    sys.exit(main())
