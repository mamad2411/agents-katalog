---
name: document-release
license: CC-BY-4.0
description: >-
  Post-ship documentation check: compare the branch diff with every project doc
  (README, architecture, contributing, agent instructions, changelog, TODOs,
  VERSION), fix factual drift, and report a health summary per file. Use after
  shipping a feature or when docs may be stale. Commits, pushes or PR edits only
  when the user asks for them.
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# Document Release

Outcome: the project's docs match what the branch ships, every doc found gets
a status line, and nothing is published beyond what the user asked for.

## What the request authorizes

| Request | Edit docs | Commit | Push / PR body |
|---|---|---|---|
| Review, check, "what is stale" | no, propose edits | no | no |
| Update or fix the docs | yes | only if asked | only if asked |
| "…and commit" / "…commit and push" | yes | yes | push if asked; PR body if asked |

Showing a draft is not approval to publish it. A question that needs the user
(VERSION, narrative rewrites) does not block the rest of the authorized work:
finish it and list the open questions in the report.

## 1. Establish what shipped

- Base branch: the PR's base (`gh pr view --json baseRefName -q .baseRefName`),
  else the default branch (`git symbolic-ref --short refs/remotes/origin/HEAD`
  prints `origin/<name>`), else `main`. On the base branch itself, stop and say so.
- Read `git log <base>..HEAD --oneline`, `git diff <base>...HEAD --stat`, and the
  changed code. List user-visible changes: commands, flags, options, config,
  APIs, install steps, removed or renamed features.

## 2. Find the docs

Discover them instead of assuming a fixed set: tracked Markdown, RST and text
files (`git ls-files '*.md' '*.rst' '*.txt'`), `docs/`, agent instructions
(`AGENTS.md`, `CLAUDE.md`), `CHANGELOG*`, `TODOS*`, and `VERSION`. Skip vendored,
generated and dependency trees; handle changie fragments in step 4.

## 3. Check each doc against the diff

- **README:** features, usage examples, options, install steps.
- **Architecture docs:** change only what the diff contradicts.
- **Contributing / agent instructions:** would each listed command and path
  still work for a new contributor?
- **Any other doc:** does it contradict the diff?
- **Across docs:** versions agree; every doc is linked from the README or the
  agent instructions (flag orphans).

Fix factual drift directly when editing is authorized: paths, counts, options,
tables, examples, stale cross-references. Propose and ask for narrative or
positioning changes, security descriptions, section removals, and rewrites of
more than about ten lines. Read a file fully before editing it and keep edits
narrow; write for a reader who has not seen the code.

## 4. Changelog, version, TODOs

- **Never clobber the changelog.** Do not delete, reorder or regenerate
  entries; polish wording only and ask before changing meaning. Apply a narrow
  patch with exact current text as context, and inspect the diff afterwards.
  Never overwrite CHANGELOG.md as a whole file.
- **Changie projects** (`.changie.yaml`): leave `CHANGELOG.md` alone and do not
  create fragments. You may polish the `body` of existing unreleased fragments
  within the project's kinds and `body.maxLength`. Report a user-visible change
  that has no fragment.
- **VERSION:** never change it without the user's approval. If it was not
  bumped on the branch, report the current value and recommend following the
  project's release process. If it was bumped, check that the changelog for
  that version covers everything on the branch and report what it misses.
- **TODOs:** mark an item done only with clear evidence in the diff; propose
  new items for meaningful `TODO`/`FIXME` comments added by the branch.

## 5. Publish only what was asked

- **Commit:** stage the edited doc files by name (never `git add -A`), with a
  message that says what changed (for example
  `docs: document --json flag in README`) in the repository's commit style.
- **Push:** only when asked. If it fails (no remote, authentication, rejected),
  report the error and that the commit is local only.
- **PR body:** only when asked and a PR exists. Replace or append a
  `## Documentation` section listing each changed file, and pass it with
  `gh pr edit --body-file`. Report a failed edit.

## 6. Report

End with a health summary, one line per doc found:

```text
Documentation health:
  README.md      Updated: documented --json flag in Usage and Options
  CONTRIBUTING   Current
  CHANGELOG.md   Current: changie project; fragment Added-…yaml covers --json
  VERSION        Needs decision: 1.4.0, not bumped on this branch
```

Statuses: Updated (what changed), Proposed (review only), Current, Needs
decision (the question), Voice polished. Then state what was committed and
pushed, with any failure.
