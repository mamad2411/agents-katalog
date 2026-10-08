---
name: lokei
version: 2.0.0
description: |
  Put local dev surfaces behind trusted HTTPS `.test` domains — real certs and DNS, not
  localhost:port — with the `lokei` CLI: framework-aware `run`, public tunnels via `share`/`--expose`,
  `docker up` and `.test.yaml` multi-service orchestration, and `doctor`/`routes`/`logs` diagnostics,
  backed by a one-time setup that mints and trusts a local CA and wires `.test` DNS and port
  forwarding. Never auto-runs setup, service-install, or uninstall — those wait for approval. Use for
  local HTTPS, named domains, tunnel sharing, or lokei diagnosis.
allowed-tools:
  - AskUserQuestion
  - Bash
  - Read
argument-hint: "[run, share, docker, diagnose, or tunnel request]"
arguments:
  - request
when_to_use: |
  Use when the user wants to run a project on a `.test` domain, set up local HTTPS, expose localhost
  publicly, or debug lokei. Examples: "run my dev server with HTTPS", "give this app a .test domain",
  "share localhost", "why is lokei broken?". Do NOT presume a public tunnel when local-only HTTPS is
  enough, and do NOT auto-run the one-time setup or uninstall flows — confirm the mode first, then run
  the smallest command that matches.
effort: high
---

<EXTREMELY-IMPORTANT>
`lokei` affects the local networking environment and can trigger setup flows.

Non-negotiable rules:
1. Verify `lokei` availability before relying on it.
2. Do not auto-run one-time setup or uninstall flows without approval.
3. Resolve whether the user wants local-only HTTPS, a public tunnel, or multi-service orchestration.
4. Prefer the simplest command that matches the job.
5. Report the resulting URLs and diagnostic blockers clearly.
</EXTREMELY-IMPORTANT>

# lokei

## Inputs

- `$request`: The local HTTPS, share, Docker, service, or diagnostics task

## Goal

Use `lokei` to:

- run a local project behind a named HTTPS `.test` domain
- expose a local service through a tunnel when requested
- orchestrate Docker or multi-service local environments
- diagnose and explain local proxy/setup problems

## Step 0: Verify installation and setup health

Check:

- `lokei --version`
- `lokei doctor`

If `lokei` is missing, tell the user:

> `lokei` is not installed. Install with:
> ```bash
> npm i -g lokei && lokei setup
> ```
> `lokei setup` runs once -- generates a local CA, trusts it in the OS keychain, configures DNS for `.test`, and sets up port forwarding.

Do not install or run setup automatically. Wait for user confirmation.

If setup is unhealthy:

- explain the failing component
- common fixes: CA not trusted or DNS resolver missing -> re-run `lokei setup`
- ask before suggesting or running one-time setup actions

**Success criteria**: `lokei` is available and its setup state is understood.

## Step 1: Resolve the requested mode

Determine whether the user wants:

- `lokei run` for one local app
- `lokei share` or `lokei run --expose` for public access
- `lokei docker up` for Docker Compose
- `lokei up` for `.test.yaml` orchestration
- `lokei routes ls`, `inspect`, or `logs` for diagnosis

Also resolve whether the project name, command, or port needs to be overridden.

**Success criteria**: The correct lokei mode is chosen before execution.

## Step 2: Run the smallest correct command

Prefer:

- `lokei run` for normal local development
- `lokei share --port <port>` for ad-hoc sharing
- `lokei run --expose` when the same session needs local HTTPS and a public tunnel
- `lokei docker up` or `lokei up` only when the project structure actually calls for them

Avoid service-install and uninstall flows unless the user explicitly asked for those operations.

**Success criteria**: The executed command matches the requested workflow without overreaching.

## Step 3: Report URLs and health clearly

After execution, report:

- local `.test` URL
- public tunnel URL if one was created
- project name and route details if relevant
- any doctor/setup blockers if the command failed

**Success criteria**: The user knows exactly where the app is reachable and what failed if it is not.

## Guardrails

- Do not auto-run `lokei setup`, `service install`, or `uninstall` without approval.
- Do not guess that the user wants a public tunnel when local-only HTTPS is enough.
- Do not hide diagnostics behind generic "setup failed" summaries.
- Do not add `disable-model-invocation`; this is a normal environment workflow skill.

## When To Load References

- `references/command-reference.md`
  Use for the full command catalog, framework detection table, architecture details, `.test.yaml` examples, git worktree behavior, and scenario quick reference.

## Output Contract

Report:

1. mode chosen
2. command run
3. resulting local or public URLs
4. any detected setup or networking blocker
5. next action if user approval is required
