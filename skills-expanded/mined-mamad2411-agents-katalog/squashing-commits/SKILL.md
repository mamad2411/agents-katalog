---
name: squashing-commits
description: Compose a polished commit message and optionally squash commits when finishing work on a branch or worktree. Use this skill whenever the user says things like "finish this branch", "squash commits", "prepare for PR", "wrap up", "finalize", "commit final", "ready for review", or wants to consolidate branch history into a single, well-crafted commit. Also use when another skill delegates commit message composition here — even for a single file or a single commit where there is nothing to squash. The core value is the structured commit message, not the squash.
---

# Squashing Commits

This skill produces a single, well-crafted commit on a feature branch — and squashes prior commits into it when needed. The output should let anyone reading `git log` months later understand the change without reading the diff: why it was needed, which decisions matter, and what they mean for the system.

## When to use

- User is done implementing on a feature branch or worktree
- User wants to squash before opening a PR
- User wants to rewrite messy history into one coherent commit
- Another skill delegates commit message composition here
- Staged/unstaged changes need a commit message — even with nothing to squash

## Step 1: Gather context

Determine state: multiple commits to squash, single commit to amend, or fresh uncommitted changes.

```bash
# Uncommitted changes?
git status --short

# Base branch + divergence
git merge-base HEAD main
git rev-list --count main..HEAD

# All commits on this branch since main (skip if count is 0)
git log --reverse --format="%h %s%n%n%b%n---" main..HEAD

# Full diff — pick the right comparison
# If commits exist on branch:
git diff --stat main..HEAD
git diff main..HEAD
# If only staged/unstaged changes:
git diff --stat HEAD
git diff HEAD

# Project commit-message conventions (type usage, voice, length)
git log --oneline -30 main

# Force-push needed after squash? Count commits since main that already exist on the remote.
upstream=$(git rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>/dev/null) && \
  git rev-list --count "main..$upstream"
# Output: number of commits on the branch that have already been pushed.
# > 0 → squashing will rewrite published history; push needs --force-with-lease.
# 0 (or no upstream configured) → nothing pushed yet; a normal push works.
```

If the user pre-specified which commits to include ("squash everything except commit X", "only the last 3 commits"), record that constraint and use it when picking the squash base in Step 6. The **default** is to squash every commit since `main`.

Read the diff carefully. The body explains *why*, not *what* — you need to understand the change deeply enough to write about its motivation and consequences.

## Step 2: Identify the story

Before writing, answer internally:

1. **What problem did this branch solve?** What was broken, missing, or inadequate before?
2. **Which decisions are significant?** Not every file change is a decision. Focus on choices that constrain future work, surprise a reader, or have functional consequences.
3. **What are the tradeoffs?** Did a decision close a door or open one?
4. **What's trivial?** Renames, formatting, mechanical config. Don't give these equal weight to architectural decisions.
5. **Do any decisions depend on others?** If decision B consumes the output of decision A, A's paragraph must come first (see "Sequence producers before consumers" in Step 4).

## Step 3: Choose the type

This project uses a deliberately small vocabulary: six types, picked so each one carries a clear release-time meaning.

| Type     | When                                                                                              |
|----------|---------------------------------------------------------------------------------------------------|
| `feat`   | New feature or significant user-visible improvement                                               |
| `fix`    | Bug or problem correction                                                                         |
| `sec`    | Security fix or hardening                                                                         |
| `revert` | Reverts a previous commit. Subject typically `revert: <original subject>`                         |
| `docs`   | Documentation work                                                                                |
| `chore`  | Everything else: refactors, tests, build/CI, dependency bumps, formatting, repo upkeep            |

`chore` is a catchall, not an auto-drop signal. The release-prep workflow inspects every `chore` body individually to decide whether it ships in CHANGELOG.md or stays in `git log` alone (see `.agents/skills/creating-release/references/categorization.md`). A `chore` that changes user-visible behaviour needs a body paragraph that says so plainly — the workflow has nothing else to read.

