---
name: bake-claude-md-files
description: >
  Converts CLAUDE.md rules into automated checks, removes the automated rules from CLAUDE.md, and verifies everything passes. Frees up agent context by replacing prose with tooling.
user-invocable: true
disable-model-invocation: true
---

Read all CLAUDE.md files in the project, along with the existing tool configurations (eslint, phpstan, pint, package.json scripts, lefthook, git hooks, GitLab CI or GitHub Actions and everything else relevant).

When the project has more than one CLAUDE.md file, fan out instead of loading them all: build the tool inventory once and hand it with one file to each clean-context agent, the root file included, then merge the verdicts in the main session. A single window holding every file blurs rules across scopes and crowds the tool configurations out of attention.

Identify rules in the CLAUDE.md files that can be turned into automated checks. Every rule we can remove is context freed up for the agent.

Before modifying any CLAUDE.md file, present a summary of:

- Which rules will be automated (and by which tool)
- Which rules will be kept (and why - e.g. requires human judgment, context-dependent)

Ask first (one AskUserQuestion) whether the user wants that summary as an interactive artifact or as plain text. The artifact is a live doc (`capabilities: {artifact: {}}`): one row per rule with its repo-relative source file, the proposed enforcement tool, an approve checkbox, a free-text input for objections, and a copy-decisions control as the fallback path back into the session.

Only proceed after the user approves. Then implement the automated checks, verify everything passes, and only remove a rule from CLAUDE.md after its corresponding check passes. Passing on the current tree is not enough: confirm the check's file globs cover the affected paths and that it runs before code lands (hook or CI).

## Building the decision artifact

The artifact is a decision surface, not a document. The user often decides from a phone, so every item renders as a compact card: path, a one-sentence claim, one evidence line. Compact governs your own prose and never the source: text the user is approving (the line being cut, the rule being written) appears verbatim and whole, however long it runs.

- **Show the line, don't cite it.** Any claim about text the reader cannot see gets a collapsed "See the lines" block quoting the offending line verbatim in diff-removed styling, with the replacement (where one exists) in diff-added styling. The reader must never need the repo open to decide. Abridge very long lines with `[...]` and point at the full diff. Quote blocks hold file lines only: never explanation prose inside the block (that belongs in the card's claim or evidence line), and each quoted line carries its real line number in a muted, unselectable gutter.
- **A note field on every row.** Every decision row carries a free-text note field, always visible and in the tab order, never behind a disclosure the user must click first: opening a control per row breaks the review flow. Keep it one row tall and let it grow with content (`field-sizing: content`, plus `resize: vertical` as the fallback). Give every interactive control a visible `:focus-visible` outline so the whole page is walkable by keyboard. The user may have an opinion or question anywhere, including near-certain items.
- **Keyboard flow.** <kbd>j</kbd>/<kbd>k</kbd> walk the decision rows, <kbd>x</kbd> toggles the row, <kbd>n</kbd> focuses its note, <kbd>e</kbd> toggles its quoted lines, <kbd>Esc</kbd> leaves the note (document the keys on the page, hidden on touch widths). On wide viewports open the quote blocks by default, so deciding needs no clicks at all.
- **Open-in-editor links.** Every file reference gets a small open link built on the user's editor URL scheme, detected from the machine (`$EDITOR`, installed apps): `zed://file{abs}:{line}`, `vscode://file{abs}:{line}`, `cursor://file{abs}:{line}`, `phpstorm://open?file={abs}&line={n}`. Always absolute paths, so the links hold from any worktree, and percent-encode them (keeping `/` in the path, encoding the whole PhpStorm query value) so a `#`, `?`, `%`, or `&` inside a path cannot truncate the target. Evidence references carrying file:line link the same way. Use `target="_blank"`, and stop click propagation on these links in a capture-phase handler, since they sit inside the checkbox label and a click must never toggle the row. The link opens on the machine running the browser, so emit these only when the session runs on the user's own machine: a remote session (SSH, devcontainer, cloud sandbox) reads a different filesystem and a different set of installed editors, so omit the links there rather than pointing an absent editor at a path that does not exist.
- **Word-level diffs.** Pair adjacent removed/added runs (SequenceMatcher on tokens, similarity at or above 0.4) and highlight only the changed tokens. Render each diff line as a `display:block` span and join the spans with no separator: a newline between block spans inside a `<pre>` renders as a phantom blank line. Lint-enforced docs keep whole paragraphs on one physical line, so wrap with `white-space:pre-wrap`, `overflow-wrap:anywhere`, and a hanging indent.
- **Questions as options.** Render each open question as radio options with a "recommended" chip plus a free-text field, mirroring AskUserQuestion. A bare textarea is only for questions with no concrete options.
- **Sticky decision bar.** Section links, a changed-from-default counter, and the copy-decisions control stay reachable while scrolling.
- **A fallback that carries everything.** The copy-decisions control serializes every control on the page: each checkbox, the selected option of each question, and each free-text field. The pasted export is an accepted approval path, so any state it drops is a decision the session then applies wrongly.
- **Triage chips.** Label each diff row by the review effort it needs (cuts-only rows are skimmable, rewrites are worth opening, adds carry new lines) and provide an expand-all-diffs control.
- **Mobile pass.** Verify the page at around 390px width before publishing. Collapse method and other secondary sections by default.
- **Republish safety.** Viewer decisions reach the session only because the page is a live doc (`capabilities: {artifact: {}}`), which saves the DOM a viewer's gesture changed back into the served document. Before any republish, fetch the live artifact and compare its state against defaults. Carry any non-default state into the rebuilt HTML, or do not republish: republishing over live decisions destroys them. Publish without that capability and the state never leaves the viewer's browser, where the session cannot read it: then the clipboard export is the only path back, and republishing is off the table once the user starts deciding.
- **Generate, don't hand-edit.** Build the page from a data-plus-template script in the scratchpad so every iteration regenerates it whole.
- **End with the trigger.** Close the page by telling the user the exact phrase that resumes the session, such as "read the artifact and apply".

