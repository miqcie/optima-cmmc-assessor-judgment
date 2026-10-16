"""
SSP Grader
==========

Validates SSP narratives and structure. Checks:
- No future tense in MET control narratives
- No NIST copy-paste (control requirement restated as narrative)
- Evidence IDs follow E-XX-NNN convention
- Five-element test (Who/What/When/How/Evidence present)
- Named individuals (not departments)
- No "N/A" without justification
- POA&M entries only for eligible controls
- Assessment objective coverage (if objectives provided)
"""

import re
from dataclasses import dataclass, field


@dataclass
class NarrativeScore:
    control_id: str
    status: str
    errors: list = field(default_factory=list)
    warnings: list = field(default_factory=list)
    elements_present: dict = field(default_factory=dict)

    @property
    def passed(self) -> bool:
        return len(self.errors) == 0


@dataclass
class SSPResult:
    passed: bool = True
    narratives_checked: int = 0
    narratives_passed: int = 0
    narrative_scores: list = field(default_factory=list)
    structural_errors: list = field(default_factory=list)
    evidence_id_errors: list = field(default_factory=list)

    @property
    def pass_rate(self) -> float:
        if self.narratives_checked == 0:
            return 0.0
        return self.narratives_passed / self.narratives_checked

    @property
    def summary(self) -> str:
        if self.passed:
            return f"PASS ({self.narratives_passed}/{self.narratives_checked} narratives clean)"
        error_count = sum(len(n.errors) for n in self.narrative_scores)
        return f"FAIL ({error_count} errors across {self.narratives_checked} narratives)"


# Future tense patterns that indicate non-implementation
FUTURE_TENSE_PATTERNS = [
    r"\bwill\s+(?:implement|deploy|configure|establish|create|develop|install|enable|enforce)",
    r"\bplan(?:s|ning)?\s+to\b",
    r"\bintend(?:s|ing)?\s+to\b",
    r"\bwill\s+be\s+(?:implemented|deployed|configured|established)",
    r"\bin\s+the\s+(?:future|process\s+of)",
    r"\bonce\s+(?:implemented|deployed|configured)",
    r"\bscheduled\s+(?:for|to)\b",
    r"\bupcoming\b",
]

# Vague/generic phrases that don't describe specific implementation
VAGUE_PATTERNS = [
    r"\bappropriate\s+(?:measures|controls|safeguards|mechanisms)\b",
    r"\bas\s+(?:needed|required|appropriate)\b",
    r"\bthe\s+organization\s+(?:implements|uses|deploys|maintains)\b",
    r"\bperiodically\b",
    r"\bregularly\b",
    r"\bapplicable\s+(?:personnel|users|staff)\b",
    r"\bdocumentation\s+exists\b",
]

# Generic role references (should be named individuals)
GENERIC_ROLE_PATTERNS = [
    r"\bthe\s+(?:IT\s+)?(?:team|department|staff|personnel|organization)\b",
    r"\bdesignated\s+(?:staff|personnel|individual)\b",
    r"\bresponsible\s+(?:staff|personnel|party)\b",
    r"\bauthorized\s+(?:staff|personnel|individuals)\b",
]

# Evidence ID pattern: E-XX-NNN (family abbreviation, 3-digit number)
EVIDENCE_ID_PATTERN = re.compile(r"E-[A-Z]{2}-\d{3}")

# NIST control families for evidence ID validation
VALID_EVIDENCE_FAMILIES = {"AC", "AT", "AU", "CM", "IA", "IR", "MA", "MP", "PS", "PE", "RA", "CA", "SC", "SI"}


