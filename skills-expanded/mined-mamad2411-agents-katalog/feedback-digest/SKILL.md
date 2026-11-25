---
name: feedback-digest
description: Score captured localization feedback (valid/constructive verdict with evidence) and apply fixes — project-local edits behind one confirm; catalog changes only as proposed patch files.
---

# feedback-digest

> Feedback that is captured but never evaluated is a guilt pile. This
> skill turns the pile into either an applied localization fix, a proposed
> catalog patch, or an explicit rejection — with evidence either way.

## When to use

- The user asks to review/apply collected feedback.
- `feedback digest` shows pending items during other localization work.

## Procedure

1. **Get the queue** (this also sweeps expired items — 180d TTL):

   ```bash
   "${POLYMATH_PLUGIN_ROOT}/bin/polymath-pipeline" feedback digest
   ```

2. **Evaluate every pending item — verdict with evidence.** Check the
   claim against current reality: read the named surface's behavior, the
   conventions docs, the run/artifact in `evidence`. Then record:

   ```bash
   "${POLYMATH_PLUGIN_ROOT}/bin/polymath-pipeline" feedback evaluate <id> \
     --verdict valid-constructive|valid-not-actionable|invalid \
     --evidence "<what you checked and what it showed>"
   ```

   `valid-constructive` = real AND a concrete fix exists. Never guess a
   verdict — the evidence string must name what you inspected.

3. **Draft fixes for every `valid-constructive` item.** Project-local
   targets, smallest first:
   - a Hard rule / correction in the relevant `conventions_docs` role doc
   - a `skill_overrides["<plugin>:<skill>"]` entry in `.polymath/project.yaml`
   - a rule in `.polymath/route-signals.project.json` (routing misses)

4. **One-confirm apply (project-local).** Present ALL drafted edits in one
   summary — file, exact change, which feedback id it fixes — and ask for
   a single confirmation. On yes: apply the edits, then for each id:

   ```bash
   "${POLYMATH_PLUGIN_ROOT}/bin/polymath-pipeline" feedback resolve <id> \
     --outcome applied --detail "<file: what changed>"
   ```

5. **Catalog-level findings are never applied.** When the right fix is in
   the Polymath catalog itself (a skill's procedure, a workflow, a
   template), write a proposed patch to
   `.polymath/feedback/catalog-proposals/<id>.md` — problem, evidence,
   proposed diff or exact wording — and resolve with
   `--outcome proposed-catalog-patch --detail "<path>"`. Never commit it,
   never edit installed plugin files; the user routes it upstream.

6. **Reject explicitly.** `invalid` / `valid-not-actionable` items get
   `resolve --outcome rejected --detail "<reason>"` — silence is not a
   resolution.

## Quality bar

- Every pending item leaves with a verdict; every verdict cites evidence.
- Project-local edits shipped behind exactly ONE confirmation, not N.
- No catalog file touched — proposals are files, not edits.
- The digest ends with the store empty of unevaluated items.
