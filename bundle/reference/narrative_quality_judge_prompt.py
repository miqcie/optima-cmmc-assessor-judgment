"""
Narrative Quality Grader (Model-Based)
======================================

Uses an LLM to evaluate qualitative aspects of agent outputs that
code graders can't check mechanically:

- Specificity (does the narrative describe THIS client's implementation?)
- Micro-contractor sensitivity (appropriate for org size?)
- Actionability (can the client act on this?)
- Assessor readiness (would a C3PAO assessor accept this?)
- Tone (consulting-appropriate, not robotic/generic?)

Runs via Anthropic API. Requires ANTHROPIC_API_KEY env var.
Returns structured scores (1-5) with rationale.
"""

import json
import os
from dataclasses import dataclass, field


GRADING_PROMPT = """You are a CMMC Level 2 assessment expert reviewing agent-generated compliance deliverables for Eagle Ridge Advisory. Grade the following output on these dimensions:

## Grading Criteria

1. **Specificity (1-5):** Does the output describe THIS client's specific implementation? Named people, specific tools, actual configurations — not generic placeholders or template language.
   - 1 = All generic/placeholder text
   - 3 = Mix of specific and generic
   - 5 = Every detail is client-specific

2. **Micro-Contractor Sensitivity (1-5):** Is this appropriate for a small organization (3-50 people)? Does it acknowledge resource constraints without being patronizing? Does it avoid recommending enterprise-scale solutions?
   - 1 = Enterprise assumptions throughout
   - 3 = Mostly appropriate but some unrealistic expectations
   - 5 = Perfectly calibrated for org size

3. **Actionability (1-5):** Can the client (a non-technical owner) understand what to do next? Are instructions clear enough to follow without a consultant translating?
   - 1 = Requires expert interpretation
   - 3 = Mostly clear, some jargon
   - 5 = A non-technical owner could follow this

4. **Assessor Readiness (1-5):** Would a C3PAO assessor accept this as-is? Does it meet assessment rigor? Is evidence traceable? Are assessment objectives addressed?
   - 1 = Would fail assessment review
   - 3 = Acceptable with minor fixes
   - 5 = Assessment-ready, no changes needed

5. **Tone (1-5):** Does it read like a professional consulting deliverable? Not too robotic, not too casual? Appropriate for a client-facing document?
   - 1 = Robotic/AI-sounding or inappropriately casual
   - 3 = Professional but bland
   - 5 = Natural consulting voice

## Context

**Client profile:** {client_profile}
**Agent:** {agent_name}
**Phase:** {phase}

## Output to Grade

{output_text}

## Instructions

Return a JSON object with this structure (no other text):
{{
  "specificity": {{"score": N, "rationale": "..."}},
  "micro_contractor": {{"score": N, "rationale": "..."}},
  "actionability": {{"score": N, "rationale": "..."}},
  "assessor_readiness": {{"score": N, "rationale": "..."}},
  "tone": {{"score": N, "rationale": "..."}},
  "overall": {{"score": N, "rationale": "..."}},
  "critical_issues": ["issue 1", "issue 2"]
}}

The overall score should be the lowest of the 5 dimension scores (weakest link).
critical_issues should list anything that would cause assessment failure or client confusion.
"""


@dataclass
class QualityScore:
    specificity: int = 0
    micro_contractor: int = 0
    actionability: int = 0
    assessor_readiness: int = 0
    tone: int = 0
    overall: int = 0
    rationales: dict = field(default_factory=dict)
    critical_issues: list = field(default_factory=list)
    raw_response: str = ""

    @property
    def passed(self) -> bool:
        return self.overall >= 3 and len(self.critical_issues) == 0

    @property
    def summary(self) -> str:
        if self.passed:
            return f"PASS (overall: {self.overall}/5)"
        issues = f", {len(self.critical_issues)} critical issues" if self.critical_issues else ""
        return f"FAIL (overall: {self.overall}/5{issues})"


def grade_narrative_quality(
    output_text: str,
    agent_name: str,
    phase: str,
    client_profile: str = "Small DoD contractor, 3-10 employees, non-technical owner",
    api_key: str | None = None,
) -> QualityScore:
    """Grade agent output quality using an LLM.

    Args:
        output_text: The agent output to grade
        agent_name: Which agent produced it (e.g., "cmmc-gap-assessor")
        phase: Which phase (e.g., "Phase 2: Gap Assessment")
        client_profile: Description of the client for context
        api_key: Anthropic API key (falls back to ANTHROPIC_API_KEY env var)

    Returns:
        QualityScore with dimension scores and rationales
    """
    key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        score = QualityScore()
        score.raw_response = "SKIPPED: No ANTHROPIC_API_KEY set"
        score.overall = -1
        return score

    try:
        import anthropic
    except ImportError:
        score = QualityScore()
        score.raw_response = "SKIPPED: anthropic package not installed (pip install anthropic)"
        score.overall = -1
        return score

    prompt = GRADING_PROMPT.format(
        client_profile=client_profile,
        agent_name=agent_name,
        phase=phase,
        output_text=output_text[:15000],  # Truncate to avoid token limits
    )

    client = anthropic.Anthropic(api_key=key)
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = response.content[0].text
    score = QualityScore(raw_response=raw)

    try:
        data = json.loads(raw)
        score.specificity = data["specificity"]["score"]
        score.micro_contractor = data["micro_contractor"]["score"]
        score.actionability = data["actionability"]["score"]
        score.assessor_readiness = data["assessor_readiness"]["score"]
        score.tone = data["tone"]["score"]
        score.overall = data["overall"]["score"]
        score.critical_issues = data.get("critical_issues", [])
        score.rationales = {
            k: data[k]["rationale"]
            for k in ("specificity", "micro_contractor", "actionability", "assessor_readiness", "tone", "overall")
        }
    except (json.JSONDecodeError, KeyError) as e:
        score.raw_response = f"Parse error: {e}\nRaw: {raw}"
        score.overall = -1

    return score
