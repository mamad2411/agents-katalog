---
name: craft-skill-spec
description: Design a new skill (or skill suite, subagent, or plugin) using CraftKit's current radar guidance. Use this whenever a user wants to create, architect, or spec a new skill-like artifact and needs help deciding the artifact class, what patterns to adopt/avoid, and the file or package shape before writing `SKILL.md` — including requests like "design a skill", "spec this skill", "make a meta-skill", "design a subagent", "spec a plugin", or "what should this be — skill or subagent?"
---

# craft-skill-spec

## Purpose

Design a new skill spec using CraftKit's current canonical view of good skill-authoring patterns.

This is not a generic skill-creation walkthrough. It is the decision layer that turns a rough skill idea into a concrete, reviewable spec: what the artifact should do, what patterns it should adopt or avoid, how much freedom it should allow, what files it needs, and how it should be evaluated.

Use it when the question is not just "how do I write a skill?" but "what kind of artifact should this become right now?"

## How it differs from related skills

- `craft-scaffold` structures vague requests into a plan. `craft-skill-spec` is narrower: it produces an **artifact-specific design spec** informed by the current radar.
- `craft-survey` studies prior art. `craft-skill-spec` starts from the already-curated `references/radar/current.md` and only dips into snapshots when a watched area matters.
- `craft-tune` improves an existing skill. `craft-skill-spec` is for designing a new one or reshaping a skill before the draft exists.
- generic `skill-creator` guidance explains how skills work broadly. `craft-skill-spec` makes a concrete CraftKit judgment for *this* proposed skill.

## Inputs

- the rough skill idea
- target users or agents
- expected outcome
- any hard constraints
- optional related assets or prior art

If the user does not state all of these, infer what is safe to infer and keep moving.

## Required reads

Before producing the spec:

1. Read `references/radar/taxonomy.md` and classify the artifact: `single skill`, `skill suite`, `subagent`, or `plugin`.
2. Read `references/radar/current.md`.
3. If the target touches a `Watch` area, or if the artifact class is `subagent` or `plugin`, consult `references/radar/policy.md` and the relevant entries in `references/radar/sources.md`.
4. Read the newest relevant snapshot in `references/radar/` only when the policy requires fresh context.
5. Read an existing CraftKit skill only when it is directly adjacent to the proposed job.

Do not start with open-ended web research unless the user explicitly asks for it. The point of this skill is to use the curated internal layer first.

## Steps

1. Classify the artifact first. If it should really be a `subagent` or `plugin`, say so before drafting a skill-shaped answer.
2. Restate the proposed artifact's real job in one sentence. If you cannot state the job cleanly, the spec will drift.
3. Define the wedge. Name what the artifact should do and what it should explicitly not try to do.
4. Apply the current radar. Pick the relevant `Adopt`, `Avoid`, and `Watch` items from `references/radar/current.md`.
5. Decide the degree of freedom. Choose whether the core should be high-freedom guidance, medium-freedom templates/pseudocode, or low-freedom exact commands/scripts.
6. Decide the file or package shape. Start from the smallest viable artifact class and add `references/`, `scripts/`, `templates/`, agents, or plugin surfaces only when the proposed job clearly earns them.
7. Draft the trigger surface if the artifact includes one or more skills. Write frontmatter `description` lines that say what each skill does and when it should be used.
8. Draft the first eval plan. Name 3-5 realistic prompts and the key checks that would tell you whether the design is working.
9. Surface only the open questions that would materially change the architecture. Drop wording nits.

## Decision rules

### Adopt

Treat radar `Adopt` items as defaults, not suggestions. If you reject one, say why.

### Avoid

Treat radar `Avoid` items as hard warnings. If you knowingly violate one, mark it as an explicit tradeoff.

### Watch

Use `Watch` items to decide whether to:

- keep a pattern out of the core spine
- isolate it in a guide, example, or optional reference
- postpone the decision until later

Do not silently convert a `Watch` item into a default.

## Output format

### Summary
One short paragraph: what artifact is being proposed, for whom, and why this shape is better than a generic skill-creation pass.

### Artifact class
- class
- why this class fits better than the next smaller one
- escalation note if the boundary is close

### Artifact thesis
- job
- non-goals
- target users or agents
- success condition

### Radar judgment
- **Adopt** — 3-5 patterns from `references/radar/current.md` that should shape this skill, each with a one-line why
- **Avoid** — 2-4 patterns that would hurt this skill, each with a one-line why
- **Watch** — only the watched patterns that actually matter here, with a one-line handling rule

