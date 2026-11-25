---
name: converting-skills
description: "Converts an existing Agent Skill to the steer framework, preserving its content and behavior: license triage, mapping hand-rolled machinery to steer components, rebuild with steer new, validation, and a measured comparison against the original. Use when the user asks to convert, port, migrate, or rebuild an existing skill on steer."
metadata:
  version: 0.1.0
---

# converting-skills
Port an existing skill onto steer without changing what it does. The
user gets a drop-in rebuild (same name, same triggers, same
capabilities), a NOTICE.md recording every delta, and a measured
comparison against the original instead of a vibe.

The conversion flow and lessons run on this skill's bundled runtime
(`scripts/steer.py`); authoring the rebuild additionally needs the
installed `steer` CLI, checked below.

## Before you start

1. **Check steer.** Run `steer --version`. If it is missing, ask the
   user to install it (`uv tool install steer-ai` or
   `pip install steer-ai`); do not hand-roll a lookalike scaffold.
2. **Set two paths.** `SKILL` is this skill's own directory (this
   file's parent); `WS` is a scratch directory for this conversion.
3. **Apply past lessons.** Run
   `python3 "$SKILL/scripts/steer.py" learn show` and follow what it
   says; those lessons came from real previous conversions.
4. **Building something new instead?** Creating a skill from scratch
   or improving one you own is the building-skills skill's job, if
   installed; this one is for porting an existing skill faithfully.

## Ground rules

- **The prose is the payload.** The source skill's rules, red-flag
  lists, and phrasing are tuned content; convert the machinery around
  them and keep the voice verbatim.
- **Rebuild exactly.** Same name, same description triggers, same
  capabilities. Anything you deliberately change goes in NOTICE.md.
- **License is a gate, not a formality.** Per skill, not per repo.
  No-derivatives means stop and tell the user.

## Process

The conversion runs behind an enforced flow: steps verify themselves
against the conversion workspace, and you cannot skip ahead. The flow
lives next to this file and operates on the conversion workspace:

    python3 "$SKILL/scripts/steer.py" flow status --workspace "$WS"
    python3 "$SKILL/scripts/steer.py" flow next --workspace "$WS"

Lay the workspace out the way the flow verifies it:

    original/          vendored copy of the source skill
    rebuild/<name>/    the steer rebuild
    out/conversion/    triage.md, comparison.md

The steps:

1. **triage**: inventory the original, identify its license, and map
   each piece of hand-rolled machinery to a component
   (`references/component-mapping.md`, `references/licensing.md`).
   Everything lands in `out/conversion/triage.md`.
2. **scaffold**: `steer new <original-name> --dir rebuild` with exactly
   the components triage mapped. Not more; a toolkit skill gets no
   flow, a knowledge skill may need no runtime components at all.
3. **port**: move the content, swap machinery for the generated
   component instructions, put branch-only material behind
   `references/` pointers, carry the license file, record every delta
   in NOTICE.md.
4. **verify**: `steer validate rebuild/<name>` gates the flow; fix
   findings rather than arguing with them.
5. **compare**: measure both sides with
   `references/measuring.md` and write
   `out/conversion/comparison.md`; present the deltas to the user.

Do NOT claim the conversion is done while
`python3 "$SKILL/scripts/steer.py" flow status --workspace "$WS"` shows
incomplete steps.

## Learning

This skill improves with use. As you work:

- The moment the user corrects you, or something fails and then works a
  different way, capture it:
  `python3 "$SKILL/scripts/steer.py" learn note "<one imperative rule>" --kind correction`
  Lessons are atomic rules ("Use X not Y when Z"), never secrets.
- When a lesson from `python3 "$SKILL/scripts/steer.py" learn show`
  helped, run `python3 "$SKILL/scripts/steer.py" learn confirm <id>`;
  when one was wrong, `python3 "$SKILL/scripts/steer.py" learn dispute <id>`.
- Before finishing, record the outcome:
  `python3 "$SKILL/scripts/steer.py" learn run ok` (or `failed` with
  `--note`).

If a `learnings.md` exists in this skill, read it too; those are
promoted lessons that shipped with the skill.

## References

Load these only when that step of the work is hit:

- Mapping hand-rolled machinery to components (triage, scaffold):
  first read `references/component-mapping.md`.
- License identification and attribution artifacts (triage, port):
  first read `references/licensing.md`.
- The comparison checklist (compare): first read
  `references/measuring.md`.

## Gotchas

- Well-built originals validate CLEAN. Do not promise "steer will find
  errors"; the wins live in failure behavior, enforcement, secret
  hygiene, and context economy. Measure, then claim.
- Verify conditions need reality to check. Find the artifacts the
  original's own prose already demands ("write it down") and make them
  files; use mandate steps only where no artifact exists.
- Moving files into `references/` silently breaks their mentions of
  each other; grep the moved files for cross-references and fix paths.
- Instructions in the original that print credential values (grepping
  `.env` files, echoing tokens) leak secrets into the transcript.
  Convert to name-only detection, export by substitution, and
  persistence through the secrets component, and say so in NOTICE.md.
- Do not restate flow directives in the body or vice versa; directives
  point at body sections, one source of truth.
- Remove scaffold directories the rebuild does not use (an empty
  `assets/` or `references/`) before validating; `scripts/` stays, it
  holds the bundled runtime.
