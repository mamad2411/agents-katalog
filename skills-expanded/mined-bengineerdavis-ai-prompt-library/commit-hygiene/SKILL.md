---
name: commit-hygiene
description: Keeps commits scoped to one logical change, sizes the message to the change rather than padding it, names the paths being committed so a concurrent process cannot contribute files, and checks afterwards that the commit contains what was intended. Use when committing work, dividing finished changes into commits, or reviewing whether a commit's scope and message match.
spec_hash: 204653837d70
---

# Commit Hygiene

Commits drift two ways at once: they absorb unrelated changes, and the message
grows to cover the sprawl. The length that should have warned you becomes the
camouflage. Treat message length as a **scope signal**, not a quality metric.

## Before committing

1. **List what changed.** `git status --short` and `git diff --stat`.
1. **Name the change in one line, without "and".** If you need "and", that is
   two commits. Split.
1. **Commit by path, never by index state** (see below).
1. **Check what you actually committed** — `git show --stat HEAD`.

## Splitting has a floor

Atomic means **self-contained**, not small. Never split so far that a commit
leaves the tree unbuildable or its tests red for the next commit to repair —
that breaks `git bisect` and makes every intermediate state a lie. Keep together
anything meaningless alone: a flag and the code that reads it, a rename and its
call sites, a signature change and its callers.

Split when a reader would ask "why is this here?", when one part could be
reverted while keeping the rest, when the subject needs "and", or when a
drive-by fix rode along with a feature.

## Size the message to the change

| Change                                               | Message                                                                                              |
| ---------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| Mechanical — typo, rename, version bump, formatting  | Subject only                                                                                         |
| Small, single-purpose — one function, a flag, a test | Subject + 1–2 sentences of why                                                                       |
| Ordinary feature or fix                              | Subject + 1–2 short paragraphs                                                                       |
| Large or security-sensitive                          | Structured body (bullets, full arc) — earned when ONE rationale needs it; still reconsider splitting |

## Structure the body

The blank line is the only delimiter git treats semantically — one
blank-delimited block, one unit; never blank-separate a continued thought.

**The arc.** A body paragraph serves one of four moves, in this order when
all apply: the problem (present tense), why the result is better,
alternatives discarded, review resolutions. The first sentence of each
paragraph *is* its heading — no markup needed.

- **One claim per paragraph.** Test: a reviewer can title the block with a
  single problem statement. Two problem statements = two paragraphs — or
  two commits.
- **Bullets are parallel items of one claim.** Mixed-kind bullets, or an
  inventory growing its own navigational section, is a split signal, not
  structure.
- **No markdown headers.** Bodies render as 72-column plain text in log,
  email and tooling, so `##` is inert there — and needing navigational
  headers is itself evidence the commit holds more than one change. If you
  reach for `##`, ask whether it is a split. Trailers stay available for
  machine consumption (`Refs: #123`, `BREAKING CHANGE: ...`) — they parse;
  decoration does not.
- **No measured length threshold exists** (the 50/72 limits are interface
  constraints, not reader-load findings). Bands are observable:
  *subject-only* when no reviewer question survives the subject; *short*
  when one paragraph discharges the single claim; *structured* when the one
  claim has parallel evidence items worth enumerating; *long* when each of
  the arc's four moves needs its own paragraph for ONE rationale.
  Per-module sections are not "long" — they are the split signal.
- **Band check:** subject strain ("and"), more than one type, or more than
  one rationale → split, don't lengthen. Length is never the fault;
  multiplicity of rationale is.

## Scope: group, split, or series

One commit = one judgeable claim a reviewer can rule on **without reading
the patch**.

- **Revert-together:** if either rationale would ever be reverted without
  the other, it was never one change — split.
- **Test-together:** each commit builds and passes the suite alone. Commit
  N needing N−1 green means resequence, squash, or admit it is one change.
- **Series, not fat commit:** cross-module changes sharing one rationale
  ship as a series — a shared `area:` prefix, the unifying rationale in the
  first commit's body, one change per commit. Adjacency is not coupling:
  tree-wide cleanups ship separately from real work.
