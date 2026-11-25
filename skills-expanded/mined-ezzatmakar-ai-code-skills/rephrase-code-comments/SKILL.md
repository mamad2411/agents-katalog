---
name: rephrase-code-comments
description: Rewords existing code comments and docblocks in place so they read concise, direct, plain English, and human instead of wordy, vague, or machine-written. Measures wording against the Google developer documentation style guide, Microsoft Writing Style Guide, US Federal Plain Language Guidelines, ASD-STE100, and each language's doc-comment grammar (PEP 257, Javadoc, Go doc comments, Rust RFC 1574). Fixes wordy phrases, filler, hedges, AI-sounding vocabulary, "This function is used to" openers, passive voice, long sentences, wrong summary mood, time words, non-inclusive terms, and misspellings, keeping every fact, identifier, and number. Use when asked to rephrase, reword, humanize, simplify, or proofread code comments, e.g. "these comments sound like AI" or "rewrite the docstrings in plain English". Edits comment wording only, never code, and previews first. Not for deleting, sorting, or moving comments (use comment-cleanup), writing new docs, or translating.
license: MIT
compatibility: Requires git and python3 (3.8+, standard library only). Stack-agnostic — reads C-style, hash, SQL, HTML, CSS, Lua, and Python comment syntax, and defers to the repository's own prose linters (Vale, alex, write-good, cspell, pydocstyle, eslint-plugin-jsdoc) when one is configured. Designed for Claude Code, Codex, and OpenCode using the Agent Skills open standard.
metadata:
  author: Ezzat Malak
  version: "1.0.0"
---

# Rephrase Code Comments

Reword a codebase's **comments** so each one is **concise**, **direct**, **plain**, and **human**, and so it
follows the standards cited in [references/WRITING_STANDARD.md](references/WRITING_STANDARD.md). This skill
**edits by default**. It does not write a report. Because it edits in place, every run passes through a preview
gate first. It changes wording only. It never changes a line of executable code.

It is the wording counterpart of `comment-cleanup`. That skill decides **whether** a comment should exist, how
long it is, and where it sits. This skill takes the comments that stay and makes **their sentences** better. When a
comment should be deleted rather than reworded, say so and leave it for `comment-cleanup`.

References, loaded as needed:

- [references/WRITING_STANDARD.md](references/WRITING_STANDARD.md): the four house rules and their sources.
- [references/REWRITE_RULES.md](references/REWRITE_RULES.md): every rule ID, how to rewrite it, and when to keep
  the original.
- [references/LANGUAGE_MOOD.md](references/LANGUAGE_MOOD.md): each language's doc-comment grammar (imperative or
  third person, sentence or fragment, name-first).
- [references/WORD_LIST.md](references/WORD_LIST.md): wordy phrases, filler, AI vocabulary, time words, and
  inclusive terms, each with its source.

Two helpers do the mechanical work. Resolve `<skill-directory>` from the loaded skill path:

- `<skill-directory>/scripts/scan-prose.py` finds every English prose comment and flags wording by rule ID.
- `<skill-directory>/scripts/detect-stack.sh` summarizes the languages, tooling, and prose linters in play.

## Non-negotiable output

- **Comments only. Never executable code.** No renames, no reformatting, no "while I was in there" fixes. If a
  comment is only unclear because the code is unclear, report it (`ESCALATE`) and move on. At the end, `git diff`
  must not change any non-comment line.
- **Keep the meaning, all of it.** Every fact, condition, number, unit, limit, error name, issue link, URL, and
  warning in the old comment must be in the new one. Do not add a claim the old comment did not make. If you cannot
  tell what a comment means, leave it and escalate it. A reworded comment that loses a constraint is a bug.
- **Never touch code inside a comment.** Identifiers, `code spans`, file paths, CLI flags, `@param` names, tag
  names, `{@link}` targets, doctest lines (`>>>`), and fenced examples stay byte-identical. The scanner masks them.
  Your rewrite must too.
- **Reword. Do not restructure.** Do not delete a comment, move it, merge two, add a new docblock, or reorder tags.
  That is `comment-cleanup`'s job. Cutting filler words inside a sentence is rewording and is allowed.
- **A wrong comment is escalated, not polished.** If the comment contradicts the code, rewording it would make a
  false statement easier to believe. Report it as `STALE` with the evidence and leave the text alone.
- **Refuse to start on a dirty working tree.** Run `git status --porcelain`. If it is not empty, stop and say so.
  The user must be able to `git diff` the whole result and `git checkout .` to undo it. Continue only if they
  explicitly accept mixing this pass into their existing changes.
- **Preview before editing.** No file changes until the user approves the plan (Phase 4), even for one file.
- **Never translate.** Rephrase English comments only. The scanner counts non-English comments and skips them.
  Keep the file's spelling variant too: do not turn `colour` into `color` or `initialise` into `initialize`.
