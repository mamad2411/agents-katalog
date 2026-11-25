---
name: authoring-project-skills
description: Use when creating, updating, reviewing, or deciding whether to write a project skill (docs/skills/*.md) — covers the file template, verb-led naming, the quality bar, the pre-write 5-weakness self-check, and when NOT to write a skill. Pairs with the always-on "scan docs/skills before a task / create-or-update after" rule in CLAUDE.md.
metadata:
  author: Ken Nguyễn <ntnpro@gmail.com>
---

# Authoring project skills

Project skills live in `docs/skills/` and document repeatable workflows for humans and AI. The
always-on trigger lives in CLAUDE.md (*scan `docs/skills/` before a task; create/update one after a
repeatable task, ending your response with `✏️ Skill <created|updated>: docs/skills/<file>.md — <reason>`*).
**This skill is the full how-to** for actually writing one well.

## Signals to skill it
- Hit a non-obvious gotcha (env mismatch, hidden dependency, undocumented step).
- Ran a multi-step sequence to set up, debug, deploy, or migrate.
- Answered "how do I X here" by tracing through several files.
- A teammate is likely to ask the same question later.

## Scope: generalize before writing
A skill must cover the *class* of problems, not the single incident that triggered it. Before
writing, ask: "what is the general workflow this incident is one instance of?" — and write THAT.
Parameterize the incident-specific parts (the specific package, workflow file, error code, branch)
into steps that work for the whole class; keep concrete values only as examples inside the steps.
- Bad (incident-scoped): `fix-github-packages-401-in-ci.md` — one package, one workflow, one status code.
- Good (class-scoped): `fix-ci-package-registry-auth.md` — any registry auth failure (401/403), any workflow, any repo.
- If the generalized version would duplicate an existing skill, update that skill instead.

## No trash skills — skip when in doubt
A skill that's never opened again is noise that buries the useful ones. Skip creation when:
- The task is genuinely one-off (exploratory question, throwaway script, trivial edit).
- It's already covered — code comments, existing docs/skill, or a CLAUDE.md / AGENTS.md rule.
- The fix is a single obvious change anyone would find from the error message alone.
- The knowledge goes stale within weeks (a temporary state, one ticket, one secret's current value).
- It merely restates standard framework/library/language behavior a competent dev already knows from
  the framework docs. Before writing, ask: "Would a competent dev know this from the docs or the
  error?" If yes → trash; at most link or extend an existing doc.

"General" alone isn't enough — a skill must also be **project-specific AND non-obvious**.

## Pre-write self-check — kill these five weaknesses before saving
1. **Discriminating trigger, not a symptom magnet.** The `description`/When-to-use must distinguish
   THIS cause from other causes of the same symptom. A trigger like "endpoint 500s" or "field is
   null" fires on dozens of unrelated bugs → opened at the wrong time and ignored. Anchor it to the
   *distinctive* signal: a specific log string, error class, or precondition — not the user-visible
   symptom alone.
2. **Re-test "non-obvious" against existing tooling.** Check whether the stack trace, logs, or error
   message *already* surface the cause (e.g. the controller already logs the real message). If they
   do, the skill can't rest on "the bug is mysterious" — it must earn its place on something else (a
   multi-place invariant, a counter-intuitive mechanism) or be cut. Make Step 1 = read that signal.
3. **Disambiguate every overlap.** If any existing skill OR a CLAUDE.md/AGENTS.md rule shares the
   symptom, add a one-line "this vs that — same symptom, different cause" and cross-link it.
4. **Strip generic advice; if little remains, it's trash.** Delete sentences a competent dev already
   knows. Keep only the repo-specific mechanism. Strip test: remove the obvious lines — if the skill
   collapses, don't write it.
5. **Write for the world as it is now.** Note what's already fixed/mitigated and exactly where the
   class still bites, so the skill doesn't describe an already-closed path as if it were live.

## File template
Every skill file must follow this exact structure:

    ---
    name: <skill-name>
    description: <one line — when to use this>
    last-updated: YYYY-MM-DD
    ---

    ## When to use
    <one paragraph — the trigger condition, including phrases the AI or a user might say>

    ## Steps
    1. ...

    ## Verification
    <how to confirm it worked — a command + expected output, a file that should now exist, an HTTP status, etc.>

    ## Related (optional)
    - [other-skill](./other-skill.md) — short reason for the link

## Naming
Short, verb-led, kebab-case. Good: `setup-local-dev.md`, `run-migrations.md`, `debug-failing-tests.md`,
`add-env-var.md`. Bad: `notes.md`, `misc.md`, `useful.md`.

## Quality bar
- Steps specific enough for a fresh assistant or teammate to execute without context. Replace
  "configure the env" with the exact env var name and an example value.
- Verification must be observable, not "looks good" — prefer a command + expected output over prose.
- One skill = one workflow. If you have two sets of steps in one file, split.
- Broad scope, concrete steps: the *trigger* and *steps* generalize to the whole class; the
  *examples* inside steps stay concrete (real commands, real paths, real error strings).

## Updating existing skills
Found a new gotcha or a changed step? Update the existing skill in place — don't create a
near-duplicate. Bump `last-updated` to today. If a workflow is fully superseded (tool replaced,
approach abandoned), delete the file in the same commit and link the replacement from any related
skill's `Related` section.

## When the project has no `docs/skills/` yet
First time you'd write a skill in a repo without the folder: create `docs/skills/` and a minimal
`README.md` pointing back to this rule, then add the first skill. Don't skip just because the folder
is missing.
