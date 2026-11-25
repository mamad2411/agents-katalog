---
name: ma-laws
description: Use when an agent needs to look up, quote, search, summarize, cite, or reason from the Massachusetts Constitution, Massachusetts General Laws, or Massachusetts Rules of Civil Procedure.
---

# Massachusetts Laws

Use this skill for Massachusetts constitutional, statutory, and civil-procedure research. The Constitution and statutes are generated from the official Massachusetts General Court website. The civil rules are generated from the Massachusetts Trial Court Law Libraries' individual Mass.gov rule pages.

On the first lookup, `read_section.py` resolves the latest Massachusetts release, downloads its corpus from DocketDrafter's public S3 bucket, verifies its SHA-256 checksum, and installs it under `~/Documents/DocketDrafter Library/corpora/ma-laws/`. Subsequent research is local and works offline. Set `DOCKETDRAFTER_DATA_DIR` to use a different library directory.

## Lookup

```bash
python scripts/read_section.py "Mass. Gen. Laws ch. 93A, § 2"
python scripts/read_section.py "M.G.L. c. 260, § 2A"
python scripts/read_section.py "Chapter 149, Section 148"
python scripts/read_section.py "Mass. R. Civ. P. 12"
python scripts/read_section.py "Massachusetts Rule of Civil Procedure 56"
python scripts/read_section.py "Mass. Const. pt. 1, art. 10"
python scripts/read_section.py "Mass. Const. pt. 2, ch. 1, § 1, art. 1"
python scripts/read_section.py "Mass. Const. amend. art. 97"
python scripts/read_section.py "Mass. Const. pmbl."
python scripts/read_section.py --search "public records" --limit 20
python scripts/read_section.py --list-chapter 93A
python scripts/read_section.py --list-rules
python scripts/read_section.py --list-constitution
```

Use `--format json` or `--format markdown` for structured output, and `--max-bytes N` to limit displayed text. Lookup and search results include links to the official section pages.

Always use `scripts/read_section.py` for research. Search covers the Constitution, statutes, and civil rules, including Reporter's Notes. Constitutional lookups distinguish the Declaration of Rights (`pt. 1`), the frame of government (`pt. 2`), and articles of amendment (`amend. art.`). Treat each source as current only as of its retrieval timestamp in `references/index.json`, and consult the linked official page when source authority or very recent amendments matter. The Trial Court Law Libraries caution that their online rules are not an official source.

Sources:

- https://malegislature.gov/Laws/Constitution
- https://malegislature.gov/Laws/GeneralLaws
- https://www.mass.gov/law-library/massachusetts-rules-of-civil-procedure
