---
name: ctf-vm
description: Use when pi should autonomously enumerate and solve Linux-focused CTF machines or service-style targets such as HackMyVM, Hack The Box, VulnHub, or internal practice labs. Best for workflows that start from an IP, URL, service, credential, binary, or partial foothold and need recon, web testing, exploit chaining, Linux privilege escalation, note-taking, and writeup generation. Do not use for unauthorized targets or pure crypto-only tasks unless the user narrows the scope.
---

# CTF VM

## Overview

Drive a box from initial recon to proof-backed compromise with a calm, evidence-first workflow. This skill is the box-specialist branch of the wider CTF suite. Prefer small, reversible steps, keep a short hypothesis log, and leave behind notes that can be turned into a clean Chinese writeup.

## Use This Skill For

- A target IP, hostname, or box name is provided and the user wants enumeration.
- The user already has partial findings such as open ports, source code, credentials, or a low-privilege shell and wants the next path.
- The user wants a concise exploitation trail or a full writeup from rough notes.
- The box is primarily Linux, Web, SSH, service exploitation, privilege escalation, or light binary triage.

## Guardrails

- Work only on authorized CTF, lab, or training targets.
- Prefer verification over assumption. If a result is ambiguous, prove it with a smaller follow-up action.
- Avoid destructive changes unless the user explicitly wants them. Backdoor planting, service restarts, overwriting files, and aggressive brute force need a pause-and-confirm moment.
- If a step may be noisy or time-heavy, tell the user what you are about to do and why before running it.
- Keep track of facts, hypotheses, and dead ends so the reasoning stays inspectable.

## Core Workflow

1. Normalize the starting point.
   Capture target, scope, known creds, known files, desired flag depth, and whether the user wants solving, review, or writeup mode.
2. Build the first evidence set.
   Enumerate reachable services, titles, versions, and obvious content. Prefer broad-but-fast discovery first, then deeper scans where the results justify them.
3. Branch by the most promising attack surface.
   Web, SSH, mail, file shares, exposed source, leaked creds, binaries, and local privilege escalation each get their own checklist.
4. Convert findings into a single concrete hypothesis.
   State the vulnerability or path you believe is viable, what evidence supports it, and the smallest proof step.
5. Exploit carefully and preserve proof.
   Save the exact request, payload, file path, or command that moved the box forward.
6. Re-enumerate after foothold.
   Check identity, groups, sudo, scheduled tasks, writable scripts, secrets, internal services, and unusual file capabilities before chasing complicated chains.
7. Close with notes the user can reuse.
   Summarize the route in order: recon, foothold, privilege escalation, flags, and the facts that made each jump credible.

## Working Style

- Keep a running log in the form `fact -> inference -> next action`.
- Prefer one decisive action at a time over spraying tools blindly.
- When a tool produces too much noise, extract the 2 to 5 findings that actually change the next move.
- If a dead end is likely, say so quickly and pivot rather than overfitting to the first idea.
- Default to concise Chinese explanation unless the user asks for English.

## Reference Routing

- For detailed stage-by-stage checklists, read [references/workflow.md](references/workflow.md).
- For mapping local tools and MCP services to common CTF tasks, read [references/tool-routing.md](references/tool-routing.md).
- For writeups that match the style already used in this workspace, read [references/writeup-style.md](references/writeup-style.md).

## Output Expectations

- During solving: report only the findings that change the next decision.
- During review: prioritize likely misses, false assumptions, and missing verification.
- During writeup: keep a narrative flow, include commands that mattered, and explain why each pivot was taken.
