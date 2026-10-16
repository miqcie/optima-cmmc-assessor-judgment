"""Fetch Nathan Maine's CMMC benchmark v3 (gated, CC-BY-4.0) and write the fixed-seed
calibration slice. Needs HF_TOKEN in the environment and the dataset gate accepted."""
import json, os, random, urllib.request, pathlib
S = pathlib.Path(__file__).resolve().parent.parent / "bundle" / "calibration"
DS = "Nathan-Maine%2Fcmmc-benchmark-v3-comprehensive-2026-q2"
H = {"Authorization": "Bearer " + os.environ["HF_TOKEN"]}
rows, off = [], 0
while True:
    u = f"https://datasets-server.huggingface.co/rows?dataset={DS}&config=default&split=test&offset={off}&length=100"
    d = json.loads(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=60).read())
    rows += [r["row"] for r in d["rows"]]
    if len(rows) >= d["num_rows_total"] or not d["rows"]: break
    off += 100
random.seed(20260910)
want = {"Assessment Determination": 5, "Threshold Testing": 2, "Hallucination and Boundary": 3, "Adversarial Gap Analysis": 2,
        "Trick Regulatory": 2, "Evidence Sufficiency": 2, "Factual Recall": 2}
# dropped after hand review: hedged or methodology-contradicting keys (see ATTRIBUTION.md)
drop = {"T12-Q12", "T12-Q17", "T12-Q18", "T12-Q20", "T12-Q30"}
out = []
for cat, n in want.items():
    pool = [r for r in rows if r["category"] == cat and r.get("expected_answer")]
    if len(pool) < n: pool = [r for r in rows if r["category"] == cat]
    for r in random.sample(pool, n):
        if r["id"] in drop: continue
        keep = {k: v for k, v in r.items() if v not in (None, [], "")}
        keep["source"] = "Nathan-Maine/cmmc-benchmark-v3-comprehensive-2026-q2 (HuggingFace, CC-BY-4.0)"
        out.append(keep)
assert [r["id"] for r in out] == ['T12-Q29','T1-Q132','T1-Q142','T7-Q46','T7-Q74','T7-Q33','T4-Q81','T4-Q86','T9-Q86','T9-Q100','T12-Q03','T1-Q51','T1-Q89'], [r["id"] for r in out]
(S / "nathan_maine_cmmc_benchmark_v3_slice.jsonl").write_text("".join(json.dumps(r) + "\n" for r in out))
(S / "ATTRIBUTION.md").write_text(f"""# Calibration slice attribution

Source: Nathan Maine, "CMMC Benchmark v3 Comprehensive, Q2 2026", HuggingFace dataset
`Nathan-Maine/cmmc-benchmark-v3-comprehensive-2026-q2`, 1,274 questions, CC-BY-4.0.
Gated (auto-approved) behind a no-training acknowledgement. Used here for evaluation only.

This slice: {len(out)} questions sampled with a fixed seed across seven of its categories, then
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
""")
print(len(out), "calibration rows written")
