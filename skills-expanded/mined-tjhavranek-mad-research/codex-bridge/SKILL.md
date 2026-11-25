---
name: codex-bridge
description: |
  Lets Claude call the Codex CLI for a single ad-hoc task — no
  protocol, no rounds, no synthesis. Use this when you want a one-shot
  second opinion or a quick external draft without the full MAD
  scaffolding.

  Triggers:
   - "have Codex <verb> <thing>"  (e.g. "have Codex draft X", "have Codex review file Y")
   - "ask Codex to <verb>"
   - "use Codex for <task>"
   - "run Codex on <file>"
   - Explicit "codex-bridge" mention.

  For structured Claude + Codex collaboration (drafts → cross-review →
  revisions → merge), use the mad-build skill instead.

  For an adversarial audit of a research document, use the
  mad-research skill instead.
---

# codex-bridge skill

A minimal foundation: just the verified `codex exec` invocation
pattern plus a doctor for pre-flight checks. No multi-round protocol,
no synthesis, no role assignment.

## When this skill is the right tool

- "Have Codex draft a Python function for X." One-shot draft.
- "Have Codex review the file I just wrote." One-shot review.
- "Ask Codex to extract the tables from this PDF and write them as
  markdown." One-shot transformation.
- "Run Codex on this dataset and tell me what stands out."

## When this skill is NOT the right tool

- You want Claude AND Codex to both draft something and then critique
  each other → use **`mad-build`**.
- You want a structured adversarial audit of a paper or grant → use
  **`mad-research`**.

## When Claude should proactively propose codex-bridge

The triggers above cover user-invoked use ("have Codex do X"). There
is one additional case: **sequential routing**. When Claude is
working alone on a user task and hits a concrete wall that
codex-bridge's harness may clear, Claude should name codex-bridge as
a user-controlled option, not struggle silently, partially complete,
or apologize without action.

Use this only for observable limits, not for "this feels hard":

- Missing browser / GUI automation.
- Sandbox or network operation denied by Claude Code's harness.
- Package / tool installation failed for a needed dependency.
- Long-running shell or background workflow that exceeds the
  harness.
- Repeated authenticated-download or auth-handshake failures despite
  the user's legitimate authorization.

Claude does NOT silently dispatch a codex-bridge call. The proposal
is named; the user decides.

### Policy-sensitive blockers: three-step protocol

If the blocker is policy-sensitive rather than purely tooling:

1. **Concern first.** Name what Claude is uncertain about (e.g.,
   "this looks like paywalled access. Are these your own
   subscription credentials?").
2. **Clarification second.** Use the user's confirmation of
   legitimacy, ownership, or authorization.
3. **Route third, only if the task is then legitimate AND Claude's
   harness still blocks.** If the task remains disallowed after
   clarification, decline. codex-bridge is not a policy escape
   hatch.

Frame codex-bridge as a different harness and tool path, not as
"Codex is better than Claude at task X." The honest description is
"different defaults", not model-ranking folklore.

## What this skill does

1. Run `helpers/doctor.md` pre-flight (Node.js, Codex CLI, flags, auth).
2. Write the user's request to a prompt file under the user's `cwd`
   (e.g. `mad_sessions/<YYYYMMDD-HHMM-slug>/prompt.txt`, same session
   folder convention as the other two skills, for consistency).
3. Call `codex exec` per `helpers/invoke_codex.md`. Use
   `--sandbox read-only` if the user's task is purely informational;
   `--sandbox workspace-write` if Codex needs to write file(s) into
   the run folder.
4. Capture Codex's output to `output.md` and present it to the user.

## What this skill does NOT do

- No multi-round protocol.
- No anonymization, no rubric, no synthesis.
- No assumption that Codex's output is verified. Claude may
  optionally read and comment, but does not run a structured audit on
  it.
- No `--dangerously-bypass-approvals-and-sandbox` by default. Users
  who want it must say so explicitly (e.g., "run unsafe-yolo Codex
  on...").

## Files

```
codex-bridge/
├── SKILL.md # this file
├── helpers/
│   ├── invoke_codex.md # verified codex exec patterns (safe defaults)
│   └── doctor.md # pre-flight checks
└── README.md # what to install and why
```
