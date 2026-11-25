---
name: jargon
description: "Switches Sulis between plain-English and technical replies for the session."
user_invocable: true
standards:
  input: [REFERENTIAL_INTEGRITY_STANDARD]
  output: [TONE_STANDARD]
register:
  founder_mode: default
  technical_mode:
    shape: raw_tool_output
    triggers: [intent, --raw, /sulis:jargon]
verification_spiral:
  tier: light
  template_base: LIGHT_TIER_DEFAULT
related_skills:
  - relationship: depends_on
    skill: ../../agents/sulis.md
    notes: the Sulis agent body owns the dual-register behaviour; this skill only flips the session default it reads
  - relationship: depends_on
    skill: ../../references/founder-facing-conventions.md
    notes: Rule 6 (Dual register) defines the on|off mechanics and the one-sentence confirmation this skill emits
  - relationship: related_to
    skill: ../change/SKILL.md
    notes: the --raw flag on any command is the per-invocation equivalent; this toggle is the session-wide one
---

# /sulis:jargon — switch between plain English and the technical version

## Conclusion (lead with the answer)

`/sulis:jargon on` tells Sulis to give you the raw, technical version by
default for the rest of this session. `/sulis:jargon off` switches it back
to plain English. That's the whole skill — it flips a setting Sulis reads
on every reply.

This is the session-wide switch. If you only want the technical version for
one answer, just ask ("show me the raw output") or add `--raw` to a command.

## What it does

The Sulis agent is dual-register: plain English by default, the technical
version on request. This skill sets which one is the **default** for the
session. It does not change anything about the work itself — same substance,
just a different shape on the way out.

| You type | Effect |
|---|---|
| `/sulis:jargon on` | Technical-mode is the default until you turn it off or the session ends |
| `/sulis:jargon off` | Plain-English (founder-mode) is the default again |
| `/sulis:jargon` (no argument) | Reports which mode is currently the default |

## The mechanism (session state)

The toggle is **session state**, read by the Sulis agent on every reply.
Per Founder-Facing Conventions Rule 6, the register default is keyed on
`SULIS_JARGON`. A skill can't reach into the parent shell to set an
environment variable, so the durable handle is a session-scoped state file
the agent reads each turn:

- **On `on`:** write `on` to `.sulis/.session/jargon` (create the directory
  if needed). This is private agent state — a dot-prefixed file, never a
  founder-readable artifact (per the agent body's "track calibration state
  in private agent state" rule).
- **On `off`:** write `off` to the same file (or delete it — absence means
  founder-mode default).
- **On no argument:** read the file and report the current default.

Precedence the Sulis agent applies, highest to lowest:

1. A per-response intent ("plain English please" / "give it to me straight")
   — wins for that one response, whatever the session default is.
2. The `SULIS_JARGON` environment variable, if the founder set it in their
   shell (e.g. via a spawned change terminal).
3. `.sulis/.session/jargon`, the file this skill writes.
4. Default: founder-mode.

So a one-off "plain English please" still works even with jargon on — the
session toggle sets the *default*, never a lock.

## What to say (the confirmation)

Confirm the switch in **one sentence**, then stop. Do not restate the whole
dual-register pattern — the agent body owns that.

- **On `on`:**
  > "Switched to technical-mode for the rest of this session — `/sulis:jargon off` reverts."
- **On `off`:**
  > "Back to plain English — `/sulis:jargon on` switches to the technical version again."
- **No argument, currently on:**
  > "You're in technical-mode for this session — `/sulis:jargon off` reverts."
- **No argument, currently off:**
  > "You're in plain-English mode (the default) — `/sulis:jargon on` switches to the technical version."

## Vocabulary

This skill performs no operator → founder translation of its own — it is the
switch that decides which register everything *else* uses. The one term it
surfaces is "technical-mode", and it always pairs it with the plain-English
gloss ("the technical version" / "the raw output") so the label never stands
alone.

## Gotchas

- **Operator-vocab leak (MUC-F1):** the confirmation sentence is the only
  founder-visible string; it is already plain English with the command in
  backticks. Do not echo the state-file path or the env-var name to the
  founder unless they asked for the technical version.
- **The toggle sets a default, not a lock (MUC-R1 / MUC-R3):** jargon-on
  must never suppress a per-response "plain English please". The session
  default is the floor, not a ceiling — intent for one response always wins.
- **Turning it on does not skip safety:** technical-mode still prompts before
  destructive actions (Rule 3); only the language gets terser, never the
  guard.
