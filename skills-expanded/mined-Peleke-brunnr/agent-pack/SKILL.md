---
name: agent-pack
description: >
  Package a piece of completed work into an agent-consumable pack: an entrypoint README, the
  source documents, and an input-output contract, ready to hand to an agent (or to a person who
  will hand it to their agents). Use when a deliverable needs to be executed, not just read,
  when sending work that a fleet will act on, or whenever a message asks for action and should
  carry its own context, input, and output contract.
---

# Agent Pack

A deliverable used to have one audience: a person who reads. Now it often has two. A person skims and decides; an agent parses and executes. This skill builds the agent half: a self-contained pack a fleet can run without a human re-explaining it.

## What it produces
A folder (optionally zipped) containing:
- **`README.md`** — the entrypoint. What is in the pack, how to run it, the input-output contract, the rules, and the goal.
- **The source documents** — whatever the agent needs to do the work.

## The standard layout
The shape is fixed on purpose, so whoever opens it (a person or a model) starts in the same place every time:

```
pack/
  README.md      # entrypoint: context, input, output, rules, goal
  <documents>    # source files, named by what they are
```

Zip the folder for a single-attachment handoff. The value is not the format; it is that the format does not change.

## The contract (the core idea)
Every actionable pack carries three things, stated explicitly in the README:
- **Context** — what this is and why it exists.
- **Input** — what the agent consumes to start (the decisions a human already made, the parameters, the source data). If a required input is missing, the agent halts on that branch and flags it rather than guessing.
- **Output** — what the agent should produce (the artifacts, the next-actions, the format).

Plus the **rules** it works under (confidentiality, tone, what not to invent).

## Steps
1. **Gather** the artifacts: the specs, docs, data, and any prior results the agent should build on.
2. **Define the contract:** write the context, the input (what it consumes), the output (what it returns), and the rules.
3. **Write the entrypoint `README.md`** using the template in `README-template.md`. It reads top to bottom: what this is, the files, how to run, the contract, the rules, the goal.
4. **Assemble** the folder, README first, then the documents. Name files by what they are, not how they were built.
5. **Scrub** anything confidential: codename real clients, strip identifying detail, keep the content executable.
6. **Zip** it for a clean single-attachment handoff.

## Rules this skill enforces
- **Entrypoint first.** A pack without a README is a pile of files. The README is what makes it runnable.
- **The contract is explicit.** Context, input, output, stated, not implied.
- **Halt on missing input.** The receiving agent flags a gap rather than inventing one.
- **Confidentiality by default.** Scrub before it leaves your machine.
- **Plain prose.** The README is read by both people and models; keep it direct.

## Files
- `README-template.md` — the entrypoint template to fill.

## The pairing
An agent pack usually ships next to a human pack (a deck, a one-pager, a summary), because the two audiences need different surfaces. Build both from one source; the audiences differ, the truth does not.
