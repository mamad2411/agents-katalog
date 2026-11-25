---
name: proof-plan
description: "Prepare GPT-pro-ready proof planning or diagnosis bundles from a user's idea, packaging claims, sources, givens, and open questions for review without solving gaps locally."
---

# Proof Plan

Turn a raw proof idea into a compact GPT-pro prompt bundle that the user can
review before spending GPT-pro budget.

This skill is a product-manager-style standardization agent. Codex clarifies,
formalizes, and packages the user's idea: target claims, notation, source
materials, user-stated givens, unresolved questions, and the exact questions
GPT-pro should answer. Codex may perform only mechanical local checks needed to
avoid malformed handoffs, such as verifying that cited files exist, normalizing
notation, and flagging obvious inconsistencies from the supplied materials.
Proof-gap diagnosis, substantive repairs, central theorem claims, and lemma
completion belong in the GPT-pro task or another explicitly approved reviewer
path, not in local silent completion. Assume GPT-pro is mathematically strong
and broadly knowledgeable, but does not know this project's purpose, local
notation, user intent, or which source materials are authoritative.

## Output Directory

Create one run directory per idea:

```text
mindflows/<YYMMDDHH-num>/
```

Use local time for `YYMMDDHH`. Use a two-digit counter such as `01`, `02`, `03`; choose the next unused counter when several ideas are prepared in the same hour.

The minimal GPT-pro-facing bundle is:

```text
mindflows/<YYMMDDHH-num>/task.md
mindflows/<YYMMDDHH-num>/materials.md
```

Optional local-only files may be added when useful:

```text
mindflows/<YYMMDDHH-num>/codex-notes.md
mindflows/<YYMMDDHH-num>/review.md
mindflows/<YYMMDDHH-num>/sources/
```

Do not force a fixed section list into `task.md` or `materials.md`. Include only the information GPT-pro needs to do the assigned proof task well.

## Workflow

1. Read the user's idea and only the local files needed to understand notation, user-stated conditions, and source materials.
2. Normalize the idea into a GPT-pro task:
   - what GPT-pro is being asked to prove, disprove, repair, or diagnose;
   - which local materials are authoritative inputs;
   - which givens or constraints the user explicitly stated;
   - which unresolved points should be passed to GPT-pro as questions rather than resolved locally;
   - which claims are targets or context rather than locally established facts.
3. Write `task.md` as the GPT-pro-facing instruction. Keep project motivation short; include only enough context for GPT-pro to understand why the task matters.
4. Write `materials.md` as the GPT-pro-facing task materials. This may contain pasted definitions, notation, source excerpts, formal target statements, and pointers to files in `sources/`.
5. If needed, copy directly readable source snapshots into `sources/`. Prefer exact local material over memory.
6. Write `review.md` when the user needs an approval checkpoint. This file should make it easy for the user to see what GPT-pro will be asked and which inputs are being sent.
7. If Codex performed a mechanical local consistency check, record it in
   `codex-notes.md` or `review.md` with its dependency on the supplied
   materials. Do not add local proof claims to `task.md`; ask GPT-pro to
   diagnose or prove them instead.
8. Stop for user review unless the user already explicitly approved handoff packaging.

## GPT-pro Prompt Rules

`task.md` should tell GPT-pro to:

- give a direct conclusion first;
- separate proved statements, conjectures, imported results, repaired statements, and unsupported claims;
- classify gaps as detail-fillable, requiring additional assumptions, requiring an external theorem, or not currently provable from the supplied materials;
- label any assumption GPT-pro adds beyond the materials as a proposed repair;
- avoid inventing citations, theorem numbers, regret bounds, or proof obligations;
- use Obsidian-compatible Markdown math with `$...$` and `$$...$$`.

## Route-Neutral Task Rule

Assume GPT-pro is brilliant and needs the mathematical task, not Codex's proof
strategy. Codex must not search for, evaluate, sketch, hint at, exemplify, or
recommend possible technical routes in GPT-pro-facing files. Describe only the
target claim or diagnosis task, authoritative inputs, explicit givens,
constraints, and unresolved questions. Keep research goals, user taste, project
purpose, budget concern, orchestration state, local plausibility checks, legacy
skill comparisons, and any Codex-side route thoughts in `codex-notes.md` or
`review.md`, do not dispatch legacy proof workers unless the user explicitly
requests a legacy comparison, and never mark a statement as proved before
GPT-pro output and a later audit support it.
