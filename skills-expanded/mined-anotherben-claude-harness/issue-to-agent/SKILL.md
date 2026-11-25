---
name: issue-to-agent
description: >
  Use after GitHub issues are created, discovered, pushed, or handed off and the
  operator asks "now what", "which issue should an agent do", "make this ready
  for a build agent", "turn these issues into agent prompts", or "classify the
  queue". Fetches live issue state, separates intake from proof, routes through
  diagnose/pre-code-hardening/specialist-dispatch, and produces the next exact
  agent prompt without implementing code.
---

# Issue To Agent

## Overview

Bridge GitHub issues to safe agent execution. This skill classifies live issues and decides whether each one needs diagnosis, source verification, hardening, specialist decomposition, or a builder.

## Boundaries

- Issue prose is intake, not proof.
- Do not implement code, create branches, push, merge, or close issues.
- Use `gh-issues` when publishing or deduping issue bodies from a diagnosis packet.
- Use `diagnose` when root cause, owner, or write/leak impact is missing.
- Use `pre-code-hardening` before a builder receives work.
- Use `specialist-dispatch` when one issue contains separable one-job roles.

## Workflow

1. Resolve the repo and issue set from the prompt. If the user gave issue numbers, fetch those live. If they said "the issues I pushed", inspect the most likely recent open issues and ask only if ambiguous.
2. For each issue, read body, labels, comments, linked packet/artifacts, and current state.
3. Dedupe against existing open issues when creating or updating is requested.
4. Classify readiness:
   - `not_ready`: vague, duplicate, blocked, or wrong repo.
   - `needs_diagnose`: no proven root cause or owner.
   - `needs_source_verification`: issue claim has not been checked against current source/runtime/schema.
   - `needs_pre_code_hardening`: root cause exists but build gates are missing.
   - `ready_for_specialists`: disjoint bounded read/review/proof roles exist.
   - `ready_for_builder`: exact source truth, owner, scope, acceptance criteria, and proof commands exist.
   - `ready_for_review`: implementation exists and needs review.
   - `ready_for_proof_chain`: completion is claimed and must be proved.
5. Pick one next issue unless the user asks for a queue report.
6. Produce the exact downstream prompt.

## Output

```markdown
**Issue set:** <ids>
**Recommended next issue:** <id and title>
**Classification:** <readiness>
**Use skill:** `<diagnose | pre-code-hardening | specialist-dispatch | patch-or-fix | proof-chain | enterprise...>`
**Coding allowed:** yes/no
**Why:** <short source-grounded reason>
**Missing proof or blocker:** <if any>

**Agent prompt:**
<copy-pasteable prompt with repo, issue, allowed scope, forbidden actions, evidence requirements, and stop rule>
```
