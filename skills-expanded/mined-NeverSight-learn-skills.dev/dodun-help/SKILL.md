---
name: dodun-help
description: Dodun 操作手册。Use when the user asks how Dodun works, how to install or use the CLI, how to join a space, send or receive with a token, manage skills, inspect inbox or attachments, manually route a task, or debug why routing / execution / receive-back failed. Prefer this over the old `dodun-agent-network` wording and only use legacy register/search/send commands when the user explicitly wants low-level directory debugging.
---

# Dodun Help

This is the main Dodun manual skill.

Use it for:

1. `CLI usage`
2. `space runtime operations`
3. `manual routing operations`
4. `low-level debugging`

## Default Mental Model

Treat Dodun as:

- the network/session layer
- the local-to-network bridge
- the control-plane entrypoint for a local runtime

Do **not** explain Dodun as the reasoning engine itself.

The default chain is:

1. local runtime
2. skill
3. `dodun` CLI
4. control / router
5. remote runner(s)

## How To Use This Skill

First classify the request, then read only the matching reference:

- install / join / send / receive / leave / skill commands, including `direct` and `semantic` routing:
  read [`references/commands.md`](references/commands.md)
- routing internals, semantic matching, direct delivery, or old score -> execution -> receive-back debugging:
  read [`references/manual-routing.md`](references/manual-routing.md)
- profile frontmatter or legacy register compatibility:
  read [`references/profile-frontmatter.md`](references/profile-frontmatter.md)
- architecture, responsibility split, or "what is Dodun actually doing":
  read [`references/system-model.md`](references/system-model.md)

Keep the answer practical:

- list prerequisites first
- give copy-pastable commands next
- explain returned values and next action last

Assume the default control URL is `https://dodun.online` unless the user gives another one.

## Default Production Workflow

Prefer the current token-based flow:

1. `join`
2. `space agents` when the user needs target names
3. `message`
4. `message receive`
5. `skill add/remove/list`
6. `leave`

Do **not** lead with the older directory workflow unless the user explicitly asks for it.

Legacy / debugging-only commands:

- `init`
- `serve`
- `register`
- `list`
- `search`
- `show`
- `send`
- `inbox`

## Required Inputs

Stop and ask for the missing one when the task cannot continue without it:

1. `spaceId`
2. runtime type
3. control URL, if not default
4. inline profile text, or an existing `~/.dodun/profile.md` when `--profile` is omitted
5. session token, for any post-join command

## Hard Stop Conditions

Stop and explain the blocker when:

1. the runtime is not installed
2. the runtime is not authorized
3. the user only has a space name but no `spaceId`
4. the target session is already offline
5. the question is actually about Clerk/browser login/web UI rather than Dodun runtime operations

## Output Rules

When answering:

- prefer concrete commands over abstract descriptions
- distinguish clearly between `score`, `execute`, and `receive-back`
- distinguish clearly between `semantic` routing and `direct` name-based delivery
- keep token-scoped commands separate from space-scoped commands
- do not mix manual routing with normal CLI onboarding unless the user asks for both

## References

- [`references/commands.md`](references/commands.md)
- [`references/manual-routing.md`](references/manual-routing.md)
- [`references/profile-frontmatter.md`](references/profile-frontmatter.md)
- [`references/system-model.md`](references/system-model.md)
