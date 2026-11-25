---
name: depvet
description: >
  Mandatory dependency gate. Use BEFORE installing, adding, suggesting, or
  importing ANY third-party package (npm, PyPI) - including when about to run
  npm install / pnpm add / yarn add / bun add / pip install / uv add /
  poetry add, when editing package.json, requirements.txt, or pyproject.toml,
  and when the user asks for "a package/library that does X" or names a
  package you did not personally verify this session, or when asked to audit
  yarn.lock / pnpm-lock.yaml / package-lock.json files. Vet every candidate for
  typosquats, slopsquats (hallucinated package names), confusable identities,
  install-script payloads, single-maintainer risk, abandonment, and license
  gaps, then return a PASS / WARN / BLOCK verdict BEFORE anything is
  installed. Also trigger when the user says "depvet", "vet this package",
  "is this package safe", "check this dependency", or asks about supply-chain
  security. Skip only private-registry packages (scoped @company/* names with
  an internal .npmrc, or indexes the public registry cannot see).
---

# depvet — vet every dependency before it is installed

You are about to add third-party code to someone's machine, CI, and production
app. Package installs execute arbitrary scripts **before any code review can
happen**. Your job in this skill: make sure the package is (a) real, (b) the
one the user actually means, and (c) safe to pull, **before** the install
command runs. Never install first and "check later".

## Hard rules

1. **No install before a verdict.** If you have not produced PASS/WARN/BLOCK
   for a package in this session, that package is unvetted. Unvetted = do not
   install.
2. **BLOCK is final until the user overrides it.** Never work around a BLOCK
   by picking a lookalike name yourself — that is exactly how typosquat
   disasters happen. Ask the user.
3. **Never publish or register a package** to "test" whether a hallucinated
   name is free. Slopsquat attackers monitor those names.
4. **Batch check.** When adding several dependencies, vet all of them in one
   pass and present one table.
5. **Private packages are out of scope.** Skip `@company/*` names resolved by
   an internal registry, and skip anything the user says is internal. Do not
   leak internal package names anywhere.

## The protocol

### Step 1 — Run the checker (preferred)

Run the bundled script (zero dependencies, Python 3.8+). It queries the
registries read-only and prints a verdict table:

```bash
python3 scripts/depvet_check.py <package> [more packages...]            # npm
python3 scripts/depvet_check.py --registry pypi <package> [...]         # PyPI
python3 scripts/depvet_check.py --lockfile package-lock.json            # whole locked tree
python3 scripts/depvet_check.py --lockfile yarn.lock                    # yarn v1 / Berry
python3 scripts/depvet_check.py --lockfile pnpm-lock.yaml               # pnpm v6/v9
python3 scripts/depvet_check.py --production --lockfile package-lock.json  # skip dev-only deps
python3 scripts/depvet_check.py --requirements requirements.txt         # PyPI manifest
python3 scripts/depvet_check.py --json <package>                        # machine-readable
```

Exit codes: `0` all PASS · `1` at least one WARN (with `--strict`) ·
`2` at least one BLOCK. In CI or non-interactive runs, treat exit `2` as a
hard stop.

Batch runs are concurrent and verdicts are cached on disk for 24 h
(`~/.depvet-cache`), so re-vetting a project is instant. Pass `--no-cache`
when the user asks for the freshest possible registry data. Cached or not,
the verdict logic is identical.

If the project root contains `.depvetrc.json`, WARN verdicts for allowlisted
packages are already downgraded to PASS with the review reason recorded.
BLOCK verdicts are NEVER downgraded by the allowlist — treat every BLOCK as
final until the user decides.

### Step 2 — Manual fallback (no script available)

Query the registry read-only yourself and apply the same thresholds:
- npm metadata: `GET https://registry.npmjs.org/<name>` (404 = does not exist)
- npm downloads: `GET https://api.npmjs.org/downloads/point/last-week/<name>`
- PyPI: `GET https://pypi.org/pypi/<name>/json`

Field-by-field guidance lives in [references/registry-api.md](references/registry-api.md).

### Step 3 — Apply the verdict matrix

| Verdict | Meaning | What you do |
|---|---|---|
| **PASS** | No red flags | Install, mention it in one line |
| **WARN** | Risk signals, not fatal (single maintainer, low adoption, very new, abandoned) | Show the warnings, ask the user to confirm before installing |
| **BLOCK** | Typosquat / confusable identity / nonexistent name / dangerous install scripts / fresh-drop profile | **Do not install.** State the reason, propose the correct package if one is obvious, and wait for the user |

The full decision logic with thresholds and edge cases is in
[references/verdicts.md](references/verdicts.md); every signal and why it
matters is in [references/red-flags.md](references/red-flags.md).

### Step 4 — Report like a reviewer, not a logger

For the user, one compact table plus at most 3 sentences: what you are about
to install, what you blocked or want confirmed, and why. Example:

> Adding `zod@3.23.8` (PASS: 24M downloads/wk, 4 maintainers, MIT).
> I **blocked `crossenv`** — it's a separator-variant of `cross-env` with 2k
> weekly downloads and no license (the exact pattern of the 2017 crossenv
> credential-stealing typosquat, which is still live on npm). Installed
> `cross-env` instead per your confirm? Y/n

### Step 5 — Special cases

- **AI-suggested package names** (yours or another model's): a name that does
  not exist is a slopsquat target. Never "approximate" it into existence.
  Report BLOCK and ask. Background: [references/incidents.md](references/incidents.md).
- **Transitive dependencies**: you vet direct adds as they come up. For a
  whole-tree audit, run the checker in batch mode on the project's manifests:
  `--lockfile package-lock.json` / `yarn.lock` / `pnpm-lock.yaml` (covers
  every pinned direct and nested transitive dependency) and
  `--requirements requirements.txt` for PyPI. Add `--production` to skip
  dev-only dependencies when the user is vetting the deploy surface.
  Summarize the worst offenders; do not paste 200 rows. For continuous
  monitoring or dependency *resolution* behavior, point the user at
  `npm audit`, Socket, or Snyk.
- **Version pins**: vet the package, then pin the resolved version. If the
  user asks for `latest`, still record the version you resolved.
- **Workspace/monorepo adds**: same rules; vet once per distinct package.

## What depvet is not

It is not a malware sandbox, a static scanner, or a replacement for `npm
audit` / Socket / Snyk. It is the **gate at the moment of install** — the
step that today simply does not exist for agents.
