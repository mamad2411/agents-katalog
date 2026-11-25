---
name: pr-description
description: Generates complete, structured pull request descriptions. Use when the user says "write a PR description", "generate a pull request", "describe my changes", "write the PR for this diff", "help me document this PR", or pastes a git diff, commit list, or change summary and asks for a description.
---

# PR Description Writer

Generates clear, structured pull request descriptions from a diff, commit list,
or change summary. Covers what changed, why, how to test it, and any risks —
so reviewers can understand and merge with confidence.

---

## Required Details

Collect or infer before writing. Ask if critical ones are missing.

| Detail | Example |
|---|---|
| **What changed** | Diff, commit messages, or plain description |
| **Why** | Feature request, bug fix, refactor, chore |
| **Ticket / issue** | `PROJ-123`, `#456`, or none |
| **How to test** | Steps to verify the change works |
| **Breaking change?** | Yes / No — affects other teams or APIs |
| **Screenshots needed?** | Yes for UI changes, No for backend |

---

## Instructions

### Step 1 — Classify the change type

| Type | Label |
|---|---|
| New functionality | `feat` |
| Bug fix | `fix` |
| Refactor without behavior change | `refactor` |
| Tests only | `test` |
| Config, deps, tooling | `chore` |
| Docs only | `docs` |

### Step 2 — Extract the key changes

From the diff or description, identify:
- **What** files/components/APIs changed
- **Why** the change was needed
- **How** it was implemented (if non-obvious)
- **What was NOT changed** (scope clarification, if needed)

### Step 3 — Write the description using this structure

```markdown
## Summary
[1-3 sentence overview. What changed and why.]

## Changes
- [Most important change]
- [Second change]
- [Additional changes...]

## How to Test
1. [Step 1]
2. [Step 2]
3. Expected result: [what success looks like]

## Screenshots
[If UI change — before/after. Otherwise omit this section.]

## Notes
[Breaking changes, migration steps, follow-up tickets, caveats.]
```

### Step 4 — Write the PR title

Format: `type(scope): short description`

```
feat(auth): add OAuth2 login with Google
fix(api): handle null user in /me endpoint
refactor(db): migrate queries to Drizzle ORM
chore(deps): upgrade Next.js to 15.1
```

Rules:
- Lowercase after the colon
- No period at the end
- Max 72 characters
- Scope is optional but helps in monorepos

---

## Non-Negotiable Acceptance Criteria

Do not deliver the description unless ALL of these are true:

- [ ] Title follows `type(scope): description` format, under 72 chars
- [ ] Summary answers "what changed" and "why" in plain language
- [ ] Changes section uses bullet points — one change per bullet
- [ ] "How to Test" has numbered steps and an expected result
- [ ] Breaking changes are explicitly called out in Notes (or stated "None")
- [ ] No implementation details that belong in code comments, not in the PR

---

## Output Format

~~~
## PR Title

[title]

## PR Description

[full markdown description ready to paste into GitHub/GitLab/Bitbucket]
~~~