- **Protected text is never reworded.** Pragmas and tool directives (`eslint-disable`, `@ts-expect-error`,
  `# noqa`, `//go:build`, `# type: ignore`, …), licence and copyright headers, generated files, and vendored code.
- **Never reproduce a suspected secret.** Report the file, the line, and the kind of credential, redacted. Say that
  rewording does not fix it: the value must be rotated.
- **The repository's configuration wins.** If a prose linter or doc-comment rule is configured, follow it over
  the house rule and name it in the summary.
- **Report faithfully.** State what changed, what you kept and why, and what you escalated. Never describe an edit
  you did not make.

## Phase 0: Resolve inputs

Settle these first and echo them back:

1. **Scope.** Default: the whole repository. Honor explicit paths, directories, or globs. For "my changes" or "this
   PR", use `--since <base>` (for example `--since origin/main`). The scanner always excludes generated, vendored,
   minified, and lockfile paths.
2. **Depth.** Default **standard**.
   - **light**: mechanical fixes only (`WORDY`, `FILLER`, `SPELL`, `TERM`, `SHOUT`, `NEG`, `AI`).
   - **standard**: everything the scanner flags.
   - **deep**: standard, plus a read-through of every comment in scope, flagged or not, for clarity.
3. **Sentence limit.** Default 25 words (`--max-words N`), the ASD-STE100 limit for descriptive text.
4. **Python docstring mood.** Default: match the file (`--python-mood consistent`). Use `imperative` when the repo
   enforces pydocstyle `D401` or asks for PEP 257. See [references/LANGUAGE_MOOD.md](references/LANGUAGE_MOOD.md).
5. **Apply or preview only.** Default: apply, after the Phase 4 gate. With `preview only`, stop after the plan.
6. **Clean tree.** Run `git status --porcelain` and apply the rule above.

## Phase 1: Detect the stack, the local rules, and the house voice

1. Run `<skill-directory>/scripts/detect-stack.sh`.
2. Read repository guidance if present: `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, a style guide in `docs/`.
3. **Find any prose or doc-comment rule the project already enforces, and follow it:**
   - Prose linters: `.vale.ini` and its styles, `.alexrc`, `.textlintrc`, `write-good`, `cspell.json` /
     `.cspell.json` (and its custom word list).
   - Python: `ruff` `D` rules or `pydocstyle` convention (`pep257` enforces imperative mood through `D401`;
     `google` does not).
   - JS/TS: `eslint-plugin-jsdoc` rules such as `jsdoc/require-description-complete-sentence`.
   - Go: `golangci-lint` `godot` (period at the end) and `revive` `exported` (name-first).
   - C#: StyleCop `SA1623` (property summaries start with "Gets" or "Gets or sets").
4. **Record the house voice** so rewrites do not sound foreign next to their neighbors:
   - summary mood per language (imperative or third person);
   - contractions (`don't`) or none (`do not`);
   - whether comments say "we";
   - US or UK spelling;
   - line width of wrapped comments.

## Phase 2: Inventory

```bash
python3 <skill-directory>/scripts/scan-prose.py [paths...] [--since REF] [--max-words N] [--json]
```

The scan reports. It never blocks, and it always exits 0. Each line is a **candidate, not a verdict**. Useful
flags: `--rules WORDY,FILLER` to focus a pass, `--summary-only` for a baseline, `--json` for structured input,
`--max-per-file N` to limit output.

| ID | Means | Default |
|---|---|---|
| `WORDY` | wordy phrase with a plain replacement (`in order to`, `utilize`) | `REWRITE` |
| `FILLER` | minimizer or throat-clearing (`simply`, `just`, `note that`) | `REWRITE` |
| `AI` | machine-sounding vocabulary or pattern (`delve`, `robust`, emoji, em-dash chains) | `REWRITE` |
| `OPENER` | describes the comment, not the code (`This function is used to…`) | `REWRITE` |
| `NARRATE` | first person or tutorial voice (`Here we…`, `Let's…`) | `REWRITE` |
| `LONG` | sentence over the word limit | `REVIEW` up to +10 words, `REWRITE` beyond |
| `MOOD` | summary mood breaks the language or file convention | `REWRITE` |
| `FORMAT` | doc summary lowercase, or missing its period where the language requires one | `REWRITE` |
| `TERM` | non-inclusive or ableist term | `REWRITE`, or `ESCALATE` if code shares the name |
| `SPELL` | common misspelling | `REWRITE` |
| `SHOUT` | all-caps words or `!!!` | `REWRITE` |
| `NEG` | double negative (`not uncommon`) | `REWRITE` |
| `HEDGE` | hedge that hides what is known (`probably`, `I think`) | `REVIEW` |
| `PASSIVE` | passive voice with a named actor (`is called by the router`) | `REVIEW` |
| `VAGUE` | names nothing (`stuff`, `handle it`, `for some reason`) | `REVIEW` |
| `TIME` | time-relative word that goes stale (`currently`, `the new API`) | `REVIEW` |
| `READ` | Flesch-Kincaid grade over the limit, for comments of 30+ words | `REVIEW` |
| `SECRET` | possible credential in a comment | `ESCALATE`, redacted |

