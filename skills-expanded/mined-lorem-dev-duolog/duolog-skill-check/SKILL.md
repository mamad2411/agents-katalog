---
name: duolog-skill-check
description: Use only in a project that has .duolog/config.yaml. Test a changed SKILL.md or a file it loads across models. Applies to changes by the lead or workers; the lead runs the tests.
metadata:
  duolog-version: "1.11.1"
---

Stop unless this project has `.duolog/config.yaml`.

# Test a changed skill

Read the person's own skill guidelines first, from memory, instruction files,
or sources they name. Follow them; they take precedence here.

Use an installed skill for writing skills, such as skill-creator or
superpowers:writing-skills, to write and review the change. This skill adds
only the cross-model test.

Propose concrete situations from the rules the change touches, plus earlier
failures. Each needs one expected action and a check independent of wording.
Reuse `.duolog/skill-tests/<skill>.plan.yaml`:
`situations: [{id, text, check}]`. Checks support `contains`, `absent`, `starts`
and `regex`; all given parts must hold, ignoring case. Show the plan first.

Read the repository's `skill_tests` preference. With `ask` (the default), ask
once about this change with the plan and estimated cost. Offer test, skip,
always for this repository, and never for this repository. With `always`,
test without asking again; with `never`, skip. Remember a preference with
`duolog skill test --remember always` or `--remember never`; it writes
`.duolog/config.local.yaml`. Use `--remember ask` to restore questions.
Do not write global memory unless asked.

The lead runs `duolog skill test <SKILL.md>`. After approval, use `--yes` to
avoid a second question. The command prints run count and estimated cost
before starting. Workers report changes to the lead; they cannot run tests.

Read the table and failed answers. Fix the skill for failures the person
agrees are real. If the expected answer was wrong, fix the plan, not the skill.

