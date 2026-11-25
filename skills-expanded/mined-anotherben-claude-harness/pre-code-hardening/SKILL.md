---
name: pre-code-hardening
description: >
  Run before coding starts when the user wants best-practice hardening outside or
  before the enterprise pipeline: live source truth, live proof plan, domain
  hardening opportunity, SRP/refactor opportunity, table/write ownership
  compliance, SQL/schema risk, blast radius, edge cases, recurrence guards, and
  clear stop rules. Use for "before we code", "make this agent-ready", "harden
  the plan", "full best practices", or "is this ready to build".
---

# Pre-Code Hardening

## Overview

Create a build-readiness gate before implementation. This skill composes existing skills; it does not duplicate their workflows.

## Required Skill Reuse

Use these as subroutines when applicable:

- `deep-think`: mandatory for substantive coding, debugging, refactor, review, design, schema/data, UI, and integration work.
- `zoom-out`: map callers, consumers, lifecycle/status cohorts, ownership, and workflow context.
- `blast-radius`: trace affected files/symbols/SQL/routes/tests before coding.
- `diagnose`: route here first when root cause is unknown.
- `hardening-gate` or `plan-360-audit`: use when a plan/fix proposal already exists and needs structural approval.
- `frontend-clean-architecture`: use when frontend feature setup, UI, React, TypeScript components, hooks, client services, accessibility, single-purpose file architecture, or rendered workflow structure is in scope.
- `sql-guard`: use when SQL, DB writes, migrations, schema, joins, tenant scoping, or table ownership is in scope.
- Repo-local enterprise overlays: use when route cards or governed artifacts require them.

## Gate Checklist

Block coding unless each relevant item is proven or explicitly marked not applicable:

- Route/worktree/edit authority is known.
- Current source truth has been read, not inferred from issue text or memory.
- Domain owner and wrong-owner risk are named.
- SRP/refactor opportunities are classified as `fix_now`, `follow_up`, or `not_applicable`.
- Table ownership/write ownership compliance is checked for DB-backed work.
- Live schema/runtime proof path is named where runtime shape can break the work.
- Browser proof path is named for UI/workflow/rendered-output changes.
- Blast radius and sibling bug class are mapped.
- Edge cases and recurrence guard are named.
- Verification commands or proof actions are concrete enough for a builder.
- Stop rules are explicit.

## Verdicts

- `READY_TO_CODE`: source truth, ownership, hardening opportunities, proof path, and stop rules are sufficient.
- `NEEDS_DIAGNOSIS`: root cause or owner is unknown.
- `NEEDS_SOURCE_TRUTH`: current source, schema, issue, PR, or runtime state was not read.
- `NEEDS_PROOF_SURFACE`: no credible live/runtime/schema/browser proof path exists.
- `NEEDS_PLAN_REWRITE`: plan is too vague, sequenced badly, or lacks acceptance criteria.
- `ENTERPRISE_REQUIRED`: governed or high-risk work needs enterprise overlays before build.
- `BLOCKED`: external dependency, route guard, env proof, or authorization is missing.

## Output

```markdown
**Verdict:** <READY_TO_CODE | ...>
**Coding allowed:** yes/no
**Required downstream skill:** `<skill-name>`
**Source truth read:** <files/issues/PRs/runtime surfaces or missing>
**Domain/SRP hardening:** <fix_now/follow_up/not_applicable>
**Ownership/table compliance:** <proven/missing/not_applicable>
**Blast radius:** <mode and summary>
**Live proof plan:** <commands/actions or blocker>
**Stop rules:** <bullets>

**Builder prompt:**
<exact prompt only if READY_TO_CODE>
```
