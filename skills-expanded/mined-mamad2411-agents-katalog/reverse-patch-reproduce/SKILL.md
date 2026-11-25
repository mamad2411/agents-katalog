---
name: reverse-patch-reproduce
description: Use when investigating bug fixes to understand what was broken and verify the fix works. Trigger keywords: debug bug fix, reverse patch, reproduce bug, verify fix, git revert fix, test bug reproduction, investigate commit fix.
---

# Debug by Reverse-Patch Reproduction

## When to use
- Investigating a bug fix commit to understand what was broken
- Verifying that a fix actually solves the problem (not just masking symptoms)
- Understanding the root cause by reproducing the original failure
- Documenting bug behavior for regression tests

## Procedure

### 1. Identify the fix commit
```bash
git log --oneline -20 -- <affected-files>
```
Look for commits with messages like "fix:", "resolve:", or referencing the bug.

### 2. Examine the fix
```bash
git show <commit-hash> -- <file>
```
Review what changed. Note the specific lines modified.

### 3. Check pre-fix state
```bash
git show <commit-hash>^:<file> | sed -n '<start>,<end>p'
```
View the code before the fix to understand the bug.

### 4. Verify clean working tree
```bash
git status --porcelain
```
Ensure no uncommitted changes before reverting.

### 5. Reverse-patch the fix
Manually revert the changes shown in the fix commit. Use your editor to undo the specific modifications, or:
```bash
git revert --no-commit <commit-hash>
```
(Use `--no-commit` to stage without committing, allowing you to test first.)

### 6. Reproduce the failure
```bash
pytest <test-file>::<TestClass> -v
```
Run the tests that should now fail. Confirm the bug manifests as expected.

### 7. Restore the fix
```bash
git checkout -- <files>
```
Or manually re-apply the fix if you edited manually.

### 8. Verify the fix works
```bash
pytest <test-file>::<TestClass> -v
```
Tests should pass again.

### 9. Run full test suite
```bash
pytest tests/ -x -q
```
Ensure the fix doesn't break anything else.

### 10. Verify clean state
```bash
git diff --stat <files>
git status --porcelain
```
Confirm files are back to the fixed state.

## Verification
- Bug reproduces after reverse-patch (tests fail)
- Bug disappears after restoring fix (tests pass)
- Full test suite passes with fix in place
- Working tree is clean after restoration

## Pitfalls
- **Forgetting to restore**: Always verify clean state after investigation
- **Incomplete revert**: Manual reverts may miss related changes in other files
- **Test environment drift**: Ensure test environment matches original conditions
- **Side effects**: The fix may depend on other changes; check commit dependencies
- **Not running full suite**: A fix might solve one bug but break another feature

## Example workflow
```bash
# Find the fix
git log --oneline -10 -- src/module.py
# Show what changed
git show abc123 -- src/module.py
# Revert to reproduce
git revert --no-commit abc123
pytest tests/test_module.py::TestBugCase -v  # Should fail
# Restore
git checkout -- src/module.py
pytest tests/test_module.py::TestBugCase -v  # Should pass
pytest tests/ -x  # Full suite
```
