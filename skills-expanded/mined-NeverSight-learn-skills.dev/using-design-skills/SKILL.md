---
name: using-design-skills
description: Meta-router and multi-agent conductor for design work that needs skill selection or a multi-stage pipeline — visual frontend (web pages, landing pages, product UI, mobile screens), data visualization, HTML deliverables (reports/diagrams/plans), artifacts, motion polish, and module/API interface design. The STABLE unified entry point — member skills churn underneath, this router discovers them live, picks one direction authority, delegates image-generation stages to Codex workers, and closes every pipeline with an evidence-first anti-slop quality loop. Do NOT invoke for a one-line CSS/copy tweak, for backend-only work, or when the user explicitly names a single member skill for a single-skill-sized task — those go direct.
---

# using-design-skills

You decide **which** design skills a task needs, in **what order**, and **who
executes each stage**, then defer to them. Member roster, role tables, and
executor details live in `references/design-roles.md` — read it at pipeline
composition time; never route from memory of it.

## BYPASS

- Backend-only / non-UI work · one-line CSS or copy tweak (inline; at most
  consult DESIGN.md) · the user names ONE member skill for a
  single-skill-sized task → go direct.
- Loop-shaped non-design work (audits, plan→build) → `using-workflows`.

## TRIGGER

Any deliverable whose value is visual or interface-shaped: pages, screens,
HTML reports/diagrams/plans, artifacts, dashboards, motion, mockups,
module/API interface design.

## QUESTIONS — compose the pipeline (answer in order)

Q1 **Base deliverable — who owns the output?** Diagram / report / plan page →
the HTML trio or `plannotator-visual-explainer` · web/mobile → target stack ·
Artifact → artifact file · data file → `data-report` · module/API/domain →
Pipeline D · token work → DESIGN.md itself · mockup-only → imagegen output ·
"would this work?" → `prototype`, alone, no loop.

Q2 **Variant.** Existing interface → audit-first (authority critiques the
CURRENT render before rebuild). New + ambitious + imagegen available →
image-first (imagegen ⇒ image-to-code ⇒ loop); ordinary task → direct build,
say so when skipping imagegen.

Q3 **Orthogonal specialists (additive).** Charts → `dataviz` if it resolves
under SELECT (else apply charting best-practices inline — no dedicated chart
skill is guaranteed installed). Artifact → `artifact-design` (a bundled skill;
MANDATORY before publishing). Motion/gesture → `apple-design`. Constraint sets,
loaded inline.

Q4 **Executor per stage** — the executor table in
`references/design-roles.md`. Direction runs INLINE; imagegen/image-to-code →
agent-tmux codex persistent worker; non-trivial build → agent-tmux claude persistent
worker; every review → FRESH headless one-shot, never the author.

Q5 **Verifier.** Render in scope → the visual quality loop below (full Gate 0
screenshot evidence). DESIGN.md-only → document-only evidence (file
hash/commit, token completeness, contrast math). Pipeline D → non-visual
loop: design comparison judged against `codebase-design` depth criteria by a
fresh reviewer, verdict still PASS/BLOCK. `prototype` → none.

## SELECT — discover live, then bind roles

1. `ls ~/.claude/skills/ ~/.agents/skills/ 2>/dev/null | sort -u`, cross-check
   against THIS turn's active available-skills listing — a directory copy that
   isn't loaded is not invocable; a member gated `disable-model-invocation:
   true` (check `head -8`) is reached by reading its SKILL.md inline, never
   via `Skill()`.
2. Exactly ONE direction authority for a visual pipeline (ZERO for Pipeline
   D / prototypes / trivial tweaks). Never stack two — they fight. An unknown
   skill is never auto-promoted to authority.
3. A prior member that is absent or uncallable → STATE the absence and the
   substitute in your plan; an empty role → degrade explicitly. Never
   substitute silently.
4. Read each selected skill's SKILL.md before its stage runs.

## DEFER — cross-stage contracts

- **DESIGN.md**: the direction stage WRITES it (prefer `design-md`; fall back
  to plain Read/Write and say so); every later stage and every worker prompt
  READS it. Workers have no chat memory — never carry direction in chat only.
- **Dispatch**: tmux dispatches route through `using-tmux-agent-tools`;
  worker prompts from `delegation-templates`; tiers per
  `~/.agents/rules/model-dispatch.md` §5, verification §7. Fanout/dialogue
  need the user's exact authorization.
- **Loop topology (fixed)**: the BUILDER is a persistent worker — BLOCK
  findings return to the SAME builder (worker-reuse protocol). Each REVIEWER
  is a fresh headless one-shot, never the builder, never reused.
- Worker-prompt addendum: "DESIGN CONTEXT: read `{repo}/DESIGN.md` first;
  conform to its tokens. SKILL: read and follow `{member-SKILL.md}` first."

## The quality loop — no pipeline ends at "built"

**Gate 0, fail-closed:** the reviewer RECORDS build identity (hash/commit),
artifact path/URL, screenshot path(s), viewport(s), full-page/uncropped.
Desktop AND mobile for responsive deliverables. Missing/stale/cropped
evidence → UNCONFIRMED → overall BLOCK; never PASS on code-only review.
(Document-only exception: DESIGN.md-only deliverables record file
hash/commit instead — the instant any render exists, full contract resumes.)

**Rubric, in order:** 1. THE SLOP TEST — the authority's audit rubric;
generic gradient-hero / emoji-bullet / card-grid sameness = BLOCK regardless
of correctness. 2. Prose discipline — no filler, scannable hierarchy.
3. DESIGN.md conformance. 4. The stage's frozen ACCEPTANCE criteria.

**Report contract:** per-item PASS / FAIL / UNCONFIRMED + one-line reason,
findings tagged persistent/new/regression/evidence-gap, all blockers in ONE
pass, final line exactly `VERDICT: PASS` or `VERDICT: BLOCK`, quoted
verbatim in your report.

**Rounds:** BLOCK → same persistent builder fixes → fresh reviewer
re-audits. Hard cap two fix rounds, then route by CAUSE: same-root failures
+ wrong-direction signals (`judgment-rubrics.md` §4) → back to direction ·
evidence-gap → repair evidence path, re-audit · new/regression → triage
separately · otherwise → stop and ask the user with the failure trail.
PASS → persist tokens via design-md, report with the evidence bundle.
"Built and audited: PASS" is a completion claim; "built" alone is not.

## NOT-FOUND

A needed role has no installed member → degrade the pipeline explicitly and
say what was skipped — never fake a stage. Member contracts: each skill's
own SKILL.md · roster/roles/executors: `references/design-roles.md` ·
worker mechanics: `tmux-agent-tools` · prompts: `delegation-templates`.
