"""Offline assertions that qgc4qgis still matches the frozen upstream QGC contract.

This test never touches the network: it only reads ``tests/upstream_contract.json``
(refreshed by ``tests/upstream_sync.py``) and delegates to
``upstream_sync.compatibility_report`` -- the same check the network-facing CLI
runs -- to compare it against the constants and data files ``qgc4qgis`` actually
ships. If it fails, either the plugin drifted from upstream and needs a code
change, or the contract is stale and needs a refresh
(``python tests/upstream_sync.py --refresh``).

Note: this test requires PyQGIS (via ``tests/conftest.py``'s autouse fixture)
and therefore does not run on plain CI runners. The real drift gate is
``upstream_sync.cmd_check`` (``just qgis-upstream-check`` / the sync workflow),
which reuses the same ``compatibility_report`` function without importing QGIS.
"""

import sys
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

import upstream_sync  # noqa: E402


def _problems_matching(problems: list[str], needle: str) -> list[str]:
    return [problem for problem in problems if needle in problem]


def test_plan_file_version_matches_upstream():
    """qgc4qgis must write the same Plan file version upstream QGC reads."""
    contract = upstream_sync.load_contract()
    problems = upstream_sync.compatibility_report(contract)
    plan_version_problems = _problems_matching(problems, "PLAN_VERSION")
    assert not plan_version_problems, "\n".join(plan_version_problems)


def test_survey_version_within_upstream_range():
    """qgc4qgis must write a Survey ComplexItem version upstream QGC still accepts."""
    contract = upstream_sync.load_contract()
    problems = upstream_sync.compatibility_report(contract)
    survey_version_problems = _problems_matching(problems, "SURVEY_VERSION")
    assert not survey_version_problems, "\n".join(survey_version_problems)


def test_camera_metadata_matches_upstream():
    """qgc4qgis's bundled camera catalog must be byte-identical to upstream's."""
    contract = upstream_sync.load_contract()
    problems = upstream_sync.compatibility_report(contract)
    camera_problems = _problems_matching(problems, "cameras.json")
    assert not camera_problems, "\n".join(camera_problems)
