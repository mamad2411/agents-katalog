---
name: deploy-custom-policy
description: Validate then upload a custom Harness SAST `.policy`. Bare /deploy-custom-policy only validates and asks; push and assignment require an explicit user reply. Invoke when the user runs /deploy-custom-policy or asks to upload, publish, push, or assign a policy after local validation.
argument-hint: '[path-to-policy.policy] [label[:tag]] [--project app-id]'
---

# Deploy custom policy

Upload a **validated** local `.policy` via **slmcp** (`sl_policy_push`, `sl_policy_assignment_*`). Requires **`sl auth`** and org permissions to upload/assign. If MCP tools are missing, run `/setup-harness-code-security-mcp` first.

Authoring belongs in **`/create-custom-policy`**. This skill starts only after `sl_policy_validate` returns `ok: true`.

## Invoke `sl_*` tools (required)

Logical names like `sl_policy_push` are **MCP tools**, not shell commands. Use ToolSearch + native MCP invocation with the host-prefixed name. **Never** run `sl policy …` via Bash in this skill.

Mutating tools (`sl_policy_push`, `sl_policy_assignment_set`, `sl_policy_assignment_remove`) require **`confirm: true`**. Pass that only in **Phase 2** after the user confirmed in a **later** message.

## Two phases (required)

Push and assignment **mutate the org**. Treat them as a second turn.

| Phase | This turn may call | Must not call |
| --- | --- | --- |
| **1 — Validate and ask** | `sl_ensure_cli`, `sl_policy_validate`, `sl_policy_assignment_list` (read-only) | `sl_policy_push`, `sl_policy_assignment_set`, `sl_policy_assignment_remove` |
| **2 — Mutate** | Push / assign / remove with `confirm: true` | Nothing until Phase 1 already ran and the user replied |

**Bare `/deploy-custom-policy` is not consent to upload or assign.** End the turn after Phase 1.

**Assignment is opt-in.** Default after a confirmed push is **upload only** (no `sl_policy_assignment_set`). Org-wide default is the most dangerous option — never assume it.

Phase 2 is allowed on the **same** turn only if that user message already names **label:tag** (or an explicit basename) **and** says what to do: push, assign org-wide, assign to a project id, or push only. `/deploy-custom-policy` alone does not qualify.

## Phase 1 — Validate and stop

1. **`sl_ensure_cli`**
2. Resolve **path** — user argument, or the policy created in this session (e.g. `policies/unaudited-data-use.policy`).
3. Propose **label[:tag]** — user argument, or basename of the policy file. **Do not invent** a label. Missing tag defaults to **`latest`**.
4. **`sl_policy_validate`** — `{ "path": "…" }` until `ok: true`. Stop and fix if `INVALID_FORMAT` / `UNAUTHORIZED`.
5. **Stop here.** Reply with this checklist and wait. Do not call mutating tools on this turn.

```
Ready to upload (org-mutating). Reply to continue:

- **path:** policies/unaudited-data-use.policy
- **label:tag:** unaudited-data-use:latest   (edit if you want a different tag)
- **assignment:** none (default) | org-wide | project <app-id>
```

## Phase 2 — Only after the user replies

Re-validate if the file may have changed, then:

1. **`sl_policy_push`** — `{ "policy": "<label[:tag]>", "path": "…", "confirm": true }` until `ok: true`. Note returned `fqn` and `policyIds`.
2. **Assignment** — only if the user chose it in that reply:
   - Org-wide: **`sl_policy_assignment_set`** — `{ "policy": "<same fqn or label:tag>", "confirm": true }`
   - Per-project: **`sl_policy_assignment_set`** — `{ "policy": "…", "project": "<app-id>", "confirm": true }`
   - Skip if they said push only / none / omitted assignment.
3. Optional: **`sl_policy_assignment_list`** to show current assignments.
4. **Hand off** — pushed `fqn`, whether assigned (org vs project vs none), and next steps:
   - Run `/run-security-scan` so the policy is evaluated
   - Docs: [custom policies](https://docs.shiftleft.io/sast/policies/custom-policies), [CLI reference](https://docs.shiftleft.io/cli/reference/policy)
   - Semantic proof still needs a scan — validate/push do not prove the policy finds real findings

Clearing a default uses **`sl_policy_assignment_remove`** with `confirm: true` (do not call set with an empty policy). Without `project`, that clears the **org-wide** default — same confirmation rules.

## Guardrails

- Surface `UNAUTHORIZED` / `INVALID_FORMAT` from tool JSON — do not trust CLI exit codes alone.
- If `confirm` is missing or the tool rejects the call, ask the user; do not retry with `confirm: true` unless they already approved.
- Do not pass `confirm: true` because the skill was invoked, because a prior turn validated, or because a demo “usually assigns org-wide.”

## Outcomes

| Tool                          | `ok` / `status`  | Meaning                                |
| ----------------------------- | ---------------- | -------------------------------------- |
| `sl_policy_validate`          | `OK`             | Safe to **ask**, not to push yet       |
| `sl_policy_push`              | `OK`             | Uploaded; use `policyIds` / `fqn`      |
| `sl_policy_push`              | `UNAUTHORIZED`   | `sl auth` or missing upload permission |
| `sl_policy_push`              | `INVALID_FORMAT` | Re-validate / fix file, then retry     |
| `sl_policy_assignment_set`    | `assigned: true` | Default set for org or project         |
| `sl_policy_assignment_remove` | `removed: true`  | Default cleared                        |

## Related

- Author / validate only: `/create-custom-policy`
- Docs: https://docs.shiftleft.io/sast/policies/custom-policies
- CLI: https://docs.shiftleft.io/cli/reference/policy