The scanner cannot find these. You find them by reading:

- `STALE`: the comment contradicts the code.
- `UNCLEAR`: you cannot tell what the comment means.
- `DELETE-CANDIDATE`: the comment restates the code or is dead. Hand it to `comment-cleanup`.

A large scan result does not replace reading the files you edit.

## Phase 3: Draft the rewrites

Open each flagged file and decide per comment: `REWRITE`, `KEEP`, or `ESCALATE`. Use
[references/REWRITE_RULES.md](references/REWRITE_RULES.md) for each rule. For every `REWRITE`, follow this recipe:

1. **Find the load-bearing fact.** What does a reader need that the code does not already say? Usually a *why*, a
   constraint, a unit, a side effect, or a warning.
2. **Lead with it.** Doc summaries start with the verb, in the language's mood (`Returns…` or `Return…`). Inline
   comments start with the reason (`Upstream 502s under load, so…`).
3. **Cut what carries nothing:** filler, hedges, openers, narration, intensifiers.
4. **Use the plain word:** `use`, not `utilize`; `before`, not `prior to`; `if`, not `in the event that`.
5. **One idea per sentence**, within the word limit. Split with a period, not an em dash.
6. **Name the actor when it matters:** `The router calls this`, not `This is called by the router`.
7. **Keep everything else exactly:** identifiers, code spans, numbers, units, links, tags, markers
   (`TODO(#123):`), line wrapping style, and comment syntax.
8. **Read it aloud.** It should sound like a careful colleague explaining the code: specific nouns, no sales
   language, no chat phrases, no stacked hedges.

Bias hard toward `KEEP` for:

- licence text, legal notices, and quoted error messages;
- comments that quote a spec, an RFC, or an API's own wording;
- framework-scaffolded config comments the team never wrote;
- test names and scenario descriptions whose wording other tools match;
- any comment where you are not sure a rewrite keeps the meaning.

Record the reason for each `KEEP` so the next run does not argue it again.

## Phase 4: Preview gate

**No file changes until this passes.** Present:

1. The files to be touched, and the count per rule ID.
2. How many comments will be reworded, kept, and escalated.
3. Three to five **before/after** pairs, including the most aggressive rewrite you plan.
4. Everything escalated: `STALE`, `UNCLEAR`, `SECRET`, and `TERM` where code shares the name.
5. Anything skipped and why: non-English, generated, vendored, protected, or controlled by a linter.

If the scope is more than about 20 files, write this to `REPHRASE_PLAN.md` at the repository root and give the
path instead of flooding the chat. Then get explicit confirmation. The user may narrow the scope, drop a rule, or
change the depth. Re-plan instead of applying part of the old plan.

## Phase 5: Apply

Work in **batches of related files**, so a bad batch can be reverted without losing the good ones. In each batch:

1. Edit comment text only. Keep the comment markers, indentation, alignment, and the file's wrap width. Never
   exceed the configured line length.
2. Keep docblock structure: the same tags, in the same order, with the same names and types. Only the prose after
   a tag changes.
3. If a sentence cannot be improved without changing its meaning, leave it and record `KEEP`.

Then verify the batch (Phase 6) before you start the next one.

## Phase 6: Verify

After each batch, and again at the end:

```bash
git diff --stat
git diff -U0 | grep -E '^[+-]' | grep -vE '^(\+\+\+|---)'
python3 <skill-directory>/scripts/scan-prose.py [paths...] --summary-only
```

1. **Read every changed line.** Each must be either wholly comment text, or a line whose **code part is
   byte-identical** to the original and differs only in a trailing comment. Revert anything else at once.
2. **Check meaning, pair by pair.** For each before/after, list the facts in the old text and find each one in the
   new text. A missing fact is a failed rewrite. Restore the original.
3. **Re-scan.** Counts should fall, and no new rule should fire on lines you wrote.
4. **Run what the project already has and is cheap:** the prose linter, the doc-comment linter, the type checker,
   and a docs build (`typedoc`, `sphinx`, `cargo doc`, `godoc`) if one exists. A docblock edit can break a build,
   for example malformed C# XML docs or a rustdoc fence. Never claim a check passed if you did not run it.

## Phase 7: Summarize

Report briefly in chat:

- The files changed and the counts by rule and disposition.
- What was **escalated** and needs a person: comments that contradict the code, unclear comments, suspected
  secrets (redacted), and terms that are also code names.
- What was deliberately kept, and which repository rules you followed instead of the house rules.
- The verification commands you ran and their results.
- Comments that look like deletion candidates, as a pointer to `comment-cleanup`.

Remind the user the whole pass is one reviewable diff: `git diff` to inspect it, `git checkout .` to undo it.
