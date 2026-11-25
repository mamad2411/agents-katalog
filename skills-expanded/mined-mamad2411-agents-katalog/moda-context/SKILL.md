---
name: moda-context
description: >-
  Pin a repo to Moda defaults via .moda/context.json — org, brand, canvas — so
  every run in this repo lands in the right place; check credits with `moda
  account usage/costs`. CLI-only: these defaults are files on your disk.
argument-hint: "[what to pin: org | brand | canvas — or 'show']"
allowed-tools: Bash(moda:*), Read
---

# moda-context

<!-- moda:banner -->
**PREREQUISITE — load `moda-core` once per session** (step-0, write contract,
free/metered map). Already loaded? Skip ahead. If you cannot load it, the
non-negotiables: run `moda doctor --json` before anything; `moda brand list`
before creating; every write carries the latest revision — on
`stale_revision`, re-read and retry once (it heals); send the canvas link the
moment it exists; stuck or failed? `moda ask "<question>"` — free and fast,
never guess.
<!-- /moda:banner -->

Second run in the same repo landing in the same workspace, on the same kit,
against the same canvas? Pin it once and every later run needs no flags.

## What gets pinned, and where

- `.moda/context.json` — committed. The repo's shared default, so a teammate's
  run lands in the same workspace with the same brand.
- `.moda/context.local.json` — gitignored. Yours alone; it wins over the
  committed file.
- Three keys only: `org`, `brand`, `canvas`. Discovered by walking up from the
  working directory, so a subdirectory inherits the repo's pins.

Precedence, highest first: an explicit flag on the command → `MODA_ORG` /
`MODA_API_BASE` in the environment → `context.local.json` → `context.json` →
this install's config → the built-in default.

## The three commands

```
moda context show                       # effective values AND where each came from
moda context set brand [bk_…]           # every create in this repo binds this kit
moda context set canvas [cvs_…]         # "the" canvas this repo keeps updating
moda context set org [ORG_ID] --local   # keep a personal org pin out of the commit
moda context clear [key]                # omit the key to clear all three
```

`moda context show` is the first thing to run when a command lands somewhere
unexpected: the `[source]` marker on each line names the file or flag that won.

## What to pin (and what not to)

- **brand** — the kit the repo's work belongs to. Pin it after `moda brand
  list` confirms which kit the user means; never guess between two kits.
- **canvas** — only when the repo really has ONE living artifact (the README
  deck, the status one-pager). A pinned canvas is a default, not a lock: an
  explicit ref in the ask always wins.
- **org** — whose workspace and billing the work lands in. Never pin or switch
  an org on your own initiative. Ask, then set exactly what the user names.
- Nothing here is secret, so nothing here is a credential: keys live in the OS
  keychain or the environment, never in these files.

## Credits and spend

```
moda account status                     # plan + balance — the honest credit check
moda account usage --days 30 [--by-operation]
moda account costs                      # what is metered vs not, from the server
```

- Canvas authoring, reads, screenshots, exports, and sites cost 0 credits on
  every plan. Only the media-generation and web-research lanes meter.
- Direct media calls do not return a per-call credit amount; the balance from
  `moda account status` is the honest answer, and totals live in `usage`.
- Answer a "how many credits do we have?" question with the balance and the
  plan, not an estimate — never hardcode what is metered, read `costs`.

## Examples

- "make this repo always use our brand" → `moda brand list` → confirm → `moda
  context set brand bk_…` → say what future runs will now do by default.
- "why did that land in the wrong workspace?" → `moda context show`, read the
  `[source]` column, fix the file that actually won.
- "keep updating the same deck from here" → `moda context set canvas cvs_…`.
- "how much have we spent this month?" → `moda account usage --days 30`.

## Errors

Any typed error → load moda-core and read its recovery reference. A pin whose
id no longer resolves fails at the verb that uses it, not at `set` — re-run
`moda context show`, then re-pin or clear.

## Make it recurring

A pinned repo is what makes an unattended run flagless — the scheduled half is
moda-automate. Pin the brand once and every later artifact is on-brand by
default (moda-brand owns the kit itself).

See also: moda-core — the contract, recovery, everything Moda can do.
