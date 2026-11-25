---
name: upkeep
description: >
  Maintain AGENTS.md as the agent ops manual; create or repair CLAUDE.md so its
  entire body is exactly AGENTS.md; ensure CHANGELOG.md exists and Unreleased
  notes cover the session; in release-cut mode promote Unreleased to a dated
  version. Use when auditing or rewriting AGENTS.md, after implement or
  code-review, when layout/commands/boundaries change, when CLAUDE.md is
  missing or drifts, when CHANGELOG.md is missing/stale, or when commit/release
  passes release_intent with a confirmed version.
---

# upkeep

Keep `AGENTS.md` accurate and executable. Keep `CHANGELOG.md` current for
human/release notes. Do not edit `CONTEXT.md` or `knowledge/` here — that is
the `context` skill.

## Completion bar

Done when:

- `AGENTS.md` matches repo evidence
- `CLAUDE.md` exists and its full body is exactly the six characters `AGENTS.md` plus optional trailing newline
- `CHANGELOG.md` exists (Keep a Changelog shape) with session-notable items under `## [Unreleased]` when this run follows implement/code-review work — **or**, in release-cut mode, Unreleased promoted to dated `## [X.Y.Z…]` with cut content **and** a fresh empty/stub Unreleased (ship bullets must not remain under Unreleased; see [references/release-cut.md](references/release-cut.md))
- no glossary definitions were copied into `AGENTS.md`

## Workflow

### 1. Discover

Read existing `AGENTS.md` (if any), `README.md`, `CHANGELOG.md` (if any),
`CONTEXT.md` (for links only), manifests, scripts, and CI. Build a fact sheet
from evidence — never invent commands. Note whether **release context** is
present (`release_intent: true` + confirmed `version`).

**Done when:** facts are listed or explicitly marked unknown; mode known
(ordinary vs release-cut).

### 2. Ensure CLAUDE.md pointer

If `CLAUDE.md` is missing, or its content is anything other than `AGENTS.md`
(optional final newline allowed), write:

```text
AGENTS.md
```

**Done when:** pointer contract holds.

### 3. Ensure CHANGELOG.md

If `CHANGELOG.md` is **missing**, create a Keep a Changelog stub with
`## [Unreleased]` (Added/Changed/Fixed as needed) and a one-line pointer that
the project uses SemVer — except under release-cut rules in
[references/release-cut.md](references/release-cut.md) (hard-stop / waive).

If it **exists** and this upkeep follows **`implement`** / **`code-review`** /
**`commit`** maintenance (or the user asked for changelog hygiene):

1. Ensure a `## [Unreleased]` section exists (create near the top, above dated
   releases, if absent).
2. Add concise bullets for **user-facing or operator-facing** changes from the
   session that are not already listed — packaging/CI/workflow, skills
   behavior, install contract, ADRs. Skip pure typo/noise.
3. Apply **release-cut** when context warrants — see
   [references/release-cut.md](references/release-cut.md). Without release
   context: do **not** invent a version bump.

**Done when:** changelog exists; Unreleased reflects the session (ordinary); or
in release-cut, evidence in
[references/release-cut.md](references/release-cut.md) holds — dated
`## [<authorized-version>]` with cut content **and** Unreleased empty/stub
(not still holding those bullets).

### 4. Draft or patch AGENTS.md

Prefer operational sections: overview, structure, setup, validation, style,
git/PR, boundaries, security, references.

Link to `CONTEXT.md` and `docs/adr/` instead of restating glossary or ADR bodies.

Preserve any **Test index (OKF)** one-liners under Testing — `tdd` owns
appending them; `upkeep` keeps them accurate and linked. Do not expand them
into suite dumps.

Mention `.scratch/` in structure/boundaries when the repo uses that pad
(ignored; agent dumps only).

Mention `CHANGELOG.md` in references (and structure if useful) when the file
exists.

Cite evidence-backed CI/workflow commands (e.g. `.github/workflows/`) when
present.

When this session added or changed skill `scripts/`, or Code style needs a
scripts policy line: ensure `AGENTS.md` **Code style** links
[Skill scripts vs LLM](../../knowledge/skill-scripts.md) (one line + link —
do not paste the essay). Soft-skip the link if that OKF page is absent in a
consumer repo.

**Done when:** every command cited is evidence-backed; boundaries include
“skills only under `skills/`” and the post-`implement`/`code-review` hook to
run `upkeep` then `context`; Test index preserved when present; skill-scripts
pointer present when this library’s OKF has that concept.

### 5. Validate

Check paths exist; root vs nested instructions do not conflict; no secret
material.

**Done when:** file is safe to commit from an ops perspective.

## Boundaries

- Do not edit `CONTEXT.md` or `knowledge/`.
- Do not paste the full [skill-scripts](../../knowledge/skill-scripts.md)
  essay into `AGENTS.md` — ops gets a one-line pointer; depth stays in OKF.
- Do not invent a SemVer bump or promote Unreleased → dated without
  `release_intent` + confirmed version.
- Do not invent CHANGELOG content to unblock a release when CHANGELOG is
  missing — hard-stop or honor explicit waive.
- Do **not** “heal” setup **B** repos by re-adding `/docs/prd/` (or equivalent)
  ignore lines — PRD track-vs-ignore is owned by **`setup-bmurrtech-skills`**
  ([ADR 0013](../../docs/adr/0013-ADR-prd-tracking-choice.md)); upkeep has no
  gitignore PRD mandate.

## Template

Use [references/AGENTS.template.md](references/AGENTS.template.md) as a starting
shape; delete irrelevant sections.
