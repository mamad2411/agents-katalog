---
name: extract-project-context
description: GREENFIELD / Path-B project-context bootstrap — derives mission, domain, personas, KPIs, anti-goals from a user PROMPT when there's no codebase to read yet, and writes ai/project-goals.md + ai/users-and-personas.md + ai/business-domain.md. For EXISTING codebases the canonical pipeline (extract-codebase-overview → extract-business-context → Phase 4.7b) owns these targets; this skill is the greenfield path only.
kind: skill
pack: learning
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash]
---

# Skill: extract-project-context

The **greenfield** project-context bootstrap. Without it, a brand-new project (empty folder + a prompt) has no durable record of "what is this" — every session re-derives it from the prompt. This skill captures the prompt-derived identity ONCE into durable files.

> **Scope boundary (existing-codebase path is owned elsewhere).** When the target already has source code, the canonical pipeline owns the `ai/` context targets:
> - `extract-codebase-overview` → `.claude/_extracted-codebase.md` (modules, stack, conventions, signals).
> - `extract-business-context` → `.claude/_extracted-business.md` (mission, personas, KPIs, business model, anti-goals).
> - Phase 4.7b → projects `_extracted-business.md` into `ai/project-goals.md`, `ai/users-and-personas.md`, `ai/business-model.md`, `ai/competitive-context.md`, `ai/roadmap.md`.
>
> That pipeline has mechanical halts + provenance markers this skill does not, so it wins wherever
> the two could both run. **This skill runs ONLY when there is no code to read** (greenfield / CREATE
> mode from a prompt). A directory holding a README, a manifest and git history but no source tree is
> still greenfield and is still this skill's job — Step 0 mines those signals — but the first source
> file that appears moves the work to the pipeline above, permanently.

## Premise

- Real source is the truth. Read READMEs + manifests + git history + sibling repos before populating any facet — and on greenfield, parse the prompt explicitly before falling back to defaults.
- Every fact written to `ai/business-domain.md` / `ai/project-goals.md` / `ai/users-and-personas.md` cites its source (README path, manifest field, commit signal, prompt line, or user answer).
- Inferred values are flagged as inferred with the signal they derive from; default values from the prompt are flagged as defaults the user can override.
- Empty extraction is honest — `_TBD — ask user_` for a facet no source covers is a valid output; the gap report surfaces them.
- Fabrication — inventing a persona from training-data tropes, a KPI from product-category memory, a competitor never named — locks the wrong identity into every downstream agent prompt.

## Mechanical halt

- Hand-wave facet content — `enterprise customers`, `typical SaaS users`, `appears to target`, `etc.`, `...`, a non-`_TBD_` answer without a cited source — REFUSE to write.
- Re-derive from a real source OR write `_TBD — ask user_` and surface the gap.
- If a source is genuinely absent (no README, no manifest description, no git history, no prompt content for the facet), record `<NOT-DETECTED: <facet>: <sources searched>>` in the report's gaps section.
- Never synthesize a persona / KPI / competitor / business-model to make the file feel complete — Step 3's consolidated question is the only mechanism for filling unknowns, not LLM imagination.

## When to use

- **Greenfield only**: `/setup-project` in CREATE mode (Path B — prompt, no codebase). This is the canonical use.
- A directory that holds only README / manifest / git metadata and no source tree — still greenfield; Step 0 mines what is there.

**Do NOT use** on an existing codebase — `extract-codebase-overview` + `extract-business-context` + Phase 4.7b own those targets (see the scope boundary at the top). On stale-context refresh for an existing project, run `/refresh-knowledge`, which re-runs the canonical pipeline, NOT this skill.

## Prerequisites

- Repository (or empty folder + user prompt).
- Read access to: `README*`, `package.json`/equivalent manifests, `.git/`, sibling repos in workspace if any.

## Procedure — ONE path

There used to be two. Path A ("a repo dir exists but has no source code to analyze") was deleted:
its own gate was *zero source files*, and its step 5 ran `/setup-project` Phase 2.x business-domain
and technical-signal detection — which reads source files. Unreachable under its own precondition.
Its steps 6-7 also wrote the same seven `ai/` targets `extract-business-context` + Phase 4.7b own,
which is the collision the scope boundary at the top of this file forbids. What was worth keeping
from it — README / manifest / git / sibling mining — is Step 0 below, and it now runs whenever those
signals exist rather than only in a mode that could not fire.

### Step 0 — Mine whatever non-source signal is on disk (optional; skip silently if none)

A greenfield directory is rarely empty. Run these four before parsing the prompt, and record which
of them produced anything — a facet sourced from a README is `[found:]`, the same facet guessed from
the prompt is a default the user may override, and the report must not blur them.

1. **README** — `find . -maxdepth 3 -iname 'README*' -not -path '*/node_modules/*' -not -path '*/.git/*'`.
   Take: one-line description (first para after the title), `## Features` bullets, mission/vision if
   explicit, and any `Built with` / `Tech stack` / badge stack signal.
