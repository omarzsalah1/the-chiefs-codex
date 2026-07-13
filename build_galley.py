#!/usr/bin/env python3
"""Rebuild THE_CHAMBERLAINS_CIPHER_COMPLETE.md (the 'cake') from ingredients.
Rule: 00_FRONT_MATTER.md + Ch01..Ch19 (sorted), each rstripped, joined with
four newlines (three blank lines), single trailing newline. The galley is
DERIVED — never hand-edit it; regenerate with this script after ingredient edits.
Run from inside 'Medieval Italian Codex/'."""
import glob, io, hashlib
parts = ["00_FRONT_MATTER.md"] + sorted(glob.glob("Ch[0-9][0-9]_*.md"))
assert len(parts) == 20, parts
texts = [io.open(p, encoding="utf-8").read().rstrip() for p in parts]
galley = "\n\n\n\n".join(texts) + "\n"
io.open("THE_CHAMBERLAINS_CIPHER_COMPLETE.md", "w", encoding="utf-8").write(galley)
print(len(galley.split()), "words,", hashlib.sha256(galley.encode()).hexdigest()[:12])
