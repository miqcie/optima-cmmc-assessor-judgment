import csv, yaml, json
W = yaml.safe_load(open("bundle/reference/nist_800_171_controls_sprs_weights.yaml"))["controls"]
gm = [r for r in csv.DictReader(open("bundle/marlin_diligence/Appendix_A_SSP_Gap_Matrix.csv")) if r["Control ID"].startswith("3.")]
pt = [r for r in csv.DictReader(open("bundle/marlin_diligence/Appendix_D_POAM_Tracker.csv")) if r["NIST Control"].startswith("3.")]
findings = {"max_score_mismatch": [], "partial_credit_on_non_partial_control": [], "dod_recomputed": {}, "poam_issues": []}
ded = 0; not_met = []
for r in gm:
    cid = r["Control ID"]; w = W[cid]["weight"]
    if r["Max Score"].strip() and int(r["Max Score"]) != w:
        findings["max_score_mismatch"].append({"control": cid, "matrix_max": r["Max Score"], "dod_weight": w})
    cur = r["Current Score"].strip()
    fully = (cur.isdigit() and int(cur) == int(r["Max Score"]))
    if not fully:
        not_met.append(cid)
        d = 3 if (cid in ("3.5.3", "3.13.11") and cur == "Partial") else w
        ded += d
        if cur not in ("0", "") and cid not in ("3.5.3", "3.13.11"):
            findings["partial_credit_on_non_partial_control"].append({"control": cid, "matrix_current": cur, "dod_treatment": f"NOT MET, full {w}-point deduction"})
findings["dod_recomputed"] = {"controls_listed_in_matrix": len(gm), "controls_not_fully_met": len(not_met),
    "dod_deduction_for_listed_gaps": ded, "sprs_if_all_unlisted_controls_met": 110 - ded,
    "report_claims_sprs": 76, "report_claims_deductions": 34,
    "note": "Matrix lists only 38 of 110 controls; the report's 76 assumes the other 72 are MET and applies fractional partial credit the DoD methodology does not allow."}
poam_ids = {r["NIST Control"] for r in pt}
for cid in not_met:
    if cid not in poam_ids: findings["poam_issues"].append({"control": cid, "issue": "gap in matrix but absent from POA&M tracker"})
for r in pt:
    cid = r["NIST Control"]; w = W[cid]; pts = r["SPRS Points Lost"].strip()
    if not w["poam_eligible"]: findings["poam_issues"].append({"control": cid, "issue": f"{w['weight']}-point control on POA&M; not POA&M-eligible for conditional status", "tracker_points": pts})
    if pts.lstrip("-").isdigit() and abs(int(pts)) != w["weight"] and cid not in ("3.5.3","3.13.11"):
        findings["poam_issues"].append({"control": cid, "issue": f"tracker shows {pts}, DoD weight is {w['weight']}"})
findings["poam_tracker_points_sum"] = sum(int(r["SPRS Points Lost"]) for r in pt if r["SPRS Points Lost"].lstrip("-").isdigit())
json.dump(findings, open("marlin_findings.json", "w"), indent=1)
print(json.dumps(findings, indent=1))
