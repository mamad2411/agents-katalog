---
name: review-change
description: Reviews a change for security and privacy risk and writes security-review.md with findings ranked by severity. Use when acting as the security role, or when asked for a security review of a diff or work item.
---
# Review a change

**Role:** security. This skill is the method. The security `ROLE.md` holds when you run, how the item goes back to the reviewer, and what you must never do (paste a secret, above all). Follow both.

1. Read the brief and the diff. Identify new inputs, trust boundaries, secrets, dependencies and permissions.
2. Compare against the threat model in `docs/security/`. Update it when the change adds surface.
3. Create `security-review.md` with `python3 tools/item_file.py <id> security-review`, then fill it: findings ranked blocker / major / minor, each with impact, evidence and a recommended fix. If the file already exists (the item came back for a second look), add a dated section to it: the tool will not overwrite it.
4. If a finding needs the human (risk acceptance, disclosure, spend), ask with `python3 tools/question.py ask`, giving a recommendation and the cost of guessing wrong.
