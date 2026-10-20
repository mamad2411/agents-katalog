---
description: Address PR review comments by updating spec, tests, or implementation as needed. Follows the spec change protocol when behavior changes are requested.
argument-hint: "<PR number or description of review feedback>"
---

Address review comments for:

$ARGUMENTS

## Steps

1. **Gather feedback**: Read the PR review comments (`gh pr view <number> --comments` or
   `gh api repos/{owner}/{repo}/pulls/<number>/comments`). Categorize each comment as:
   - **Style/naming** — code style, variable names, formatting (fix directly)
   - **Bug fix** — reviewer found a logic error (fix in implementation, verify tests catch it)
   - **Behavior change** — reviewer wants different behavior (requires spec update first)
   - **Missing coverage** — reviewer wants additional scenarios (add to spec first)
   - **Question** — reviewer asks for clarification (answer in PR comment)

2. **Handle behavior changes** (if any) using the Spec Change Protocol.

   Phase 7 already archived the change, so `specs/changes/<name>/` no longer exists. The
   behavior now lives in the capability, and the archived delta is the record of what shipped —
   update both so the audit trail matches reality:

   a. Update `specs/capabilities/<domain>/behavior.feature` first (and `rules.md` if rules
      changed). A repair that removes a guarantee is a spec weakening: it needs sign-off, and it
      is never applied under "match the code"
   b. Update the archived delta in `specs/changes/archive/<YYYY-MM-DD>-<name>/` to match, so
      history shows what actually shipped rather than what was first proposed
   c. Update or add test stubs — confirm they are red
   d. Update implementation — confirm all tests are green
   e. Run quality gates

3. **Handle bug fixes**:
   a. Verify the bug exists (if possible, demonstrate with a failing test)
   b. Fix the implementation
   c. Run tests to confirm the fix
   d. Run quality gates

4. **Handle style/naming feedback**:
   a. Make the requested changes
   b. Run quality gates to confirm nothing breaks

5. **Run all quality gates** after all changes are made.

6. **Commit and push** the changes:

   ```
   fix: address PR review feedback

   - <summary of each change made>
   ```

7. **Report** what was changed and which review comments were addressed.

## Rules

- **Never change behavior** without updating the spec first
- **Never modify tests** to accommodate a code fix — fix the code
- If a reviewer requests behavior that contradicts the spec, flag it and ask: "This would change
  the spec. Should I update the spec to reflect this new requirement?"
- Address ALL review comments — don't leave any unresolved
- Run quality gates after every batch of changes
