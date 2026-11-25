---
name: tool-allowlist
description: Use when deciding which tools an AI agent may call, writing or reviewing a Claude Code permissions block (allow, ask, deny in settings.json), scoping Bash, file read, file edit, web fetch or MCP tool access for one task, or after an agent ran a command it should not have. Triggers on "tool allowlist", "least privilege for my agent", "lock down Claude Code permissions", "what should go in permissions.allow", "default deny tools", "review my settings.json permissions". Ships a linter that fails blocklist keys, wildcard and credential-leaking policies, and a converter to Claude Code permissions. Do not use for choosing or scoping MCP server credentials (use mcp-least-privilege), for OS-level sandbox configuration, or for general prompt-injection defence.
---

# Tool allowlist

An agent gets the tools its current task needs and nothing else. This skill gives you a
harness-neutral policy file, a linter that fails blocklist keys, wildcard allows, dead allows and
unprotected credentials, and a converter that writes Claude Code's `permissions` object with
`defaultMode: "dontAsk"` for unattended runs.

No account or API key needed. Node 18 or later; both scripts have zero dependencies.

## Principles

1. **Allowlist first.** `"default": "deny"`; every allow names the task need in `why`. A list of
   forbidden things without a default-deny dispatcher lets new tools through. An empty allow list
   is valid for a paused agent; explicit blocklist keys are rejected.
2. **Deny wins.** Claude Code: "Rules are evaluated in order: deny, then ask, then allow. The first
   match in that order determines the outcome, and rule specificity doesn't change the order."
   Put narrow denies inside broad allows, never a narrow allow inside a broad deny.
3. **Least privilege per task.** One policy per task (review, deploy, research). A rule whose
   `why` names no task need gets deleted.
4. **Enforce natively before you build a gateway.** "Permission rules are enforced by Claude Code,
   not by the model. Instructions in your prompt or `CLAUDE.md` shape what Claude tries to do, but
   they don't change what Claude Code allows." Use the harness's rules, its sandbox and its
   PreToolUse hooks first. Write your own gateway only for an agent loop that has no native layer;
   lint the same policy file and enforce it in your tool dispatcher.

## Workflow

1. Write `policy.json` in the format in [references/policy.md](references/policy.md). Start from
   [scripts/fixtures/good.policy.json](scripts/fixtures/good.policy.json).
2. Lint until exit 0: `node scripts/lint-policy.mjs policy.json` (add `--json` for machines).
   Exit 1 lists each error with its rule index and the fix; exit 2 means unreadable or invalid JSON.
3. Convert: `node scripts/to-claude-settings.mjs policy.json`. It refuses any policy with a lint
   error. Merge the printed `permissions` into the settings file you choose below. `dontAsk` denies
   calls that would prompt, including `ask` rules; choose Manual mode for an attended approval flow.
4. Check what Claude Code loaded with `/permissions`, which "lists all permission rules and the
   `settings.json` file each rule comes from."
5. Re-run `node --test scripts/lint-policy.test.mjs scripts/to-claude-settings.test.mjs` after
   changing either script.

## Policy format to Claude Code

| Policy rule | Claude Code rule | Doc note |
|---|---|---|
| `shell` `git diff *` | `Bash(git diff *)` | "A `*` in a Bash rule matches any text, including spaces" |
| `shell` `npm run build` | `Bash(npm run build)` | "A rule with no `*` matches one exact command" |
| `read` `src/**` | `Read(src/**)` | gitignore syntax; `//path` absolute, `~/path` home, `/path` relative to the settings source |
| `edit` `src/**` | `Edit(src/**)` | "`Edit` rules apply to all built-in tools that edit files"; for a `Write` path rule, "Claude Code accepts the rule but never consults it" |
| `fetch` `docs.github.com` | `WebFetch(domain:docs.github.com)` | `domain:*.example.com` matches subdomains, "but not `example.com` itself" |
| `mcp` `github/get_*` | `mcp__github__get_*` | allow globs only after a literal `mcp__<server>__` prefix |
| `mcp` `puppeteer` | `mcp__puppeteer` | "matches any tool provided by the `puppeteer` server" |
| deny, no pattern | `Bash`, `WebFetch`, `mcp__*` | a bare tool name in deny "removes the tool from Claude's context entirely" |