2. **Manifests** — `find . -maxdepth 3 \( -name 'package.json' -o -name 'pyproject.toml' -o -name 'composer.json' -o -name 'go.mod' -o -name 'Cargo.toml' -o -name 'Gemfile' \) -not -path '*/node_modules/*'`.
   Take: name / version / description, top-20 dependencies (stack signal), and the lint / test /
   build / dev scripts (Phase 4.1 reads these for the permission allowlist).
3. **Git history** — `git log --since='6 months ago' --pretty=format:'%s' | head -100`, clustered by
   conventional-commit prefix. Gives cadence and active areas. Absent on a brand-new repo; that is a
   normal outcome, not a failure.
4. **Sibling repos** — parent dir `PROJECTS.md` / `pnpm-workspace.yaml` / `lerna.json`; for each
   sibling take its README one-liner and the relationship its name implies.

**Hard stop:** if these turn up a populated source tree, this skill is the wrong tool — hand off to
`extract-codebase-overview` + `extract-business-context` per the scope boundary above and write
nothing. Mining a manifest is not walking a codebase, and the moment there is a codebase to walk,
the pipeline with the census and the provenance markers owns the answer.

### Step 1 — Parse the prompt for facets

Mission · domain keywords · stack · users/personas · constraints and anti-goals. Anything Step 0
already sourced stays sourced; the prompt fills the rest.

### Step 2 — Identify gaps

Facets neither Step 0 nor Step 1 covers. These are the only things the question in Step 3 asks about
— re-asking for something the README already answered is how a user learns to stop reading the
question.

### Step 3 — Ask ONE consolidated question, with the sourced values shown as defaults

```
I extracted:
- Mission: <X>        [from README.md:3 | from your prompt]
- Domain: <Y>         [from your prompt]
- Stack: <Z>          [from package.json dependencies]

To complete the setup, please confirm or fill in:
1. Primary user persona: <inferred default | ASK>
2. Business model: <inferred default | ASK>
3. Top 3 KPIs that would mean "this works":
4. Anti-goals (what this project is NOT):
5. Maturity stage: idea | prototype | MVP | production

Reply with corrections or "all defaults look good".
```

### Step 4 — Write the three files this skill owns

`ai/project-goals.md`, `ai/users-and-personas.md`, `ai/business-domain.md` — the same three the
frontmatter names, and no others. `ai/business-model.md`, `ai/competitive-context.md`,
`ai/roadmap.md` and `.claude/codebase-profile.md` are **not** this skill's to write: Phase 4.7b
projects the first three out of `_extracted-business.md`, and Phase 2 owns the profile. Writing them
here is how a greenfield run ends up with two authors for one file and no way to tell which won.

Anything still unknown after Step 3 is `_TBD — ask user_`, listed in the report's gaps section.

## Output

```
## extract-project-context — extraction report

Mode: greenfield-from-prompt

Files written (three — the rest belong to Phase 4.7b and Phase 2):
  ai/business-domain.md              (domain: <X>, signals: <list>)
  ai/project-goals.md                (mission ✓, KPIs <count>, anti-goals <count>)
  ai/users-and-personas.md           (personas: <count>)

Step 0 signal sources that fired: <README | manifest | git-history | siblings | none>

Auto-extracted from:
  - <path>/README.md (mission + setup)
  - <path>/package.json (stack + scripts)
  - git history (velocity + active areas)
  - <N sibling repos>

Gaps requiring user input (placeholder _TBD_ written):
  - ai/project-goals.md KPIs (ASK)
  - ai/users-and-personas.md secondary persona (no signal)

Next step:
  - Review the generated files.
  - Fill in _TBD_ placeholders.
  - Run /refresh-knowledge (or @knowledge-curator mode regenerate) to regenerate the compact derived files (_session-digest, _decision-index, _convention-cheatsheet); /audit-knowledge then checks them read-only.
```

## Failure modes

- **README missing or unhelpful** (template README with placeholder text): rely on manifests + git history + ASK.
- **Multiple READMEs in monorepo**: read each sub-project's README; aggregate at workspace level.
- **Step 0 finds a real source tree**: stop and hand off. This is a routing bug upstream, not a mode of this skill.
- **No git history yet** (brand-new repo): skip the history step; rely on prompt.
- **Domain detection ambiguous** (signals from 2+ domains): ASK with the candidates as options.
- **User refuses to answer the consolidated question**: write `_TBD_` for every unknown; flag in report.

## See also

- `/setup-project` CREATE mode (Path B, greenfield) — the canonical invoker.
- `extract-codebase-overview` + `extract-business-context` + Phase 4.7b — the **existing-codebase** owners of these `ai/` targets; this skill defers to them.
- `/refresh-knowledge` — re-runs the canonical pipeline on existing projects to catch drift (NOT this skill).
- `ai/business-domain.md`, `ai/project-goals.md`, `ai/users-and-personas.md` — destinations.
- `knowledge-curator` agent — uses this skill's output to maintain compact derived files.
