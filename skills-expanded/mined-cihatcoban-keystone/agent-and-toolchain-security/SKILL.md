---
name: agent-and-toolchain-security
description: Secures the coding agent's own toolchain - MCP servers, plugins, skills, hooks, permission and approval modes, credentials the agent can reach. Use before adding or trusting agent tooling. Triggers - add an MCP server, is this plugin safe, audit agent config, yolo mode, pin MCP version, hook runs a script.
---

# Agent and Toolchain Security

Application security asks whether the code you ship can be abused. This skill
asks a different question: **can the agent that writes the code be turned
against you?** A coding agent runs shell commands with your credentials, reads
every file you can read, and loads instructions and executables from MCP
servers, plugins, skills and hooks written by people you have never met. Each
of those is a dependency with root-equivalent reach, usually installed with
less review than a one-line npm package.

Use `security-and-threat-modeling` for the product, `configuration-and-secrets`
for the application's `.env` contract, and `ai-integration-guardrails` for an
LLM inside the product. This skill covers the agent's configuration itself.

## The trust map

| Component | What it can do | Who wrote it | Typical failure |
|---|---|---|---|
| Permission / approval mode | Decides which actions need a human | You | Approvals switched off "for one task" and never back on |
| MCP server | Runs code locally or receives your data remotely; its tool output enters the model's context | Third party | Unpinned `npx pkg` pulls a new, compromised release |
| Plugin / extension | Ships skills, commands, hooks and MCP servers at once | Third party | One install adds an auto-running hook nobody read |
| Skill | Instructions the model follows, often with bundled scripts | Third party or team | A skill that tells the agent to fetch and run a script |
| Hook | Runs a shell command on agent events, unattended | You or a plugin | `curl … \| sh` inside a hook; secrets echoed to logs |
| Tool output, web pages, files | Text the model reads as context | Anyone | Instructions hidden in content steer the agent (prompt injection) |

The last row is why the others matter: any text the agent reads can try to
make it misuse a tool. You cannot make the model immune, so you limit what a
misled agent can reach.

## Least privilege for agents

1. **Keep approvals on.** Allow-list the read-only and routine commands your
   project uses (`git status`, the test command); never `Bash(*)`, `*`, YOLO or
   bypass mode on a machine holding real credentials. Unattended runs belong in
   a sandbox or container with no production access.
2. **Scope credentials to the agent.** Give it its own tokens — read-only where
   possible, short-lived, revocable without breaking humans. A shell that has
   production credentials exported is a shell the agent can use them from.
3. **Deny secret files to file tools** (`templates/agent-secret-guards.md`),
   and remember the shell route around those rules.
4. **Ask before irreversible actions.** Keystone's `irreversible.command` and
   `git.force-push` hooks implement `CLAUDE.md` §1.3 at runtime; keep them on.
5. **Limit egress where you can.** An agent that cannot reach arbitrary hosts
   cannot exfiltrate to them.

## Admitting a new MCP server, plugin, skill or hook

Treat it like a dependency (`dependency-and-license-policy`) with higher stakes,
because it executes with your identity:

| Question | Acceptable answer |
|---|---|
| Who maintains it, and is it alive? | A named owner, recent releases, an issue tracker that answers |
| What does it run, and where? | Read the hook commands, server entry point and bundled scripts — all of them |
| Is the version pinned? | `pkg@1.4.2`, `==1.4.2`, an image digest — never bare `npx pkg` or `:latest` |
| What data leaves the machine? | Named endpoints; remote servers over HTTPS only |
| What does it need? | The narrowest tool list and credentials; read-only first |
| Can it be switched off alone? | Yes — per server, per hook ID, per skill |

Review updates the same way: a version bump of a hook-shipping plugin is new
code that runs unattended.

## MCP: tool definitions are prompt text

An MCP server's tool names, descriptions and parameter docs enter the model's
context next to your instructions. Admission review therefore reads them as
prompts, not as API docs:

- A description that tells the model to read unrelated files, include
  credentials, or send data to another tool is a finding — reject the server.
- The tool list can change after approval: the protocol lets a connected server
  announce a new tool list, and any release can ship different tools. The pin
  freezes what you reviewed; every version change is a new review.
- Tools that reach the network — fetch, post, create an issue — are
  exfiltration paths. Give them the same scrutiny as the shell, and do not
  allow-list them wholesale.

## Limit what a task can write

For a focused or unattended task, narrow writes to the paths the task owns:
the harness's path rules (in Claude Code, `Edit(...)` deny rules for paths the
task must not touch; a deny always wins over an allow), a separate worktree per
agent, or a sandbox. Path rules cover the agent's file tools and the shell file
commands the harness recognizes — not a script the agent runs that opens files
itself. Only a sandbox bounds that.

## Audit mechanically

`scripts/audit_agent_config.py` reads Claude Code, Gemini CLI, Codex, Cursor and
VS Code agent configuration in a project (`--user` adds the home directory) and
reports, without printing values:

| Code | Finding | Level |
|---|---|---|
| A1 | Approvals or sandbox switched off wholesale | error |
| A2 | MCP server from a version range, tag or image tag instead of an exact version or digest, or over plain http | warning |
| A3 | A literal credential in agent configuration | error |
| A4 | A hook or MCP command that pipes a download into a shell | error |
| A5 | A `.env` exists and no agent config denies reading it | warning |
| A6 | A blanket allow rule for the shell | warning |

Run it in CI for repositories that commit agent configuration, and before
trusting a repository someone else configured: a cloned `.claude/settings.json`
or `.codex/hooks.json` is code you are about to run.

## When something gets through

1. Stop the session and disable the component: remove the server, uninstall
   the plugin, disable the hook ID.
2. **Rotate every credential the agent could reach**, first — not after the
   investigation.
3. Read the transcript and shell history for what ran and where data went.
4. Add the check that would have caught it: a project rule in
   `.keystone/rules/`, a deny rule, a pin.

## Exit checklist

- [ ] No wholesale approval bypass, YOLO mode or `Bash(*)` outside a sandbox
- [ ] Every MCP server, plugin and hook reviewed, pinned and switchable alone;
      MCP tool descriptions read as prompts; re-reviewed on every version change
- [ ] Network-capable tools scoped like the shell; write scope narrowed for
      unattended tasks
- [ ] Agent credentials are the agent's own, scoped and revocable
- [ ] Secret files denied to file tools; the shell route considered
- [ ] `audit_agent_config.py` reports 0 errors, warnings explained
- [ ] Irreversible-action hooks enabled
