---
name: pastiche-write-wisdom
description: Use when adding or revising an atom-intrinsic rule in WISDOM.md — including when triaging a `wisdom-gap` follow-up from the pastiche skill.
---

# Pastiche — write WISDOM

Inserts one atom-intrinsic rule into `pastiche/WISDOM.md` per invocation. See WISDOM.md's header for the bullet format. Tags are **FACT entries verbatim**; never derived utility forms. `[GENERAL]` is the lone non-FACT tag, reserved for system-wide rules.

## Workflow

1. **Get the rule.** If a proposed rule is already on the table from the surrounding conversation (e.g., a `wisdom-gap` follow-up), use it. Otherwise ask the user for the rule. Read `pastiche/FACT.md` in full.

2. **Atom-intrinsic test.** Can the rule be stated as a property of the atom that holds *everywhere* the atom appears? If it contains a scenario qualifier ("in payment flows", "for destructive actions", "when used as a primary CTA"), it is scenario-conditional and belongs in KNOWLEDGE. Stop and report:

   > This rule is scenario-conditional (qualifier: `<phrase>`). It belongs in KNOWLEDGE as a scenario→atom mapping. Re-invoke `/pastiche-write-knowledge` with this rule.

   Counter-example that fails the test (this is KNOWLEDGE, not WISDOM):
   - *"Destructive actions must use ConfirmDialog rather than a generic Modal."* — qualifier: "destructive actions".

3. **Pick tags.**
   - If the user proposed `[GENERAL]` upfront, skip to step 4.
   - Otherwise lock the primary atom tag. If the user gave a tag, verify it appears in FACT verbatim. If not, retry case-insensitively / for near-matches and surface the closest match for confirmation. If still no match, stop and report:
     > Tag `<X>` is not in FACT.md. Either it's misspelled, FACT is stale (run `/pastiche-sync`), or the atom doesn't exist — in which case reconsider as KNOWLEDGE (scenario-conditional) or `[GENERAL]` (system-wide).
   - If the user did not give a tag, suggest candidate atoms from FACT that the rule plausibly tags. User picks the primary tag.
   - **Multi-tag.** Scan FACT and propose additional atoms the rule applies to identically. User picks any (zero or more). Verify each picked tag against FACT spelling as above.
   - **5+ tags → re-route.** Prompt: *"This applies to many atoms — consider `[GENERAL]` instead?"* If yes, go to step 4.

4. **`[GENERAL]` gate** (only when `[GENERAL]` is proposed). Apply both tests; halt on either failure:
   - **Tag-fit:** Can the rule be tagged to a specific atom or finite set of atoms from FACT? If yes, halt and redirect to step 3 with that tagging.
   - **System-wide:** Does the rule hold for *all* UI in the project regardless of which atoms are used? If no, halt and ask whether it is scenario-conditional (→ `/pastiche-write-knowledge`) or atom-specific after all (→ step 3).

   Only proceed when both tests pass and the user explicitly confirms `[GENERAL]`.

5. **Show existing neighbors.** For each chosen tag, `grep -nE '\[([^]]*,)?<Tag>(,[^]]*)?\]' pastiche/WISDOM.md | grep -vE '^[0-9]+:[[:space:]]*<!--'` (escape any regex meta-characters in `<Tag>`). Show the matching entries to the user so they can self-detect duplication or refinement opportunities before drafting.

6. **Draft and confirm.** Compose the bullet in canonical form: `- [Atom1,Atom2] rule text.` Show the exact line and ask: `yes / edit text`. Loop on edits until confirmed.

7. **Insert.** For each tag in the new entry, `grep -nE '\[([^]]*,)?<Tag>(,[^]]*)?\]' pastiche/WISDOM.md | grep -vE '^[0-9]+:[[:space:]]*<!--'` (escape regex meta-characters in `<Tag>` as in step 5). Insert the bullet immediately after the last matching line across all the entry's tags. If no tag has any existing match, append to end of file.

8. **Lint.** Shell: `pastiche-lint` (on PATH via plugin `bin/` — do not search), cwd = repo root. Forward stdout; on non-zero exit, also forward stderr. Don't revert; don't abort. Then close with:

   - exit 0: *"Inserted at WISDOM.md:`<line>`. Lint passed. Re-invoke for additional rules."*
   - exit non-zero: *"Inserted at WISDOM.md:`<line>`. Lint output above — review and remediate. Re-invoke for additional rules."*