## Implementation priority

1. **Discover existing tooling first** - inventory linters, test frameworks, static analyzers, CI pipelines, and git hooks before implementing anything
2. **Use native capabilities** - express checks through tools already in the project:
   - Linter/formatter rules (ESLint, Biome, Prettier, Pint, Ruff, gofmt)
   - Static analysis, including authoring custom rules (TypeScript strict, PHPStan strictness levels and custom PHPStan rules, mypy, Rector)
   - Architecture tests (Pest arch, ArchUnit, dependency-cruiser)
   - Structural search and lint (ast-grep) for syntax-shaped rules a stock linter cannot express (a banned call pattern, a required argument shape)
   - Git hooks (Lefthook, Husky, pre-commit)
   - CI pipeline steps
   - Agent-harness hooks (Claude Code PreToolUse deny rules) for rules about how a command is invoked (a required flag, a banned subcommand), which no linter or code check can see
3. **Custom scripts only as last resort** - only when no existing tool can express the check
4. **Wire into existing runners** - new checks must run via existing test/lint commands, not new entrypoints

## Keep prose when the feedback loop is late

A format-time auto-fix corrects violations silently, so its prose can always go. A check that fails only at suite time (architecture test, CI step) corrects the agent after the code is written. When the surrounding code mostly violates the rule, neighbors teach the wrong pattern and the agent writes the violation first, every time. Keep a one-line prose rule next to that check, noting what enforces it.

## The quartet

- `feed-claude-md-files` adds rules from observed patterns
- `bake-claude-md-files` converts crystallized rules into tooling and removes the prose
- `audit-claude-md-files` prunes and verifies what remains
- `split-claude-md-files` moves what remains to the scope that reads it

Run `feed` after a working session, `bake` once enough rules have accumulated to be worth automating, `audit` when CLAUDE.md files have grown without review, and `split` after an audit leaves a resident file carrying rules that govern one area.