**Breaking changes:** mark a breaking commit with `type!:` in the subject (e.g. `feat!: drop /v1`) or a `BREAKING CHANGE:` paragraph in the body. The release-prep workflow reads both markers; pick whichever fits the message better. A breaking commit always carries one of those two signals — `creating-release` will not infer a break from prose alone, so a renamed CLI command, a removed config key, or a changed wire format that ships without one of the markers gets silently classified as non-breaking and skips the release-note's `## Important: breaking changes` block. If a caller could pin it, mark it.

**Mixed branches:** when a single squash bundles work that spans multiple types (a feature plus its CI plumbing, a fix plus a docs update), pick the type that names the user-visible change. `feat` beats `chore` when both ship together; `fix` beats `docs` when a bug fix is documented alongside.

## Step 4: Write the commit message

**REQUIRED SUB-SKILL:** Invoke `writing-clearly-and-concisely` and apply its rules to every paragraph as you draft. Strunk's discipline (omit needless words, prefer active voice, use definite specific concrete language, put statements in positive form) catches the slop this skill's structural rules don't — wandering paragraphs, weak verbs, hedged claims. The structural rules below give shape; the writing skill gives tightness. Apply both.

Format:

```
type: subject

Problem description.

Solution detail.
```

This project does not use scopes. The subject is `type: subject` only — never `type(area): subject`.

### Subject line rules

- All lowercase, no trailing period, max 72 chars
- Imperative verb (`implement`, `fix`, `add`, `bootstrap`)
- Must complete the sentence "This commit will… [subject]"

### Body rules

The body is **prose paragraphs**. No bullet lists. Default to English unless the user prefers otherwise.

**Problem paragraph:** Why the change was needed. The reader should grasp the motivation without reading the diff.

**Solution paragraphs:** Technical decisions and their *functional consequences*. The diff shows what changed; the body explains why this approach and what it means for users of the system.

### Writing principles

**Write in system terms, not author terms.** The problem paragraph states the condition of the project the change addresses — not the author's experience of it. "The diff alone cannot carry intent across months" belongs in a commit; "I kept writing bad commits at the end of branches" does not. Declarative present tense ("This project adopts X.", "X now happens before Y.") reads cleaner than past-tense narrative ("we observed X drifting"). Applies to every commit type: feature, fix, CI, tooling, refactor.

**Omit provenance of inspiration.** Prior art outside the repo — upstream skills, blog posts, other projects that solve a similar problem, conference talks, an abandoned earlier branch — is out of scope. The reader is looking at *this* repo's history and needs to understand *this* repo's decision. Where the idea came from is irrelevant to whether the decision was right.

**Spend at most one sentence on methodology.** TDD cycles, baseline evaluations, A/B tests, survey-then-validate processes — the reader cares the change works, not how you proved it. One sentence at most, often zero. If methodology is genuinely load-bearing (regulated environment, reproducible-build requirement, security review trail), it earns its sentence; otherwise it's noise.

**Lead with functional impact, not implementation detail.** A decision matters because of what it enables or prevents, not because of which file was edited.

- Good: "A `ch version` subcommand was added alongside, so an installed binary can report what release it came from — and so the pipeline can prove the version actually made it into the artifact."
- Bad: "Adds cmd/version.go with `newVersionCmd()` returning a cobra.Command that prints `cmd.Root().Version`, wired through `cmd.Execute(version string)` from main.go."

**Stay one level above flag-level detail.** Don't enumerate ldflags, YAML keys, or env var names unless they're load-bearing for the reader. "Builds reproducibly across linux/darwin × amd64/arm64" beats listing `-trimpath`, `CGO_ENABLED=0`, and every matrix cell.

**Sequence producers before consumers.** If paragraph B references an artifact produced by paragraph A, put A first. Example: the release workflow publishes `docs/release-notes/<version>.md` as the GitHub release body — so the skill that drafts that file must be introduced before the workflow that consumes it. Reorder paragraphs as needed; don't force a chronological "what we did first" structure.

