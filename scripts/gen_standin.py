"""Generate the fictional stand-in org (Tidewater Biologics) from the real register's
status pattern. Statuses are the ground truth; every identifier is invented.
Self-check: recomputed SPRS must equal the engagement's signed-off figures."""
import yaml, json, pathlib, re
S = pathlib.Path(__file__).resolve().parent.parent / "bundle"
weights = yaml.safe_load(open(S/"reference/nist_800_171_controls_sprs_weights.yaml"))["controls"]
real = yaml.safe_load(open((S.parent/"local/source_register.path").read_text().strip()))["controls"]  # gitignored, see local/README.md
PARTIAL_SPECIAL = {"3.5.3": 3, "3.13.11": 3}

def deduction(cid, status):
    if status in ("MET", "N/A"): return 0
    if status == "PARTIAL" and cid in PARTIAL_SPECIAL: return PARTIAL_SPECIAL[cid]
    return weights[cid]["weight"]

def sprs(reg):
    return 110 - sum(deduction(c, v["status"]) for c, v in reg.items())

# --- ground-truth checks against the signed-off engagement numbers
assert sprs(real) == -150, sprs(real)
alt = {c: dict(v) for c, v in real.items()}; alt["3.12.2"]["status"] = "NOT_MET"
assert sprs(alt) == -153, sprs(alt)

# --- stand-in register: same statuses, reworded justifications, new identity
just = {
 "3.1.1": "Shared lab@ mailbox still enabled; no device authorization for the two lab laptops",
 "3.1.2": "Google Workspace enforces sharing settings but CUI is not labeled and flow is not restricted",
 "3.1.18": "Phones excluded from the CUI boundary by written policy dated 2026-03-19; no phone stores or processes CUI",
 "3.1.19": "Phones excluded from the CUI boundary by written policy dated 2026-03-19; no phone stores or processes CUI",
 "3.12.4": "SSP in draft during this engagement",
 "3.13.11": "Encryption in use but the modules are not FIPS 140-2 validated",
}
standin = {"meta": {
  "client": "Tidewater Biologics LLC",
  "assessment_date": "2026-03-25",
  "version": "0.5",
  "scope_notes": ["Mobile phones excluded from CUI boundary (policy dated 2026-03-19)",
                  "Team chat excluded from CUI boundary via organizational policy"]},
 "controls": {}}
for c, v in real.items():
    e = {"status": v["status"]}
    if c in just: e["justification"] = just[c]
    if "tier" in v: e["tier"] = v["tier"]
    if c == "3.12.2": e["notes"] = "MET: the POA&M produced in this engagement is the artifact that satisfies this control"
    standin["controls"][c] = e
(S/"standin_org").mkdir(exist_ok=True)
yaml.safe_dump(standin, open(S/"standin_org/tidewater_control_register.yaml","w"), sort_keys=False, allow_unicode=True)

# --- answer key for the seeds
rows=[]; blockers=[]; poam=[]
for c, v in standin["controls"].items():
    d = deduction(c, v["status"])
    if d or (v["status"] in ("NOT_MET","PARTIAL")):
        w = weights[c]
        elig = w["poam_eligible"] if not (v["status"]=="PARTIAL" and c in PARTIAL_SPECIAL) else (c=="3.13.11")
        (poam if elig else blockers).append(c)
        rows.append((c, v["status"], d, elig))
key = {"sprs_score": sprs(standin["controls"]), "controls_met": sum(1 for v in standin["controls"].values() if v["status"]=="MET"),
       "controls_na": sum(1 for v in standin["controls"].values() if v["status"]=="N/A"),
       "controls_partial": sum(1 for v in standin["controls"].values() if v["status"]=="PARTIAL"),
       "controls_not_met": sum(1 for v in standin["controls"].values() if v["status"]=="NOT_MET"),
       "total_deductions": 110 - sprs(standin["controls"]),
       "poam_eligible_gap_controls": len(poam), "poam_eligible_points": sum(deduction(c, standin["controls"][c]["status"]) for c in poam),
       "blocker_controls": len(blockers), "blocker_points": sum(deduction(c, standin["controls"][c]["status"]) for c in blockers),
       "conditional_status_reachable_now": False,
       "sprs_if_3_12_2_not_met": sprs(alt)}
json.dump(key, open("standin_answer_key.json","w"), indent=1)
print(json.dumps(key, indent=1))
print("zero-point NOT_MET/PARTIAL rows:", [r for r in rows if r[2]==0])
