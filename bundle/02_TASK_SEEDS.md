# Task seeds

One entry per candidate instance. Every established answer below was recomputed
from `reference/nist_800_171_controls_sprs_weights.yaml` with a script during
staging, not typed by hand. Conventions: "DoD-conservative" means every
INSUFFICIENT INFO control is treated as NOT MET, which is the posture required
before posting to SPRS. "As-stated" is the fixture author's own number.

## A. SPRS arithmetic and POA&M eligibility

### A1. Worst case and bucket counts
- Input: `fixtures/all_110_not_met.json`, `reference/nist_800_171_controls_sprs_weights.yaml`
- Answer: SPRS -203. 44 five-point controls, 14 three-point, 51 one-point, 1 zero-point (3.12.4). Of the 51 one-point controls, 46 are POA&M eligible and 5 are excluded: 3.1.20, 3.1.22, 3.10.3, 3.10.4, 3.10.5.
- Evidence: `expected` block in the fixture; header comment of the weights YAML.
- Near-misses seen: worst score given as 0; "all 1-point controls are POA&M eligible"; 3.12.4 counted as 1 point.

### A2. The partial-credit pair
- Input: a register where 3.5.3 is PARTIAL (MFA on privileged and remote only) and 3.13.11 is PARTIAL (encryption present, not FIPS validated), everything else MET.
- Answer: score 104. Each deducts 3, not 5. 3.13.11 may go on the POA&M; 3.5.3 may not. Conditional status is not reachable while 3.5.3 is PARTIAL.
- Evidence: `partial_credit` blocks at 3.5.3 and 3.13.11 in the weights YAML (`poam_if_partial: false` vs `true`); `POAM_SPECIAL_PARTIAL` in `reference/cmmc_register_rules.py`.
- Near-misses: treating both the same; deducting 5 for either; putting 3.5.3 on the POA&M.

### A3. Zero-point blocker and the 3-to-1 override
- Input: everything MET except 3.12.4 NOT MET; separately, everything MET except 3.1.4 NOT MET.
- Answer: 3.12.4 case scores 110 and conditional status is still blocked (not eligible, no SSP). 3.1.4 case scores 109 and is POA&M eligible; 3.1.4 is a 1-point control by DoD override even though it sits in a 3-point bucket.
- Evidence: `weight_note` on 3.1.4 and `poam_note` on 3.12.4 in the weights YAML.

### A4. Partial assessment with unknowns (Acme Biomaterials)
- Input: `fixtures/sample_gap_assessment.json` (states SPRS 73)
- Answer: 15 gap controls. As-stated 73 excludes two INSUFFICIENT INFO controls (3.1.16, 3.1.17, 5 points each). DoD-conservative score is 63. POA&M-eligible deductions: 7 points (3.1.6, 3.1.7, 3.1.8, 3.1.9 at 1 each, 3.13.11 PARTIAL at 3). Blockers: 40 points, including 3.1.20 (1-point but excluded) and 3.5.3 PARTIAL (3 points, not eligible). Conditional status is not reachable under either convention.
- Evidence: control list in the fixture; recomputed during staging.
- Near-miss: accepting 73 without stating what was done with the unknowns.

### A5. Full assessment with POA&M (chain scenario)
- Input: `fixtures/chain_scenario_biotech.json` (states SPRS 67; 20 POA&M entries; conditional date 2026-05-15)
- Answer: 71 MET, 28 NOT MET, 9 INSUFFICIENT INFO, 2 PARTIAL. As-stated 67 excludes the 9 unknowns (37 points); DoD-conservative is 30. POA&M deductions total 22, all on eligible controls including 3.13.11 PARTIAL. Score with POA&M items removed: 89 as-stated (meets the 88 floor), 52 conservative (does not). The correct determination is that conditional status depends on resolving the 9 unknowns first.
- Evidence: `_comment` in the fixture; `stated_sprs_score`; recomputed during staging.
- Clean aspect: the 20 POA&M entries are all valid. A model that "finds" an ineligible one is wrong.

### A6. POA&M entry validity
- Input: `fixtures/sample_poam.json` (conditional date 2026-06-01)
- Answer: valid: 3.1.8 (1-point, eligible, due 2026-07-15) and 3.13.11 PARTIAL (eligible, due 2026-07-30). Invalid: 3.3.1 (5-point), 3.7.1 (3-point), 3.1.20 (1-point but excluded). All five dates fall within 180 days of 2026-06-01 (deadline 2026-11-28), so feasibility is not the defect.
- Evidence: `is_poam_eligible` in `reference/cmmc_register_rules.py`.
- Near-miss: rejecting 3.13.11 because it is a 5-point control; flagging dates.

