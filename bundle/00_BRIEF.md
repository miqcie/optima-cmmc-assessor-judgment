# Eagle Ridge Advisory helps small defense contractors reach CMMC Level 2 and post a defensible SPRS score

We are a CMMC consultancy for 3-to-50-person contractors. The work is NIST SP
800-171 Rev 2 gap assessment, SPRS scoring under the DoD Assessment
Methodology v1.2.1, POA&M construction, and SSP narrative writing that a
C3PAO assessor would accept. We also do buy-side CMMC diligence for private
equity, which means auditing another assessor's gap matrix and POA&M.

## The task we want measured

The repeating job is assessor judgment on documents. A control register, gap
matrix, POA&M tracker, SSP narrative, or intake transcript arrives. The output
is a written determination with the arithmetic and the rule cited: the SPRS
score, which gaps may go on a POA&M and which block conditional status,
whether a narrative is assessor-ready, and what an intake is hiding.

What makes it hard is that the DoD scoring rules are small, exact, and
counter-intuitive, and models that know the framework still get them wrong:

- 110 controls weighted 5, 3, or 1 point, plus one zero-point control. Worst score is -203, not 0.
- No partial credit except two controls: 3.5.3 (MFA) and 3.13.11 (FIPS crypto) each deduct 3 when PARTIAL. Every other PARTIAL is a full deduction.
- Those two behave differently on the POA&M: 3.13.11 PARTIAL is eligible, 3.5.3 PARTIAL is not.
- 3.12.4 (the SSP) is worth zero points but blocks conditional status when missing.
- 3.1.4 is a 1-point control despite sitting in a 3-point bucket. Five 1-point controls (3.1.20, 3.1.22, 3.10.3, 3.10.4, 3.10.5) are excluded from the POA&M.
- Conditional status needs a score of 88 or more with at most 22 points of POA&M deductions, all on eligible controls, closed within 180 days.
- Unverified controls ("insufficient info") count as NOT MET when posting to SPRS.

## What's attached

- `reference/`: the 110-control weight file (real, verified against the DoD PDF), the scoring and eligibility rules as Python, the SSP narrative rules, the POA&M quality rubric, and the LLM-judge prompt we use for narrative quality. All real, none confidential.
- `fixtures/`: seven synthetic assessment artifacts we built for our own test suite. Real structure, deliberate errors, one name swapped during staging.
- `marlin_diligence/`: a full buy-side diligence package, anonymized from a real deal with a tested anonymization pipeline. The gap matrix and POA&M tracker were produced by the target's prior assessor and contain real scoring mistakes we found during diligence. This is the richest audit material in the bundle.
- `standin_org/`: a generated stand-in for a real three-person biotech engagement. Control statuses are the real ones; every identifier is invented. Includes the judgment log recording where the consultant overrode the AI draft.
- `calibration/`: 13 questions sampled from a public CC-BY-4.0 CMMC recall benchmark, with attribution. A control group, not the core.

## What a good answer looks like

- States the score as an integer, shows the deductions that produced it, and names the rule when the case is a trap. "3.5.3 PARTIAL deducts 3, not 5, and it is not POA&M eligible" is the shape.
- Separates POA&M-eligible gaps from blockers and says whether conditional status is reachable now, with the two numbers that decide it.
- On a gap matrix audit, lists each row that breaks a DoD rule with the rule it breaks, and leaves the correct rows alone.
- On a narrative, gives a determination (MET, NOT MET, N/A defensible or not) and the specific defect: future tense on a MET control, requirement text pasted as implementation, N/A with no policy or technical basis.
- Fits the org. A three-person company gets Google Workspace settings, not a SIEM.

## What a weak answer looks like

- Reports compliance as a percentage or awards fractional credit ("4 of 5 points"). The prior assessor in the Marlin package did this on 14 controls.
- Puts 5-point and 3-point controls on the POA&M and calls the result conditional-eligible.
- Treats 3.5.3 and 3.13.11 the same way because both are 5-point controls with partial credit.
- Misses that 3.12.4 blocks even though it deducts nothing.
- Counts "insufficient info" controls as MET, or does not say which convention it used.
- Accepts a narrative that says "will implement" under a MET status, or one that restates the NIST requirement.
- Marks phones N/A on the owner's say-so with no policy or technical enforcement cited.
- Recommends enterprise tooling to a micro-contractor.

## How this work divides

1. SPRS arithmetic and POA&M eligibility from a register or gap assessment.
2. Auditing another assessor's gap matrix and POA&M tracker against the DoD rules.
3. SSP narrative review: determination and defect.
4. Scoping and intake judgment: what the facts of an org imply for boundary, instrument type, N/A claims, and viability.
5. Recall calibration from the public benchmark.

## The shape of an answer

Plain written text about the attached files. Integers for scores and point
totals, control IDs for anything named, a one-line rule citation for traps.
No files produced.

## Scale

Thirty to forty tasks. The seeds file lists more candidates than that so you
can choose.

## Task drafting rules (learned from a first build attempt)

- Do not put answer-shaped hints in prompts. The benchmark measures whether the model knows a counter-intuitive rule. "Do not assume PARTIAL makes a control POA&M eligible" gives the rule away. Keep format instructions (show arithmetic, cite the rule, one determination per control). Drop any sentence that names the wrong answer, the trap, or the distractor.
- Never label inputs as good or bad. Attach all six narratives in `fixtures/sample_ssp_narratives.json` unlabeled and ask for one determination per control. Do not describe rows as "candidate-good" or "designated clean".
- Audit tasks cover the whole document. "Audit all 38 rows and list every mismatch" works. "Review the rows whose Max Score equals the DoD weight and find mismatches" is circular and finds nothing.
- Include clean instances as false-positive controls, at least four across categories: the 3.5.3 CRITICAL row in the Marlin matrix (scored correctly), the 28 matrix rows with the correct weight, the 20 valid POA&M entries in the chain scenario, the three good narratives. The right answer there is "this is correct" or "all entries are valid", and the grader must reward not inventing an error without the prompt saying so.
- Keep the trap cases as separate tasks: 3.5.3 PARTIAL versus 3.13.11 PARTIAL, 3.12.4 as a zero-point blocker, 3.1.4 as a 1-point override, the five excluded 1-point controls.
- Grade multi-row audit tasks proportionally. A model that finds 12 of 14 flagged rows earns partial credit. Reserve all-or-nothing for single-determination tasks.
- On the two fixtures with INSUFFICIENT INFO controls, accept an answer that states both the as-stated score and the DoD-conservative score and names the conservative one for SPRS posting. Penalize a single number given without saying how unknowns were treated.
- `standin_org/tidewater_judgment_log.yaml` is grading evidence only. Never attach it as a task input and never mention it in a prompt.
- Suggested split for 36 tasks: about 9 SPRS and eligibility, 8 assessor work audit, 7 SSP narrative review, 7 scoping judgment, 5 recall calibration. Keep calibration at 6 or fewer so it stays a control group.
- Tag a "core determination" criterion so the correct-determination rate is reported separately from rationale quality.

## Over to you

Design the benchmark as you see fit. Task count, wording, and grading are
your call. Show me the plan before you build it.
