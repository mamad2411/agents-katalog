---
name: compile-core
description: >
  The compile lane's half of the ingest skill: choose a source's depth after reading it, write the
  source page from the depth's template, assign confidence, network the knowledge, and propose the
  registry lines rather than writing them. Preloaded into a wiki-compile lane home; the head keeps
  the orchestration half (conversion, de-dup, pacing, parallel merge, the verify step, sorting, the
  run ledger). Slice source: the ingest skill, sections Depth, Step 3, Step 4 and Hard constraints.
user-invocable: false
---

# compile-core — compile an assigned source into wiki pages

You compile the sources your brief assigns and nothing else. A gap in them is reported, never
filled from your own knowledge. The page schema, its frontmatter fields and the confidence ordinal
live in `contract/schema-s4.md` and `contract/confidence-rubric.md` beside this slice — read them
rather than recalling them.

## 1 · Read, then choose the depth

Read the source in full first. **Depth is decided after the read — never from a filename, folder,
length or marker**, none of which separate a research-worthy source from an ordinary one.

Your brief names the run's **authorised range** (default: all three). Never choose outside it. If
a source genuinely needs a depth the range excludes, compile at the nearest authorised depth, say
so, and report it as a gap.

Three triggers, judged on the source you have just read:
- **T1 · Reuse** — original figures, a reimplementable method, or wording where a paraphrase would
  falsify the claim.
- **T2 · Proximity** — it bears on a topic the owner's own pages name, or on an open question the
  wiki already holds (a `## Conflicts / Open Questions` block, a `flagged:` page). Where those
  pages are outside your reading list, read T2 as "a topic with at least three source pages in
  `wiki/index.md`"; where the wiki is too small for that, say so once and work in concise or
  standard only.
- **T3 · Novelty** — it adds something no existing page holds.

**`research` = T1 ∧ T2 · `concise` = ¬T3 · `standard` = everything else.**

Overrides, which fire regardless of the triggers: a source that is the owner's own work is never
below standard; a source that corrects an existing wiki page is always research, because a
correction has to be exact; a source whose conversion collapsed word boundaries can never be
research (verbatim quoting is impossible on it) — compile at standard and say so.

**Name the evidence or drop a rung.** Every depth you record carries a locator:
`research — T1 (Table 3 ablation) · T2 (calibration, an owner page)`, `concise — ¬T3 (link post,
all three tools already have pages)`. A trigger letter with empty parentheses is a defect, not a
record. Where you cannot name the evidence, take the lower rung.

What each depth changes:
- **standard** (the usual outcome) — articles, blogs, posts, docs. Sections 2–4 as written.
- **concise** — thin or fully redundant sources: a concise summary, minimal bullets,
  new pages only for genuinely new entities or concepts.
- **research** — primary material the owner will need to reuse exactly. Preserve exact figures (no
  rounding), quote critical claims verbatim with section or page references, mark anything not
  directly stated as `unverified`, never infer a number, use the research template below, add the
  academic frontmatter, and cross-check findings against existing pages, flagging confirmations and
  contradictions explicitly. Long block quotes stay in the raw file — link, never transplant.

Record it always: the source page carries `depth:`, and your report carries the depth with its
locator for every source.

## 2 · The source page

Write to `wiki/sources/<slug>.md`, kebab-case, inside your file whitelist.

Both templates are copied verbatim from the ingest skill, comments included. Where a comment cites
`CLAUDE.md §4.x`, the text it points at is in the `contract/` slices you hold: §4.1–§4.6 in
`contract/schema-s4.md`, the confidence rubric in `contract/confidence-rubric.md`.

**Standard and concise depth:**

