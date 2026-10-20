---
name: interrogate
description: Multi-model adversarial review — independent reviewers challenge a change from different angles to surface blind spots.
disable-model-invocation: true
---

# Interrogate

Spawn one reviewer per configured model to adversarially review code changes. Each model gets the same prompt and rubric. The adversarial signal comes from model diversity, not assigned personas.

The deliverable is a synthesized verdict. Do NOT auto-apply changes.

## Step 1, Determine Scope

Identify what to review from context:

- If the user points at specific files or a diff, use that
- If on a feature branch, run `git diff main...HEAD` (or the appropriate base branch) for the full changeset
- If the user's message references recent work, gather the relevant files

Package the diff (or file contents) plus any surrounding context files the reviewers need to understand the code.

## Step 2, State the Intent

Before spawning reviewers, state the intent explicitly. Derive this from:

- The user's message
- Commit messages
- PR description if one exists
- The code itself

Write one clear paragraph. If you're unsure about the intent, ask the user before proceeding.

## Step 3, Spawn Reviewers

Launch all reviewers in a single message using the `Agent` tool. **Three reviewers, hard cap** — see [Fan-out](#fan-out).

Cross-model diversity is the whole mechanism here: three reviewers on one model is three correlated opinions, not a panel. Resolve the `panel` tier to three *different* models where the harness offers them, and say so in the report when it cannot.

| Subagent | Tier |
|----------|------|
| Reviewer A | `panel`, first model |
| Reviewer B | `panel`, second model |
| Reviewer C | `panel`, third model |

For each reviewer:
- `subagent_type`: `general-purpose`
- `model`: the corresponding `panel` entry from the fan-out policy
- `readonly`: `true`

If a model slug is rejected as unresolvable, check the valid slugs in the `Agent` tool's error message, pick the closest equivalent (prefer the highest-reasoning tier of the same family), and spawn with that. Do not block the review on a slug issue; note the substitution in the report and fix the policy file afterward. If a policy entry is `inherit-parent` or `auto`, omit `model` instead — those are aliases, not broken slugs.

Read `references/reviewer-prompt.md` and fill in the template with:
1. The stated intent
2. The diff or file contents
3. The review rubric from `references/rubric.md`
4. The code-quality lens from `references/code-quality-review.md`

The same filled template goes to all reviewers, so every model applies the code-quality lens.

## Step 4, Synthesize

As results come back, build a unified picture:

1. **Parse all findings** from the reviewers
2. **Identify consensus**. Findings raised by 2+ models independently are highest signal.
3. **Identify lone-model findings**. Still worth reading, but weight accordingly.
4. **Deduplicate**. Different models may describe the same issue differently. Merge these and note which models raised it.
5. **Note disagreements**. If one model flags something and another explicitly says the opposite, that's useful context for the verdict.

## Step 5, Lead Judgment

You are the lead reviewer, a pragmatic senior engineer, not a neutral aggregator.

Read `references/lead-judgment.md` for the full framework.

Categorize every finding using these buckets:

- **Act on**. Real issues affecting correctness, security, or maintainability given the actual goals. These would block a real PR.
- **Consider**. Legitimate points, but you're not sure they outweigh the cost of addressing them right now. Worth the user's attention.
- **Noted**. Technically valid but not actionable. Context-dependent, premature optimization, or low-impact given the current stage.
- **Dismissed**. Wrong, nitpicky, or missing context. Brief explanation why.

For each finding, include:
- Which model(s) raised it
- The category (act on / consider / noted / dismissed)
- A one-line rationale for the categorization

## Output Format

Present the verdict in this structure:

### Intent
> [The stated intent paragraph from Step 2]

### Reviewers
- Reviewer [label]: [model name], [N findings] (one bullet per reviewer)

### Act On
[Findings that should be addressed. For each: description, which models raised it, why it matters.]

### Consider
[Findings worth thinking about. For each: description, which models raised it, tradeoff involved.]

### Noted
[Valid but low-priority. Brief list.]

### Dismissed
[Rejected findings with brief rationale.]

### Agreement Map
[Where did models agree, where did they diverge, and what does the pattern of agreement/disagreement tell us?]

## Fan-out

Caps are **ceilings, not targets**, and they are hard.

| Role | Tier | Cap |
| --- | --- | --- |
| Reviewers | `panel` | 3 |

`panel` is the top rung of the effort ladder (`scan` < `scoped` < `judgment` <
`divergent` < `panel`) and the most expensive thing this plugin does. A tier
names a rung, never a model; the mapping is per-harness and lives in the
fan-out policy `/setup-ph-build` writes. With no policy file, use three
distinct models of the highest tier available.

Upstream's text anticipated a fourth reviewer (the A/B/C/D labels). Three is the
ceiling here.