Two Bash details the linter encodes. Put the `*` after the subcommand: "`Bash(git log *)` allows
only `git log` commands, and `Bash(git *)` allows every git command." And operators split commands:
"The recognized command separators are `&&`, `||`, `;`, `|`, `|&`, `&`, and newlines. A rule must
match each subcommand independently." An allow pattern containing an operator therefore does not
mean what it reads as; the linter rejects it unless you mark the rule `"reviewed": true`.

## Where the rules live

- Project, shared: `.claude/settings.json`. Local, yours: `.claude/settings.local.json`. User, every
  project: `~/.claude/settings.json`. One run: `--settings <file>`. Organisation: managed settings.
- "Permission rules follow the same settings precedence as all other Claude Code settings, with
  managed settings highest." The full order among user, project and local files is
  [not stated in the docs read on 2026-10-02]; it lives on the settings page.
- "If a tool is denied at any level, no other level can allow it." A user-level deny blocks a
  project-level allow and the reverse.
- Project allow rules need workspace trust: in `claude -p` or an SDK session on an untrusted folder,
  `permissions.allow` rules in `.claude/settings.json` are "Not used." Deny and ask rules always apply.

## Permission modes

| Mode | What it does with your policy |
|---|---|
| `default` (Manual) | "Prompts for permission on first use of each tool" not covered by allow |
| `dontAsk` | "Auto-denies every call that would otherwise prompt"; the closest match to `"default": "deny"` for unattended runs |
| `acceptEdits` | also auto-accepts file edits and `mkdir`, `touch`, `mv`, `cp` in working directories |
| `plan` | reads and read-only commands only |
| `auto` | a classifier reviews actions instead of you |
| `bypassPermissions` | skips prompts; "Only use this mode in isolated environments like containers or VMs" |

The converter sets `permissions.defaultMode` to `dontAsk`. This does not implement a universal
default-deny dispatcher: built-in reads and read-only commands can still run without approval.
Use explicit Read denies for credentials, Edit denies for protected writes including NotebookEdit,
and OS isolation or a tool dispatcher for a strict boundary. Other settings and CLI flags can
override the starting mode. Block the riskiest two with
`permissions.disableBypassPermissionsMode` or `permissions.disableAutoMode` set to `"disable"`.

## What a policy cannot do

Quoted from the docs:

- Bash rules match text, not programs: a deny or ask rule "covers the invocation Claude usually
  produces and isn't a security boundary around the program." `Bash(git push *)` does not stop
  `git -C . push origin main`, and `Bash(rm *)` does not stop `bash -c 'rm -rf build/'`.
- "Bash permission patterns that try to constrain command arguments are fragile."
  `Bash(curl http://github.com/ *)` misses `curl -X GET ...`, `https://`, redirects and variables.
- "Note that using WebFetch alone doesn't prevent network access. If Bash is allowed, Claude can
  still use `curl`, `wget`, or other tools to reach any URL."
- Read and Edit denies "don't apply to ... arbitrary subprocesses that read or write files
  indirectly, like a Python or Node script that opens files itself."
- A Read deny also blocks Edit and Write on that path, but "NotebookEdit isn't covered, so add an
  `Edit` deny rule for paths no tool may change."
- An installed mod can override: outside managed settings or Team and Enterprise plans, "the mod can
  approve a call that a deny rule refuses."

For a boundary that must hold, add the OS layer: "For filesystem and network enforcement that
doesn't depend on the command text, use sandboxing." Sandboxing "applies only to Bash, PowerShell,
and Monitor commands and their child processes", so you need both.

## Other harnesses

The policy file is harness-neutral; only the Claude Code converter ships here.

- Claude Agent SDK: the permissions page says SDK sessions never show the trust dialog and that
  hosts can pass managed policy through the SDK `managedSettings` option. The SDK's own
  allowed-tools option is [not stated in the docs read on 2026-10-02]; check the vendor docs.
- Codex sandbox and approval policy, Gemini CLI tool settings: check the vendor docs. Map the
  policy by hand and keep the lint pass; do not copy rule syntax between harnesses.

## Stop conditions

Stop and fix before the agent runs again if:

- the agent has tools and no policy file, or the policy fails the linter;
- an allowed call surprised you: shrink the allow, add a deny, then look for the same gap elsewhere;
- a deny you relied on was bypassed by a different spelling: move that boundary to the sandbox or
  a PreToolUse hook.

Verified against code.claude.com/docs/en/permissions on 2026-10-05.
