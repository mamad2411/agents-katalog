---
name: okf-docs
description:
  Author, validate and approve OKF v0.2 documentation — ADRs, feature requests,
  runbooks, concepts — with enforced folder layout, AI/human attribution,
  approval gating and a maintained log.md edit log. Also installs its own
  pre-commit validation into a repository's existing hook mechanism. Invoke with
  a verb — new, validate, pending, verify, hooks — or use it whenever writing,
  restructuring, reviewing or validating any project documentation, architecture
  decision, runbook or knowledge-base page, even when the user does not say
  "OKF" — and before creating any new .md file under a docs bundle.
license: MIT
compatibility:
  Designed for Claude Code or similar AI coding agents. Requires bun to run the
  bundled okf-validate.ts / okf-review.ts scripts.
metadata:
  author: ibaou-dev
  version: "0.5.0"
  openclaw:
    emoji: "📚"
    homepage: https://github.com/ibaou-dev/skills
    requires:
      bins:
        - bun
    install: []
user-invocable: true
allowed-tools: Read Glob Grep Edit Write Bash(bun:*) Bash(date:*)
---

# OKF Docs

A knowledge bundle is a directory of Markdown files whose frontmatter tells an
agent what each document is, who wrote it, who approved it, and when it goes
stale. This skill is how you write into one without corrupting it.

## Verbs

This skill exposes five verbs, invoked as the first token of the arguments
following the skill (the exact prefix is set by whichever harness loaded it —
`/skill:okf-docs <verb>` on oh-my-pi, `/okf-docs <verb>` on Claude Code). With
no arguments the rules below are loaded as knowledge and nothing runs.

| Verb       | Form                                                           | Procedure                                      | Writes |
| ---------- | -------------------------------------------------------------- | ---------------------------------------------- | ------ |
| `new`      | `new <type> "<title>" [--slug s] [--status draft]`             | `skill://okf-docs/references/verb-new.md`      | yes    |
| `validate` | `validate [paths…]`                                            | `skill://okf-docs/references/verb-validate.md` | no     |
| `pending`  | `pending [--json]`                                             | `skill://okf-docs/references/verb-pending.md`  | no     |
| `verify`   | `verify <paths…> \| --all [--by human:id] [--date YYYY-MM-DD]` | `skill://okf-docs/references/verb-verify.md`   | yes    |
| `hooks`    | `hooks`                                                        | `skill://okf-docs/references/verb-hooks.md`    | yes    |

Read the verb's procedure file with the `read` tool before acting — it carries
the argument contract and the failure modes. An unrecognised verb is a stop, not
a guess: report the five valid verbs and end.

Run `verify` only when a human asked for it in this turn; a trust layer an agent
can sign for itself is decoration.

## Resolving `$OKF_DOCS_HOME`

Every script invocation below names a real filesystem path — `bash` cannot
expand `skill://`. Resolve it once per session: read `skill://okf-docs/SKILL.md`
(or use the base directory the `/skill:` wrapper already supplied) and take the
directory from the response's `[<path>#<tag>]` snapshot header, then use that as
`$OKF_DOCS_HOME`. Example: a header of `[.claude/skills/okf-docs/SKILL.md#a1b2]`
means `OKF_DOCS_HOME=.claude/skills/okf-docs`.

## The one rule, and the four that make it useful

OKF v0.2 conformance is a single requirement: **a document declares a non-empty
`type`**. Anything else in frontmatter is optional to the format, and consumers
must tolerate keys they do not recognise. That tolerance is what keeps a bundle
readable a year later — but on its own it produces a folder of documents nobody
can trust. So this project adds four contracts on top:

1. **Attribution is not optional.** Every document carries
   `generated: {by, at}`. `by` is `agent:<harness>/<model-id>` or `human:<id>`;
   `at` is an ISO 8601 timestamp.
2. **Approval is a human act.** `status: stable` requires
   `verified: {by: human:…}`. An agent authors; only a human approves. Never
   write a `verified` block for your own output — that is the one edit that
   turns the trust layer into decoration.
