---
name: opencode-policies
license: CC-BY-4.0
compatibility: >-
  OpenCode `experimental.policies` and `permission` config; checked against v1.18.33
  docs and config schema (packages/core/src/v1/config) on 2026-09-29. Policies are
  experimental and may change.
description: >-
  Author OpenCode enterprise governance — the `experimental.policies` provider
  allow/deny layer and the `permission` per-tool gate — for `opencode.json` /
  `.opencode/`. Use when configuring which LLM providers OpenCode may use,
  migrating off `disabled_providers`/`enabled_providers`, locking down a fleet,
  or setting tool permissions (`allow`/`ask`/`deny`) for `bash`, `edit`, `read`,
  `external_directory`, `doom_loop`, etc. Trigger on mentions of OpenCode
  policies, `experimental.policies`, `provider.use`, `permission` config, OpenCode
  `.env` access, doom-loop / external-directory guards, per-agent permission
  overrides, or "restrict OpenCode to Anthropic only".
argument-hint: "What governance do you want? (e.g. 'allow only Anthropic provider', 'deny edit but allow docs', 'why can OpenCode still read .env?')"
user-invocable: true
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# OpenCode Policies & Permissions

Two **separate** governance layers in OpenCode config. Don't conflate them:

| Layer | Key | Governs | Values |
|---|---|---|---|
| **Policies** | `experimental.policies` (array) | *Whether OpenCode may use a resource* — today only **LLM providers** | `effect: allow\|deny` |
| **Permissions** | `permission` (top-level) | *What tools may do in a session* — per tool, per pattern | `allow` \| `ask` \| `deny` |

> OpenCode's API moves fast and predates the model's training cutoff — before
> writing policies code, read `references/policies.rst` + `references/permissions.rst`
> AND re-check https://opencode.ai/docs/policies/ and
> https://opencode.ai/docs/permissions/ for drift. The official config schema is
> `https://opencode.ai/config.json`. Policies are still under `experimental.`.

Verbatim docs live in `references/`. This file is the **delta a fresh model gets
wrong** — read it before authoring, then verify against the references.

---

## Layer 1 — Policies (`experimental.policies`)

The traps that bite, in order of how often a fresh model gets them wrong:

1. **It's nested under `experimental.`, not a top-level `policies` key.**
   `{ "experimental": { "policies": [ … ] } }`. A bare top-level `"policies"` is
   silently ignored.
2. **`provider.use` is the ONLY `action` that exists today.** Policies govern
   **LLM providers, not tools/commands/permissions.** You cannot deny a tool or a
   slash command with a policy — that's the permission layer (Layer 2). If you
   catch yourself writing `"action": "tool.use"` or `"bash"`, you're in the wrong
   layer.
3. **Precedence is INVERTED vs normal config merge.** Everywhere else in OpenCode,
   project config overrides global. For policies, **global beats project** — a repo
   `opencode.json` *cannot* re-enable a provider the global config denied. This is
   the enforcement guarantee an enterprise relies on.
4. **Default-when-no-match is `allow`.** Policies are a denylist by default. To run
   an allowlist ("only Anthropic"), you must put a broad `deny *` FIRST, then
   `allow` the specific providers.
5. **Last-matching statement wins** (within a list). Order broad → specific. With
   default-allow + last-match-wins, the allowlist idiom is: `deny *` then
   `allow anthropic`.
6. **Policies replace the older `disabled_providers` / `enabled_providers`** (still
   accepted by the v1.18.33 schema; the docs direct you to policies). Translate them:
   - `disabled_providers: [openai, google]` → one `deny provider.use` per id.
   - `enabled_providers: [anthropic, openai]` → `deny *` then `allow` each id.

Statement shape (all three fields required):

```json
{ "effect": "deny", "action": "provider.use", "resource": "openai" }
```

`resource` is a provider id or wildcard (`*` = zero-or-more chars, `?` = one char),
e.g. `"company-*"`. See `assets/policies.json` for the allowlist template.

### Allowlist (only Anthropic) — the canonical pattern

```json
{
  "$schema": "https://opencode.ai/config.json",
  "experimental": {
    "policies": [
      { "effect": "deny",  "action": "provider.use", "resource": "*" },
      { "effect": "allow", "action": "provider.use", "resource": "anthropic" }
    ]
  }
}
```

