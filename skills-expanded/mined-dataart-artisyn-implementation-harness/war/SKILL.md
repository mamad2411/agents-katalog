---
name: war
metadata:
  version: 2.0.0
  internal: true
description: Well-Architected Review (/war [design|implementation] [VERSION]). Prompts design vs implementation if ambiguous, then follows the matching reference exactly. @architect assesses against the configured AWS Well-Architected Framework pillars.
---

The developer wants to run a Well-Architected Review. Here is their input:

---

## $ARGUMENTS

---

> ⚠️ Follow every step in order. Do not skip, summarize, or improvise. If you are unsure, ask before deviating.

## Route

Parse `$ARGUMENTS` into an optional leading stage word and the remaining version/pillar input:

- `design {input}` or a leading `d` → follow `references/01-design.md` exactly
- `implementation {input}` or a leading `impl`/`i`/`code` → follow `references/02-implementation.md` exactly
- A version only (e.g. `MVP`, `V1`), or no argument → present the options below and ask which audit to run

Present:

> "Which audit would you like to run?
>
> - **A — Design audit** (`/war design`): reviews Target Architecture documents against WAF pillars. Use this to validate the design before implementation begins, or to assess an existing design version.
>
> - **B — Implementation audit** (`/war implementation`): reviews the codebase against the Target Architecture. Use this to find gaps between design intent and what was built.
>
> (**A** / **B** / **both**)"

**Stop and wait.** Then follow the selected reference exactly (both, in sequence, if "both").

**Compatibility:** `/war-design`, `/war-implementation` are retired as separate skills — use `/war design|implementation [VERSION]` instead.

---

## Companion

For a delivery gap view across all three dimensions (designed / implemented / documented):

```
/where-we-are
```
