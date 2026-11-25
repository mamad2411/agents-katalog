---
name: btclib-table
description: "btclib-table — one table of every btclib-org repository, measured now: open issues, open pull requests, CI and README badge status, last release, whether a new one is due"
---

# The btclib-org table

Show the human one table of every repository of `btclib-org` that is not
archived, read from the API now: never from memory, and never from an
earlier run.

The skill only reads. It writes nothing, comments nowhere and takes no
decision, so it needs no worktree and none of the roles of
`$PROCESS/process/btclib-common.md` (`echo "$PROCESS"` prints the
clone's path). What it writes after the table follows that file's
*Write plainly*.

## Measure

Run this, which only reads:

```shell
sh "${PROCESS:?}/skills/btclib-table/measure.sh"
```

The last line gives the totals the table's headings carry. The badge
project is the first `bestpractices.dev/projects/` link of the README;
its `repo_url` names the repository, or its package where the two
differ.

`ci` names each active workflow whose latest completed run on `main`
concluded neither `success` nor `skipped`, `ok` where none did.
`release.yml` is left out: on `main` it runs only as a rehearsal, and a
release runs on its tag. Only a workflow's 20 latest completed runs on
`main` are read, so a run still in progress is not among them. A
`cancelled` run and a run from a fork's `main` are passed over for the
one before. A disabled workflow, and one with no run that counts among
those 20, count for nothing. One call reads the repository's 100 latest
completed runs on `main`; a workflow they do not settle gets a call of
its own, and where that call fails, every workflow does.

`badges` names each image of the README that does not render green or
blue, `ok` where none. Every `![…](…)` image counts as a badge. Its
colours are the SVG's `fill` and `stop-color` values with an HSV
saturation of 0.5 or more; the greys, white and black of the frame fall
below that. An image renders green or blue where it has such a colour
and each such colour has a hue from 70° (green) to 260° (blue). An image
that does not download (a download that stalls for 10 s fails), or is
grey only, does not.

A `pypi/status` badge is not read: its colour is the development status,
yellow at beta and red at alpha. A bestpractices badge titled `openssf
best practices: silver` or `…: gold` counts as green: its colour is the
metal, grey `#c0c0c0` for silver.

The other calls behind `iss`, `pr` and `ci`, and the README fetch, go
through `call`: one that fails, or prints anything on stderr, puts
`error:` and its message in that value, or in `badges` for the README,
where a 404 means no README. A badge script that fails puts `error: the
badge script failed` in `badges`. A bestpractices fetch that fails, or
whose answer is not JSON holding the fields read, puts `error:` and its
message in `bl3` and `gold`, and the row keeps its name, `pypi` and
`deps`. A row whose `iss` or `pr` holds an error is left out of the
totals, and the last line says so.

The measure reads six repositories at once. Within one, it reads the
counts, the CI, `release.yml` and the tags beside the README,
`pyproject.toml` and the badges. It reads the workflows that get a call
of their own eight at a time, as it does the images. The rows print in
repository order.

A PyPI project of the same name with no tag of ours is someone else's:
say so in one line.

## Order

Top to bottom, in sections ordered by what each repository depends on,
with no section heading (the human knows them):

1. `.github`: the other repositories' workflows call its reusable
   workflows pinned to its tags, so a `.github` tag is a release they
   wait on;
1. ai-agents-process: it follows `.github`'s standard, and no other
   repository's workflow calls it;
1. packages whose runtime `dependencies` are empty: the standard library
   only;
1. packages that depend on third-party packages only, none of the
   organization's;
1. packages that depend on other packages of the organization, each
   below every one it depends on;
1. bbt, benchmarks and functional-tests: they depend on
   the organization's packages, and have no tag and no `release.yml`;
1. portanode: it uses no package of the organization;
1. btclib-org.github.io: it has a folder for each other repository.

Within a section, alphabetical, unless the dependency order says
otherwise.

A repository with a `release.yml` workflow sits in its package section
even before its first release, with `never`. One the list does not name,
with neither a tag nor `release.yml`, goes beside bbt where it depends
on the organization's packages. Any other goes in its own section, one
per repository, just above btclib-org.github.io.

## The new 🚀? column

Whether a release is due, judged from the commit subjects since the last
tag:

- `⏳`: a release pull request or tag is under way;
- `YES`: a user of the package would notice a change, and one pull
  request makes the release urgent;
- `yes`: the same, with no urgency (lowercase means not urgent);
- `no`: only tests, CI, docs, process files or the next cycle landed;
- `-`: the repository has no tag and no `release.yml`.

## Show it

A box-drawn table inside a code block, at most 80 columns wide, so that it
reads in the terminal:

```text
┌───────────────┬─────┬────┬─────┬─────┬────┬────┬────────────┬─────┐
│ Repository    │ 233 │ 51 │ BL3 │ 🥇% │ CI │ 📛 │ last       │ new │
│               │ ISS │ PR │ (%) │     │    │    │ 🚀         │ 🚀? │
├───────────────┼─────┼────┼─────┼─────┼────┼────┼────────────┼─────┤
│ .github       │  45 │  1 │   - │   - │ ✅ │ ✅ │ 2026.10.26 │ no  │
├───────────────┼─────┼────┼─────┼─────┼────┼────┼────────────┼─────┤
│ base58-bech32 │   1 │  0 │   0 │   0 │ ✅ │ ❌ │ never      │ ⏳  │
│ bip39-slip39  │   3 │  0 │ 100 │  🥇 │ ❌ │ ✅ │ 2026.10.17 │ YES │
├───────────────┼─────┼────┼─────┼─────┼────┼────┼────────────┼─────┤
│ …             │     │    │     │     │    │    │            │     │
└───────────────┴─────┴────┴─────┴─────┴────┴────┴────────────┴─────┘
```

The columns are Repository, ISS, PR, BL3, 🥇%, CI, 📛, last 🚀 and new 🚀?,
in that order, each heading on two lines. Repository holds the
repository's name. The row of `btclib-org.github.io` is named
`btclib.org`, the site it serves, so that the column is as wide as
`ai-agents-process`. The first line of ISS and PR is the total on the
measure's last line, which leaves out a row whose ISS or PR count is an
error. BL3 is the badge project's baseline percentage. 🥇% is its gold
percentage, `🥇` where that is 100. Both are `-` where the repository has
no badge project. CI and 📛 are `✅` where the measure's `ci` and `badges`
say `ok`, and `❌` otherwise. An ISS, PR, BL3 or 🥇% cell whose value is
an error shows `err`.

last 🚀 is the latest tag without its leading `v`, `never` where
there is none. A cell holds its value and nothing else.

Each column is as wide as its longest cell, plus one space on each side.
`✅`, `❌`, `⏳`, `🥇`, `📛` and `🚀` each take two columns of the
terminal, and the widths and the alignment count them so. Numbers are
right-aligned. A horizontal rule goes between two sections, never between
two rows of one section. Where the table would pass 80 columns, a cell
too long goes on in a continuation line, its other cells empty. No
Markdown table.

After it, at most two lines: what a reader cannot see in the table, such
as the pull request that makes a `YES` urgent, or a repository whose
package name differs from its own (`.github`'s is
`btclib-alignment`).
