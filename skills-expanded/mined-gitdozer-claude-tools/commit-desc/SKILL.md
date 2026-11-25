---
name: commit-desc
description: Propose a Conventional Commits message for the changes currently staged in git. Use right before committing, when the user asks for a commit message, a commit description, or what to write for this commit.
model: haiku
effort: low
context: fork
background: false
argument-hint: "[optional extra context, e.g. issue number or intent]"
allowed-tools: Bash(git *), Bash(head *), Bash(wc *)
---

# Propose a commit message

The staged changes are collected below. Do not run any command and do not read
any file: everything you need is already in this prompt. Answer in one turn.

BRANCH: !`git rev-parse --abbrev-ref HEAD`

RECENT COMMIT SUBJECTS (match this repository's existing style):
!`git log -5 --pretty=%s`

STAGED FILES (added/deleted line counts; `-` means git treats the file as binary):
!`git diff --cached --numstat -M`

DIFF SIZE in characters, measured before the 20000-character cap is applied:
!`git diff --cached -M -U2 --no-color --no-ext-diff --diff-algorithm=minimal -- . ':(exclude)*.lock' ':(exclude)*-lock.json' ':(exclude)*.lockb' ':(exclude)pnpm-lock.yaml' ':(exclude)*.min.js' ':(exclude)*.min.css' ':(exclude)*.map' ':(exclude)*.snap' ':(exclude)*.ipynb' ':(exclude)*.csv' ':(exclude)*.tsv' ':(exclude)*.parquet' ':(exclude)*.xlsx' ':(exclude)*.geojson' ':(exclude)*.pdf' ':(exclude)*.svg' ':(exclude)*.png' ':(exclude)*.jpg' ':(exclude)*.jpeg' ':(exclude)*.gif' ':(exclude)*.ico' ':(exclude)*.pkl' ':(exclude)*.h5' ':(exclude)*.onnx' ':(exclude)*.zip' ':(exclude)dist/*' ':(exclude)*/dist/*' ':(exclude)build/*' ':(exclude)*/build/*' ':(exclude)node_modules/*' | wc -c`

DIFF (2 lines of context; lock files, build output, notebooks, data files and images are listed above but not diffed here):
!`git diff --cached -M -U2 --no-color --no-ext-diff --diff-algorithm=minimal -- . ':(exclude)*.lock' ':(exclude)*-lock.json' ':(exclude)*.lockb' ':(exclude)pnpm-lock.yaml' ':(exclude)*.min.js' ':(exclude)*.min.css' ':(exclude)*.map' ':(exclude)*.snap' ':(exclude)*.ipynb' ':(exclude)*.csv' ':(exclude)*.tsv' ':(exclude)*.parquet' ':(exclude)*.xlsx' ':(exclude)*.geojson' ':(exclude)*.pdf' ':(exclude)*.svg' ':(exclude)*.png' ':(exclude)*.jpg' ':(exclude)*.jpeg' ':(exclude)*.gif' ':(exclude)*.ico' ':(exclude)*.pkl' ':(exclude)*.h5' ':(exclude)*.onnx' ':(exclude)*.zip' ':(exclude)dist/*' ':(exclude)*/dist/*' ':(exclude)build/*' ':(exclude)*/build/*' ':(exclude)node_modules/*' | head -c 20000`

Extra context from the user (may be empty): $ARGUMENTS

## What to produce

One Conventional Commits subject line, in English, describing the staged changes.

Format: `type(scope): subject`

- **type** — exactly one of: `feat` (new user-facing capability), `fix` (bug
  fix), `refactor` (behaviour-preserving restructuring), `perf`, `docs`, `test`,
  `build` (dependencies, packaging), `ci`, `style` (formatting only), `chore`
  (everything else: config, housekeeping), `revert`.
- **scope** — optional, lowercase: the module, package, or top-level directory
  most affected (`auth`, `api`, `etl`). Omit it when the change spans several
  unrelated areas.
- **subject** — imperative mood ("add", never "added" or "adds"), lowercase
  first letter, no trailing period, 72 characters maximum including the prefix.
- Add `!` before the colon (`feat(api)!:`) only when the diff clearly breaks an
  existing interface.

Rules:

- Describe **what the change accomplishes**, not which files were touched.
  Prefer `fix(etl): handle empty csv rows without crashing` over
  `fix: update loader.py`.
- Stay grounded in the diff. Never invent a motivation, ticket, or effect that
  the diff does not show.
- When the diff mixes several things, name the dominant one and use its type
  (`feat` outranks `refactor`, `fix` outranks `chore`).
- Match the style of the recent commit subjects above when they already follow a
  consistent convention.
- The DIFF section is capped: if it looks truncated, or a file appears only in
  STAGED FILES, judge that file from its name and line counts alone.
- If STAGED FILES is empty, reply with a single line saying nothing is staged and
  that `git add` is needed first. Nothing else.

## Output format

Reply with **only** the blocks below: no preamble, no explanation, no
alternatives, no follow-up question.

**Truncation warning — do this first.** Compare DIFF SIZE with 20000. If DIFF
SIZE is greater than 20000, the diff you received is incomplete, and the very
first line of your reply must be exactly this, with the real number in place of
N and no other comment:

    WARNING: diff truncated, 20,000 characters sent out of N. The message is based on part of the changes.

If DIFF SIZE is 20000 or less, do not mention truncation at all.

Then, in both cases:

The message:

    <the commit message>

Ready to run:

    git commit -m "<the commit message>"