3. **The folder map is enforced.** A `type` determines a directory. A misplaced
   document is an error, not a style preference, because the bundle-relative
   path is the concept ID that every link resolves through.
4. **The log is the bundle's history, not a changelog of this skill's own
   tooling.** Creating, deleting, moving or changing the status of a _document
   in the bundle_ gets one line under today's date in `log.md` — the path and
   why, never a paragraph. A material edit to a `stable` document also gets one.
   Editing the skill's own scripts, templates, verb files or evals is not a
   bundle change: that history lives in git, which is invisible to a bundle
   reader — which is exactly why bundle changes need their own record and
   skill-development ones do not.

## Frontmatter contract

Canonical key order — keep it, so diffs stay readable:

```yaml
---
type: "adr"
title: "ADR 0004: OKF Documentation Governance"
description: "One factual sentence about what this document decides or reports."
status: "stable"
sources: []
tags:
  - "documentation"
  - "okf"
generated:
  by: "agent:omp/claude-opus-5"
  at: "2026-08-21T13:45:00Z"
verified:
  by: "human:ibaou"
  at: "2026-08-21"
stale_after: "2027-02-17"
# obsidian-block: drop these two keys when obsidian is disabled
aliases:
  - "ADR-0004"
cssclasses:
  - "clean-embeds"
---
```

| Field                             | Required                                     | Notes                                                            |
| --------------------------------- | -------------------------------------------- | ---------------------------------------------------------------- |
| `type`                            | yes                                          | the one rule of conformance; drives the folder map               |
| `title` / `description`           | yes here                                     | OKF-optional, but a bundle of untitled documents is unsearchable |
| `status`                          | yes here                                     | `draft`, `proposed`, `stable`, `superseded`, `deprecated`        |
| `superseded_by`                   | when `status: superseded`                    | bundle-relative concept ID (path minus `.md`) of the successor   |
| `sources`                         | when the document rests on external material | bare URL string, or OKF object `{id, resource, title}`           |
| `generated`                       | yes                                          | `by` matches `^(agent\|human):`; `at` is ISO 8601                |
| `verified`                        | only when `status: stable`                   | `by` matches `^human:`; `at` is `YYYY-MM-DD` (project extension) |
| `stale_after`                     | optional                                     | `YYYY-MM-DD`; a past date on a `stable` document is an error     |
| `tags` / `aliases` / `cssclasses` | Obsidian projects                            | must be plural and list-valued; quote any `[[wiki link]]`        |

`proposed` and `superseded` are documented extensions to OKF's three statuses,
carrying the ADR/FR lifecycle `proposed → stable → superseded | deprecated`.
Field-by-field detail, plus a worked block for each type, is in
`skill://okf-docs/references/frontmatter.md`.

## Folder map

| `type`      | Path                                           | Notes                                             |
| ----------- | ---------------------------------------------- | ------------------------------------------------- |
| `adr`       | `<bundleRoot>/adrs/NNNN-<slug>.md`             | 4-digit, zero-padded, monotonic, never renumbered |
| `feature`   | `<bundleRoot>/features/NNNN-<slug>.md`         | same numbering discipline                         |
| `runbook`   | `<bundleRoot>/runbooks/<slug>.md`              | operational procedure                             |
| `concept`   | `<bundleRoot>/concepts/<slug>.md`              | research reports, explanations                    |
| `reference` | `<bundleRoot>/references/<slug>.md`            | lookup material                                   |
| reserved    | `<bundleRoot>/index.md`, `<bundleRoot>/log.md` | see below                                         |

Nesting stops two levels below the bundle root. Reserved files are special-cased
and carry no `type`: the root `index.md` declares `spec: 0.2` **and nothing
else**, a non-root `index.md` carries no frontmatter at all, and `log.md`
carries no frontmatter and uses `## YYYY-MM-DD` sections, newest first. Layout
rationale and the healthy-bundle example tree are in
`skill://okf-docs/references/folder-structure.md`.

## Required sections

The body is free-form Markdown with exactly one H1 — except that a type with a
contract must honour it, because these are the sections a reader goes looking
for:

| `type`                 | Required `##` sections                                         |
| ---------------------- | -------------------------------------------------------------- |
| `adr`                  | Status, Context, Decision, Consequences                        |
| `feature`              | Status, Problem, Requirements                                  |
| `runbook`              | Purpose, Preconditions, Procedure, Verification, Failure modes |
| `concept`, `reference` | none                                                           |

## Writing a document

1. **Scaffold, do not copy a neighbour.** The `new` verb
   (`new runbook "Rotate the signing key"`) resolves the template, computes the
   path and the next number, substitutes attribution, writes the log entry and
   validates the result. Hand-copying is how a bundle acquires two conventions.
2. **Fill the sections; delete no heading.** An empty required section is a
   signal — write "none known" rather than removing it.
3. **State findings, not process.** Open with what is true, not with "this
   document explores".
4. **Cite what you used.** A claim resting on an external source carries an
   inline link, and that URL appears in `sources`. `sources` equals the cited
   set: not a superset, not a subset.
5. **Leave `verified` alone.** Ship at `draft` (or `proposed` for a decision
   awaiting a call). A human promotes it.
6. **Log it.** One bullet under today's date naming the path and the action.
7. **Validate before you claim done.** A finding is a defect in the document,
   never in the rule.

## Editing an existing document

Renames and deletions break links, and a broken link in a knowledge bundle is
worse than a missing document because it looks like knowledge. When you move or
delete a file:

- Grep the bundle for its basename and its path, then fix every hit. Wiki links
  resolve by basename, so a rename that preserves the basename keeps links valid
  — and a rename that _takes over_ another document's basename silently repoints
  every link that used it. Check the prose still says something true afterwards,
  not merely that the link resolves.
- Deleting is fine when git keeps the history, but the deletion goes in `log.md`
  — that is the only record a reader of the bundle can see.
- A material edit to a `stable` document invalidates its approval. Either
  re-verify with the human who owns it, or drop it to `draft` in the same edit.
  Silently editing under someone's `verified` block is the failure this layer
  exists to prevent.

## Using this skill from a subagent

A skill governs the session that loaded it. It does not automatically reach a
subagent that session spawns — on Claude Code, a subagent sees this skill only
if its own definition lists `skills: [okf-docs]`. The parent having the skill is
not sufficient: an agent with `Write` access and no `skills:` entry will write
into the bundle with invented frontmatter, the wrong folder, and no `log.md`
entry, and the parent session — which does know the rules — never sees the write
happen.

- **Any agent that writes into the bundle needs `skills: [okf-docs]`.** No
  exceptions for "it only writes one small file."
- **Restate the non-negotiables in the prompt too, for an agent whose output is
  not schema-constrained:** `status: "draft"`, never a `verified` block,
  `sources` equal to the cited set, the folder map, and the `log.md` entry. The
  skill's rules are knowledge the agent must load and apply, not a schema the
  harness enforces for it.
- **Parallel writers must not each append to `log.md`.** It is one shared file;
  two agents appending concurrently lose entries. Either serialise the log
  write, or have one final agent record every entry after the parallel writes
  complete.
- **A read-only reviewing agent gets the skill and the validator command, not
  `Write`.** Give it `skills: [okf-docs]` so it knows the rules to check
  against, but not write access — otherwise a reviewing agent can "fix" a
  finding into existence instead of reporting it.

## Validating

```bash
# whole bundle, human-readable
bun run $OKF_DOCS_HOME/scripts/okf-validate.ts

# specific files, machine-readable
bun run $OKF_DOCS_HOME/scripts/okf-validate.ts --json docs/adrs/0004-okf-documentation-governance.md
```

Exit 0 means clean; exit 1 prints `❌ <path>: <rule> — <message>` per finding.

Two extra modes exist for documents that are not (yet) placed in a bundle:
`--draft` skips the position rules for a checkpoint such as
`.raw/runs/<runId>/draft-2.md`, and any file under a `templates/` directory is
validated in template mode, where `__PLACEHOLDER__` tokens satisfy format rules.
Every rule id, its exact message and its fix is in
`skill://okf-docs/references/validation.md` — read that file when a finding is
not self-explanatory, rather than guessing at the rule's intent.