### A7. Real-shaped register (Tidewater Biologics, stand-in)
- Input: `standin_org/tidewater_control_register.yaml`, `standin_org/tidewater_org_profile.md`
- Answer: SPRS -150. 15 MET, 2 N/A, 4 PARTIAL, 89 NOT MET. 260 points deducted. POA&M-eligible: 40 controls, 42 points. Blockers: 53 controls, 218 points. 3.1.1 and 3.1.2 PARTIAL deduct the full 5 each. 3.13.11 PARTIAL deducts 3 and is eligible. 3.12.4 PARTIAL deducts 0 and blocks. If 3.12.2 were NOT MET the score would be -153.
- Evidence: recomputed during staging; the 3.12.2 reclassification and the -153 to -150 move are recorded in `standin_org/tidewater_judgment_log.yaml` (sprs-sign-off gate).
- Near-misses: giving partial credit on 3.1.1 and 3.1.2; treating the N/A controls as deductions; reporting a percentage.

## B. Auditing another assessor's work (Marlin package)

### B1. Max Score column versus DoD weights
- Input: `marlin_diligence/Appendix_A_SSP_Gap_Matrix.xlsx`, weights YAML
- Answer: 10 rows carry a Max Score that disagrees with the DoD weight: 3.1.3 (5 vs 1), 3.5.6 (5 vs 1), 3.8.9 (3 vs 1), 3.1.5 (5 vs 3), 3.3.2 (5 vs 3), 3.5.7 (5 vs 1), 3.5.8 (5 vs 1), 3.5.9 (5 vs 1), 3.7.1 (5 vs 3), 3.11.1 (5 vs 3). The other 28 control rows have the correct weight.
- Evidence: recomputed during staging.
- Clean rows to leave alone: 3.5.3, 3.1.18, 3.1.19, 3.1.1, 3.1.2, 3.1.16, 3.1.17, 3.3.1, 3.4.2, 3.6.2, 3.13.5, 3.14.1, 3.14.2, 3.14.4 and others with Max Score equal to the DoD weight.

### B2. Fractional and "Partial" credit
- Input: same matrix
- Answer: 14 rows award credit the methodology does not allow. Six are marked "Partial" (3.1.3, 3.5.6, 3.8.1, 3.8.3, 3.8.9, 3.4.7); eight carry 4 of 5 or 3 of 5 (3.1.12, 3.4.1, 3.5.2, 3.6.1, 3.11.1, 3.12.1, 3.13.1, 3.14.6). Each is NOT MET with a full deduction. Only 3.5.3 and 3.13.11 could ever be partial, and 3.5.3 here is 0 of 5, which is correct.
- Evidence: recomputed during staging.

### B3. Recomputing the score
- Input: matrix plus the report's claim of "SPRS 76, 69% compliant, 34 points short"
- Answer: the matrix lists 38 controls. Under DoD rules those 38 alone carry 67 points of deductions (17 controls not fully met). If every unlisted control is MET, the score is 43, not 76. The report's 76 comes from fractional credit and wrong weights. "Percent compliant" is not a DoD concept.
- Evidence: report section 2.2; recomputed during staging.

### B4. Is the CRITICAL finding scored right?
- Input: report section 2.3 and the matrix
- Answer: yes. 3.5.3 at 0 of 5 with "SPRS Impact: -5" is correct. This is a clean instance; a model that disputes it is wrong.

### B5. POA&M tracker arithmetic
- Input: `marlin_diligence/Appendix_D_POAM_Tracker.xlsx`, the report
- Answer: the 17 control rows sum to 35 points; the report claims a 34-point gap. The CRITICAL 3.5.3 gap and the 3.1.12 gap appear in the matrix but not in the tracker.
- Evidence: recomputed during staging.

### B6. POA&M eligibility of the tracker
- Input: same
- Answer: 14 of 17 rows are on controls that are not POA&M eligible for conditional status. Thirteen are 5-point or 3-point controls (3.1.18, 3.1.19, 3.4.7, 3.8.1, 3.8.3, 3.5.2, 3.6.1, 3.11.1, 3.12.1, 3.13.1, 3.14.6, 3.4.1, 3.3.1). One is 3.1.20, a 1-point control on the exclusion list. The three eligible rows are 3.1.3, 3.5.6, and 3.8.9, all 1-point controls; two of those three carry the wrong point value in the tracker.
- Evidence: recomputed during staging.

### B7. Point values in the tracker
- Input: same
- Answer: 13 of 17 rows show a point value that is not the DoD weight, for example 3.1.3 shown as -5 (weight 1), 3.4.7 as -3 (weight 5), 3.3.1 as -1 (weight 5), 3.5.2 as -1 (weight 5), 3.8.1 as -1 (weight 3). The four correct rows are 3.1.18 (-5), 3.1.19 (-3), 3.8.9 (-1), and 3.1.20 (-1). Leave those alone.
- Evidence: recomputed during staging.

