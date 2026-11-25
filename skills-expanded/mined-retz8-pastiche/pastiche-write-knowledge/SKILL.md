---
name: pastiche-write-knowledge
description: Use when adding or revising a scenario → atom mapping in KNOWLEDGE.md — including when triaging a `knowledge-gap` follow-up from the pastiche skill.
---

# Pastiche — write KNOWLEDGE

Inserts one scenario → atom(s) mapping into `pastiche/KNOWLEDGE.md` per invocation. See KNOWLEDGE.md's header for the scenario format (prose framing line(s), then one or more `→ <atom expression>` lines; atom names backticked, prop expressions bare).

Multi-`→` scenarios are allowed within a single invocation; multiple scenarios are not — re-invoke for each.

## Workflow

1. **Get the scenario.** If a scenario is already on the table (free-form discussion, or a `knowledge-gap` follow-up carrying scenario text + optionally file/line/would-be atom), use it. Otherwise ask the user for one or two lines of scenario phrasing. Read `pastiche/FACT.md` in full.

2. **Identify the section.** List the candidate sections: `grep -n '^## ' pastiche/KNOWLEDGE.md | grep -v '## Brand Identity'`.

   - **Brand Identity is out of scope.** If the user names `## Brand Identity` (or the scenario is brand-prose rather than a scenario→atom mapping), stop and report:

     > Brand Identity is prose, not a scenario mapping. Edit `pastiche/KNOWLEDGE.md`'s Brand Identity section directly, or run `/pastiche-setup --section brand-identity` to rewrite it.

   - If the user named a section, verify spelling against the list (case-insensitive / near-match; surface the closest match for confirmation if no exact hit). If no plausible match, stop and report the misspelling.
   - If the user did not name a section, propose the best-fit section from the list based on the scenario text and confirm with the user. The user may override.

3. **Show existing neighbors.** Read the chosen section by line range (from `## <Section>` to the next `## `) and display it to the user so they can self-detect duplication or refinement opportunities. If the section's only content is `_(empty — run /pastiche-setup --section <name>)_`, show that line and note there are no neighbors yet.

4. **Draft and confirm.** Compose the scenario as it will appear in the file: one or more prose framing lines, followed by one or more `→` lines. Atom names backticked — **FACT entries verbatim**; never derived utility forms or untracked utility classes (those belong as WISDOM `[GENERAL]` rules). Prop expressions bare.

   If the available context is missing either the framing or the atom expression(s), ask only for the missing piece. Surface candidate atoms from FACT when helpful.

   **Verify each backticked identifier against FACT before showing the draft.** For each identifier `X`:
   - Component lookup: `grep -nE '^X:' pastiche/FACT.md` (inside the `## Components` YAML block; top-level keys only).
   - Token lookup: `grep -nFx 'X' pastiche/FACT.md` (flat lines under `## Tokens`).

   If neither matches: retry case-insensitively and surface the closest match for confirmation. If still no match, stop and report:

   > Identifier `<X>` is not in FACT.md. Either it's misspelled, FACT is stale (run `/pastiche-sync`), or the atom doesn't exist — in which case rephrase the scenario around an atom that does, or treat it as a knowledge-gap to surface to the DS owner.

   Show the exact lines as they will appear in the file and ask: `yes / edit`. Loop on edits until confirmed.

5. **Insert.** Find the chosen section's end (the line before the next `## ` heading, or end-of-file if it's the last section).

   - If that range's sole content is `_(empty — run /pastiche-setup --section <name>)_`, **replace** that marker line with the new scenario (preserve a single blank line above and below as the surrounding sections have).
   - Otherwise **append** the new scenario at the end of the section (insert before the next `## ` heading; preserve a single blank line of separation from the prior scenario).

6. **Lint.** Shell: `pastiche-lint` (on PATH via plugin `bin/` — do not search), cwd = repo root. Forward stdout; on non-zero exit, also forward stderr. Don't revert; don't abort. Then close with:

   - exit 0: *"Inserted at KNOWLEDGE.md:`<line>`. Lint passed. Re-invoke for additional scenarios."*
   - exit non-zero: *"Inserted at KNOWLEDGE.md:`<line>`. Lint output above — review and remediate. Re-invoke for additional scenarios."*
