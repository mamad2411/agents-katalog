---
name: release-with-approval
description: Prepares a customer-facing or production release with human approval before final steps. Use when shipping a feature, API change, or release that requires human sign-off.
---

# Release with Human Approval (Human-in-the-Loop)

This skill runs an **advanced workflow** for customer-facing or production changes. It includes a **mandatory human review** step before any release or deploy actions. The agent stops and waits for explicit human approval before proceeding past the gate.

## Business context

Use this when:
- Releasing a new feature or API change to customers
- Making changes that could be breaking or high-impact
- Your policy requires human sign-off before merge, tag, or deploy

## Steps

### 1. Plan

- Invoke the **planner** subagent with the release goal (e.g. "Release the new billing API" or "Ship feature X to production").
- Capture: scope, implementation steps, any breaking changes, rollout or migration notes.
- Present the plan to the user. If they want changes to scope, adjust before implementing.

### 2. Implement

- Implement the planned changes. Follow project rules (`@general-conventions`, `@api-conventions` or others as relevant).
- Include tests and update docs/changelog placeholders where appropriate.
- Do **not** merge, tag, or deploy in this step.

### 3. Verify

- Invoke the **verifier** subagent to confirm tests pass and the implementation matches the plan.
- If the change touches auth, payments, or PII, optionally invoke the **security-auditor** subagent and attach its report to the review package.

### 4. Prepare review package for human

Produce a **single, clear summary** for the human reviewer. It must include:

- **What changed:** Short list of files and behavioral changes.
- **Breaking changes:** Any API, config, or contract changes that affect callers or users.
- **Risk notes:** Config, env, or deployment requirements; rollback considerations.
- **How to review:** e.g. "Review the diff in `git diff` or in your IDE before approving."

Then output an **explicit handoff line** for the human, for example:

```
--- HUMAN REVIEW REQUIRED ---
Please review the changes above. Reply with one of:
- "Approved" or "Looks good" → I will proceed to step 5 (release notes / tag suggestion).
- "Request changes: [your feedback]" → I will adjust and re-run from step 2 or 3 as needed.
- "Abort" → I will stop; no further release steps.
--- END HUMAN REVIEW ---
```

**Stop here.** Do not run step 5 until the user has replied with approval (or requested changes / abort).

### 5. After human approval only

Run this step **only** after the user has explicitly approved (e.g. said "Approved", "Looks good", or equivalent).

- **Release notes / changelog:** Generate or update release notes or a changelog entry for this release. Do not push or tag unless the user explicitly asks you to.
- **Tag / version suggestion:** If the project uses semantic versioning or tags, suggest the next version or tag message. Do not create the tag unless the user explicitly asks.
- **Deploy:** Do **not** run deploy or production commands unless the user explicitly instructs you to. Remind them to run their own deploy process or CI if that is the policy.

If the user requested changes or said "Abort", do not run step 5; instead address their feedback or confirm abort.

## Notes

- Human-in-the-loop is mandatory: the agent must never assume approval. If in doubt, treat as "not approved" and ask again.
- Steps 1–4 can be automated; step 5 runs only after explicit human approval.
- Adapt "release notes" and "tag" to your repo (e.g. CHANGELOG.md, GitHub Releases, or internal runbook).
