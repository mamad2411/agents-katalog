---
name: create-custom-policy
description: Create and validate a custom Harness SAST `.policy` file. Invoke when the user runs /create-custom-policy or asks to add a policy (e.g. audit logging for private data, insufficient logging). Scaffold, author, and validate locally — use /deploy-custom-policy for push and assignment.
argument-hint: '[use case or path-to-policy.policy]'
---

# Create custom policy

Author **local `.policy` files** via **slmcp** (`sl_policy_create`, `sl_policy_validate`, `sl_policy_info`). Requires **`sl auth`** for validate/info (not for create). If MCP tools are missing, run `/setup-harness-code-security-mcp` first.

## Invoke `sl_*` tools (required)

Logical names like `sl_policy_create` are **MCP tools**, not shell commands. Use ToolSearch + native MCP invocation with the host-prefixed name. **Never** run `sl policy …` via Bash in this skill.

## Scope (this skill only)

**`sl_ensure_cli`** → **`sl_policy_create`** → edit if the use case says so → **`sl_policy_validate`** until `ok: true`.

**Stop here.** Do not push, assign, or run analyze in this skill. For upload, run **`/deploy-custom-policy`** (it validates, then **asks before** push/assign). Docs: [custom policies](https://docs.shiftleft.io/sast/policies/custom-policies), [CLI reference](https://docs.shiftleft.io/cli/reference/policy).

## Pick one use case

Match the user's words to **one** recipe. Bare `/create-custom-policy` → **Use case 1**.

| User says (examples) | Use case |
| --- | --- |
| *(nothing)*, audit logging, private data, insufficient logging, unaudited data | **1 — Unaudited private data** |
| custom `DATA`, sensitive-data groups, no default dictionary | **2 — Custom DATA groups** |
| controllers only, HTTP only, narrow to routes | **3 — Controller-scoped unaudited data** |
| path only, blank policy, start from scratch | **4 — Empty scaffold** |

---

### Use case 1 — Unaudited private data *(default)*

**Goal:** Flag sensitive data used without an audit-logging sink (Gabe demo / [business logic policies](https://docs.shiftleft.io/sast/policies/business-logic)).

1. **`sl_ensure_cli`**
2. **`sl_policy_create`** — `{ "pattern": "unaudited-data-use", "path": "policies/unaudited-data-use.policy" }`  
   (or `policies/custom.policy` if the user named a path)
3. **Adapt audit tags if the repo is not Java** — bundled `IO audited` lines are Java SLF4J. Keep `CONCLUSION` and `EMIT`; replace only the `IO audited` block. See [adapting-audit-tags.md](references/adapting-audit-tags.md).
4. **`sl_policy_validate`** — `{ "path": "…" }` until `ok: true`
5. **Hand off** — file path, what the `CONCLUSION` checks, whether audit sinks were adapted; suggest `/deploy-custom-policy` (asks before push)

Reference body: [unaudited-data-use.policy](references/unaudited-data-use.policy) (also what `pattern` writes).

---

### Use case 2 — Custom DATA groups

**Goal:** Policy with your own `DATA` definitions; no bundled sensitive-data dictionary.

1. **`sl_ensure_cli`**
2. **`sl_policy_create`** — `{ "template": "no-dictionary", "path": "policies/custom.policy" }`
3. **Author** — add `DATA` blocks, then `CONCLUSION` / `WHEN … EMIT` as needed. Syntax: [dsl-cheatsheet.md](references/dsl-cheatsheet.md)
4. **`sl_policy_validate`** until `ok: true`
5. **Hand off** — file path, `DATA` groups defined; suggest `/deploy-custom-policy` (asks before push)

---

### Use case 3 — Controller-scoped unaudited data

**Goal:** Same as use case 1, but only flows that pass through HTTP/controller code.

1. Complete **use case 1** (create + adapt + validate the base policy).
2. **Edit `CONCLUSION`** — add an `IO (http)` hop:

   ```
   CONCLUSION unaudited-data-use = FLOW IO (http) -> DATA (payment-data OR location OR account-info OR pii OR medical) -> IO (NOT audited)
   ```

3. **`sl_policy_validate`** again until `ok: true`
4. **Hand off** — note that findings are limited to controller/http-tagged paths

---

### Use case 4 — Empty scaffold

**Goal:** Minimal starting file; user will author from scratch or gave only a path.

1. **`sl_ensure_cli`**
2. **`sl_policy_create`** — `{ "template": "default", "path": "<user path or policies/custom.policy>" }`  
   Use `no-dictionary` instead of `default` if they want no bundled dictionary (same as use case 2 scaffold).
3. **Author** — [dsl-cheatsheet.md](references/dsl-cheatsheet.md); validate often while editing
4. **`sl_policy_validate`** until `ok: true`
5. **Hand off**

---

## Validate outcomes

| `status` | Meaning |
| --- | --- |
| `OK` | Policy accepted by API |
| `INVALID_FORMAT` | Fix syntax per `errors` / `message`, re-validate |
| `UNAUTHORIZED` | Run `sl auth` or check org permissions |
| `NOT_FOUND` | Path missing |

Use the JSON `ok` field from `sl_policy_validate` — do not trust `sl` exit code alone.

Optional: **`sl_policy_info`** with `{ "policy": "io.shiftleft/default", "public": true }`.

## Docs

- Lifecycle: https://docs.shiftleft.io/sast/policies/custom-policies
- Business logic example: https://docs.shiftleft.io/sast/policies/business-logic
- Policy language: https://docs.shiftleft.io/sast/core-concepts/policy-language
- CLI: https://docs.shiftleft.io/cli/reference/policy
