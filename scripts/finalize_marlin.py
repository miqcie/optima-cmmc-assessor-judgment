"""Optima reads CSV as flat text and truncates files over 50K chars: convert the Marlin
appendices to xlsx and split the report. Idempotent."""
import csv, pathlib, openpyxl
M = pathlib.Path(__file__).resolve().parent.parent / "bundle" / "marlin_diligence"
for p in sorted(M.glob("Appendix_*.csv")):
    wb = openpyxl.Workbook(); ws = wb.active; ws.title = p.stem[:31]
    for row in csv.reader(open(p, newline="")):
        ws.append([(int(c) if c.lstrip("-").isdigit() else c) for c in row])
    wb.save(p.with_suffix(".xlsx")); p.unlink()
rep = M / "marlin_cmmc_diligence_report.md"; txt = rep.read_text()
if "\n## APPENDICES" in txt:
    i = txt.index("\n## APPENDICES")
    (M / "marlin_cmmc_diligence_report_appendices.md").write_text("# Meridian Federal Systems Due Diligence Report, Appendices (continued from marlin_cmmc_diligence_report.md)\n" + txt[i:])
    txt = txt[:i] + "\n\n(Appendices continue in marlin_cmmc_diligence_report_appendices.md; the tables themselves are the Appendix_*.xlsx files.)\n"
if "\n## 5. COST-TO-CURE" in txt:
    i = txt.index("\n## 5. COST-TO-CURE")
    (M / "marlin_cmmc_diligence_report_part2.md").write_text("# Meridian Federal Systems Due Diligence Report, Part 2: sections 5 to 8 (continued from marlin_cmmc_diligence_report.md)\n" + txt[i:])
    txt = txt[:i] + "\n\n(Sections 5 to 8 continue in marlin_cmmc_diligence_report_part2.md.)\n"
rep.write_text(txt)
for f in sorted(M.glob("*.md")): assert len(f.read_text()) < 50000, f
print("marlin finalized")
