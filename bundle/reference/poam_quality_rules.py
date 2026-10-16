"""
POA&M Grader
============

Validates POA&M entries from SSP writer and POA&M manager output. Checks:
- Eligibility (only 1-point controls, minus 6 exclusions)
- Entry completeness (8 required fields, scored 0-16)
- 180-day feasibility
- Total deduction <= 22 points
- No 5-point or 3-point controls (critical finding)
- Traceability to gap assessment findings
"""

from dataclasses import dataclass, field
from datetime import datetime

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from conftest import get_control_weight, is_poam_eligible, POAM_EXCLUDED_ONE_POINT


REQUIRED_FIELDS = [
    "weakness",
    "current_state",
    "target_state",
    "tasks",
    "resources",
    "milestones",
    "completion_date",
    "responsible",
]


@dataclass
class POAMEntryScore:
    poam_id: str
    control_id: str
    eligible: bool
    eligibility_reason: str = ""
    quality_score: int = 0  # 0-16
    quality_details: dict = field(default_factory=dict)
    feasible: bool = True
    feasibility_notes: str = ""

    @property
    def assessment_ready(self) -> bool:
        return self.eligible and self.quality_score >= 12 and self.feasible


@dataclass
class POAMResult:
    passed: bool = True
    entries: list = field(default_factory=list)
    total_deduction: int = 0
    critical_findings: list = field(default_factory=list)  # 5/3-point in POA&M
    eligibility_errors: list = field(default_factory=list)
    quality_summary: dict = field(default_factory=dict)

    @property
    def summary(self) -> str:
        if self.critical_findings:
            return f"CRITICAL ({len(self.critical_findings)} ineligible high-weight controls in POA&M)"
        if not self.passed:
            return f"FAIL ({len(self.eligibility_errors)} eligibility errors)"
        return "PASS"


def score_entry_quality(entry: dict) -> tuple[int, dict]:
    """Score a POA&M entry on the 0-16 scale.

    Each of 8 fields scores 0 (missing), 1 (present but vague), or 2 (specific).
    """
    details = {}
    total = 0

    for field_name in REQUIRED_FIELDS:
        value = entry.get(field_name, "")
        if not value or value.strip() == "":
            details[field_name] = 0
        elif _is_vague(field_name, value):
            details[field_name] = 1
            total += 1
        else:
            details[field_name] = 2
            total += 2

    return total, details


def _is_vague(field_name: str, value: str) -> bool:
    """Heuristic: is a field value vague/generic rather than specific?"""
    vague_patterns = {
        "weakness": ["security weakness", "not implemented", "gap exists", "needs improvement"],
        "current_state": ["not in place", "does not exist", "none", "n/a"],
        "target_state": ["implement", "deploy", "will be", "compliant"],
        "tasks": ["implement solution", "deploy tool", "fix", "remediate"],
        "resources": ["tbd", "to be determined", "as needed", "staff"],
        "milestones": ["tbd", "to be determined", "as needed"],
        "completion_date": ["tbd", "asap", "to be determined"],
        "responsible": ["it team", "security team", "management", "staff", "tbd"],
    }

    value_lower = value.lower().strip()
    patterns = vague_patterns.get(field_name, [])

    # If the entire value is just a vague phrase, it's vague
    for pattern in patterns:
        if value_lower == pattern or value_lower == pattern + ".":
            return True

    # Very short values (< 10 chars) for descriptive fields are likely vague
    if field_name in ("weakness", "current_state", "target_state", "tasks") and len(value_lower) < 15:
        return True

    return False


def validate_poam(
    entries: list[dict],
    gap_findings: list[dict] | None = None,
    conditional_status_date: str | None = None,
) -> POAMResult:
    """Validate a complete set of POA&M entries.

    Args:
        entries: List of POA&M entry dicts with keys:
            - poam_id: str
            - control_id: str (e.g., "3.5.3")
            - status: str (NOT MET / PARTIAL)
            - weakness, current_state, target_state, tasks, resources,
              milestones, completion_date, responsible: str
        gap_findings: Optional list of gap assessment findings for traceability
        conditional_status_date: Optional date string (YYYY-MM-DD) for 180-day check

    Returns:
        POAMResult with pass/fail and detailed findings
    """
    result = POAMResult()
    total_deduction = 0

    for entry in entries:
        cid = entry["control_id"]
        status = entry.get("status", "NOT MET")
        weight = get_control_weight(cid)

        # Eligibility check
        eligible = is_poam_eligible(cid, status)
        reason = ""
        if not eligible:
            if weight >= 3 and not (cid == "3.13.11" and status == "PARTIAL"):
                reason = f"{weight}-point control — NOT POA&M eligible (assessment blocker)"
                result.critical_findings.append(f"{cid} (weight={weight}): {reason}")
            elif cid in POAM_EXCLUDED_ONE_POINT:
                reason = "1-point control but specifically excluded from POA&M eligibility"
                result.eligibility_errors.append(f"{cid}: {reason}")
            result.passed = False

        # Deduction calculation
        if status == "PARTIAL" and cid == "3.13.11":
            deduction = 3
        else:
            deduction = weight
        total_deduction += deduction

        # Quality scoring
        quality_score, quality_details = score_entry_quality(entry)

        # Feasibility check (180-day)
        feasible = True
        feasibility_notes = ""
        if conditional_status_date and entry.get("completion_date"):
            try:
                csd = datetime.strptime(conditional_status_date, "%Y-%m-%d")
                completion = datetime.strptime(entry["completion_date"], "%Y-%m-%d")
                days = (completion - csd).days
                if days > 180:
                    feasible = False
                    feasibility_notes = f"Completion {days} days after conditional status (max 180)"
                elif days < 0:
                    feasible = False
                    feasibility_notes = "Completion date is before conditional status date"
            except ValueError:
                feasibility_notes = "Could not parse date"

        entry_score = POAMEntryScore(
            poam_id=entry.get("poam_id", "unknown"),
            control_id=cid,
            eligible=eligible,
            eligibility_reason=reason,
            quality_score=quality_score,
            quality_details=quality_details,
            feasible=feasible,
            feasibility_notes=feasibility_notes,
        )
        result.entries.append(entry_score)

    result.total_deduction = total_deduction
    if total_deduction > 22:
        result.eligibility_errors.append(f"Total POA&M deduction: {total_deduction} points (max 22)")
        result.passed = False

    # Quality summary
    scores = [e.quality_score for e in result.entries]
    if scores:
        result.quality_summary = {
            "assessment_ready": sum(1 for s in scores if s >= 12),
            "needs_fixes": sum(1 for s in scores if 8 <= s < 12),
            "rewrite": sum(1 for s in scores if s < 8),
            "avg_score": round(sum(scores) / len(scores), 1),
        }

    # Traceability check
    if gap_findings is not None:
        poam_controls = {e["control_id"] for e in entries}
        gap_eligible = {
            f["control_id"]
            for f in gap_findings
            if f.get("status") in ("NOT MET", "PARTIAL")
            and is_poam_eligible(f["control_id"], f.get("status", "NOT MET"))
        }
        # POA&M items without gap finding
        orphans = poam_controls - {f["control_id"] for f in gap_findings}
        if orphans:
            result.eligibility_errors.append(
                f"POA&M entries without gap assessment finding: {', '.join(sorted(orphans))}"
            )
        # Gap findings eligible for POA&M but missing
        missing = gap_eligible - poam_controls
        if missing:
            result.eligibility_errors.append(f"Eligible gap findings missing from POA&M: {', '.join(sorted(missing))}")

    return result
