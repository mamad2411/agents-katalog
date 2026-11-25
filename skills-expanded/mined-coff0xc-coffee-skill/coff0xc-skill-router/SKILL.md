---
name: coff0xc-skill-router
description: "Coff0xc lightweight skill router/composer. Use only when the user asks AI to decide which coff0xc skills to use, chain skills, build a task/workflow graph, orchestrate vibe coding, handle cross-domain/multi-domain work, or recover an uncertain trigger. Also for broad plan work spanning dev API UI or security cloud identity detection compliance Office. Chinese triggers: autonomous orchestration, multiple skills, AI decides, cross-domain, workflow graph. Do not use the router for narrow tasks."
---

# coff0xc-skill-router

<!-- skill-id: cs-srt-b7a20c6d -->

## Quick Rules (read this first for everyday tasks)
> **[Single-domain direct]** If one specialist skill can finish the job, use it directly; do not output a long skill graph.
> **[Cross-domain orchestration]** Only when the task genuinely spans multiple domains, or the user asks AI to chain skills itself, give the primary skill, supporting skills, stages, and gates.
> **[Lightweight execution]** For complex tasks, give only a 3-5 line executable workflow, then move into the first stage immediately.
> **[Complex upgrade]** Read `references/complex-workflow.md` only for multi-file, multi-stage, architecture/API/schema/auth, or multi-worker tasks.
> **[Release boundary]** Trigger eval, quality eval, workflow trace, and golden responses are only for review/eval/release/CI/push.

Route ordinary tasks with this section; read references only for router debugging, skill quality validation, or complex cross-domain workflows.

## Capability
A lightweight autonomous skill composer for uncertain and cross-domain tasks. It does not merge all capabilities into one big skill, and it is not a required step for ordinary tasks; it only steps in when a task genuinely needs selection, routing, or cross-domain orchestration.

A single task picks exactly one most-specific skill; a complex task outputs the primary skill, supporting skills, execution order, gates, and re-routing conditions.

## What It Can Deliver
- Lightweight routing results: current primary skill, necessary supporting skills, skills not used for now
- Staged execution order: which skill each stage calls, inputs, outputs, completion gates
- Candidate skill comparisons, trade-off reasons, and applicability boundaries
- The fewest clarification questions needed
- Conditions for adding, removing, or switching skills mid-execution
- Manual trigger or natural-language trigger phrasings for later use

## What Input It Can Take
- Vague task descriptions, mixed multi-domain requirements, vibe coding requests
- The user is unsure which skill to use, or auto-triggering failed
- Mixed material such as repos, screenshots, logs, papers, configuration
- The user asks AI to decide, chain skills, and complete work by workflow

## Safe-Use Boundaries
- Owns planning and orchestration; does not replace the deep execution rules of specialist skills
- For security, production, credential, deletion, remote-write, or paid actions, follows the target skill's gates
- When uncertain, gives 2-3 candidate combinations and asks the smallest clarification question
- Security capabilities are used only for authorized, defensive, detection, hardening, validation, and reporting purposes by default; do not provide unauthorized attack, credential theft, persistence, detection evasion, C2, phishing collection, data exfiltration, or destructive steps.

## Why You Can Trust It
- Keeps skills modular, loading the matching specialist flow only when needed
- Every skill must have a clear responsibility, inputs, outputs, and exit gates
- Re-routes on real evidence during execution instead of clinging to the initial judgment
- Keeps manual trigger phrasings, so the user can still force a specific skill

## Typical Usage
```text
Use coff0xc-skill-router to judge which skill this task should use.
Use coff0xc-skill-router: this request spans API, UI, and security; route it for me.
Decide for yourself which coff0xc skills to use and chain them into a workflow to complete this feature.
This vibe coding task may span frontend and backend, databases, security, and docs; orchestrate the skills.
Use coff0xc-skill-router when a Coff0xc skill did not auto-trigger.
```

## Default Output
- Close with only done, verified, remaining, and next steps; give a path or location for any file/code/rule artifacts.
- Checks not actually run are marked unverified; security/architecture conclusions carry an evidence level.

## Expand on Demand
- Everyday tasks execute only the quick rules, capability boundaries, and typical usage above; do not read the full gates by default.
- Read `references/full-workflow.md` for deep architecture, complex multi-stage work, quality evaluation, release, formal delivery, or when the current task lacks evidence.
- After reading a reference, keep context to the minimum necessary; do not output long process write-ups or extra self-justifying material just because a reference exists.
