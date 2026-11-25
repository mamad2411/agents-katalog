---
name: skill-audit
description: Audits every skill installed on this agent and reports which ones are broken. Measures each SKILL.md against the published Agent Skills limits, flags descriptions that never say when to use the skill and therefore never fire, finds files over the 500 line and 5,000 token ceilings, reports how much context all the names and descriptions cost on every single message, and lists any skill shipping executable code. Use when the user asks to audit, check, review, measure or clean up their skills, asks which skills are safe to install or worth keeping, asks why a skill never runs or never triggers, asks what their skills are costing them in tokens or context, or says their agent has got slower or heavier since installing things. Also use before installing a skill from a stranger.
license: MIT
metadata:
  author: sharbelxyz
  version: "1.0"
---

# Skill Audit

Measures every installed skill and reports what is wrong with it.

## Steps

1. **Find the skills directory.** Default is `~/.hermes/skills`. If the user names a different
   path, or their skills live elsewhere, use theirs. Do not guess more than once, ask.

2. **Run the script. Do not read it as reference material, run it.**

   ```
   python3 scripts/audit.py <path-to-skills-directory>
   ```

   Add `--json` if the user wants the raw rows to work with.

   The script does every count itself. Do not estimate any of these numbers yourself and do not
   recalculate them, because you will get a different answer each time you try.

3. **Report the table exactly as the script printed it.** Do not summarise it away. The user
   asked what is wrong with their skills, and the table is the answer.

4. **Then give them the three things to do first**, in this order:
   - Any skill flagged `NEVER SAYS WHEN` is invisible to you. It loads on every message and can
     never fire. Rewriting that one line is the cheapest fix available.
   - Any skill they do not recognise or have not used in a month should be turned off, not
     deleted. It costs context on every single message either way.
   - Any skill flagged `SHIPS CODE` should be opened and read before it runs again.

5. **Verify before you report.** Open the output and check it against what was asked for. If the
   script errored, if it found zero skills, or if the path was wrong, say that plainly. Do not
   report a successful audit you did not run.

## What the flags mean

| Flag | What it means |
|---|---|
| `NEVER SAYS WHEN` | The description says what the skill is but not when to use it. Only names and descriptions load at startup, so this is the line that decides whether the skill ever runs. |
| `OVER TOKEN CEILING` | Body is over 5,000 tokens. Published guidance is to move branch-specific material into a `references/` folder the agent opens only when it needs it. |
| `OVER LINE CEILING` | Body is over 500 lines. Same fix. |
| `NAME TOO LONG` / `DESC TOO LONG` | Over the 64 and 1,024 character limits in the Agent Skills specification. |
| `SHIPS CODE` | The skill folder contains executable files. Not a problem in itself. A problem if nobody has read them. |

## Gotchas

- **Token counts are only exact if `tiktoken` is installed.** The script says which mode it used
  in its header. If it says ESTIMATED, tell the user, and offer `pip install tiktoken` to get the
  real number. Never present an estimate as measured.
- **`NEVER SAYS WHEN` is a text match, not a judgement.** It catches the common phrasings. A
  description can pass the check and still be useless. Read the flagged ones and sanity-check a
  couple that passed.
- **The startup number is the one that matters most.** It is what every skill costs on every
  message whether it fires or not. Most people have never seen it.
- **Turning a skill off is not deleting it.** Say that explicitly, because people hesitate.
