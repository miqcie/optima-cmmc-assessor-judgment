import zipfile, pathlib, re
here = pathlib.Path(__file__).resolve().parent
src = here.parent / "bundle"
out = here.parent / "dist" / "optima-cmmc-assessor-judgment.zip"
# identifiers to refuse live in gitignored local/identifiers.txt (see local/README.md)
terms = [t.strip() for t in (here.parent / "local/identifiers.txt").read_text().splitlines() if t.strip()]
bad = re.compile("|".join(terms), re.I)
files = sorted(p for p in src.rglob("*") if p.is_file()
               and not any(part.startswith(".") or part == "__pycache__" for part in p.relative_to(src).parts))
leaks = [str(p) for p in files if p.suffix in (".md", ".yaml", ".json", ".jsonl", ".csv", ".py") and bad.search(p.read_text(errors="ignore"))]
assert not leaks, f"real identifiers found: {leaks}"
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for p in files:
        z.write(p, p.relative_to(src).as_posix())
    z.comment = b"optima eval_type=document_input name=CMMC Assessor Judgment"
print(f"wrote {out} ({out.stat().st_size / 1024:.0f} KB, {len(files)} files)")
