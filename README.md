# CMMC Assessor Judgment

A custom benchmark on Artificial Analysis Optima that tests whether a model can do what a
CMMC Level 2 assessor does: score an SPRS, rule on POA&M eligibility, audit another
assessor's gap matrix, reject a defective SSP narrative, and scope an engagement.
No public benchmark covered this before (closest prior art: Nathan Maine's keyword-graded
CMMC benchmark v3 on HuggingFace, which supplies this bundle's recall-calibration slice).

Results (2026-10-15, 36 tasks, 9 models, 1,027 rubric criteria): see `results/`.

| Rank | Model | Mean score | Cost per task |
|---|---|---|---|
| 1 | GPT-6 Astra (medium) | 90% | $0.13 |
| 2 | Claude Fable 5.1 (medium) | 88% | $0.414 |
| 3 | Inkling (xhigh) | 88% | $0.06 |
| 4 | GPT-5.6 Luna (medium) | 82% | $0.0046 |
| 5 | GLM-5.3-Flash | 80% | $0.0025 |
| 9 | Gemma 4 31B | 56% | $0.0011 |

## Layout

- `bundle/` — exactly what was uploaded: brief, sources manifest, task seeds, fixtures, the
  anonymized Marlin diligence package, the Tidewater stand-in org, and the calibration slice.
- `scripts/` — regenerators. Every number in the answer keys is computed from the DoD
  weight file, never typed.
- `build.sh` — rebuilds `bundle/` and `dist/optima-cmmc-assessor-judgment.zip`, then runs
  the Optima bundle checker. Needs `~/GitHub/eagle-ridge-methodology`, `uv`, and `HF_TOKEN`
  for the calibration refetch (the committed slice is kept when the token is unset).
- `results/` — the Optima report PDF.

## Upload

Drop the ZIP on https://artificialanalysis.ai/optima/upload. The evaluation type
(`document_input`) travels in the archive comment. The task-drafting rules in
`bundle/00_BRIEF.md` came from a first build attempt whose prompts leaked the answers.
