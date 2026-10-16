# Sources manifest

Provenance key: REAL = used as-is from our repo; REDACTED = real with identifiers changed; GENERATED = written for this bundle; ANONYMIZED = real deal run through a tested anonymization pipeline; PUBLIC = third-party, licensed.

## reference/

| Path | What it is | Provenance | Notice |
|---|---|---|---|
| `reference/nist_800_171_controls_sprs_weights.yaml` | All 110 NIST SP 800-171 Rev 2 controls with title, family, DoD weight (5/3/1/0), POA&M eligibility, override notes. | REAL | The scoring authority for every task. 44 five-point, 14 three-point, 51 one-point, 1 zero-point. `weight_note` and `poam_note` fields mark the traps (3.1.4, 3.12.4, the five excluded 1-point controls). |
| `reference/cmmc_register_rules.py` | Python view of the same rules: `get_control_weight`, `is_poam_eligible`, partial-credit specials, thresholds 88 / 22 / 180. | REAL | Path patched so it loads the YAML beside it. Runnable with PyYAML. |
| `reference/ssp_narrative_rules.py` | Deterministic SSP narrative checks: future tense on MET, NIST copy-paste, five-element structure, evidence IDs, N/A justification. | REAL | These are the defects the narrative tasks in seeds C are keyed to. |
| `reference/poam_quality_rules.py` | POA&M entry quality rubric, 8 fields x 0/1/2 = 0-16, plus eligibility and 180-day feasibility. | REAL | Assessment-ready means eligible, 12+/16, feasible. |
| `reference/narrative_quality_judge_prompt.py` | LLM-judge prompt with five 1-5 dimensions: specificity, micro-contractor fit, actionability, assessor readiness, tone. | REAL | Use the anchored descriptors as grading criteria for narrative tasks. |

## fixtures/  (synthetic, built for our test suite)

| Path | What it is | Provenance | Notice |
|---|---|---|---|
| `fixtures/all_110_not_met.json` | Every control NOT MET, plus partial variants and an expected-counts block. | REAL synthetic | Answer key embedded: worst SPRS -203, 44/14/46/5/1 buckets, six excluded IDs. Seed A1. |
| `fixtures/sample_gap_assessment.json` | 45-control partial assessment for "Acme Biomaterials", 5-person biotech. States SPRS 73. | REAL synthetic | Two controls are INSUFFICIENT INFO. The stated 73 excludes them; DoD-conservative posting is 63. Seed A4. |
| `fixtures/chain_scenario_biotech.json` | Full 110-control assessment, 20 POA&M entries, 5 narratives. States SPRS 67. | REAL synthetic | Nine INSUFFICIENT INFO controls (37 points) excluded from the stated score. POA&M points 22. Seeds A5, C3. |
| `fixtures/sample_poam.json` | Five POA&M entries against a conditional-status date of 2026-06-01. | REAL synthetic | Three are ineligible. Seed A6. |
| `fixtures/sample_ssp_narratives.json` | Six SSP narratives, three good and three flawed. | REDACTED | One person's name replaced with "Dr. Priya Raman" during staging. Seed C1. |
| `fixtures/multi_client_scenarios.json` | Three fictional clients (M365 biotech, AD/Palo Alto manufacturer, Okta/AWS software firm), five narratives each. | REAL synthetic | Built to test that narratives are client-specific, not templated. Seed C2. |
| `fixtures/adversarial_intakes.json` | Four intake scenarios with `expected_agent_flags` already labeled. | REAL synthetic | University spinout, 3-person shop, cloud-only, ITAR-mixed. Seeds D1-D4. |

## marlin_diligence/  (anonymized real deal)

| Path | What it is | Provenance | Notice |
|---|---|---|---|
| `marlin_diligence/marlin_cmmc_diligence_report.md` | Buy-side CMMC diligence report on "Meridian Federal Systems" for a PE sponsor: executive summary and sections 1 to 4 (company, compliance assessment, risk, backlog). | ANONYMIZED | Claims SPRS 76 and "69% compliant". Names 3.5.3 as the CRITICAL gap. Dollar figures scaled uniformly; contract numbers offset. Split into three files for the read limit. |
| `marlin_diligence/marlin_cmmc_diligence_report_part2.md` | Sections 5 to 8: cost to cure, roadmap, investor considerations, recommendations. | ANONYMIZED | Context for the audit tasks; no scoring claims beyond section 2. |
| `marlin_diligence/marlin_cmmc_diligence_report_appendices.md` | Appendix narrative text (A to H). The tables themselves are the xlsx files below. | ANONYMIZED | |
| `marlin_diligence/marlin_executive_summary.md` | Executive summary of the same. | ANONYMIZED | |
| `marlin_diligence/Appendix_A_SSP_Gap_Matrix.xlsx` | 38-control gap matrix from the target's prior assessor: Current Score, Max Score, Compliance %. | ANONYMIZED | The audit target. 10 rows have a Max Score that disagrees with the DoD weight; 14 rows award fractional or "Partial" credit on controls with no partial credit. Seeds B1-B4. |
| `marlin_diligence/Appendix_D_POAM_Tracker.xlsx` | 17 POA&M rows plus summary rows. | ANONYMIZED | Points sum to 35 against a claimed 34-point gap; the CRITICAL 3.5.3 gap is absent; 14 of 17 rows are on controls that are not POA&M eligible; 13 carry a point value that is not the DoD weight. Seeds B5-B7. |
| `marlin_diligence/Appendix_B_Contract_Backlog.xlsx`, `Appendix_C_Cost_Model.xlsx`, `Appendix_E_Backlog_Waterfall.xlsx` | Financial appendices. | ANONYMIZED | Context only. Not scoring material; no seeds keyed to them. |

## standin_org/  (generated stand-in for a real engagement)

| Path | What it is | Provenance | Notice |
|---|---|---|---|
| `standin_org/tidewater_org_profile.md` | Three-person biotech, Navy contract, Google Workspace, three laptops, phones excluded. | GENERATED | Mirrors a real engagement's facts with every identifier invented. |
| `standin_org/tidewater_control_register.yaml` | 110-control register with status, justification, tier. | GENERATED from REAL statuses | Statuses are the real engagement's. Recomputed SPRS -150. Seed A7. |
| `standin_org/tidewater_judgment_log.yaml` | Six review gates where the consultant accepted or overrode the AI draft. | GENERATED from REAL decisions | OUTCOME EVIDENCE. Records the right call on instrument type, non-US person, weight audit, N/A for phones, and the 3.12.2 reclassification. Grade against it; do not hand it out as task input. Seeds D5-D7. |

## calibration/  (public benchmark slice)

| Path | What it is | Provenance | Notice |
|---|---|---|---|
| `calibration/nathan_maine_cmmc_benchmark_v3_slice.jsonl` | 13 questions from Nathan Maine's CMMC Benchmark v3 (HuggingFace, CC-BY-4.0). | PUBLIC | Recall and single-fact items. Control group. Seed E. |
| `calibration/ATTRIBUTION.md` | License, sampling method, and the five rows dropped for ambiguous or rule-breaking keys. | GENERATED | |
