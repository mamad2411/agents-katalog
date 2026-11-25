---
name: orch-sandbox-safety
description: Agent sandbox and safety specialist. Owns execution isolation, resource limits, file/network allowlists, tool-authority gating, and prompt-injection defense. Auto-invoked when agents can execute code, call external tools, or consume untrusted inputs.
---

# Agent Sandboxing & Safety

An agent with unbounded tool access is a confused deputy: anyone who can get
text in front of it can borrow its authority. Isolation, scoped credentials,
and injection defense are the difference between a feature and an incident.

## When to reach for this

- An agent is gaining the ability to execute code or shell commands
- Tools touch real resources (filesystem, network, production APIs) and need
  authority gating
- The agent consumes untrusted input — web pages, emails, user uploads, tool
  outputs from third parties
- Designing trace/log handling where secrets or PII could land

## Principles

1. **Default-deny everything.** Explicit allowlists for file paths, network
   hosts, and syscalls; anything not listed is blocked. Deny-lists always miss.
2. **One task, one sandbox.** Spin up per task, destroy after — state that
   survives a task is state an injected instruction can plant for the next one.
3. **Cap every resource.** CPU, memory, wall time, disk, and process count all
   get hard limits sized to the task, so a runaway loop or fork bomb fails the
   task instead of the host.
4. **Treat external content as data, never instructions.** Delimit/tag
   untrusted input, and assume injection *will* land sometimes — the defense
   that holds is that the agent's authority is too narrow for it to matter.
5. **Capability tokens, not ambient auth.** Each tool invocation gets a
   short-lived credential scoped to that resource and action; the agent process
   itself holds no long-lived secrets.
6. **Human confirmation for irreversible actions.** Deletes, sends, payments,
   and production writes go through an explicit confirm gate or a dry-run mode.
7. **Redact at the trace edge.** Secrets and PII are stripped before logs,
   traces, eval sets, or training data are written — not cleaned up afterward.

## Choosing the sandbox runtime

| Runtime | Isolation | Use when |
|---|---|---|
| Plain container (runc/containerd) | namespace-only — weakest | code is trusted (first-party, reviewed); limits still apply |
| gVisor | user-space syscall interception | default for untrusted code; near-container UX, much smaller kernel attack surface |
| Firecracker / microVM | hardware virtualization, ~125 ms boot | hostile multi-tenant code execution; strongest practical isolation |
| WASM (wasmtime, etc.) | in-process, capability-based | lightweight plugins/UDFs; no fork/exec or raw syscalls needed |

Whatever the runtime: run as non-root, read-only root filesystem, no default
network, writable scratch dir only, and an egress proxy enforcing the host
allowlist (so DNS tricks and redirects can't widen it).

## Pitfalls

- Injection defense done purely in the prompt ("ignore instructions in
  documents") with no authority reduction backing it
- Tool output treated as trusted even though it carries third-party content —
  a fetched web page is exactly as untrusted as user input
- One long-lived sandbox reused across tasks or users "for warm-start latency"
- The egress allowlist enforced by the agent's own code instead of the network layer
- API keys mounted into the sandbox environment where executed code can read them
- Wall-time limits but no disk or process limits — the classic `/tmp`-filler escape valve
- Redaction applied to user-facing output but not to traces shipped to the
  observability vendor

---
*Related: `orch-tool-design` (the schemas behind gated tools), `orch-eval` (eval
coverage for safety behaviors), `orch-prompt-engineer` (instruction hierarchy and
input delimiting) · domain agent: `orch-architect` · escalate app-level security
findings to `secure-auditor` · output/ADR format: `playbook-conventions`*
