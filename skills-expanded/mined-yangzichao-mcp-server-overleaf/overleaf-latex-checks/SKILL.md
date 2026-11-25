---
name: overleaf-latex-checks
description: Lint, format and word-count an Overleaf paper with local LaTeX tools (chktex, lacheck, latexindent, texcount) run in the Overleaf MCP server's local clone. Use when the user asks to check a paper's LaTeX for mistakes, tidy its formatting, or count words per section, and you can run shell commands where the server runs.
---

# LaTeX checks on an Overleaf paper

The Overleaf MCP server keeps each project in a local Git clone. These tools run in that
clone. Without a shell, use the server's `check_references` and `look_up_citations` tools
instead, and `read_project` (view `word_count`) for a word count.

## 1. Find the clone

Call `read_project` (view `overview`). It reports the clone's absolute path and the likely
main document. Use them below as `$CLONE` and `main.tex`.

## 2. Lint

chktex reports common LaTeX mistakes: missing non-breaking spaces before `\cite` and
`\ref`, spaces before punctuation, wrong dashes, unmatched braces. Run it on every source
file rather than relying on it to follow `\input`:

```sh
cd "$CLONE" && find . -name '*.tex' -not -path './.git/*' -print0 | xargs -0 chktex -q -v1
```

`lacheck main.tex` is a second, older checker that finds a few things chktex does not.

Group the findings by file and line, skip ones that are clearly intentional, and fix the
rest with `edit_file` (action `replace_text`), which refuses an ambiguous match instead of
editing the wrong place.

## 3. Format (ask first)

latexindent rewrites indentation across a whole file. That makes a co-author's next diff
noisy and raises the chance of a conflict on push, so ask the user before formatting a file
someone else is also editing. Keep its backup files and `indent.log` out of the clone with
`-c`, because `push_changes` publishes every file in the clone:

```sh
tmp=$(mktemp -d) && cd "$CLONE" && latexindent -s -wd -c="$tmp/" sections/intro.tex
```

If it fails with `Can't locate File/HomeDir.pm`, the Perl modules it needs are missing
(common with MacTeX); `cpan File::HomeDir YAML::Tiny` installs them, or skip formatting.

## 4. Count words

`read_project` (view `word_count`) gives the numbers Overleaf's Word Count menu shows, with
included files followed. With a session cookie it is Overleaf's own count of what has been
pushed; with only a Git token it runs texcount in the clone, so unpushed edits count and it
lists words per file. For a count per section, run texcount yourself:

```sh
cd "$CLONE" && texcount -inc -sub=section main.tex       # per section
```

Report "Words in text" as the body count; headings, captions and math are counted
separately.

## 5. Before anything is pushed

```sh
git -C "$CLONE" status --porcelain
```

Delete any file a tool left behind (logs, `.bak` files, aux files), then show the user the
pending diff with `read_project` (view `changes`) and publish only with `push_changes`.
Read-only Git commands are fine in the clone; never commit, pull, push or reset there
yourself.