- **Grouping by `git add -p`** is normal practice: one issue per commit,
  even within one file. Difficulty writing the subject means too many
  changes.

When the body keeps growing past the arc, re-read the diff: a body that
needs its own navigation is the commit telling you it contains more than one
idea. Split it; each piece then needs far less explaining, because each one
is about a single thing.

Never pad. A one-word typo fix with a three-paragraph body is worse than no
body: it trains readers to skip your messages.

## Write why, not what

The diff shows what changed. The message carries what the diff cannot: the
problem, why this approach over the obvious one, and any consequence worth a
warning.

Leave out the process ("first I tried X, then Y"), and leave out enumerations
the diff already makes plain — if you added eleven validators, say why
validation was needed and what breaks without it, not what each one matches.

## Commit by path, not by index

`git commit` commits **the whole index**. Anything another process, session, or
hook has staged rides along under your message.

```sh
git commit -o path/to/file another/file -m "..."   # --only: exactly these paths
git commit -m "..." -- path/to/file                # equivalent; pathspec implies --only
```

Both forms ignore the rest of the index entirely. Prefer `-o` where a project
has settled on it — it names the intent (`--only`) instead of relying on the
reader knowing that a bare pathspec implies it. Use it whenever
anything else might be touching the repo — a parallel agent, a watcher, a
teammate's script. `git add -A` and bare `git commit` are how unrelated files
end up under someone else's subject line.

## Then verify

```sh
git show --stat HEAD
```

Confirm the file list is exactly what you meant. If it is not, **say so** —
report the mismatch rather than the commit. A commit that succeeded is not a
commit that is correct, and this check costs one command.

## Worked example — a commit that should have been four

A single commit carried: a new deterministic redaction layer, a verification
layer, a Python compatibility fix, and a test-fixture change. Its message ran 51
lines and enumerated all eleven detector classes. It should have been:

```
pii-redactor: add a deterministic pass before the model
pii-redactor: verify the output before writing it
pii-redactor: keep annotations lazy so 3.9 still runs it
tests: stop mocking the model as a pass-through
```

Each subject fits in one line without "and". Each body is two or three
sentences, because each commit is about one thing. The eleven classes need no
enumeration — they are the diff.

The same commit also swept in 52 unrelated files, because it was made with
`git add` plus a bare `git commit` while another session had files staged. Both
failures, once. The pathspec form and the post-commit check each prevent it
independently.

## Repo-specific conventions still win

This skill is portable. Where a repository documents its own commit conventions
— scope vocabulary, subject format, worked examples from its own history — read
and follow those; they are more specific. The dotfiles repo keeps its version in
`CONTRIBUTING.md` § "Commit granularity" (a queued move to `docs/COMMITS.md`).

## Notes and other tools' contributions

Git notes follow the same structure rules as commit bodies: a subject-style
first line, one claim per paragraph, bullets for parallel facts. A wall of
prose in a note is the same unreadable failure.

Notes do not travel with `git push` by default — `refs/notes/commits` needs
an explicit refspec (`git push origin main refs/notes/commits`), and forges
such as GitHub do not render notes at all; only `git log` and
`git notes show` do. Treat notes as git-local annotations, not a publication
channel. Note text gets stripspace treatment (trailing whitespace trimmed,
blank runs collapsed), `append` inserts a blank line between paragraphs, and
`git notes add` fails when a note already exists — that failure is the
guardrail the overwrite rule below leans on.

Never overwrite another tool's or session's contribution — a note, a config
file, a generated artifact — unless the owner asked explicitly. Your own
freshly-written note may be replaced; anything you did not write gets
appended to (`git notes append`) or left alone, and the question goes to the
owner. `git notes add` fails when a note exists — that failure is the
guardrail, not an obstacle to work around with `-f`.

## Never

- Never sweep unrelated modified files in to get a clean tree.
- Never stage a whole directory when only some of its files belong to the change.
- Never lengthen the message to justify an overgrown commit.
- Never overwrite another tool's or session's contribution without an
  explicit ask — see § Notes above.
- Never rebase, amend, or force-push history others may have built on to fix
  scope or wording. Propose the options and let the owner choose.
