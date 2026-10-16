# Calibration slice attribution

Source: Nathan Maine, "CMMC Benchmark v3 Comprehensive, Q2 2026", HuggingFace dataset
`Nathan-Maine/cmmc-benchmark-v3-comprehensive-2026-q2`, 1,274 questions, CC-BY-4.0.
Gated (auto-approved) behind a no-training acknowledgement. Used here for evaluation only.

This slice: 13 questions sampled with a fixed seed across seven of its categories, then
reviewed by hand. They are recall and single-fact items graded by keyword list or a short
expected answer, with no attached documents. They are a calibration control, not the core of
this benchmark. The finding we want to expose is a model that scores well here and then fails
the document-grounded scoring and eligibility tasks in the rest of the bundle.

Grading note: the source's `expected_keywords` are substring checks. Prefer `expected_answer`
where present.

Rows removed during review (kept out so the key never contradicts the DoD methodology):
- T12-Q12: key calls a BitLocker key-management gap "PARTIAL COMPLIANCE". Under the DoD
  Assessment Methodology only 3.5.3 and 3.13.11 carry partial credit; SC.L2-3.13.16 is MET or NOT MET.
- T12-Q17, T12-Q18, T12-Q20, T12-Q30: keys are hedged ("MET or NOT APPLICABLE", "requires
  careful assessment", "generally out of scope"), so a grader cannot fix a right answer.

Rows kept were checked against NIST SP 800-171 Rev 2, 32 CFR 170, and the DoD Assessment
Methodology v1.2.1 during staging: the 180-day POA&M closeout, the three-year certification
with annual affirmation, the CMMC-does-not-replace-800-171 point, and the Level-by-information
rule all match those sources.
