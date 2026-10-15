---
name: skillrig
description: >-
  Point a repository at your org's agent-skills library and manage vendored skills with the
  `skillrig` CLI — bind/choose the origin (`init`), search/discover skills in it (`search`),
  vendor/add a skill (`add`, local or remote, with an optional immutable `--pin`),
  verify/check that committed skills are exactly what was approved (`verify`), and generate
  the origin's catalog (`index`). Use whenever the user wants to find, search, discover,
  install, add, vendor, pull in, lock, or pin an agent skill from a skills library; filter
  skills by topic; set/configure where skills come from or fix a "no origin configured" error;
  point a repo at a skills repo (OWNER/REPO[@branch]) or use SKILLRIG_ORIGIN; fetch from a
  private/remote origin or debug auth / unreachable / not-found / no-such-version fetch errors;
  or verify / check / audit that vendored skills haven't been tampered with (a CI gate) and
  debug `mismatch`/`orphan`/`missing`/`dirty` verdicts. Discovery and vendoring require an
  origin, so `skillrig init` comes first. Trigger even when the command isn't named — e.g.
  "point this repo at our skills", "what skills does our library have for terraform", "pull in
  the terraform-review skill", "pin it to v1.4.0", "make sure nobody changed our skills", "why
  did the skills check fail in CI", "our agent skill got edited".
license: MIT
metadata:
  author: skillrig
  cli: skillrig
  user-invocable: true
---

# skillrig

`skillrig` is a single, generic, **consume-only** CLI for pointing a repo at an **origin** —
the `OWNER/REPO` that hosts your org's agent skills — and managing the skills vendored from
it. The same binary serves humans, agents, and CI. There is no publish/login: GitHub is the
authority plane ("publishing" = a PR to the origin).

**The promise:** *the skill your agent runs is exactly the version that was reviewed and
approved.* `add` records a tamper-evident git tree-SHA when a skill is vendored; `verify`
recomputes it and fails if it drifted — same primitive on both sides, so the gate cannot lie.

## When to use this skill

Use it whenever the user wants to **find / search / discover / install / add / vendor / pull
in** an agent skill from a library, **set or fix the origin** ("point this repo at our
skills", "no origin configured"), **fetch from a private/remote origin** (and debug
auth/unreachable/not-found errors), or **verify / check / audit** that vendored skills are
unmodified (a CI gate), including debugging command output:

| Activity | Command | Read |
|---|---|---|
| Choose where skills come from (bind the origin) | `skillrig init` | [references/init.md](references/init.md) |
| Discover skills in the origin (search/filter by topic) | `skillrig search [QUERY...]` | [references/search.md](references/search.md) |
| Vendor a skill into the repo (local or remote; `--pin` a version) | `skillrig add <skill>` | [references/add.md](references/add.md) |
| Prove vendored skills match what was approved | `skillrig verify` | [references/verify.md](references/verify.md) |
| **Origin-side:** generate the origin's catalog (`index.json`) | `skillrig index` | [references/index.md](references/index.md) |

Load only the reference for the activity at hand. `init`/`search`/`add`/`verify` run in a
**consumer** repo; `index` runs **inside the skills-library (origin) repo** (usually its CI).

## Prerequisite: an origin must be configured (run `init` first)

`search` and `add` both need to know **where** skills come from, so a configured origin is a
precondition. **Smoketest before discovering/vendoring:** is an origin resolvable?

- project: `.skillrig/config.toml` exists (at the git repo root), **or**
- env: `$SKILLRIG_ORIGIN` is set, **or**
- global: `~/.config/skillrig/config.toml` exists.

Precedence (highest wins): `SKILLRIG_ORIGIN` > project config > global. If none resolve,
`search`/`add` fail with `no origin configured` — run `skillrig init --origin OWNER/REPO`
first (see [references/init.md](references/init.md)). **`verify` needs no origin** (it reads
the committed lock + tree, offline).

**Remote vs local origin.** A bare `OWNER/REPO` origin is **fetched over `git`** by
`search`/`add` (a private one auto-resolves a read-only token via `GH_TOKEN` > `GITHUB_TOKEN`
> `gh auth token`, so `gh auth login` once is enough); a filesystem-**path** origin is read
locally with no network. The form is classified automatically — you don't pick a mode.

## The typical workflow

```
skillrig init --origin my-org/my-skills      # 1. bind the origin (once per repo)
skillrig search terraform                    # 2. discover an approved skill (its name/version)
skillrig add terraform-plan-review           # 3. vendor it into .agents/skills/ (+ optional --pin v1.4.0)
git add -A && git commit -m "vendor skill"   # 4. commit (verify checks committed content)
skillrig verify                              # 5. prove it matches the recorded version (CI gate)
```

Exit codes are load-bearing for CI/agents: `0` ok · `1` usage/config · `2` verification
failure · `3` reserved (never emitted). Errors are what/why/fix on stderr; `--json` is the
complete machine view on stdout; `--verbose` shows the raw cause. Details per command in the
references.

## Scope vs. the generic `find-skills` skill

`skillrig search`'s "find" means *find an approved skill in **your origin*** — distinct from
the generic `find-skills` skill (discovering skills from anywhere). So "find/install a skill
from our library" is `skillrig`; "what skills exist out there for X?" is `find-skills`.

## Not here yet

Designed but **not implemented** (don't assume they exist): multi-client symlink views, a
prerequisite/health `doctor` (the reserved exit `3`), `bump --pr` upgrades, and `global`
scope. The shipped surface is `init` + `search` + `add` (local **or** remote, with `--pin`) +
`verify`, plus the origin-side `index` generator.
