---
name: compounded-typo-fixer
description: Use this skill when the user reports a typo in their codebase or documentation and asks for it to be fixed across the project, or when reviewing code and noticing a misspelled identifier, comment, or string that should be corrected consistently across all occurrences.
---

# Typo Fixer

A demo skill that ships with compounded to show the full lifecycle. Starts as `.verified` (we shipped it pre-verified to make the demo work). After 3 successful uses without correction, it auto-promotes to `.trusted`. After 10 uses with zero corrections in the last 5, it goes `.autonomous`.

## When to use

- The user reports a misspelling and asks for it to be fixed everywhere
- You notice a misspelled identifier in a code review and decide it should be corrected
- The user provides both the wrong spelling and the correct one explicitly

## Inputs

- **`<wrong>`**: the misspelled token (case-sensitive by default)
- **`<right>`**: the correct token
- **`<scope>`** (optional): a directory to limit the search to. Default: the project root.

## Procedure

1. Confirm with the user: "Replacing `<wrong>` with `<right>`" — show this before searching.

2. Run a recursive search for the wrong spelling:

   ```bash
   grep -rn "<wrong>" <scope> --include="*.{ts,tsx,js,jsx,py,go,rs,md,txt}" 2>/dev/null
   ```

   Adjust the `--include` glob to match the project's primary languages.

3. Review the matches. For each one, decide if it is a true positive (a real instance of the typo) or a false positive (a substring that incidentally contains the typo, or a deliberate use like in a test fixture).

4. If any false positives exist, list them to the user and ask which to skip.

5. Apply the replacements via the `Edit` tool, one file at a time. Do NOT use `sed -i` for this — it is too easy to corrupt files when the replacement is not what was expected.

6. After all edits, re-run the grep to verify no instances of `<wrong>` remain in the affected files.

7. Run the project's test suite if one exists, to verify nothing broke. Common commands: `npm test`, `pytest`, `cargo test`, `go test ./...`.

## Pitfalls

- **Substring false positives.** `recieve` is a typo. `recieve_count` containing `recieve` is also a typo and *should* be fixed. But `received` (correct) contains `recei`, and a careless replacement of `recei` → `recie` would corrupt it. Always match whole tokens when possible.

- **Case sensitivity.** `Recieve`, `recieve`, and `RECIEVE` may all need fixing, but the replacements differ. Either run three passes or use a case-aware tool. Do not lowercase identifiers blindly.

- **Test fixtures with intentional typos.** Some test files deliberately contain misspellings (e.g., a parser test for typo tolerance). Skip those files unless the user confirms.

- **Locked or generated files.** `package-lock.json`, `Cargo.lock`, `*.generated.ts`, and similar files should not be hand-edited. Skip them; they will regenerate.

## Verification

After all replacements:

1. `grep -rn "<wrong>" <scope> --include="<langs>"` returns no matches in non-skipped files
2. The project's test suite passes
3. The user confirms the fix looks right

If any of these fail, report the failure honestly. compounded will count this as a correction event and demote the skill if appropriate.