If you flipped the order (`allow anthropic` then `deny *`), last-match-wins means
`deny *` wins for *every* provider including Anthropic — nothing works. Broad first.

---

## Layer 2 — Permissions (`permission`)

Per-tool / per-pattern gate over tool **actions** in a session. Three resolved
states: `allow` (run silently), `ask` (prompt), `deny` (block).

### The non-uniform-defaults trap

There is no single default. A fresh model assumes "everything defaults to allow" —
wrong on three counts:

| Key | Default | Why it surprises |
|---|---|---|
| most tools | `allow` | the baseline |
| `doom_loop` | **`ask`** | fires when the **same tool repeats 3× with identical input** |
| `external_directory` | **`ask`** | fires when a tool touches a path **outside the project cwd** |
| `read` of `.env` | **`deny`** | `*.env` + `*.env.*` deny, `*.env.example` allow |

So "why can't OpenCode read `.env`?" / "why did it pause on the 3rd identical call?"
are *defaults*, not bugs. To let OpenCode read a secret file you must explicitly
`allow` it under `read`; to silence the loop guard set `doom_loop: "allow"`.

### Other delta to pin

- **One `edit` permission covers `edit`, `write`, and the patch tool** (named
  `apply_patch` in OpenCode's built-in tool list; the `/docs/permissions/` page
  refers to it loosely as "patch"). There is no separate `write` or `patch`
  permission key.
- **Last-matching pattern wins** (same as policies). Put `"*"` first, exceptions
  after. `{ "bash": { "*": "ask", "git *": "allow", "rm *": "deny" } }`.
- **Pattern needs the trailing wildcard for args.** `"grep *"` matches
  `grep foo file.txt`; bare `"grep"` matches only the literal word and blocks the
  call. Commands with arguments require the explicit `*`.
- `~` / `$HOME` expand at the **start** of a pattern.
- **Key vocabulary (this skill owns it).** Keys are tool names matched as wildcard
  patterns, so custom and MCP tools work too (`"mymcp_*": "deny"`). Built-in keys and
  their shapes in the v1.18.33 schema:
  - pattern object **or** shorthand action: `read`, `edit`, `glob`, `grep`, `list`,
    `bash`, `task`, `external_directory`, `lsp`, `skill` (the permissions page calls
    `lsp` non-granular, but the schema accepts an object);
  - shorthand action only: `todowrite` (also gates `todoread`), `question`,
    `webfetch`, `websearch`, `doom_loop`.
  `task` matches subagent names; `skill` matches skill names. See
  `references/permissions.rst` for what each key matches on.
- Set everything at once with a string: `"permission": "allow"`.
- **Legacy `tools` map.** `tools: { x: false }` (top level or per agent) is deprecated
  since v1.1.1 and converted to `permission` (`false` → `deny`, `true` → `allow`;
  `write`/`patch` map to `edit`). An explicit `permission` entry at the same level wins.
- **Auto mode.** `opencode --auto` / `opencode run --auto` approves every request that
  would `ask`; explicit `deny` rules still apply.

### Per-agent override

Agent-level permission rules **beat** the top-level `permission` block. This is a
separate axis from policies — don't assume the policy global>project rule carries
over to permissions; it doesn't. Override via `agent.<name>.permission` in JSON, or
`permission:` in a markdown agent's frontmatter:

```yaml
---
description: Code review without edits
mode: subagent
permission:
  edit: deny
  bash: ask
  webfetch: deny
---
Only analyze code and suggest changes.
```

See `assets/permission.json` for a JSON template with `bash`, `edit`, and a
per-agent block.

### "Ask" outcomes

When OpenCode prompts: `once` (this request only), `always` (future matching
requests, **current session only** — not persisted), `reject`.

---

## Quick checklist before you ship a governance config

- Provider lock-down → `experimental.policies`; tool lock-down → `permission`.
  Never `provider.use` for a tool.
- Allowlist = `deny *` FIRST, then `allow <id>` (default is allow; last match wins).
- Enterprise floor goes in **global** config (project can't override policies).
- Migrating? Delete `disabled_providers`/`enabled_providers`; emit policies instead.
- Remember the non-uniform permission defaults: `.env` already denied, `doom_loop`
  + `external_directory` already `ask`.
- One `edit` key = edit + write + apply_patch.
- Validate against `https://opencode.ai/config.json` and re-check the live docs.