**Validation is read-only.** When asked whether the docs are conformant, run the
validator and report what it says. Do not create, move or edit files as part of
answering that question.

## Reviewing and approving

The `pending` verb lists the documents nobody has reviewed: every `unverified`
document (no `verified.by`) and every `verified` approval whose `stale_after`
has passed. It is read-only.

The `verify` verb
(`verify <paths…> | --all [--by human:id] [--date YYYY-MM-DD]`) writes
`verified.by` and `verified.at`, sets `status: "stable"`, refreshes
`stale_after` from `staleAfterDays`, and appends the approval to `docs/log.md`.
It refuses a document that carries any other validator finding — approval never
launders a defect through a human's name — and refuses a reviewer id that is not
`human:`-prefixed, because an agent must never be able to sign a document off.

```bash
bun run $OKF_DOCS_HOME/scripts/okf-review.ts list
bun run $OKF_DOCS_HOME/scripts/okf-review.ts approve --all
```

Run the `verify` verb only when a human asks for it: a trust layer an agent can
sign for itself is decoration.

## Installing the pre-commit gate

The `hooks` verb (`hooks`) installs the validator into whatever pre-commit
mechanism this repository already uses — the Python `pre-commit` framework,
Husky, or a plain git hooks directory — bootstrapping a plain one only when none
exists yet. It never introduces a second, competing hook mechanism and never
rewrites a hook it did not add itself; an unrecognised mechanism is reported,
not overridden.

```bash
bun run $OKF_DOCS_HOME/scripts/install-hooks.ts
```

Not a bundle change — it touches repository tooling, not `docs/`, so it gets no
`log.md` entry.

## Project configuration

Read from `.omp/okf-docs.json`, or `.okf-docs.json` at the same search root when
the project has no `.omp/` directory — both are looked up by walking up from the
working directory, the primary name wins when both exist at the same level, and
either is read by the validator and both commands:

```json
{
  "bundleRoot": "docs",
  "obsidian": true,
  "agentId": "agent:omp",
  "humanId": "human:ibaou",
  "staleAfterDays": 180
}
```

Absent (both names, all the way up) means `bundleRoot: "docs"`,
`obsidian: false`, `agentId: "agent:omp"`, `humanId: null`,
`staleAfterDays: null`. `obsidian: true` is what makes templates emit the
`aliases`/`cssclasses` block and what turns on wiki-link integrity checking — in
a non-Obsidian project `[[…]]` means nothing and is not validated. `agentId` is
a prefix: append your own model id at write time, e.g.
`agent:omp/claude-opus-5`.

## Files

| Path                                              | Role                                                                         |
| ------------------------------------------------- | ---------------------------------------------------------------------------- |
| `skill://okf-docs/references/frontmatter.md`      | every field, required vs optional, worked examples                           |
| `skill://okf-docs/references/folder-structure.md` | the layout, reserved files, numbering, log discipline                        |
| `skill://okf-docs/references/validation.md`       | R0–R19: what each rule checks and how to fix it                              |
| `skill://okf-docs/templates/*.md`                 | one complete skeleton per type                                               |
| `skill://okf-docs/scripts/okf-validate.ts`        | the validator; invoke as `$OKF_DOCS_HOME/scripts/okf-validate.ts`            |
| `skill://okf-docs/scripts/okf-review.ts`          | lists and approves reviews; invoke as `$OKF_DOCS_HOME/scripts/okf-review.ts` |
| `skill://okf-docs/references/verb-new.md`         | the `new` verb: scaffolding procedure                                        |
| `skill://okf-docs/references/verb-validate.md`    | the `validate` verb: conformance reporting procedure                         |
| `skill://okf-docs/references/verb-pending.md`     | the `pending` verb: review backlog procedure                                 |
| `skill://okf-docs/references/verb-verify.md`      | the `verify` verb: approval-recording procedure                              |
| `skill://okf-docs/references/verb-hooks.md`       | the `hooks` verb: pre-commit installation procedure                          |
| `skill://okf-docs/scripts/install-hooks.ts`       | the hook installer; invoke as `$OKF_DOCS_HOME/scripts/install-hooks.ts`      |
