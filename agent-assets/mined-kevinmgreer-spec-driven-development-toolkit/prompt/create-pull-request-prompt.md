---
description: "Create a pull request from completed ATDD work. Creates a branch, commits changes, pushes, and opens a PR with the spec as the description."
agent: agent
tools: [read, search, execute]
argument-hint: "Feature name or description for the PR title"
---

Create a pull request for the completed feature:

${input}

## Steps

1. **Verify readiness**: Before creating a PR, confirm:
   - All quality gates pass (`/run-quality-gates`)
   - Spec review passed (`/verify-spec-coverage`)
   - All tests are green

2. **Detect Git state**:
   - Current branch name
   - Default branch (`main` or `master`)
   - Whether there are uncommitted changes
   - Remote name (usually `origin`)

3. **Create a feature branch** (if not already on one):

   ```
   git checkout -b feat/<feature-name>
   ```

   Use the kebab-case feature name from the spec file.

4. **Stage and commit** changes with a meaningful commit message:

   ```
   feat: <short description of the feature>

   Implements specs/capabilities/<domain>/behavior.feature
   Change archived at specs/changes/archive/<YYYY-MM-DD>-<name>/

   - N scenarios (smoke, happy-path, edge-case, error)
   - All acceptance tests passing
   - Quality gates: lint ✅ format ✅ typecheck ✅ build ✅ tests ✅
   ```

5. **Push** the branch:

   ```
   git push -u origin feat/<feature-name>
   ```

6. **Create the PR** using the GitHub CLI (if available) or provide the URL:
   - **Title**: `feat: <feature description>`
   - **Body**: Include the ATDD checklist from `docs/atdd/checklist.md`, filled in with actual
     paths and check marks for completed items
   - **Labels**: Add relevant labels if the project uses them

7. **Report** the PR URL and summary.

## PR Body Template

```markdown
## Feature: <name>

Implements `specs/capabilities/<domain>/behavior.feature`.

### Artifacts

| Item           | Path                             |
| -------------- | -------------------------------- |
| Capability      | `specs/capabilities/<domain>/behavior.feature` |
| Rules           | `specs/capabilities/<domain>/rules.md`         |
| Archived change | `specs/changes/archive/<YYYY-MM-DD>-<name>/`   |
| Tests          | `<test-file-path>`               |
| Implementation | `<src-file-path(s)>`             |

### Scenario Summary

| Scenario | Tag | Status |
| -------- | --- | ------ |
| ...      | ... | ✅     |

### Quality Gates

| Gate       | Status |
| ---------- | ------ |
| Lint       | ✅     |
| Format     | ✅     |
| Type check | ✅     |
| Build      | ✅     |
| Tests      | ✅     |

### Spec Compliance

- [x] Every scenario has a corresponding test
- [x] Every business rule is enforced
- [x] No behavior without spec coverage
```

## Rules

- Ask for user confirmation before pushing and creating the PR
- Use conventional commit format if the project uses it
- Do not force-push
- Do not push to the default branch directly
