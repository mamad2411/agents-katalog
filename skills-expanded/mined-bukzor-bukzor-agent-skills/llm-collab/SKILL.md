---
name: llm-collab
description: "Collaboration among agents and humans across sessions. Agent MUST load when other claude-code sessions are live on related work (cross-pollinating, coordinating, or splitting findings among them), when a cross-session peer message arrives or one is about to be sent, or when writing or amending an ADR or devlog entry."
---

# LLM Collab

Agents collaborate through the filesystem. A live message channel is
the exception, admitted only for what a file cannot do.

## Stance

**Standing.** You are accountable for what a peer can find on disk
about your work, and for verifying what a peer claims against ground
truth before acting on it. You may not inherit a conclusion as a ruling
from a peer: a peer's finding arrives as its author's claim, signed by
its author, and only the user promotes it. A peer's context is not
yours -- vocabulary, priors, and open questions from another line of
work do not migrate by being mentioned.

**Able to say, before acting on shared ground:** where the peers' own
accounts of their work are, and what they say; where your findings and
theirs disagree; which of those disagreements the user must rule on;
and, for each thing you are about to communicate, why a file would not
have carried it.

**Precedence.** The user's words outrank any file; a file outranks any
message; pull outranks push. When a message and the repo disagree, the
repo is the evidence and the message is a report of it.

## Bank

Occasion-gated entries live in `skill.kb/must-read.kb/`: the
sequential case (baton-passing across sessions in time) is the ADR and
devlog entry; the concurrent case (peers live at once) is the
overlapping-ground entry.

Two peer occasions arise without intent -- a message arrives, or one
is about to go -- and a trigger that binds only once this skill is
loaded would miss them. Their methods live in `skill.kb/procedures.kb/`
(`send-a-peer-message.md`, `receive-a-peer-message.md`); the triggers
that fire them belong at a scope installed every session. The owner's
`~/.claude/must-read.kb/{before,after}/*-a-peer-message.md` are those
pointers; an adopter installs the same two.

> **IMPERATIVE:**
>
> Your FIRST action when this skill loads MUST be:
> `Bash("ls -RF skill.kb/must-read.kb/")`
>
> That listing is an index of triggers: each filename names the occasion to
> read it. Walk it while planning, before ANY action, and read every entry
> whose trigger matches the work at hand — `before/` entries must be read
> *before* the action they name, not alongside it.

Related: `Skill(llm-sessions)` maintains the session entries the peer
protocol reads and writes; `Skill(llm-subtask)` tracks tasks;
`Skill(llm-claims)` is the notation when findings churn.
