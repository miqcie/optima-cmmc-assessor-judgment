"""
CMMC Control Register — Single Python Source of Truth for Derived Constants
============================================================================

Loads `data/nist-800-171-controls.yaml` once and exposes derived sets and
business-rule constants that the rest of the codebase imports.

The YAML itself is the authoritative source (verified against the DoD
Assessment Methodology PDF by `tests/test_register.py`). This module is the
Python view of that YAML — derived, not duplicated. Hand-maintained sets
in scripts or tests are forbidden (see `tests/test_register.py` and
`tests/test_prose_consistency.py`).

Business-rule constants (POA&M max deduction, 180-day closeout) are encoded
here because they come from the DoD methodology directly, not from per-
control fields in the YAML. They have no other canonical home.
"""

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
BASE_CONTROLS_PATH = Path(__file__).resolve().parent / "nist_800_171_controls_sprs_weights.yaml"  # bundle: weights file sits beside this module


def load_base_controls() -> dict:
    with open(BASE_CONTROLS_PATH) as f:
        return yaml.safe_load(f)["controls"]


_BASE_CONTROLS = load_base_controls()


# Tier sets — every control by SPRS weight
FIVE_POINT_CONTROLS = frozenset(cid for cid, c in _BASE_CONTROLS.items() if c["weight"] == 5)
THREE_POINT_CONTROLS = frozenset(cid for cid, c in _BASE_CONTROLS.items() if c["weight"] == 3)
ONE_POINT_CONTROLS = frozenset(cid for cid, c in _BASE_CONTROLS.items() if c["weight"] == 1)
ZERO_POINT_CONTROLS = frozenset(cid for cid, c in _BASE_CONTROLS.items() if c["weight"] == 0)


# POA&M-ineligible 1-point controls + the zero-point control (canonical "6 exceptions").
# Note: in CMMC parlance "the 6 exceptions" includes 3.12.4 which is 0-point.
POAM_EXCLUDED_ONE_POINT = frozenset(
    cid for cid, c in _BASE_CONTROLS.items() if not c.get("poam_eligible", True) and c["weight"] <= 1
)

# 5-point controls with partial-credit semantics (3.5.3 MFA, 3.13.11 FIPS).
# Only 3.13.11 PARTIAL is POA&M-eligible; 3.5.3 PARTIAL is not.
POAM_SPECIAL_PARTIAL = frozenset(
    cid for cid, c in _BASE_CONTROLS.items() if c.get("partial_credit", {}).get("poam_if_partial", False)
)

PARTIAL_CREDIT_CONTROLS = frozenset(cid for cid, c in _BASE_CONTROLS.items() if "partial_credit" in c)

# Per-control overrides from the DoD methodology (e.g., 3.1.4 forced to 1-pt
# despite being in the 3-pt bucket).
WEIGHT_OVERRIDES = {cid: c["weight"] for cid, c in _BASE_CONTROLS.items() if c.get("weight_note")}


# Business-rule constants from the DoD Assessment Methodology v1.2.1
# and 32 CFR Part 170 §170.21.
POAM_MAX_DEDUCTION_POINTS = 22
POAM_CLOSEOUT_DAYS = 180
SPRS_PASSING_THRESHOLD = 88
SPRS_MAX_SCORE = 110
SPRS_WORST_POSSIBLE_SCORE = -203


# Convenience aliases for callers that want the canonical "6 exception" list
# (matches the well-known CMMC idiom).
POAM_EXCEPTION_CONTROL_IDS = POAM_EXCLUDED_ONE_POINT


def get_control_weight(control_id: str) -> int:
    return _BASE_CONTROLS[control_id]["weight"]


def is_poam_eligible(control_id: str, status: str = "NOT_MET") -> bool:
    """Whether a control is POA&M-eligible given its status.

    - 5pt and 3pt controls are never eligible
    - Excluded 1pt and the 0pt control are never eligible
    - Special: 3.13.11 PARTIAL is eligible at the 3-point partial-credit level
    """
    if status == "PARTIAL" and control_id in POAM_SPECIAL_PARTIAL:
        return True
    info = _BASE_CONTROLS[control_id]
    if info["weight"] >= 3:
        return False
    if not info.get("poam_eligible", True):
        return False
    return True