Every item must be specific to the proposed skill. Do not repeat the radar file mechanically.

### Design spec
- freedom level
- workflow shape
- output shape
- progressive disclosure plan
- file or package plan

For the file or package plan, name concrete paths and one-line purposes. Start with the smallest viable set.

### Trigger draft
Provide this section only when the artifact includes one or more skills.

Provide:

- `name`
- frontmatter `description`
- one sentence on why the trigger wording should discover well

### Eval plan
- 3-5 realistic user prompts
- 3-6 checks the outputs should satisfy
- one likely failure pattern to watch in the first draft

### Open questions
0-3 items only. If none remain, write `none - current constraints are sufficient`.

## Guardrails

- keep the spec narrower than the user's first instinct if that produces a stronger skill
- do not turn the output into a survey report
- do not import provider-specific quirks into the core skill unless the skill is explicitly platform-bound
- prefer one default path over many equal-weight branches
- if a script, template, reference file, subagent, or plugin surface is proposed, name the repeated pain it removes

## Failure modes

- producing a generic "good skill" checklist instead of a real spec for this skill
- repeating every radar item instead of selecting the ones that matter
- proposing too many files before the core `SKILL.md` shape is earned
- forcing a plugin or subagent when a single skill would do
- treating `Watch` items as fashionable defaults
- skipping the eval plan and leaving the design untestable

## Example

### Input

Design a meta-skill that helps create good new skills without re-researching the web every time.

### Output

**Summary**
Propose a skill-design spec that turns CraftKit's current radar into a stable decision layer for new skill creation.

**Artifact class**
- class: single skill
- why this class fits better than the next smaller one: there is no smaller reusable artifact than a single skill for this job
- escalation note: escalate to a plugin only if the solution later needs bundled agents, hooks, or MCP servers

**Artifact thesis**
- job: design a new skill spec from a rough idea
- non-goals: writing the full skill body, broad web research on every run
- target users or agents: CraftKit maintainers designing new skills
- success condition: output is specific enough that another agent can draft `SKILL.md` without guessing the architecture

**Radar judgment**
- Adopt: concise spine plus progressive disclosure — because the skill will accumulate design logic quickly
- Adopt: trigger-oriented descriptions — because discovery quality is central for new skills
- Adopt: eval-first tightening — because the first draft should already be testable
- Avoid: monolithic all-in-one files — because design rationale and deep examples should not bloat the spine
- Watch: script-heavy packaging — only add scripts if the design process repeats a deterministic transform

**Design spec**
- freedom level: medium
- workflow shape: read radar -> define wedge -> choose patterns -> draft trigger -> draft evals
- output shape: summary, radar judgment, file plan, trigger draft, eval plan
- progressive disclosure plan: keep the spine short; put deeper decision rubrics in `references/`
- file plan:
  - `skills/craft-skill-spec/SKILL.md` — operating workflow and output contract
  - `skills/craft-skill-spec/references/spec-checklist.md` — optional deeper review checklist

**Trigger draft**
- name: `craft-skill-spec`
- description: Design a new skill (or skill suite, subagent, or plugin) using CraftKit's current radar guidance...
- why it should discover well: it names both the task and the user phrasings around designing or specing a skill

**Eval plan**
- prompts: "design a release-note skill", "spec a jira-triage skill", "design a subagent for code review", "should this be a skill or a plugin?"
- checks: output names the artifact class explicitly; adopt/avoid/watch are present; file or package plan is concrete; trigger draft appears only when the artifact includes skills; eval plan is present
- likely failure pattern: drifting into generic skill advice or forcing a skill-shape onto a subagent/plugin request

**Open questions**
- none - current constraints are sufficient

## References (load on demand)

- `references/radar/taxonomy.md` — artifact classes and escalation path
- `references/radar/current.md` — current canonical judgment for skill-authoring patterns
- `references/radar/sources.md` — live reference registry for skills, subagents, plugins, and cross-platform guidance
- `references/radar/policy.md` — when canon is enough and when fresh live-source review is required
- `references/radar/decision-log.md` — why a pattern moved between adopt / avoid / watch
- `references/radar/TEMPLATE.md` — if a new snapshot or event-based addendum is needed
- `references/spec-checklist.md` — structured review pass for checking whether the spec is specific, narrow, and ready to turn into `SKILL.md`
