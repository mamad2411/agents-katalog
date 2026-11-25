---
name: discover-server
description: Discover one HX Ubuntu server and create its Phase 1 as-found inventory record. Use when asked to inspect, inventory, baseline-discover, or document a server for HX-Infrastructure before role assignment. Collect factual hardware, OS, storage, GPU, network, and relevant existing-service data only; do not assign roles or make role-specific configuration changes.
---

# Discover Server

## Objective

Create or refresh `servers/<server-name>/discovery.md` with factual as-found data for one server.

Read these project files first:

1. `GOALS-AND-OBJECTIVES.md`
2. `INFRASTRUCTURE-CONTRACT.md`
3. `SERVER-REGISTRY.md`
4. `servers/_templates/discovery.md`

## Inputs

Require a target server name or reachable SSH target. Use the project `.env` only for credentials when the project explicitly permits it; never copy secrets into Markdown, logs, or command output committed to the repository.

If target identity is ambiguous, stop and ask for the exact target.

## Phase 1 Boundary

Perform discovery and documentation only.

Do not:

- assign a server role;
- select a workload or model;
- install packages merely to improve discovery;
- install or change GPU drivers;
- install vLLM, Hugging Face tooling, Ollama, databases, or application runtimes;
- change networking, DNS, mounts, partitions, LVM, RAID, firewall state, SSH policy, sudoers, or services;
- enable or disable daemons;
- update the OS;
- change the hostname.

If a fact cannot be collected with existing tools or current privileges, record it as `not available during discovery` rather than modifying the host.

## Workflow

When the project `server-discovery` subagent is available, delegate noisy SSH inventory collection to it and use its normalized result to populate the discovery record.

0. **Read `servers/<server-name>/pre-work-results.md` before contacting the target in any way.** Not in the same batch as other calls. Not concurrently. Read it, then act on what it says.

   **The pre-work record is the source for the target address, the account, and the authentication state.** It normally contains all three:

   ```text
   IPv4 address for eno1: 192.168.50.204     <- the address
   ssh hxsa@192.168.50.204                    <- the account
   SUDO_NOPASSWD=yes                          <- privilege state
   ```

   Do not probe the network to discover facts the file already states. Do not infer an address from a numbering pattern. If the file does not give an address, ask for it rather than scanning candidates.

   It records what the human observed during preparation and is an independent second source.

   - Treat it as evidence, not as the record. The collector output remains authoritative for `discovery.md`.
   - **Cross-check it against the collected facts, especially device counts.** Agreement is corroboration. Disagreement is a finding, and it is usually hardware, not a collection error.
   - If it is truncated, ends at a shell continuation prompt, or is missing sections, say so before collecting. An incomplete pre-work run is itself a signal about the host.
   - If the human states a hardware fact that the operating system does not report, record both: what the OS enumerates, and what is reported installed. Never silently prefer one.

1. Confirm the target by hostname, current IP, OS, and architecture before trusting collected data.
2. Run the bundled read-only collector where practical:

   ```bash
   ssh <target> 'bash -s' < "${CLAUDE_SKILL_DIR}/scripts/collect-server-facts.sh"
   ```

3. Supplement only with read-only commands needed to fill missing fields.
4. Normalize results into `servers/<server-name>/discovery.md` using the project template.
5. Preserve exact hardware identifiers where useful: model, serial, GPU UUID, MAC, disk serial.
6. Explicitly state `No discrete GPU detected` if no discrete GPU exists.
7. Summarize capabilities factually without recommending or assigning a role.
8. Update only the discovered-fact columns for this server in `SERVER-REGISTRY.md`. Leave `Assigned Role` and `Workload / Model` untouched.
9. Mark discovery complete only when all required fields are populated or explicitly marked unavailable with a reason.

## Evidence Rules

Prefer observed command output over assumptions. Do not infer RAM, VRAM, disk type, NIC speed, or GPU model from a product family when the host can report it directly.

Do not paste massive raw command output into `discovery.md`. Record normalized facts and concise notes.

## Completion Report

Return a concise result containing:

- server;
- discovery status;
- discovery record path;
- registry update status;
- any missing facts;
- any observed hardware or system issue requiring an `issue` entry in `actions-and-issues.md`.

Do not include a role recommendation in the completion report.
