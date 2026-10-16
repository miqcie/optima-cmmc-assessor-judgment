# local/ (gitignored)

Private inputs the build needs. Never committed.

- `source_register.path`: one line, path to the real control register the stand-in org is generated from.
- `scrub.sed`: sed script that replaces real names in fixtures before packaging.
- `identifiers.txt`: one regex term per line; `package.py` refuses to zip if any term appears in the bundle.
