---
name: silk-sandbox
description: >-
  Use when generated code must be executed without contaminating the host.
model_adapter: gemini
system_instruction: >-
  `silk-sandbox` is the NATASHA stack's execution layer. It takes code spun by [`swarm-mind`](../swarm-mind/SKILL.md) — or any fenced block in Obsidian — and runs it inside a hardened, disposable sandbox. Every byte is wrapped in silk: isolated from the host, watched at the syscall layer, and piped back live.
---

> **Gemini adapter:** Load as a system instruction. The distilled system instruction is in the YAML frontmatter; the full skill reference follows. Source: [`../../.claude/skills/silk-sandbox/SKILL.md`](../../.claude/skills/silk-sandbox/SKILL.md).

# silk-sandbox — Execution Engine

**Suite:** The 187web Ecosystem v2. Parent index:
[`187web-ecosystem`](../187web-ecosystem/SKILL.md) · Siblings:
[widow-weaver](../widow-weaver/SKILL.md) · [neuro-tension](../neuro-toxin/SKILL.md) · [swarm-mind](../swarm-mind/SKILL.md) · [natasha-scout](../agent-charlotte/SKILL.md)

`silk-sandbox` is the NATASHA stack's execution layer. It takes code spun by
[`swarm-mind`](../swarm-mind/SKILL.md) — or any fenced block in Obsidian — and
runs it inside a hardened, disposable sandbox. Every byte is wrapped in silk:
isolated from the host, watched at the syscall layer, and piped back live.

## When to invoke

Load this skill when a markdown code block or agent-generated artifact must be
compiled, tested, or demonstrated inside a controlled environment. If the code
came from an LLM, the web, or any untrusted source, it goes through
`silk-sandbox` first — never the host shell.

## Constraints

### 1. MicroVM Isolation

**What it enforces.** Generated code executes only inside Firecracker microVMs
or gVisor sandboxes. The host filesystem, kernel, and network namespace remain
untouched. The sandbox is born for one run and destroyed afterward.

**Implementation guidance.**
- Default backend: **Firecracker** for untrusted / arbitrary LLM output; use
  **gVisor** (`runsc`) when Docker compatibility is required.
- Provision VMs from a minimal, read-only root image with no credentials,
  secrets, or host mounts beyond the explicitly declared workspace.
- Map one ephemeral working directory into the VM. Reject any mount path that
  resolves above `/workspace` or outside the allow-listed sandbox store.
- Snapshot/restore is forbidden across different code provenances; each
  execution starts cold.
- Enforce a hard timeout per run (default 120s). Kill the VM, not the process,
  on timeout.

### 2. Syscall Monitoring

**What it enforces.** All kernel surface area from the sandbox is inspected and
filtered. Unauthorized network sockets, filesystem reads outside `/workspace`,
and privilege-escalation attempts are blocked and logged.

**Implementation guidance.**
- Attach an eBPF program to `tracepoint/syscalls` for `socket`, `connect`,
  `openat`, `execve`, `setuid`, `capset`, and `mount`.
- Default policy: **deny all outbound network** unless the request explicitly
  sets `network: allow` and the runtime owner approves it.
- Filesystem allowlist: `/workspace/**`, `/tmp`, standard runtime libraries, and
  nothing else. Deny reads to `/etc/passwd`, `/proc/*/environ`, host devices,
  and kernel pseudo-filesystems.
- On a blocked syscall, terminate the VM, surface a **Widow Red** alert in
  Obsidian, and append a concise log line to the originating note.
- Rotate audit logs aggressively; never let generated code persist logs it could
  later read.

### 3. I/O Multiplexing

**What it enforces.** stdout and stderr are captured in real time and streamed
back to the Obsidian UI through WebSockets. The developer watches compile,
execute, and fail inline, beneath the code block that spawned it.

**Implementation guidance.**
- Run a per-session WebSocket broker inside Claudian. The broker accepts one
  stream per sandbox VM and forwards lines to the active Obsidian pane.
- Multiplex stdout and stderr on separate channels, preserving order with
  millisecond timestamps. Display stderr in **Widow Red** callouts.
- Buffer the last 4 KB of output server-side so late-joining panes can hydrate
  the stream. Flush on every newline for interactivity.
- Append final output as a collapsible blockquote under the originating code
  fence:

  ```markdown
  > [!quote] silk-sandbox output
  > stdout lines...
  > stderr lines...
  ```

- On non-zero exit or forced termination, render `> [!danger]` and route the
  artifact to [`Code_Explainer`](../widow-weaver/SKILL.md).

## Workflow: code block → sandbox → UI

1. **Source.** A specialist from [`swarm-mind`](../swarm-mind/SKILL.md) emits a fenced code block in
   Obsidian, or a user clicks the inline **▶ Run in silk-sandbox** button.
2. **Dispatch.** Claudian extracts the block, wraps it with the declared runtime,
   and requests a fresh Firecracker VM with `network: deny`.
3. **Execute.** The VM boots, runs the code, and streams stdout/stderr over the
   WebSocket broker.
4. **Return.** Output lines render beneath the block as they arrive. On
   completion, the VM is destroyed and the final exit code is appended.
5. **React.** A clean exit finishes silently. A boundary violation or failure
   triggers a **Widow Red** alert and routes the log to [`widow-weaver`](../widow-weaver/SKILL.md) for
   diagnosis.

## Safety warning

Never execute untrusted code without isolation. `silk-sandbox` is a containment
layer, not a proof of invulnerability. A compromised runtime, misconfigured
seccomp profile, or zero-day in the microVM hypervisor can still breach the
boundary. Review generated code before allowing network access, keep the
sandbox images minimal, and rotate audit logs.

---

*This skill defines execution policy and isolation rules. No runtime code or
backend configuration lives here; implementation belongs to the Claudian host
service and its Firecracker / gVisor drivers.*


## NATASHA LAB (v3)

Profiles: `lab:text` · `lab:python` · `lab:node` · `lab:repo` · `lab:web` ·
`lab:quantum` · `lab:evm`.

Network policy default deny-egress except declared allowlist. Emit run records
(input hash, tools, exit code, artifacts). No live production exploits.

