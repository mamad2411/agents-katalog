---
name: pr-message
description: Draft a pull-request message (title + Markdown body) for the current branch into main. Use when the user asks for a "PR message", "PR description", "pull request message", or says "write a PR message" / "give me a PR message". Output is Markdown text only — does not call `gh` or open a PR.
---

# pr-message

Draft a PR message for merging the current branch into `main` and hand
the user a single fenced Markdown block they can paste into the GitHub
UI or into `gh pr create --body-file -`.

This skill is **repo-local** to py-cv-claw. It does not call `gh` and
does not open or edit PRs.

## Defaults

- **base** = `main`
- **head** = the current branch (typically `dev`; whatever
  `git rev-parse --abbrev-ref HEAD` returns)

Print what you inferred at the top of your reply. Do not ask the user
to confirm base/head unless head is `main` itself (in which case stop
and ask — there's nothing to merge).

## Procedure

1. **Discover scope.** Run these in parallel and read the results:
   - `git rev-parse --abbrev-ref HEAD` — confirm head branch.
   - `git log --oneline main..HEAD` — commits on the branch.
   - `git diff main...HEAD --stat` — file-level shape (note the
     triple-dot: changes on HEAD relative to the merge base, ignoring
     work added to `main` since the branch diverged).
   - `git diff main...HEAD` — read enough of the actual diff to
     verify commit messages tell the truth. Commits sometimes
     mis-describe their scope; the diff is ground truth.

2. **Sanity-check the state.** Stop and tell the user (don't draft)
   when any of these hold:
   - `git log main..HEAD` is empty — no commits to describe.
   - Head branch is `main`.
   - The branch contains merge commits *from* `main` that muddy the
     diff. Offer: "Want me to describe only commits authored on this
     branch (`git log main..HEAD --no-merges`), or include the merges?"

3. **Decide whether to ask for framing.** Ask the user *before*
   drafting only when:
   - The diff spans clearly unrelated themes and the commit titles
     don't unify them (e.g. one commit is a dep bump, another is an
     unrelated feature, no shared narrative).
   - The diff is large (>~30 changed files) **and** commits are
     terse / generic.

   Otherwise: draft silently. Most branches in this repo are tightly
   themed — don't manufacture ambiguity.

4. **Pick the title.**
   - One line, ≤70 chars, imperative mood, no trailing period.
   - Prefer the dominant conventional-commit prefix from the branch
     (`feat:`, `fix:`, `refactor:`, `docs:`, `chore:`). Fall back to
     descriptive prose if commits are mixed types.
   - The title should stand on its own — a reader scanning the PR list
     should understand what's in this PR without opening it.

5. **Write the body.** Exactly three H2 sections, in this order:

   ```markdown
   ## Summary

   1–2 sentences. The "why," not the "what." Name specs implemented,
   issues closed, or design docs referenced — but only if they're
   actually present in the diff or commit messages. Never invent links
   or issue numbers.

   ## Changes

   Grouped bullets by area. Group labels are derived from the diff;
   typical groups in this repo:

   - **Code** — anything under `src/cvclaw/`.
   - **Skills** — `skills/cv-claw/` and `.claude/skills/`.
   - **Docs** — README.md, CLAUDE.md, `.claude/specifications/`.
   - **Templates** — `src/cvclaw/templates/` (the bundled root).
   - **Build/CI** — pyproject.toml, Makefile, .github/.

   Skip groups with no changes. Each bullet ≤1 line; reference files
   or subsystems (`src/cvclaw/cli.py`, "ingest.md") rather than commit
   hashes. Bold the group label.

   ## Test plan

   Markdown checklist. Use only steps the repo actually supports —
   read `Makefile` and `pyproject.toml` to ground each step. For this
   repo that's typically:

   - [ ] `make lint` is clean.
   - [ ] `uv run cv-claw render resumes/example.json` succeeds.
   - [ ] Any spec-specific manual smoke tests called out in the
         relevant `.claude/specifications/SPEC-*.md`.

   Do not invent CI jobs, test suites, or pytest invocations that
   don't exist in this repo.
   ```

6. **Output.** Reply with:
   - A single preamble line: `PR message for `<head>` → `<base>`,
     drafted from N commit(s) across M changed file(s).`
   - A single fenced code block (```markdown … ```) containing the
     title on the first line, a blank line, then the body. This makes
     the whole thing one copy-paste.

## Output template

```markdown
<title>

## Summary

<1–2 sentences>

## Changes

- **<Group>** — <bullet>
- **<Group>** — <bullet>

## Test plan

- [ ] <step>
- [ ] <step>
```

## Conventions (must follow)

- **No emojis** anywhere in the title or body.
- **No "🤖 Generated with Claude Code" trailer.** That's for
  `gh pr create` invocations; this skill produces hand-drafted
  Markdown the user pastes manually.
- **No `Co-Authored-By` trailers.** Those go on commits, not PR bodies.
- **Three sections only.** No Notes / Open questions / Followups
  section. Caveats fold into Summary or as inline bullets in Changes.
- **Don't fabricate test steps.** If a verification step isn't real
  (no test suite exists, no CI workflow exists), don't list it.
- **Don't reference specs or issues that aren't in the diff or
  commits.** If `.claude/specifications/SPEC-foo.md` is touched in
  this PR, mention it; if it isn't, don't.
- **Don't open or edit a PR.** This skill writes text. If the user
  wants the PR opened, they will say so separately and the global
  `gh pr create` flow handles it.

## Out of scope

- Running `gh pr create` / `gh pr edit` / `gh pr view`.
- Choosing reviewers, labels, assignees, milestones, or draft state.
- Cross-repo PRs or stacked PR chains.
- Updating an existing PR body in place.

## Edge cases

- **Branch is up-to-date with main** (no commits ahead). Don't draft;
  tell the user there's nothing to merge.
- **Branch is behind main.** Draft normally, but note in the preamble
  that the branch is behind and may need a rebase before opening the
  PR.
- **User asks for a PR message targeting a base other than `main`**
  (e.g. "PR message into `release/0.2`"). Honor the requested base;
  use `<base>...HEAD` for the diff range.
- **User asks while on `main`.** Stop; ask which branch they meant.
- **Detached HEAD.** Stop; ask the user to check out a branch first.
