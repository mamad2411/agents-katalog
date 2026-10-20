---
name: audit-agent-surface
description: Audit the coding agent's own configuration as an attack surface — permission rules and mode, every hook command and the writability of the script it executes, MCP servers and what they expose, installed plugins and marketplace provenance, and credentials reachable from any of them. Treats settings.json, hooks.json and .mcp.json as executable configuration rather than preferences, because each one runs code the user did not type. Use before trusting a machine with autonomous work, after installing a plugin or MCP server from anywhere, when permission mode has been loosened, or as a periodic check. Not for auditing application code, dependencies or infrastructure.
argument-hint: "[--scope user|project|all] [--fix] [--json]"
user-invocable: true
model: sonnet
effort: medium
metadata:
  foundry.vertical: core
  foundry.io: "agent configuration -> finding.v1[] + review.v1"
license: Apache-2.0
---

# Audit agent surface

A coding agent's configuration is executable. Hooks run shell commands on events the user does
not trigger deliberately, MCP servers hold credentials and reach the network, and permission rules
decide what happens without asking. All of it is edited casually, reviewed rarely, and inherited
from whoever set the machine up.

This skill reads that configuration and reports what it can actually do — not what it was
intended to do.

**Read-only by default.** `--fix` proposes exact edits and applies none without approval.

## Step 1 — Enumerate the surface

Configuration merges from several layers, and the effective behaviour is the merge, not any one
file. Read all of them and say which layer each finding comes from.

```bash
ls ~/.claude/settings.json .claude/settings.json .claude/settings.local.json 2>/dev/null
```

| Layer | Path | Scope |
|---|---|---|
| user | `~/.claude/settings.json` | every project on the machine |
| project | `.claude/settings.json` | committed, shared with everyone who clones |
| local | `.claude/settings.local.json` | this checkout, usually gitignored |
| plugin | each installed plugin's `hooks/hooks.json` and `.mcp.json` | merged in |

A rule in the project layer is a rule the repository imposes on everyone who opens it. That is the
layer where a permissive setting does the most damage, and the layer people examine least.

## Step 2 — Permission rules and mode

```bash
node -e "const s=require(process.argv[1]);console.log(JSON.stringify(s.permissions,null,2))" .claude/settings.json
```

Report, in this order:

| Check | Why it matters |
|---|---|
| `defaultMode` | `bypassPermissions` disables the prompt entirely; `acceptEdits` auto-accepts file writes |
| `allow` entries broad enough to be unbounded | `Bash(*)`, `Bash(node:*)` and similar admit arbitrary code |
| `deny` list coverage | absent `.env`, key material and credential paths means nothing is protected |
| whether `deny` still applies under the active mode | **verify this against the running build rather than assuming** — a deny list that is bypassed is a protection people believe they have |
| `ask` entries for outward-facing actions | `git push`, `gh release`, `npm publish`, `docker push`, `terraform apply` |

**`bypassPermissions` is the single highest-consequence setting here.** Report it as a finding
whenever it is on, including when it was set deliberately, and say what it removes. It is a
legitimate choice on a disposable machine and a poor one on a machine holding production
credentials — the audit states the trade-off, it does not overrule the operator.

An `allow` entry like `Bash(node:*)` deserves its own line: it permits `node -e '<any code>'`,
which is a shell by another name. Prefix-based allowlisting cannot express "node, but only the
project's own scripts".

## Step 3 — Hooks

Every hook is a command that executes without the user asking. For each one, across every layer:

1. **What runs** — the resolved command and arguments.
2. **Exec form or shell** — `command` + `args` is inspectable; a shell string is not, and it
   composes in ways nobody reviews.
3. **Where the script lives, and who can write it.** A hook whose script sits in a
   world-writable or group-writable directory is a persistence mechanism: anything that can write
   that file runs code on the next session start.

```bash
find ~/.claude/hooks .claude/hooks -type f -perm -o+w 2>/dev/null
```

4. **Which event** — `SessionStart` and `UserPromptSubmit` fire without a tool call, so they run
   even in a session where the user does nothing.
5. **Whether it can block** — a blocking hook on `PreToolUse` or `Stop` can hold a session.
6. **Network egress.** A hook that reaches the network sends whatever it was given. Report the
   destination.

Flag any hook script whose provenance cannot be established: not shipped by an installed plugin,
not in version control, not written by the user.

## Step 4 — MCP servers

```bash
cat .mcp.json 2>/dev/null
```

For each configured server report the transport, the command or URL, and — the question that
matters — **what it can reach**: the filesystem, the network, a credential in the environment, a
production system.

| Risk | What to report |
|---|---|
| credentials in the config file | a token literal in `.mcp.json` is a secret in version control |
| credentials in the environment | name the variable; never print the value |
| a server that both reads private data and reaches the network | the two capabilities together are what makes exfiltration possible |
| tool descriptions as untrusted input | a server's tool names and descriptions enter the model's context; a malicious server can put instructions there |
| unpinned remote servers | the code behind a URL can change without notice |

The last two are the ones people miss. An MCP server is not a library the agent calls — it is a
participant that supplies text the model reads.

## Step 5 — Plugins and marketplace provenance

```bash
node -e "const s=require('./.claude/settings.json');console.log(JSON.stringify(s.enabledPlugins||{},null,2))"
```

For each enabled plugin, name the marketplace it came from and whether that source is pinned. A
marketplace referenced by a moving branch supplies whatever that branch holds at install time, and
plugins ship agents, skills, hooks and MCP servers — the full surface, at once.

Skills and agents matter here too: a skill's `disallowed-tools` is the only frontmatter key that
actually denies a tool, so a guardrail written as an omission from `allowed-tools` denies nothing.
Report any asset relying on that misunderstanding.

## Step 6 — Report

Emit one `finding.v1` per issue, with the layer, the exact file, the effective consequence, and a
concrete remediation. Severity by what the finding *enables*, not by how alarming it sounds:

| Severity | Shape |
|---|---|
| critical | arbitrary code execution the user cannot see, or a credential readable by a network-reaching component |
| high | permission prompts disabled, a writable hook script, a secret in a committed file |
| medium | overly broad allowlist, unpinned marketplace, deny list with no coverage of key material |
| low | hygiene — an unused hook, a stale entry, a shell-form hook that could be exec form |

Roll up into `review.v1` with an explicit verdict on one question: **would this machine be safe to
leave running an autonomous agent?** Answer it plainly. If the honest answer is no, say no.

## Refusals

- **Never print a credential value**, even one already committed. Report the path, the variable
  name and the fact of exposure.
- **Never claim a deny rule is enforced** without having verified it against the running build.
  An unverified protection reported as working is worse than a reported gap.
- **Never auto-apply a permission change.** `--fix` proposes; a human approves.
- **Never assert a hook is safe because it is short.** Read what it executes.

## Degradation

- **No project configuration.** Audit the user layer and say the project layer is absent — that is
  itself a finding when the repository ships plugins.
- **Plugin sources unreadable.** Report which plugins could not be inspected rather than passing
  them silently.
- **Windows or a restricted shell.** The permission-bit check does not apply; say so instead of
  reporting zero writable scripts, which would be a false all-clear.

## Progressive disclosure

- `references/threat-model.md` — what an attacker gains from each part of the surface.
- `references/hardening.md` — the settings that actually reduce risk, in order of effect.
