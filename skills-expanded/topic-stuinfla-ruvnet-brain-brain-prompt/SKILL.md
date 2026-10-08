---
name: brain-prompt
description: Metaprompting assistant — "/brain-prompt <rough idea>" turns a rough ask into "the right prompt": a complete, tuned master prompt with SPARC phases, per-phase rubrics, standing rules, and cost guardrails, ready to paste or run. Use when the user says "/brain-prompt", "brain prompt", "write me the right prompt for this", "turn this idea into a proper prompt", "metaprompt this", "what should I actually ask for", or hands over a vague one-liner they want expanded into a disciplined build brief. Ends by offering to execute the produced prompt with /brain-build semantics.
updated: 2026-07-10
---

<!-- Credit: this pattern productizes community field use — the PR #8 contributor's standing
     prompt (Eva Draganova, 2026-07-10): power users were hand-writing the phase/rubric/guardrail
     contract around every rough ask. This skill writes that contract FOR them. -->

# Brain-Prompt — from rough idea to the right prompt

You are not completing the task here — you are writing the instructions for completing it. That is
rUv's own framing in his metaprompt notes (`ruv-gists/874e2138/metaprompt.txt`,
`ruv-gists/5dd85664/metaprompt.txt`): a prompt template with clearly demarcated variables,
justification demanded before any score, and structure the executing model cannot wriggle out of.
The output prompt's section shape follows rUv's SAFLA prompt-generator
(`safla/.roo-orginal/rules-prompt-generator/rules.md`): Context / Task / Requirements / Expected
Output, extended with phases and guardrails.

## Procedure

### 1. Interrogate the rough ask — silently, against a checklist

Enumerate what's underspecified: **users** (who is this for?), **data** (what exists, what shape,
how much?), **scale** (10 users or 10M?), **platform** (web/CLI/mobile? deploy target?),
**constraints** (budget, stack, deadline, compliance), **done** (what observable behavior ends
this?). Then:

- **Infer defaults — do not interrogate the human.** For everything you can reasonably default
  (from their repo, their stack, the obvious reading), pick the default and write it into the
  prompt's ASSUMPTIONS block where they can veto it by editing one line.
- **Batch the few questions that genuinely need a human** — ambiguous product intent, money,
  irreversible choices — into ONE list, each with a recommended default. Never a
  twenty-questions interview; usually the list is 0–3 items.

### 2. Ground the stack via search_ruvnet

Call `search_ruvnet` with queries describing what the build technically DOES. Which rUv tools fit
— vectors → RuVector/RVF, orchestration → ruflo, QE → agentic-qe, memory → AgentDB, methodology →
SPARC (`sparc/specification/README.md`)? **Cite the returned repo/path next to every tool the
prompt prescribes.** A prompt that names tools without citations is a guess wearing a suit — don't
ship it. No tool fits → the STACK section says so plainly rather than forcing a tie-in.

### 3. Output the master prompt — Eva's shape

Produce ONE complete, paste-ready prompt with exactly these sections:

```
GOAL         — the ask, sharpened to one testable sentence.
ASSUMPTIONS  — every inferred default, one line each (veto by editing).
STACK        — tools/libraries, each with its grounded citation (repo/path).
PHASES       — SPARC (Specification → Pseudocode → Architecture → Refinement → Completion,
               per concepts/sparc/CARD/sparc-card), a rubric per phase, and a GATE per phase.
STANDING RULES — loop-don't-ask: self-verify, grade /100 against the phase rubric with
               evidence-cited deductions, below 95 → fix and regrade, max 5 iterations,
               report only the final score + fixes + proof; batch questions into ONE list
               with defaults; READY only after verifying the deployed/running version;
               "status" → table only.
COST GUARDRAILS — tier ladder (mechanical work → cheap model via scripts/route-cheap.mjs with
               its printed receipt; frontier only for the authoritative gate run); any
               operation projected >$1 or >20 paid calls → state estimate and wait;
               print running spend during long runs.
DONE CRITERIA — shell commands, one per phase gate plus one overall.
```

**Every gate must be verifiable: done = exit code, not opinion.** A rubric line the executing
model could grade by vibes ("code is clean") must be paired with a command that can fail
(`npm test`, `curl -sf <url>`, `node scripts/loop-checkpoint.mjs check`). If you can't name the
command, the criterion isn't done yet — sharpen it until you can. Long/unattended prompts should
carry the checkpoint contract too (`scripts/loop-checkpoint.mjs`: read first, write last,
done-criteria as the shell command).

Prompt-craft rules from rUv's metaprompt notes (cited above): demarcate user-supplied variables
with XML tags; when the prompt asks the executing model for a score, demand the justification
BEFORE the score; give complex tasks a scratchpad step before the final answer.

### 4. Offer execution

End with exactly one question: **"Run this now with /brain-build semantics?"** On yes, execute
the produced prompt under the full brain-build contract (see the `brain-build` skill) — phases,
≥95 gates, cost ladder, checkpoints — starting immediately, no re-confirmation. On no, they walk
away with the prompt; it must stand alone.
