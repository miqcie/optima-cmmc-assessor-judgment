#!/bin/sh
# Rebuild bundle/ and dist/optima-cmmc-assessor-judgment.zip from sources.
# Needs: ~/GitHub/eagle-ridge-methodology, uv, HF_TOKEN (op read 'op://Developer Vault/Hugging Face MCP/credential').
set -e
cd "$(dirname "$0")"
sh scripts/stage.sh
uv run --with pyyaml,openpyxl python -I scripts/gen_standin.py
uv run --with pyyaml,openpyxl python -I scripts/finalize_marlin.py
[ -n "$HF_TOKEN" ] && python3 -I scripts/calibration.py || echo "HF_TOKEN unset: keeping committed calibration slice"
python3 -I scripts/package.py
python3 ~/.claude/skills/optima-eval-prep/scripts/check_bundle.py dist/optima-cmmc-assessor-judgment.zip