## C. SSP narrative review

### C1. Six narratives, three defective
- Input: `fixtures/sample_ssp_narratives.json`, all six attached unlabeled, one determination per control. This single task covers both the clean and the defective cases; do not split it into a "validate the good ones" task, which would label the answer.
- Answer: 3.1.1, 3.5.3, 3.10.1 are assessor-ready: named person, named system, review cadence with dates, evidence IDs in E-XX-NNN form. 3.3.1 is marked MET but written in future tense ("will implement", "plans to deploy"); determination NOT MET. 3.6.1 is marked MET but is the NIST requirement text restated with no organization-specific implementation; NOT MET. 3.8.1 is N/A with the narrative "Not applicable." and no basis; N/A rejected.
- Evidence: `_comment` in the fixture; rules in `reference/ssp_narrative_rules.py`.
- Near-miss: accepting 3.6.1 because it sounds authoritative.

### C2. Client-specific or templated?
- Input: `fixtures/multi_client_scenarios.json`
- Answer: each client's five narratives name that client's stack (Acme Biotech: M365, Entra, Virtru; Atlas Manufacturing: AD, GPO, Palo Alto, Meraki; Nimbus Software: Okta, AWS GovCloud, CrowdStrike). Task shape: given one narrative with the client name stripped, name the client and say why. Or: given two narratives for the same control, say whether one was templated from the other.
- Evidence: fixture; the 0.5 Jaccard rule in our test suite.

### C3. Narratives inside the chain scenario
- Input: `ssp_narratives` in `fixtures/chain_scenario_biotech.json`
- Answer: five narratives that pass the deterministic checks. Use as clean instances against C1.

### C4. Write one, then grade it
- Input: `standin_org/tidewater_org_profile.md`; ask for a MET narrative for 3.5.3 and an N/A narrative for 3.1.18
- Answer: graded by `reference/narrative_quality_judge_prompt.py` dimensions and the five-element structure. The 3.1.18 narrative must cite the 2026-03-19 policy and a technical enforcement, not just "we do not use phones". Micro-contractor fit: Google Workspace settings, no enterprise tools.
- Evidence: ssp-boundary-review gate in the judgment log.

## D. Scoping and intake judgment

### D1 to D4. Adversarial intakes
- Input: `fixtures/adversarial_intakes.json`, one scenario each: OceanTech Instruments (university spinout), Precision Coatings (3 people), Meridian Analytics (cloud-only), Hawkeye Defense Systems (ITAR plus CUI)
- Answer: the `expected_agent_flags` list in each scenario. Highlights: grant-versus-contract instrument check and shared university network for OceanTech; "do not recommend SIEM or SOC" and consumer router with no FIPS crypto for Precision Coatings; Salesforce explicitly out of scope and subcontract flow-down from the prime for Meridian; ITAR incident reporting to DDTC separate from DFARS 7012, and permanent residents may access CUI Basic but not ITAR technical data for Hawkeye.
- Evidence: labeled in the fixture.

### D5. Instrument type
- Input: `standin_org/tidewater_org_profile.md` with the award section reduced to "ONR BAA-derived award N0001426C0417, team believes it is a grant"
- Answer: treat as a contract until the award document says otherwise; the N00014-series number is a Navy contract format; DFARS 7012 and 7021 flow down; CMMC Level 2 applies. Do not scope the engagement on the team's belief.
- Evidence: cui-determination gate in the judgment log (agent proposed "treat as grant", overridden).

### D6. Non-US person on staff
- Input: profile
- Answer: not a disqualifier. CUI access is limited to the CEO by organizational unit and policy; log an export-control follow-up. Engagement is viable.
- Evidence: engagement-viability gate.

### D7. The deliverable is the evidence
- Input: Tidewater register with 3.12.2 NOT MET and a note that a POA&M was produced in the engagement
- Answer: 3.12.2 is MET at delivery; score moves -153 to -150. Check the other CA-family controls for the same pattern (3.12.1, 3.12.3 remain NOT MET; 3.12.4 PARTIAL until the SSP is final).
- Evidence: sprs-sign-off gate.

## E. Recall calibration

- Input: `calibration/nathan_maine_cmmc_benchmark_v3_slice.jsonl`, 13 rows
- Answer: the `expected_answer` field where present, else the `expected_keywords` list. Verified during staging: 180-day POA&M closeout; three-year certification with annual affirmation; CMMC did not replace 800-171; required level follows information type, not contractor status; 3.14.2 requires malicious-code protection on servers in the enclave, not only workstations.
- Purpose: a model that scores well here and poorly on A and B is the finding.