**Separate significant decisions from trivial ones.** Configuring a registry URL is mechanical; choosing keyless signing has architectural consequences. Give space to decisions that surprise a reader or constrain future work.

**Explain constraints and tradeoffs.** If a decision closes a door or opens one, say so. "The node ID must point to the component set, not to an individual variant — the CLI rejects variants" saves someone from repeating a mistake.

**One topic per paragraph.** Each paragraph covers one decision or a tightly related group.

**No bullet lists.** Prose forces you to connect cause to effect. Bullet lists fragment reasoning.

**Don't manufacture a paragraph per housekeeping change.** README updates, dependency pins, lockfile bumps, and design-doc links rarely warrant their own paragraph. Fold them into the topical paragraph they support (the README mention rides with the feature paragraph; a version pin rides with the integration that needs it) or, when truly cross-cutting, into a single closing "shipping" paragraph. A paragraph that only says "README was updated and the design lives at X" earns nothing.

### Anti-patterns

| Pattern                              | Problem                                                        |
|--------------------------------------|----------------------------------------------------------------|
| Listing every file changed           | The diff shows this. Redundant.                                |
| "Update X, Y, Z" subject             | Describes what, not why. Too vague.                            |
| Elevating trivial changes            | Implies equal weight to all changes.                           |
| Describing the diff in the body      | Reader can see the diff. Explain *why*.                        |
| Bullet-point body                    | Fragments reasoning. Write paragraphs.                         |
| Per-commit bullet walk               | Don't enumerate the commits being squashed in the body. The reader doesn't care about the intermediate steps — only the end state.|
| Housekeeping-only paragraph          | README/deps/design-doc mentions don't justify their own paragraph. Fold them in.|
| Autobiographical framing             | "We kept running into X, so we built Y" tells your discovery story. Reader has no shared timeline. State the system condition the change addresses, declarative present tense.|
| Provenance of inspiration            | "Inspired by/based on/borrowed from upstream X" is out of scope. Where the idea came from has no bearing on whether it was right for this repo.|
| Methodology in the body              | TDD cycles, baseline evals, survey-then-validate — the reader cares the change works, not how you proved it. One sentence at most, often zero.|
| Naming every flag/key                | Buries the functional story under config trivia.               |
| Producer paragraph after consumer    | Forces re-reading. Reorder so first mention introduces.        |
| Mixing languages within one message  | Pick one (default English; respect user preference) and stay consistent across all paragraphs of this commit.|

## Step 5: Present and iterate

Present in this exact order:

1. **First** — list every commit that will be squashed, so the user sees the destructive scope before reading the draft:

   ```
   The following commits will be squashed into one:

     <short-sha> <title>
     <short-sha> <title>
     ...
   ```

   Generate from `git log --reverse --format="%h %s" main..HEAD`. Skip this block if there's only one commit or only uncommitted changes — no destruction, nothing to disclose.

2. **Second** — the full commit message draft, exactly as it will appear in the commit.

3. **Third** — one follow-up prompt, focused on paragraph-level edits. Use this verbatim or with only minor wording changes:

   > Any paragraph to tighten, reorder, or drop? Anything missing?

   The second clause is a deliberate catchall — it lets the user surface omissions without forcing a second exchange. Do not substitute a different framing like "Does the problem description capture the motivation?" or "Did I miss any tradeoffs?". Those put the user in the role of inspector and ask them to do your analysis. The skill's prompt asks them to do their actual job: edit the prose.

Wait for explicit user approval before executing in Step 6. The approval gate applies in every case — message approval is required even when nothing destructive happens (single commit, uncommitted changes). When a squash *is* involved, the gate also protects against destroying history; flag that explicitly in the listing block.

Expect iteration — the first draft rarely lands. When the user asks for a revision (tighten paragraph N, drop a paragraph, reorder, swap subject), re-emit the *full* updated message and ask again. Don't apply edits eagerly between rounds. Don't argue with the request; the user has context you don't.

## Step 6: Execute the commit

