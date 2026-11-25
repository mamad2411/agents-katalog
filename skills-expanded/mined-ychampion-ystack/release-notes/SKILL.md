---
name: release-notes
description: >-
  Write release notes for users, not developers, from git history between two versions: read the
  commits and PRs, drop what users can't see, group the rest by what changed for them, and write each
  line as a plain-language benefit, with breaking changes and required actions first. Use for "write
  release notes", "changelog for v2.3", "what's new since the last release", "draft the update post",
  or before tagging a release.
---

# Release notes

Commit messages are written for the people who wrote the code. Release notes are for the people who
use it. The job is to translate, and to leave out everything they don't need.

## Procedure

### 1. Find the range

The last release tag to now (`git describe --tags --abbrev=0`), or the range the user gives. List
commits with `git log <from>..<to> --no-merges --format='%h %s'`. Where the project uses pull requests,
read their titles and descriptions too (`gh pr list --state merged --search "merged:>=<date>"`); they
explain why.

### 2. Sort every change

| Bucket | Goes in the notes? |
| --- | --- |
| Breaking: users must change something | Yes, first, with what to do |
| New: something users can now do | Yes |
| Improved: faster, clearer, easier | Yes, if a user would notice |
| Fixed: a bug users could hit | Yes, described by the symptom |
| Security fix | Yes, as "security fix in <area>"; no exploit detail before users can patch |
| Internal: refactors, tests, CI, deps, docs typos | No |

When a commit message is unclear, read its diff. Don't guess.

### 3. Write each line as a user outcome

- Lead with what the user can do or will notice, not what the code does.
  - Developer: "Refactor export pipeline to stream rows."
  - User: "Exports of large projects no longer time out."
- Plain words. No internal names, ticket numbers or file paths unless users see them.
- A fix names the symptom the user saw: "Fixed: the app no longer logs you out after 10 minutes."
- One line each. Merge several commits that make one user-visible change into one line.

### 4. Assemble

```
## <version> - <date>

**Action needed**
- <breaking change>: <what to do, with the exact setting or command>

**New**
- ...

**Improved**
- ...

**Fixed**
- ...
```

Leave out empty sections. Put the single most important change first in its section. If the project
has an existing CHANGELOG or release format, follow it instead.

### 5. Check

Every line traces to at least one commit or PR (keep the mapping in your working notes, not in the
output). Nothing claims more than the code does. Read it as a user who never saw the code: would they
know what changed and whether they need to act?

## Rules

- Users first: drop anything they can't see or act on.
- Breaking changes always come with the action to take.
- No hype words ("blazing", "revolutionary", "seamless").
- Don't publish or tag; hand the draft to the user.
