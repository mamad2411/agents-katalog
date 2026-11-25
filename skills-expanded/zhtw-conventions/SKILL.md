---
name: zhtw-conventions
description: The zhtw-mcp conventions no gate enforces - the register a comment, a commit message and a PR reply are written in, where Chinese belongs in the tree and where it does not, the untracked working docs at the repo root, deleting a redundant surface instead of deprecating it, and the repository layout. Use when drafting a commit message or a PR description, adding a file or a public surface, removing a flag or a subcommand, or writing a comment longer than a line.
---

# zhtw-mcp conventions

The gate settles formatting and correctness. `cargo fmt`, clippy, `black`,
`shellcheck` and `scripts/indent.sh` run in `make check`, so none of that is
here. What is here is what a reviewer would otherwise have to say out loud,
plus the rules enforced by the git hooks rather than by CI: the commit message
and the staged-content checks. Any `cargo build` installs them, through
`build.rs`; `make hooks` installs them on their own.

`README.md` and `CLAUDE.md` are the tracked and local halves respectively, and
this file does not restate either. Where two of them speak to the same thing,
`README.md` wins.

## Commit messages

The house style is Chris Beams' seven rules, and `scripts/git-commit-msg.sh`
enforces the mechanical ones: subject within 50 columns, capitalized,
imperative, no trailing period, no backticks, no conventional-commit type
prefix, body wrapped at 72 columns, no em dash character, no tabs, and no
control or bidirectional-override characters. An area prefix such as
`Windows: retry the replace` is not a conventional-commit prefix and is
allowed. Run
`git log --no-merges --format=%s` if you want the calibration set rather than
the claim; the log sits at 43 columns in the median.

Two of those rules are this project's rather than Beams'. Widths are counted in
terminal columns, so a CJK character costs two, which is what
`git log --oneline` has to fit. And the subject line is English prose that may
quote a Chinese term, which is what every subject in this log already is:

```
Narrow 聯繫 cross_strait flagging to contact-copy
Add word "test" to negative_context_clues for pass rule
Take the binary under test from cargo
```

The rule the hook cannot check is what the body says. This tree keeps its
detailed reasoning in the comment next to the code, often several paragraphs
per decision. A body that retells the mechanics duplicates that comment and
then goes stale on its own. Write the premise and the trade, once, usually a
single paragraph. Backticks are fine there and not in the subject.

## Prose register

Source comments use plain prose: no em dash, and no backticks around an
identifier. Name it plainly, and use quotes only where a bare token would read
as part of the sentence. `scripts/check-comments.sh` enforces both, in
`make check` and in the pre-commit hook, so this is a rule you hear about at
commit time rather than in review.

Two exemptions, both because the text is markup rather than prose. Markdown
files under `docs/` and the README use ordinary GitHub Markdown. Rust doc
comments, `///` and `//!`, are rustdoc markdown: a backticked span renders as
code and an intra-doc link resolves inside one, so backticks stay there. The
em dash rule has no exemption; it is about prose in any markup.

The doubled em dash is the zh-TW 破折號 and is data in this tree, not
punctuation. The checker leaves it alone, along with one inside quotes.

Chinese in a comment is not only allowed, it is often the only honest way to
say what a rule is about: `// 聯繫 is contact-copy in zh-TW and a verb in
zh-CN`. Use it where the term is the subject. Do not use it for prose that has
an English form, and keep user-facing strings, identifiers and file names
English.

## Comments

Brevity is part of correctness, but the bar is rationale rather than length:
this tree carries long comments where the reasoning is long, and the rule is
that every line says something the code cannot. Delete anything restating the
statement below it.

- Bad: `let end = start + len; // add the length`
- Good: `let end = start + len; // byte offsets, mapped back through NFC above,
  so this indexes the original text and not the normalized copy`

Comment width is settled by `commentflow` through `scripts/indent.sh`, so do
not hand-wrap to a column and do not fight the result; run `make indent`.

Never point a comment, a doc comment or a `docs/` page at `TODO.md`. It is
untracked and per-developer, so the reference dangles for everyone else.

## Working docs at the repo root

`TODO.md`, `DONE.md` and `CLAUDE.md` are excluded through `.git/info/exclude`,
not through `.gitignore`, because the exclusion is one person's habit and
`.gitignore` would push it onto everybody. Never `git add`, stage, commit or
delete them, and never assume a clone has them. Reports and analyses stay out
of the tree the same way: a scratch directory, not a new tracked file. A
finished TODO item moves to `DONE.md` rather than being deleted.

## Deleting a surface

A flag, subcommand or helper that turns out to be redundant gets deleted, along
with its call sites in the Makefile, the scripts, the README, `docs/` and the
tests. It does not become an alias and it does not get a deprecation warning.
"Never break userspace" here means the observable contract: the MCP tool schema
in `docs/mcp.md`, the CLI exit codes, the SARIF and JSON output shapes, and the
golden fixtures under `tests/`. The convenience surface is not that contract.

## Pull requests and review replies

The commit body carries what and why. A review thread carries a correction, a
measurement, or nothing: no pasted agent walkthroughs, no severity tables, no
re-summarizing a diff git already shows.

## Layout

```text
src/engine/     Scanner passes, normalization, s2t conversion, scoring
src/rules/      Rule store, ruleset schema, overrides, judgment cache
src/cli/        Argument parsing, file discovery, output rendering
src/mcp/        MCP server, stdio transport, tool types, sampling
assets/         ruleset.json, the source of truth for vocabulary rules
scripts/        Table generator, ruleset checker, gate and hook scripts
extension/      Browser extension over the browser-wasm build of the library
tests/          Integration suites, corpora and fixtures
tests/unit/     Unit test bodies, mirroring the module path they belong to
docs/           Internals, rule schema, CLI and MCP references
```

`src/engine/s2t_data.rs` is generated and gitignored. See zhtw-verify for what
regenerates it, and zhtw-rules for how a vocabulary rule is added.

## Test code does not live in src

No test bodies under `src/`. A module that has unit tests declares them and
points at the file:

```rust
#[cfg(test)]
#[path = "../../tests/unit/engine/excluded/tests.rs"]
mod tests;
```

The file lives at `tests/unit/` plus the module path plus the module name, so
`src/engine/excluded.rs` puts its `tests` module in
`tests/unit/engine/excluded/tests.rs` and `src/engine/scan/mod.rs` puts its in
`tests/unit/engine/scan/tests.rs`. The relative path in the attribute is counted
from the directory holding the source file, not from the repository root.

They stay unit tests, which is the point: they keep private access, they compile
into the same test binary, and no internal item has to become `pub` to be
reachable. Making an internal `pub` so a test in `tests/*.rs` can see it is the
thing this arrangement exists to avoid.

What legitimately remains in `src/` is not test bodies: a `#[cfg(test)]` helper
on a production type, such as `Trie::get_freq` in `src/engine/segment.rs` or
`Scanner::force_bytewise` in `src/engine/scan/mod.rs`, is an affordance the type
offers its tests and belongs with the type. A test-only free function is test
code and goes to `tests/unit/`, which is where the nine legacy grammar scanners
sit as `tests/unit/engine/scan/grammar/legacy.rs`.