```markdown
---
title: "Source: <Human Title>"
type: source
depth: concise | standard | research   # the depth you chose (Depth) — required on every source page
confidence: medium   # per CLAUDE.md §4.6 — reflects the source: peer-reviewed/expert→authoritative · preprint/official-doc/owner-work/faithful-summary(default)→high · secondary or adjacent-only grounding→medium · promo/social/transcript→low (grounding strength, not source count; a user instruction can override the tier)
audited: <YYYY-MM-DD>   # today — assignment with the source in context is the check (§4.6); on updating an existing page, re-check its badge and re-stamp
tags: [topic]
sources: [raw/2-papers/report.md, raw/2-papers/report.pdf]   # converted .md AND original; one entry if native .md or URL
source_url: "<original web URL if a clip — else omit>"        # de-dup
source_hash: "<first 16 hex chars of the raw file's sha256>"   # de-dup — the length the pre-flight greps
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
---

## Summary
[The core summary, with the detail its claims need.]

## Key Takeaways
- ...

## Related
- [[EntityName]] — why related
- [[Concept Name]] — why related
```

**Research depth (replaces the template above):**

```markdown
---
title: "Paper: <Title>"
type: source
depth: research
confidence: high   # authoritative if peer-reviewed/published; see CLAUDE.md §4.6
audited: <YYYY-MM-DD>   # today — assignment with the source in context is the check (§4.6)
tags: [paper, <field>]
authors: [<First Author>, <…>]
year: <YYYY>
venue: "<journal / conference>"
doi: "<DOI or stable URL>"
sources: [raw/2-papers/<file>.pdf, raw/2-papers/<file>.md]   # original + converted
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
---

## Citation
<full reference string>

## Research Question
## Methodology
## Key Findings
- <finding with exact figures, e.g. "+12.3 BLEU, p<0.01">
## Data / Setup
## Contributions
## Limitations & Threats to Validity
## Relation to Wiki
- Confirms [[…]]; contradicts [[…]] → flag a `## Conflicts / Open Questions` block on that page
## Key Quotes
> "<verbatim>" (§/p.)
## Open Questions / Follow-ups
## Related
- [[…]]
```

**Dual provenance:** for a converted source, `sources:` lists **both** the converted `.md` and the
original (file path, or the URL for a web or video source). Where the head sorts the raw file after
you close, predict the post-sort path so the link does not break — your brief names it.

**Research depth is not paper-only.** T1 ∧ T2 fire on any primary source whose exact wording matters
(a regulation, an institutional handbook, a contract, a policy document). Keep the frontmatter
fields that exist (no DOI → omit it; `venue:` takes the issuing body and version) and replace the
paper-shaped middle sections with genre-fitting equivalents (Scope & Applicability · Requirements &
Thresholds · Deadlines & Milestones · Governance). The obligations never flex — exact figures,
verbatim quotes with locators, `## Relation to Wiki`, `## Related` — and you declare the
substitution on the page and in your report.

## 3 · Confidence

Assign every page's `confidence:` from `contract/confidence-rubric.md`, on source authority ×
verification × derivation, and stamp `audited:` with today's date in the same pass — the stamp is
the audit trail, so never stamp a badge you did not check. Judge by **grounding strength, not
source count**: one source primary for the page's own claims grounds `high` alone; a strong source
primary only for something adjacent, or reputable-secondary grounding, is `medium`; a single
paragraph in a single witness is `low`. Compiled pages cap at `high`, the cap being a ceiling and
never a demotion. On a tie take the lower tier, and never raise an existing page's tier — you may
propose a raise with the evidence, and the head reads the source before any raise stands. Report
each page's tier with the reason that decided it.

## 4 · Network the knowledge

Add the links the source warrants, and only the pages the schema warrants.

- **Models and benchmarks are first-class.** Any LLM named gets a page under `wiki/models/`, any
  evaluation dataset a page under `wiki/benchmarks/`, and the link runs **both ways**: the source
  under the model or benchmark page's `## Appears in`, the models and benchmarks under the source
  page's `## Related`.
