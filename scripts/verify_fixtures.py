import json, sys, yaml
sys.path.insert(0, "bundle/reference")
import cmmc_register_rules as reg
F = "bundle/fixtures/"
def ded(cid, st):
    st = st.replace(" ", "_").upper()
    if st in ("MET", "N/A", "NOT_APPLICABLE"): return 0
    if st == "PARTIAL" and cid in ("3.5.3", "3.13.11"): return 3
    return reg.get_control_weight(cid)
g = json.load(open(F+"sample_gap_assessment.json"))
ctr = g["controls"]; ctr = ctr if isinstance(ctr, list) else [dict(control_id=k, **v) for k, v in ctr.items()]
d = sum(ded(c["control_id"], c["status"]) for c in ctr)
print("sample_gap_assessment: stated", g["stated_sprs_score"], "| recomputed", 110 - d, "| controls listed", len(ctr))
print("   gap controls:", [(c["control_id"], c["status"], ded(c["control_id"], c["status"])) for c in ctr if ded(c["control_id"], c["status"])])
ch = json.load(open(F+"chain_scenario_biotech.json"))
gc = ch["gap_assessment"]["controls"]; gc = gc if isinstance(gc, list) else [dict(control_id=k, **v) for k, v in gc.items()]
d2 = sum(ded(c["control_id"], c["status"]) for c in gc)
pids = {e["control_id"] for e in ch["poam_entries"]}
pd = sum(ded(c["control_id"], c["status"]) for c in gc if c["control_id"] in pids)
print("chain: stated", ch["gap_assessment"].get("stated_sprs_score") or ch["gap_assessment"].get("sprs_score"), "| recomputed", 110 - d2, "| poam pts", pd, "| score w/o poam", 110 - (d2 - pd), "| ineligible on poam:", [c for c in pids if not reg.is_poam_eligible(c, "NOT MET")])
p = json.load(open(F+"sample_poam.json"))
print("sample_poam: conditional date", p["conditional_status_date"])
for e in p["entries"]:
    cid = e["control_id"]; st = e.get("status", "NOT MET")
    print(f"   {cid:8} weight={reg.get_control_weight(cid)} eligible={reg.is_poam_eligible(cid, st)} completion={e.get('completion_date') or e.get('scheduled_completion')} note={e.get('_note') or e.get('_test_note') or ''} keys={[k for k in e if k.startswith('_')]}")
print("register constants:", reg.SPRS_PASSING_THRESHOLD, reg.POAM_MAX_DEDUCTION_POINTS, reg.POAM_CLOSEOUT_DAYS)
