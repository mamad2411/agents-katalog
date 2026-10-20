---
name: discover-context
description: "Captures what already exists in a codebase before work begins."
user_invocable: true
---

# Context Discovery

When invoked, scan the current project for existing context and produce a
classified index at `.context/{project}/INDEX.md`.

If arguments are provided, treat them as the project name to write under
`.context/`. If not, infer from the working directory's basename, or reuse the
slug from an existing `.specifications/{name}/` or `.architecture/{name}/` if
one exists.

If `.context/{project}/INDEX.md` already exists, stop and recommend
`/sulis:refresh-context` instead.

---

## Execution Model

Discovery is **synchronous and interactive**. The cartographer scans first,
then conducts a guided one-question-per-purpose conversation with the user to
classify each finding. The skill exits after writing the index and presenting
it for confirmation.

Total session typically takes 5-15 minutes for a mid-sized project. Large
projects with extensive existing documentation may take longer because
classification is per-purpose.

---

## Workflow

### Step 1 — Determine project slug

Infer from (in order of preference):

1. Argument passed to the skill
2. Existing `.specifications/{name}/` directory
3. Existing `.architecture/{name}/` directory
4. Working directory basename (sanitised)

If none of these yield a sensible slug, ask the user.

### Step 2 — Pre-flight check

Verify the project does not already have a context index:

- If `.context/{project}/INDEX.md` exists → recommend `/sulis:refresh-context`
  and exit.
- If `.context/{project}/` exists but no INDEX.md → proceed and overwrite.

### Step 3 — Scan

Walk the project tree once. For each file, match against the patterns in
`references/discovery-protocol.md` (Purposes 1-9). Record matches.

Hard limits per the protocol:
- Max 5000 files scanned
- Max 100 KB previewed per file
- Excluded: `node_modules`, `vendor`, `.git`, `target`, `dist`, `build`,
  `.next`, `.venv`, `__pycache__`, lockfiles, binaries

If the scan caps out, surface that to the user and ask whether to narrow
scope (e.g. "scan only `architecture/` and `docs/`").

### Step 4 — Infer stack

From manifest files (Purpose 9 in the protocol), infer:
- Primary language(s)
- Frameworks (best-effort, from package.json deps, pyproject.toml, etc.)
- Build tooling
- Container/deploy artefacts
- CI presence

This is informational only — recorded in the index's Stack section, not
asked about.

### Step 5 — Present findings, one purpose at a time

For each purpose with at least one match, present findings as a single framed
question. Wait for the user to classify before moving to the next purpose.

**Order of presentation:**

1. Architecture Documentation
2. ADR Registry (treat the registry as one entity, not per-ADR)
3. Conventions & Standards
4. Patterns Library
5. Tech & Debt Inventory
6. Domain Models & Glossary
7. Prior Specs (`.specifications/`, `specs/`, etc.)
8. Prior SEA/sulis-security output (`.architecture/`, `.security/`)

**Question template (per purpose):**

> "I found {N} candidate(s) for {Purpose Name}:
>
> 1. `{path}` — {first line or two as preview}
> 2. `{path}` — ...
>
> How should these be classified?
> - **authoritative** — load-bearing; downstream plugins must respect
> - **informational** — useful context, not binding
> - **superseded** — older version; ignore for new work
> - **out-of-scope** — exclude entirely
>
> You can apply one classification to all, or specify per-item (e.g. '1 authoritative, 2 superseded')."

**Skip purposes with zero matches.** Do not ask "I found no ADR libraries —
is that right?" unless the user has indicated they expect one.

### Step 6 — Open-ended probe

After all matched purposes have been classified, ask once:

> "Are there other documents I should know about? Anything in `README.md`,
> internal wikis, or elsewhere in the repo I haven't surfaced — especially
> anything load-bearing the team treats as authoritative?"

If the user names additional sources, add them and classify per the same
taxonomy.

### Step 7 — Known gaps

Ask once:

> "What topics does your existing documentation *not* cover that the
> downstream tools (SRD, SEA, sulis-security) may need to fill in? For
> example: no formal API contracts? No performance SLAs? No incident
> runbook?"

Record verbatim under **Known Gaps** in the index. This is the section that
gives SEA licence to add new ADRs / TDD sections without contradicting prior
decisions.

### Step 8 — Write the index

Generate `.context/{project}/INDEX.md` per the schema in
`references/context-index-template.md`. Populate every required section.
Omit conditional sections per the template's "Required vs Optional" table.

Set `Discovery completeness`:
- `HIGH` — at least 3 authoritative sources classified, plus ADRs or
  conventions, plus the open-ended probe yielded no surprises
- `MEDIUM` — fewer authoritative sources, or some purposes had matches the
  user couldn't confidently classify
- `LOW` — no authoritative sources, sparse documentation, mostly inferred
  stack

### Step 9 — Present and confirm

Show the user the final INDEX.md content. Ask:

> "Here's the index I'm about to write. Anything to correct before I save it?"

After confirmation, write the file. Tell the user where it lives and what
downstream commands will now use it:

> "Written to `.context/{project}/INDEX.md`. SRD, SEA, and sulis-security will
> read this first on their next invocation and apply Respect-Don't-Restate.
> Run `/sulis:show-context` any time to view this index, or
> `/sulis:refresh-context` after the project changes."

---

## Adapting Depth

- **Quick** ("I just need the index") — skip the open-ended probe and the
  known-gaps question. Index is written with only file-matched content;
  Discovery completeness capped at MEDIUM.
- **Full** (default) — all nine steps.
- **Audit-only** ("show me what you'd find but don't write the index") — run
  Steps 3-7 conversationally; do not write anything.

---

## Gotchas

- **Do not classify on behalf of the user.** Even when a file's name screams
  "authoritative" (e.g. `ARCHITECTURE.md`), ask. The team's relationship
  with a doc is what makes it authoritative, not the filename.
- **Do not load files unless asked.** The preview (first 10 lines / 500
  chars) is enough for classification. Full content is loaded only by
  downstream plugins consuming the index.
- **Do not over-batch.** "Here are 47 files I found, classify them" is a
  hostile interface. Group by purpose, one purpose per turn.
- **An empty find is not a failure.** Truly greenfield projects produce
  empty Authoritative tables. Record that honestly; the index is still
  valuable as a "we looked and found nothing" signal.
- **Slug consistency matters.** If `.specifications/payments-service/`
  exists, use `payments-service` — do not generate `payments`. Downstream
  plugins match by slug across `.specifications/`, `.architecture/`,
  `.context/`, `.security/`.

---

## See Also

- `references/discovery-protocol.md` — what to scan for and where
- `references/classification-taxonomy.md` — the four buckets explained
- `references/context-index-template.md` — the index file schema
- `../refresh-context/SKILL.md` — running discovery on a project that's already been mapped
- `../show-context/SKILL.md` — read-only view of the current index
