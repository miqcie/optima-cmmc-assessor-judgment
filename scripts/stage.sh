#!/bin/sh
# Copy source material from the methodology repo into bundle/. Idempotent.
set -e
R=${METHODOLOGY_REPO:-$HOME/GitHub/eagle-ridge-methodology}
S="$(cd "$(dirname "$0")/.." && pwd)/bundle"
mkdir -p "$S/reference" "$S/fixtures" "$S/marlin_diligence" "$S/calibration" "$S/standin_org"
cp "$R/data/nist-800-171-controls.yaml" "$S/reference/nist_800_171_controls_sprs_weights.yaml"
for f in sample_ssp_narratives sample_poam sample_gap_assessment chain_scenario_biotech adversarial_intakes multi_client_scenarios all_110_not_met; do cp "$R/tests/fixtures/$f.json" "$S/fixtures/"; done
cp "$R"/case-studies/marlin-anonymized/output/Appendix_*.csv "$S/marlin_diligence/"
cp "$R/case-studies/marlin-anonymized/output/MARLIN CMMC Diligence Report.md" "$S/marlin_diligence/marlin_cmmc_diligence_report.md"
cp "$R/case-studies/marlin-anonymized/output/Executive Summary.md" "$S/marlin_diligence/marlin_executive_summary.md"
cp "$R/tests/graders/ssp.py" "$S/reference/ssp_narrative_rules.py"
cp "$R/tests/graders/poam.py" "$S/reference/poam_quality_rules.py"
cp "$R/tests/graders/narrative_quality.py" "$S/reference/narrative_quality_judge_prompt.py"
cp "$R/scripts/cmmc_register.py" "$S/reference/cmmc_register_rules.py"
# real names in fixtures are scrubbed by the gitignored local/scrub.sed; the weights file must sit beside the rules module
sed -i '' -f "$S/../local/scrub.sed" "$S/fixtures/sample_ssp_narratives.json"
sed -i '' 's|^BASE_CONTROLS_PATH = REPO_ROOT / "data" / "nist-800-171-controls.yaml"|BASE_CONTROLS_PATH = Path(__file__).resolve().parent / "nist_800_171_controls_sprs_weights.yaml"  # bundle: weights file sits beside this module|' "$S/reference/cmmc_register_rules.py"
echo "staged into $S"