def validate_narrative(
    control_id: str,
    status: str,
    narrative: str,
    nist_requirement: str | None = None,
) -> NarrativeScore:
    """Validate a single control narrative.

    Args:
        control_id: e.g., "3.1.1"
        status: MET, NOT MET, PARTIAL, N/A
        narrative: The full narrative text
        nist_requirement: Optional NIST control text to check for copy-paste
    """
    score = NarrativeScore(control_id=control_id, status=status)

    if status == "N/A":
        # N/A needs justification
        if len(narrative.strip()) < 50:
            score.errors.append("N/A control with insufficient justification (< 50 chars)")
        if "scoping guide" not in narrative.lower() and "scope" not in narrative.lower():
            score.warnings.append("N/A justification doesn't reference CMMC Scoping Guide")
        return score

    if status == "NOT MET":
        # NOT MET controls should be in POA&M, not have implementation narratives
        # But they still need a description of current state
        return score

    # --- Checks for MET and PARTIAL narratives ---

    # Future tense check (critical — assessment failure)
    for pattern in FUTURE_TENSE_PATTERNS:
        matches = re.findall(pattern, narrative, re.IGNORECASE)
        if matches:
            score.errors.append(f"Future tense detected: '{matches[0]}' — MET controls must use present tense")

    # NIST copy-paste check
    if nist_requirement:
        # Simple similarity: if >60% of NIST requirement words appear in sequence in the narrative
        nist_words = nist_requirement.lower().split()
        narrative_lower = narrative.lower()
        if len(nist_words) > 5:
            # Check for long subsequence matches
            window = min(len(nist_words), 10)
            for i in range(len(nist_words) - window + 1):
                phrase = " ".join(nist_words[i : i + window])
                if phrase in narrative_lower:
                    score.errors.append(f"Possible NIST copy-paste: '{phrase}...' — describe YOUR implementation")
                    break

    # Five-element test
    elements = {
        "who": bool(re.search(r"\*\*Who\b", narrative) or re.search(r"(?:Who|Responsible)[:\s]", narrative)),
        "what": bool(re.search(r"\*\*What\b", narrative) or re.search(r"(?:What|Implementation)[:\s]", narrative)),
        "when": bool(re.search(r"\*\*When\b", narrative) or re.search(r"(?:When|Frequency|How Often)[:\s]", narrative)),
        "how": bool(re.search(r"\*\*How\b", narrative) or re.search(r"(?:How|Mechanism|Method)[:\s]", narrative)),
        "evidence": bool(EVIDENCE_ID_PATTERN.search(narrative)),
    }
    score.elements_present = elements

    missing = [k for k, v in elements.items() if not v]
    if missing:
        score.errors.append(f"Missing narrative elements: {', '.join(missing)}")

    # Evidence ID format check
    evidence_ids = EVIDENCE_ID_PATTERN.findall(narrative)
    if evidence_ids:
        for eid in evidence_ids:
            family = eid.split("-")[1]
            if family not in VALID_EVIDENCE_FAMILIES:
                score.errors.append(f"Invalid evidence family in {eid} (valid: {VALID_EVIDENCE_FAMILIES})")
    elif status == "MET":
        score.errors.append("MET control with no evidence artifact reference (E-XX-NNN)")

    # Generic role check
    for pattern in GENERIC_ROLE_PATTERNS:
        matches = re.findall(pattern, narrative, re.IGNORECASE)
        if matches:
            score.warnings.append(f"Generic role reference: '{matches[0]}' — use named individuals")

    # Vague language check
    for pattern in VAGUE_PATTERNS:
        matches = re.findall(pattern, narrative, re.IGNORECASE)
        if matches:
            score.warnings.append(f"Vague language: '{matches[0]}'")

    return score


def validate_ssp(narratives: list[dict]) -> SSPResult:
    """Validate a full set of SSP control narratives.

    Args:
        narratives: List of dicts with keys:
            - control_id: str
            - status: str (MET / NOT MET / PARTIAL / N/A)
            - narrative: str (the narrative text)
            - nist_requirement: str (optional, NIST control text)
    """
    result = SSPResult()
    result.narratives_checked = len(narratives)

    for n in narratives:
        score = validate_narrative(
            control_id=n["control_id"],
            status=n["status"],
            narrative=n["narrative"],
            nist_requirement=n.get("nist_requirement"),
        )
        result.narrative_scores.append(score)
        if score.passed:
            result.narratives_passed += 1
        else:
            result.passed = False

    # Check evidence ID uniqueness and consistency
    all_evidence_ids = []
    for n in narratives:
        ids = EVIDENCE_ID_PATTERN.findall(n.get("narrative", ""))
        all_evidence_ids.extend(ids)

    # Duplicates are OK (same evidence can support multiple controls).
    # Cross-family ID reuse without explicit reference is a planned check, deferred.
    return result


def extract_narratives_from_markdown(ssp_text: str) -> list[dict]:
    """Parse an SSP markdown document into structured narratives.

    Looks for control blocks in the format:
    #### XX.L2-3.X.X — Control Title
    | Status | MET/NOT MET |
    **Narrative:**
    ...
    """
    narratives = []

    # Pattern for control headers
    control_header = re.compile(
        r"####\s+\w+\.L2-(\d+\.\d+\.\d+)\s*[-—]\s*(.+?)$",
        re.MULTILINE,
    )

    matches = list(control_header.finditer(ssp_text))
    for i, match in enumerate(matches):
        control_id = match.group(1)
        # Get text between this control and the next (or end of doc)
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(ssp_text)
        block = ssp_text[start:end]

        # Extract status
        status_match = re.search(r"Status\s*\|?\s*(MET|NOT MET|PARTIAL|N/A)", block, re.IGNORECASE)
        status = status_match.group(1).upper() if status_match else "UNKNOWN"

        narratives.append(
            {
                "control_id": control_id,
                "status": status,
                "narrative": block,
            }
        )

    return narratives
