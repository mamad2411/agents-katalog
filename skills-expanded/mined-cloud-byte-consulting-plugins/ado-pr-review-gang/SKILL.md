---
name: ado-pr-review-gang
description: >-
  Adversarial Azure DevOps pull request review using Advocate, Skeptic, and
  Judge roles with fresh independent context. Self-contained for Copilot,
  Codex, Cursor, OpenCode, and Gemini (Claude agents optional). Fetches PR data
  via az repos pr first (Azure DevOps MCP for gaps). Use for PR quality gates,
  merge recommendations, and structured multi-perspective review of Azure Repos
  PRs.
---

# Azure DevOps PR Review Gang

## Purpose

Run a three-role adversarial review of an Azure DevOps pull request and produce
a Judge verdict with a merge recommendation. Role instructions below are the
portable source of truth; Claude `agents/pr-*.md` files mirror the same lanes.

## Roles (embedded)

| Role | Lane |
|---|---|
| Advocate | Defend author intent with evidence; surface missing-evidence as defensive gaps |
| Skeptic | Demonstrate falsification: concrete paths that break claims or produce wrong results |
| Judge | Synthesize Advocate and Skeptic outputs into a verdict and merge recommendation |

Invoke these roles only through this skill so each role gets fresh independent context.

### Advocate

Reconstruct intent from the PR evidence pack; defend choices with concrete
references; surface unsupported claims and framing gaps as genuine weaknesses
the author should close.

Stay in lane. Do not try to be balanced. Do not pretend certainty you lack.
Cite file paths, hunks, or PR threads for every material claim. Fetch additional
PR detail with `az repos pr` if the evidence pack is incomplete. Read-only.
No em dashes in ADO-facing comments.

### Skeptic

Show the concrete input, sequence, or path that breaks a claim or produces a
wrong result. Coverage gaps in claimed enforcement and cross-boundary bugs are
yours.

Be aggressive; the Advocate will defend false positives. An unsupported claim
alone is Advocate territory; falsify it (show the violating path) before you
re-raise. Cite evidence. Read-only. No em dashes in ADO-facing comments.

### Judge

Structural placement and consequence (layer, owner, blast radius, reversibility,
cleanup cascade) plus final synthesis of Advocate and Skeptic outputs into a
single verdict. Prefer doing the Judge lane well over duplicating Advocate or
Skeptic findings. Cite evidence. Read-only unless the user explicitly approves a
PR action. No em dashes in ADO-facing comments.

## Triggers

1. **Manual invoke** (supported now): user requests a gang review for a PR id.
2. **On PR creation** (document only): customer can wire a pipeline or webhook that invokes this skill. Hooks and customer pipeline YAML are not shipped in this plugin.

## Non-negotiable defaults

1. Fetch PR data with Azure CLI first:

```bash
az repos pr show --id <pr-id> --organization "$ORG" --project "$PROJECT" --output json
az repos pr list --organization "$ORG" --project "$PROJECT" --status active --output json
```

Use Azure DevOps MCP only for gaps (threads, file content, work-item links) when CLI coverage is insufficient.

2. Run Advocate, Skeptic, and Judge with **fresh independent context**. Do not let one role see another's draft before independent analysis completes.
3. Judge produces the final verdict and merge recommendation after reading the other two outputs.
4. Read-only by default. Do not approve, complete, abandon, or push to the PR without explicit user approval.
5. No em dashes in ADO-facing review comments.
6. Deep counterargument stages / depth flags are **TODO for Phase 2**. For this scaffold, run a single independent pass per role, then Judge synthesis.

## Host behavior

- **With subagents** (Claude Code agents, Cursor agents, similar): spawn Advocate, Skeptic, and Judge as separate contexts using the role sections above (or Claude `pr-advocate` / `pr-skeptic` / `pr-judge` mirrors).
- **Without subagents**: run three sequential passes in one session. After Advocate completes, clear working assumptions before Skeptic. Only then open both outputs for Judge. Do not blend lanes mid-pass.

## TODO (Phase 2 deepen)

- [ ] Counterargument stage (Advocate/Skeptic respond to each other) with depth flags (`fast` / `thorough` / `full`)
- [ ] Clarification probes for unresolved High/Critical disputes
- [ ] Optional structural-direction lane separate from Judge if a four-role panel is needed
- [ ] Customer-owned Azure Pipelines examples for on-PR-creation invoke

## Workflow

1. Confirm organization, project, PR id, and review focus (security, correctness, docs, architecture).
2. Fetch PR metadata, changed files summary, and linked work items via CLI (MCP for gaps).
3. Run Advocate with the PR evidence pack.
4. Run Skeptic with the same evidence pack (independent context).
5. Run Judge with the evidence pack plus Advocate and Skeptic outputs.
6. Deliver Judge output: verdict, blocking issues, non-blocking suggestions, merge recommendation (`approve` / `request changes` / `comment only`), and residual risks.

## Output shape (Judge)

```markdown
## Verdict
<one-paragraph synthesis>

## Merge recommendation
approve | request changes | comment only

## Blocking issues
- ...

## Non-blocking suggestions
- ...

## Residual risks / not assessed
- ...
```

## Safety

- Do not print PATs, tokens, or secret-bearing diffs.
- Do not queue builds to "validate" unless the user explicitly approves.
- Cite file paths, line ranges, or PR thread ids for every material claim.
