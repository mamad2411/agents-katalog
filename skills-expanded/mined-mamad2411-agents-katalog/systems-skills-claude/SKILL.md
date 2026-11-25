# CLAUDE.md

Guidance for Claude Code when working **inside this repo** (authoring or editing skills).

> If you arrived here to *use* a framework, you want a skill in `skills/`, not this file.

## What this repo is

A Claude Code **plugin marketplace** that packages 62 proven business frameworks as
guided AI skills. Distributed publicly to Memberstack customers.

## Layout

```
.claude-plugin/marketplace.json   Generated. Do not hand-edit. See "Regenerating" below.
skills/<category>/SKILL.md        Router: picks a framework, then defers to a reference
skills/<category>/references/*.md One file per framework, the real content
commands/<framework>.md           Slash command, one per framework
docs/METHOD.md                    The shared 3-phase run loop
templates/                        Boilerplate for new skills, references, commands
```

Hard rules from the Agent Skills spec:

- `skills/`, `commands/` live at the **repo root**, never inside `.claude-plugin/`.
- A skill's `name:` must exactly match its directory name.
- `name`: lowercase letters, digits, hyphens. No leading/trailing hyphen, no `--`. Max 64.
- `description`: max 1024 chars. Must say **what it does and when to use it**.
- Keep each `SKILL.md` under ~500 lines. Detail belongs in `references/`.

## Authoring rules

1. **One skill per category, not per framework.** 62 sibling skills with near-identical
   descriptions makes skill selection unreliable. The category `SKILL.md` is a router.
2. **Descriptions are problem-shaped.** Write what the *user's situation* looks like plus
   the trigger phrases they would type, then list framework names as keywords. Do not
   write "a skill for analyzing strategy".
3. **Every reference follows `templates/REFERENCE-TEMPLATE.md`.** Origin, when to use,
   when NOT to use, the canonical structure, the three phases, a worked example, failure
   modes. The "do not use it when" line is not optional; it is what stops misapplication.
4. **The canonical structure must be accurate.** These are real, documented frameworks.
   Do not paraphrase away the actual model, invent a step, or renumber it. If unsure of a
   detail, check a primary source rather than reconstructing it from memory.
5. **Worked examples use membership / SaaS / small-business situations** where natural.
   The audience is founders and no-code builders, not Fortune 500 consultants.
6. **Plain language.** Short sentences. If a term of art is unavoidable, define it inline
   the first time.
7. **No em dashes.** Use a comma, a colon, or a full stop.

## The run loop

Every framework runs Diagnose → Synthesize → Act. It is written once in `docs/METHOD.md`.
Reference files repeat only the parts specific to that framework. Do not copy the whole
loop into every file, or a change becomes a 62-file sweep.

## Regenerating the marketplace file

`.claude-plugin/marketplace.json` is produced by `scripts/build-marketplace.py`, which
holds the single source of truth for the category and framework list. To add a framework:

1. Add it to `CATALOG` in `scripts/build-marketplace.py`.
2. Run `python3 scripts/build-marketplace.py`.
3. Write `skills/<category>/references/<framework>.md` and `commands/<framework>.md`.
4. Add a row to the category `SKILL.md` routing table and to `README.md`.
5. Run `python3 scripts/check.py` and `claude plugin validate .`.

## Worked-example numbers

Every reference file tells the reader to show their arithmetic, so the file has to hold
itself to that. Rules:

- **Recompute every number when you edit a worked example.** Percentages against their own
  sample size, durations against their own volumes, timeline claims against their own
  timeline, totals against their own rows. Adversarial review found more defects here than
  anywhere else.
- **Show the working.** Write `26 x $40 = $1,040`, not `$1,040`. `scripts/check-math.py`
  can only re-verify arithmetic that is actually written down.
- **A taxonomy named in prose must match the taxonomy used in the table below it.**
- **Cross-file examples couple silently.** Several categories share one fictional company
  across their reference files. The canonical numbers are in `docs/WORKED-EXAMPLES.md`.
  Check a number against that sheet before you change it, and update the sheet too.

## Before you commit

```bash
python3 scripts/check.py        # structure, frontmatter, cross-references, style
python3 scripts/check-math.py   # re-computes every calculation the files show
python3 scripts/selftest.py     # proves the checkers still fail when they should
claude plugin validate .        # marketplace schema
```

All four must pass.
