---
name: scrub
description: Use when incrementally reviewing and repairing low-quality metadata after enrich, especially non-standard documents that need title, author, or year correction while skipping already reviewed records via .scrubbed.
---
# Scrub Metadata

Use this skill when the library contains already-ingested papers whose metadata is still clearly low quality after ingest or enrich, especially for non-standard documents that MinerU or fallback parsers converted successfully but described poorly.

`scrub` is a review-and-repair workflow, not a blind batch rewrite. It should reuse existing ScholarAIO repair and rename primitives, and it should treat `.scrubbed` as the durable marker for "reviewed and currently acceptable."

## When To Use

Use this skill when the user wants to:

- clean bad metadata after enrich
- repair placeholder or garbled titles
- fix suspicious author names
- fill in missing years when the paper content supports it
- incrementally review a large library without reprocessing already-reviewed papers

Do not use this skill for:

- normal ingest
- DOI or citation-count refresh
- paper-content enrichment such as TOC/L3 extraction
- directory normalization when metadata is already trustworthy and `rename` alone is enough

## Workflow

### 1. Find unreviewed candidates

Skip papers that already contain `.scrubbed`.

You can list suspicious, unreviewed papers with a Python helper that resolves `papers_dir` from the active ScholarAIO config:

```bash
python - <<'PY'
from scholaraio.services.audit import list_scrub_suspects
from scholaraio.core.config import load_config

cfg = load_config()

for issue in list_scrub_suspects(cfg.papers_dir):
    print(f"{issue.paper_id}\t{issue.rule}\t{issue.message}")
PY
```

If the user asked for a broad quality pass, it is also reasonable to start with:

```bash
scholaraio audit
```

Then narrow to papers that are both:

- not already `.scrubbed`
- obviously bad enough to justify manual review

### 2. Inspect one paper at a time

For candidates with readable metadata, inspect:

```bash
scholaraio show "<paper-id>" --layer 1
```

Before changing anything, record the stable paper UUID shown in the L1 header as `stable_id`. `repair` preserves this UUID even when the directory name changes.

Then read the source text as needed:

```bash
scholaraio show "<paper-id>" --layer 4
```

If the suspect is `invalid_metadata` because the directory only has `paper.md` and no readable `meta.json`, `show --layer 1` may not work yet. In that case, inspect `paper.md` directly from the configured papers directory and repair by directory name:

```bash
python - <<'PY'
from scholaraio.core.config import load_config

paper_id = "<paper-id>"
cfg = load_config()
print((cfg.papers_dir / paper_id / "paper.md").resolve())
PY
```

If the default `show --layer 4` view is too long, resolve the actual `paper.md` path with the same identifier semantics as `show` / `repair`, then inspect only the needed slice:

```bash
python - <<'PY'
from scholaraio.cli import _resolve_paper
from scholaraio.core.config import load_config

paper_id = "<paper-id>"
cfg = load_config()
print((_resolve_paper(paper_id, cfg) / "paper.md").resolve())
PY
```

If the head of the file is insufficient, inspect a larger section or search relevant phrases in the resolved `paper.md`.

Focus on extracting only the identity-critical metadata needed to make the paper usable:

- real title or at least a concise, accurate keyword title
- real first author or organization when clearly stated
- publication year when clearly supported by the document

### 3. Repair conservatively

Use `repair` to update only the fields you can support from the source:

```bash
scholaraio repair "<paper-id>" --title "Correct Title" --author "First Author" --year 2024 --no-api --dry-run
```

Then run the real repair:

```bash
scholaraio repair "<paper-id>" --title "Correct Title" --author "First Author" --year 2024 --no-api
```

`repair` now preserves existing metadata and only overwrites the fields you explicitly update through the CLI. Existing journal, abstract, paper type, citation counts, IDs, TOC/L3 fields, and other enriched metadata stay in place unless you intentionally replace them.

In scrub mode, `--no-api` should be the default. These records are often low-quality documents or weakly identified items, and conservative local repair is safer than letting API matches overwrite title, author, or year.

Only drop `--no-api` when the user explicitly wants metadata refetch behavior and has checked that the identifier quality is strong enough to support it.

Only pass `--doi` when you are intentionally correcting or adding the DOI. If you omit `--doi`, `repair` preserves the existing DOI.

Decision policy:

- Title quality is the top priority.
- Authors and year should be repaired when evidence is strong.
- Do not fabricate DOI, journal, or venue.
- If author or year cannot be confirmed reliably, leave them unresolved rather than guessing.

### 4. Handle directory renames correctly

`scholaraio repair` already rewrites `meta.json` and renames the paper directory immediately when title, author, year, or DOI changes. The rename is derived from the updated identity fields, while the rest of the metadata is preserved unless explicitly overwritten.

That means the original directory name may stop existing right after the real repair. Resolve the current directory from the stable UUID you recorded before editing:

```bash
python - <<'PY'
from scholaraio.cli import _resolve_paper
from scholaraio.core.config import load_config

stable_id = "<uuid-from-layer-1>"
cfg = load_config()
print(_resolve_paper(stable_id, cfg).name)
PY
```

If you repaired papers through `scholaraio repair`, skip `rename --all` for those same records. `repair` already rewrites `meta.json` and renames the directory immediately, including collision suffixes when needed.

Only use `rename --all` for records whose `meta.json` you edited outside `repair`, or for older records you did not already rename in the current scrub pass:

```bash
scholaraio rename --all
```

Because rename may change the directory path, always create the marker using the post-rename directory name.

### 5. Mark reviewed papers

Once a paper has been reviewed and is acceptable for current library use, create the marker:

```bash
python - <<'PY'
from scholaraio.cli import _resolve_paper
from scholaraio.core.config import load_config
from scholaraio.stores.papers import mark_scrubbed

stable_id = "<uuid-from-layer-1>"
cfg = load_config()
paper_d = _resolve_paper(stable_id, cfg)
mark_scrubbed(paper_d)
print(f"marked {paper_d.name} as scrubbed")
PY
```

Only mark a paper when:

- you have reviewed the record
- the remaining metadata quality is acceptable
- there is no known blocking issue that should force future re-review

`.scrubbed` means reviewed, not perfect.

### 6. Rebuild indexes once per batch

After finishing the batch:

```bash
scholaraio pipeline reindex
```

This keeps search and registry state aligned with renamed or repaired records.

## Heuristics

The most common scrub targets are:

- placeholder titles such as `Introduction`, `TLDR`, `Overview`, `Summary`
- garbled titles containing replacement characters like `�`
- missing or suspicious author names such as `Unknown`
- missing years or placeholder-style directory names like `XXXX`
- malformed directory names created from bad metadata

These are candidate heuristics, not auto-rewrite authority. The paper content is the final source of truth.

## Acceptance Standard

A scrubbed paper should be:

- identifiable in the library
- searchable by a meaningful title
- attributed to a plausible first author or organization when known
- assigned a real year when known
- normalized into the standard directory naming scheme

If you cannot achieve that threshold from the source text, stop short of marking the paper and report the ambiguity to the user.
