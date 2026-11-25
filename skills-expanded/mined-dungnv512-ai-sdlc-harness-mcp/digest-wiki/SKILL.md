---
name: digest-wiki
description: Synthesizes multiple existing docs/wiki/**/*.md artifacts into a new cross-source digest, written directly into docs/wiki/ as a schema-valid artifact with origin:derived. Use when the user asks for a deep dive, comparison, timeline, or structured synthesis across topics already compiled in wiki.
---

# Digest Wiki Skill

Deep cross-source synthesis over the compiled `docs/wiki/` layer, producing a new
`docs/wiki/**/*.md` artifact. This is a rewrite for stockbookapp: the mother
repo's version stored synthesized articles externally. This version writes
them to disk as plain markdown files, and provenance is recorded as an `upstream_refs`
list (empty, see step 4) plus an in-body "Synthesized from" section.

## When to Use

- "Deep dive into X"
- "Synthesize everything about X across the wiki"
- "Compare A and B"
- "Create a timeline of X"
- User explicitly wants a new, saved artifact — not just a conversational
  answer (that's `query-wiki`)

## Where the new file goes — no staging directory

Team members write these directly into `docs/wiki/<topic>/`, the same tree
`bin/ingest-confluence.sh`/`bin/ingest-jira.sh` compiled artifacts live in.
This is a deliberate decision, not an oversight: there is **no** staging or
draft directory for digests, and there will not be one added. If two people
digest overlapping ground and their files collide or disagree, that is
accepted and resolved by whoever caused it (usual `docs/wiki/` conventions: git
history + `docs/wiki/log.md` say who wrote what and when) — do not invent a
review queue this skill was explicitly told not to have.

## Steps

### 1. Identify source artifacts (confirm scope with the user)

```bash
grep -n -i "<topic>" wiki/index.md
grep -rli "<topic>" wiki/**/*.md
```

List every artifact you intend to synthesize from before writing anything,
and get the user to confirm the list is right — a digest silently built
from the wrong subset is worse than asking once.

### 2. Read all of them in full

Read each artifact's frontmatter (for `artifact_id`, `upstream_refs`,
`sources`) and body. For anything unusually large, skim the headings first,
then read the sections actually relevant to the digest.

### 3. Pick a structure

- **Deep dive** (default) — Background, Core Findings, Different
  Perspectives (if sources disagree), Knowledge Gaps, Sources
- **Comparison** ("compare X and Y") — a side-by-side table plus a verdict
- **Timeline** ("timeline of X") — chronological, dated from each source
  artifact's own `last_updated` / body dates

Every claim in the digest carries a confidence marker (see `query-wiki`
step 4 for the four values) — default to `INFERRED` unless the source
artifact states the fact directly (`EXTRACTED`), sources disagree
(`AMBIGUOUS`), or it's your own outside knowledge (`UNVERIFIED`, use
sparingly).

### 4. Write the frontmatter — `origin: derived`, schema-valid

This is the one part of the compiled `docs/wiki/` frontmatter shape that departs
from every artifact written before this skill existed: it adds an
`origin: derived` field (the same `origin` vocabulary raw/SCHEMA.md defines
for `docs/raw/` — task #4) to say, in the same self-documenting place every other
file already documents its origin, "this file has no single upstream page."
`bin/validate-frontmatter.py` does not currently run over `docs/wiki/` (only
`docs/raw/`) so it will not check this field yet — write it anyway, both because
it is the correct, forward-compatible value for a future wiki validator, and
because it saves the next person from re-deriving "why does this one wiki
file have no sources" from scratch.

```yaml
---
artifact_id: WIKI-DERIVED-<TOPIC-SLUG>-001   # increment -NNN if this slug already exists
artifact_type: digest
project_id: stockbook
origin: derived
status: compiled
created_date: '<YYYY-MM-DD>'
last_updated: '<YYYY-MM-DD>'
role: <your role, e.g. project-ba>
topic:
  - <topic keywords, same convention as other wiki/**/*.md files>
sources: []          # no single upstream page/issue -- see upstream_refs below
evidence_mode: quoted
confidence_markers:
  - EXTRACTED
  - INFERRED
upstream_refs: []    # deliberately empty -- see "why empty" below
---
```

**Why `upstream_refs: []` (not omitted, not filled in with the sources you
digested from):** `bin/generate-wiki-index.py` computes an artifact's
staleness display purely by walking its `upstream_refs` against
`sources.json` and counting how many resolve to `current`/`stale`/`unknown`.
An empty list makes that walk a no-op, so the generator renders "staleness:
no linked sources" and "upstream: (no linkable source in frontmatter)" for
this artifact — which is the correct, honest statement for a digest (it has
no single page whose version could go stale) and is what "correctly skipped
by stale-checking" means in practice. Putting the *source artifacts'*
`upstream_refs` here instead would be wrong: it would make this digest look
falsely stale/current based on pages it didn't fetch from directly, and
`bin/check-staleness.sh` would start hitting those pages' APIs on this
digest's behalf for no reason.

Provenance of what the digest *was* synthesized from is recorded in the
body instead (step 5's "Synthesized from" section) — human-readable, and
not consumed by any staleness or validation script, so it can't drift into
a false signal the way an `upstream_refs` entry would.

### 5. Write the body

Standard sections from step 3, plus a mandatory closing section:

```markdown
## Synthesized from

- [WIKI-SN-AUTH-001](../auth/auth-overview.md) — Auth: Đăng nhập & Đăng ký
- [WIKI-SN-VERIFICATION-001](../verification/verification-overview.md) — Verification
```

Link relative to the new file's own directory (same convention
`bin/check-links.sh` already enforces across `docs/wiki/`).

### 6. Append to `docs/wiki/log.md`

`bin/generate-wiki-index.py` regenerates `docs/wiki/index.md` wholesale from
frontmatter and will pick up the new artifact automatically next run, but
`docs/wiki/log.md`'s per-change history is hand-maintained and out of that
generator's scope — add one line yourself, same table format as the
existing entries:

```
| <YYYY-MM-DD> | <topic-dir> | WIKI-DERIVED-<TOPIC-SLUG>-001 | Digest: <one-line description> (synthesized from N artifacts, no upstream refs) | new digest |
```

### 7. Regenerate the index (optional but recommended)

```bash
python3 -sS bin/generate-wiki-index.py
```

Confirms the new artifact renders as expected (staleness: "no linked
sources") before handing off.