Only after the user approves the final message:

### Multiple commits → squash

```bash
# Soft reset to keep all changes staged
git reset --soft main

# Commit with the approved message
git commit -m "$(cat <<'EOF'
<the approved message>
EOF
)"
```

**Heredoc gotcha:** the `<<'EOF'` form (EOF in single quotes) disables shell expansion — so backticks, `$`, and `!` inside the body are passed through verbatim. Do **not** escape them with backslashes; inside a quoted heredoc the backslash is also literal, so `` \`foo\` `` ends up as the seven-character string `` \`foo\` `` in the commit (backslashes and all), not the intended `` `foo` ``. Write the body exactly as you want it to appear.

**If the branch is already pushed (Step 1 detected an upstream),** warn the user that squashing requires `git push --force-with-lease`. Do NOT force push without explicit confirmation.

### Single existing commit → amend

If the branch already has exactly one commit since `main` and you only need to rewrite its message:

```bash
git commit --amend -m "$(cat <<'EOF'
<the approved message>
EOF
)"
```

No reset, no force push (unless the commit was already pushed).

### Uncommitted changes → direct commit

```bash
# Stage as needed
git add <files>

git commit -m "$(cat <<'EOF'
<the approved message>
EOF
)"
```

---

After committing, run `git log -1 --format=full` and verify the body rendered cleanly (no escape artefacts, no truncation). If you spot a problem, re-present the corrected message to the user (per Step 5) and only after they re-approve, amend:

```bash
git commit --amend -m "$(cat <<'EOF'
<corrected message>
EOF
)"
```

A silent amend would bypass the approval gate; the gate exists for content, not only for destruction.

## Step 7: Offer to open the PR

A commit ready for review is the natural trigger for a PR. Ask:

> Commit created. Open the PR now? (y/N)

If yes, proceed with `gh pr create` (or invoke a PR-creation skill if one exists). The fresh commit body should be the primary source for the PR description. If the user declines or stays silent, stop here — the branch is ready when they return.

Do not block on this step. Do not open the PR without explicit confirmation.

## Example output

A commit that bundles a skill, a workflow, a build pipeline, and licensing into one coherent story. Note the producer-before-consumer ordering (skill introduces the release-notes file before the workflow that publishes it) and the functional level of detail (no ldflags, no YAML keys):

```
feat: bootstrap codeherd release process

The repo had no release path. No LICENSE, no installable binaries, and
no convention for drafting per-version notes. Cutting 0.1.0 by hand
would set no precedent and would block downstream tooling — mise
registry submission, version-pinning by users — that depends on signed,
named artifacts.

A `creating-release` skill bundle codifies how
`docs/release-notes/<version>.md` is drafted: it surveys git history
since the last tag and emits a single materialized list of surviving
features rather than a commit-by-commit log. For a first release with
no prior tag, the skill folds intermediate refactors into the feature
set. The same file is what the release workflow later publishes
verbatim as the GitHub release body, so the skill's output is the
canonical per-version narrative.

Releases are then triggered by a commit to `main` that touches
`VERSION`. The new `release.yml` workflow reads the file, builds the
linux/darwin × amd64/arm64 matrix, signs every archive and
`checksums.txt` with sigstore cosign, then creates the `v<version>` tag
and the GitHub release with `docs/release-notes/<version>.md` as the
body.

The build lives in three new Make targets so the same recipe runs
locally, in CI smoke tests, and during release. A new `ch version`
subcommand lets an installed binary report what release it came from
— and lets the pipeline prove the version actually made it into the
artifact. The PR pipeline exercises the full cross-compile matrix on
every change, surfacing toolchain regressions before they reach a
tag. The project ships under Apache 2.0, and the README points users
at the new mise + manual install paths so binary consumers are not
stuck building from source.
```

Note how the final sentence folds Apache 2.0 and the README install update into the existing build/release paragraph rather than spawning a "miscellaneous shipping" paragraph of its own. Housekeeping rides with the topic it supports.