- **A product name is a model mention.** A source that names an LLM product or family even once,
  even as a licence or plan name (ChatGPT Edu, GPT-4o, Claude, Qwen), links the family's model page
  from `## Related` — ChatGPT and every GPT-n fold into `[[GPT]]` — and says on the page what the
  source names; the model page's `## Appears in` gains the source. The link does not require
  an individually named model (schema §4.5).
- **Reuse, never duplicate.** Fold a variant into its existing page (a point release into the
  family page, a subset benchmark into its parent) rather than creating a near-twin. Canonicalise
  every name against `wiki/index.md` in `name` mode (`grep -o '^- \[\[[^]|]*' wiki/index.md | sed 's/^- \[\[//'`) before you write it — never a whole read.
- **A page exists** → read it and merge incrementally. Never clobber, and never silently overwrite
  a contradiction: keep both statements under `## Conflicts / Open Questions` and report it. A
  conflict never pauses you.
- **The stub rule.** A tool or an entity that the source gives one paragraph or one row, with no
  second witness, is **a fact on the source page — never a link and never a page**. A link forces a
  page, and a one-paragraph page carries no behaviour the fact would not. Create a tool, entity or
  concept page only where it has enough substance for the `## Definition` and `## Key Points` the
  schema requires. Models and benchmarks keep their rule above: they get pages either way.
- Every page you write ends with a `## Related` section carrying at least one link (no orphans),
  and every link you write resolves to a real page or to a target in your emitted claims.

## 5 · Registries: propose, do not write

A log entry stays concise (the §5 shape: the title line, `- **Changed**:`, `- **Conflicts**:`);
detail belongs on the pages, never in the entry. Frontmatter carries values only: no run id, lane id or
evidence in a comment — your depth and confidence evidence goes in the report.

`wiki/index.md` and `wiki/log.md` are the head agent's to write. Return, in your report:
- the `index.md` line for each page, under the heading it belongs to, one line each: `- [[Page]] —
  one-line description.`
- the `log.md` entry the run would carry, in the schema's shape.

Only where your brief explicitly grants the ingest exception do you write them yourself, and then
by anchored per-heading `Edit` for the index and a shell append for the log — never a whole-file
read-modify-write, which commits a stale snapshot and erases a concurrent writer's entry. Verify
either write back with a grep and show the grep. Any model or effort value you write into a
registry entry is copied from your brief's first line or omitted — never inferred.

**Shared-type pages under a parallel run.** Where your brief says other lanes are compiling alongside you, do not create or edit entity, concept, model or benchmark pages. Emit a claim and an anchored unified diff per target into the diff directory your brief explicitly grants. The head plans and applies the accepted diffs. Mirror each complete claim under `claims` in the `claims_emitted` ledger checkpoint as well as your report:

`{name · type · kind: create|update · target (canonicalised against index.md — a variant arrives as
an update to the family page) · facts[] with a per-fact source locator · links[] · appears_in[] ·
confidence · from: source-page · source: raw identity · diff: absolute path · base: sha256 prefix · diff_hash: sha256 prefix}`

An update diff is against the page exactly as read, with `base` the first 16 sha256 hex digits (the `source_hash` length used by de-dup). A create is a new-file diff carrying the schema's frontmatter and sections and `aliases:` with acronym and expansion wherever the source gives both. Record the diff's own sha256 prefix in `diff_hash`. Never apply the diff yourself. The lane's `lane_open` carries `role: compile` and the same lane id as the spawn record for metering.


Checkpoint key: `claims`: the list of claim objects, never a count; an optional count goes under `claims_count`. Each member is a complete object with a non-empty `name`; an empty list means no claims. Never use `claim_objects` as a substitute key. Shape-only example for a source with no claims (add the run and write-time timestamp):

`{"event":"checkpoint","stage":"claims_emitted","lane":"<lane>","source":"<raw identity>","claims":[],"claims_count":0}`

