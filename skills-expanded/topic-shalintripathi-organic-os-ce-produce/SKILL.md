---
name: ce-produce
description: Use to produce a publish-ready draft from an approved content brief - "draft the approved brief", "write this post", /organic-os:produce. Runs the six-stage pipeline.
---

# Content pipeline

1. Input: an APPROVED brief item (require_approved - drafting counts as work
   the user pays attention for, so briefs are gated before drafting).
   A user may also hand a manual brief. Register it before anything else:
   confirm scope in-session, then `create_item(kind="content-brief", ...)`
   with the brief text as the body - items are born `proposed`, never any
   other status - and record the in-session approval via the contract CLI
   so require_approved passes. Never save a hand-written file into
   `briefs/` and never set a status at creation: a brief born `drafted`
   with no approvals can neither be approved nor published, and jams the
   pipeline until `python3 -m core reset-to-proposed` repairs it. A brief
   this pipeline will draft still starts `proposed` and reaches `drafted`
   only through its approved lineage (step 4).
1b. Decision check, BEFORE registering a manual brief with `create_item`.
   Search the brain's decision memory for the topic:
   `PYTHONPATH="$CLAUDE_PLUGIN_ROOT/lib" python3 -c "..."` snippet importing
   `core.decisions` - `search(<brain>, [<topic>, <target keyword>])`. It
   returns prior decisions newest first with `date`, `choice`, `scope`,
   `item`, and the `rationale`. A hit whose `choice` is `rejected` means a
   human already refused this piece. Exactly two paths are allowed, never a
   third:
   - SKIP it: tell the user the topic was rejected on <date> because
     <reason>, and stop before creating anything.
   - Or CREATE it with a line in the brief body reading "previously
     rejected on <date> because <reason>; proposing again because <what
     changed>". What changed must be concrete - a new signal, a search-
     demand shift, a product change - never "worth another look".
   Silently re-registering a rejected topic is forbidden. A hit with any
   other `choice` is context for the brief, not a blocker. An already
   approved brief arriving from the queue has cleared this check at
   proposal time; do not re-run it there.
2. Stages, sequential agents (each receives profile path + prior artifacts):
   ce-researcher -> ce-writer -> ce-brand-auditor -> ce-seo-aeo -> ce-qa ->
   ce-editor.
3. Save the final draft as <brief-file>.draft.md next to the brief (frontmatter:
   title, slug, meta_description, focus_keyword, schema block, and
   `capsule: verified` - written only after ce-qa's capsule hard check
   passed AND ce-editor's Capsule confirmation line is present; this is
   the handoff note onsite-publish requires before publishing). Save the
   research pack + QA log under runs/YYYYMMDD-produce-<slug>/.
4. `PYTHONPATH="$CLAUDE_PLUGIN_ROOT/lib" python3 -m core status
   <brief-path> drafted --actor agent`. Then invoke ce-image for the
   featured-image step. Publishing is onsite-publish's job (separately gated).
5. Rules from the profile override everything: voice, banned phrases, rulebook.
   House defaults if profile is silent: answer capsule up top, no em-dashes,
   active voice, statistics cited inline with live links.
6. Never edit brain frontmatter directly. The contract CLI is the only write
   path for status and approvals.
7. At each stage boundary, append a one-line progress marker with a UTC
   timestamp to the run report file before starting the stage - headless
   runs are watched by tailing that file, not a terminal.

## Comparison briefs (brief_type: comparison)

When the brief's frontmatter carries `brief_type: comparison` (the field
is additive; absence means explainer - see docs/site-repo-contract.md),
the same six stages run with comparison-specific guidance layered on:

- ce-researcher: verify EVERY claim about a third-party product against
  that product's live public pages - pricing and features change, so each
  claim destined for the comparison table needs a fetch-verified source
  URL and a checked-on date in the research pack. Never from memory.
- ce-writer: produce the X-vs-Y structure - the answer capsule states the
  honest one-line difference between the two; the comparison table
  carries only rows the research pack verified; a "who should pick which"
  section treats the competitors fairly, naming where each is the better
  pick.
- ce-qa: two comparison-specific hard checks on top of the standard ones:
  (1) no unverifiable competitor claims - a row whose cells cannot be
  matched to a fetch-verified source is dropped, never guessed; (2) no
  disparagement - factual differences only, no adjectives about
  competitors.

Rationale: X-vs-Y and listicle shapes are the most-cited content shapes
in AI search (https://www.position.digital/blog/digital-pr-tactics/).