**Mandatory post-checkpoint assertion.** After every `claims_emitted` append, run the following read-only Python through `python3 -B -` with three quoted arguments: the literal ledger path, this lane id, and this checkpoint's exact source identity. Its stdin is the code below. Record the `claims-shape:` and `controls:` lines in the lane's final report under a `## Controls` heading, with one unquoted line `claims-shape: checkpoints N · objects M · invalid 0`. This evidence is required before `registered` or `lane_close`; a failed or missing assertion is a failed output gate. The verifier consumes these report lines. The check reads all matching checkpoints, so a later good append cannot conceal an earlier malformed one; it checks list shape, not factual accuracy or the full claim schema.

```python
# claims-shape assertion: kept executable for the brief suite.
import json
import sys


def stop(message):
    print("PROBE FAILED: " + message)
    raise SystemExit(2)


def valid(event):
    claims = event.get("claims")
    return (isinstance(claims, list)
            and all(isinstance(c, dict) and isinstance(c.get("name"), str)
                    and c["name"].strip() for c in claims)
            and ("claims_count" not in event
                 or (type(event["claims_count"]) is int
                     and event["claims_count"] == len(claims))))


if (valid({"claims": 1, "claim_objects": [{"name": "Example"}]})
        or valid({"claims": [{}]})
        or not valid({"claims": [{"name": "Example"}], "claims_count": 1})
        or not valid({"claims": [], "claims_count": 0})):
    stop("claims-shape controls did not discriminate")
print("controls: integer claims rejected; unnamed object rejected; object list and empty list accepted")
if len(sys.argv) != 4 or not all(sys.argv[1:]):
    stop("claims-shape needs ledger, lane and source")
ledger, lane, source = sys.argv[1:]
matched = objects = 0
try:
    with open(ledger, encoding="utf-8") as handle:
        for number, line in enumerate(handle, 1):
            event = json.loads(line)
            if not isinstance(event, dict):
                stop("ledger line %d is not an object" % number)
            if (event.get("event") == "checkpoint"
                    and event.get("stage") == "claims_emitted"
                    and event.get("lane") == lane and event.get("source") == source):
                if not valid(event):
                    stop("line %d: claims must be a list of named objects; claims_count must equal its length" % number)
                matched += 1
                objects += len(event["claims"])
except (OSError, ValueError) as error:
    stop("cannot check ledger: %s" % error)
if not matched:
    stop("no claims_emitted checkpoint for this lane and source")
print("claims-shape: checkpoints %d · objects %d · invalid 0" % (matched, objects))
```

Mark a shaky fact `unverified`. A claim's facts each carry the locator they came from; a fact
without one does not go in the claim.

## 6 · Context notes, plants and anomalies

Your brief's CONTEXT NOTES are pointers, never sources. A note the raw does not bear out is not
compiled: list it under `## Anomalies` as "not in the raw". One such note may be a deliberate plant
testing exactly this, and the rule is the same either way.

Your report ends with `## Anomalies`: everything the rubric does not cover, each with a locator —
a source-internal inconsistency (kept on the page, never resolved), a raw-versus-wiki conflict and
the block you wrote for it, a provenance gap, a context note not borne out, a thin or truncated
source, anything left unsettled. `none` is a claim, and names what you checked.

## Hard constraints

- **Never modify or delete the text inside a raw file.** Raw content is immutable; you neither move
  nor sort raw files unless your brief says so.
- Every page carries the frontmatter and the sections `contract/schema-s4.md` specifies for its
  type, a `confidence:` with today's `audited:`, and a `## Related` section.
- Every source page carries `depth:`, decided after the read, inside the authorised range. Never
  backfill `depth:` onto a page compiled before the rule.
- Write everything in British/UK English, translating a non-English source; US spelling survives
  only inside a verbatim quote, a proper noun or code.
- Never fabricate. Where you cannot ground a claim, mark it `unverified` and cite what you have, or
  leave it out and report the gap.
- Report every page you created or updated with its depth locator and its confidence reason. That
  report is the completion gate: no done-declaration without it.
