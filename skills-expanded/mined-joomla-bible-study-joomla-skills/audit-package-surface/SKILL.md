---
name: audit-package-surface
description: Audit what a Joomla extension's build actually distributes and installs — unintended shipped files, directly reachable executable entry points, unsafe installer and update behaviour, and vulnerable production dependencies. Use when reviewing release packaging or install/update surface for a Joomla extension, or when explicitly invoked for a package surface audit. Missing _JEXEC guards in intended files belong to audit-jexec.
---

# Audit Joomla release package surface

Audit what the project's build actually distributes and installs — not just what exists in the source
tree. Identify files, entry points, installer behaviour, and third-party code that unnecessarily
enlarge the production attack surface.

## Boundaries

This audit owns package composition, manifest and build mismatches, unintended directly reachable
files, installer and update surfaces, and deterministic dependency-vulnerability checks.

- Vulnerabilities *inside* first-party sinks belong to their dedicated audits.
- Missing `_JEXEC` guards in **intended** extension PHP files belong to `audit-jexec`. Report
  **unintended** shipped PHP here and cross-reference rather than duplicating the guard finding.

## Establish the package first

Read the extension manifests, package and build scripts, ignore rules, and Composer/npm production
settings. Where the repository already supports it and it is safe to do so, build the same artifact
released to users and inspect its file list.

Do not assume every Git file ships, or that every file in the package is in Git — that gap is the
whole point of this audit. **Do not install dependencies or contact registries without the user's
authorisation.**

## What to check

- Backups, editor files, SQL dumps, logs, debug tools, test fixtures, CI and development
  configuration, source credentials, private keys, source maps, sample applications, vendor demos,
  diagnostic pages, and alternate entry points.
- Executable PHP in `media/` or other directly addressable locations; unexpected
  writable-plus-executable directories; files omitted from uninstall or upgrade cleanup where
  continued reachability matters.
- Manifest paths that install broader trees than intended; stale files retained across upgrades;
  unsafe install scripts; and update or download URLs lacking the transport security or package
  authenticity the supported Joomla versions expect.
- Production packages containing development dependencies, or unnecessary tools and interpreters.
- Known vulnerabilities in locked production dependencies, using the ecosystem's lockfile-aware audit
  command where available. Record the tool and database freshness, and treat unconfirmed
  name/version matches as **leads, not proof**.

Minified assets, legitimate public keys, and test files provably excluded from every release artifact
are not findings.

### Joomla specifics

Check that `<files>` and `<folders>` in the manifest do not sweep in a whole directory when only part
of it is needed, and that the update server XML the extension points at is served over HTTPS with
hashes that actually match the published package. The `<scriptfile>` install script runs with full
privileges during install and update — read what it does, not just that it exists.

## Workflow

### Step 1 — Audit

Report findings ordered by severity:

- **CRITICAL** — a packaged credential or backdoor, or a directly reachable tool enabling
  unauthenticated code execution or takeover.
- **HIGH** — a shipped vulnerable production dependency with a reachable high-impact path; an
  executable demo or diagnostic surface; or private data in the artifact.
- **MEDIUM** — unnecessary reachable code, unsafe upgrade residue, a production development
  dependency, or a vulnerable dependency whose exploitability is constrained or unknown.
- **LOW** — metadata or source disclosure, or packaging hardening with no demonstrated exploit.

For each finding **distinguish source-tree presence from release-artifact presence**, identify the
rule that includes it, explain reachability and impact, and propose the smallest packaging or build
correction. Include dependency advisory identifiers and locked versions where applicable.

Report and await user feedback before changing any package rules or dependencies.

### Step 2 — Feedback round

The user is a subject matter expert and may reclassify or overrule a finding after giving more
context — a file that is excluded by a build step you did not read, for instance.

### Step 3 — Plan fixes

Once the user is done giving feedback, check for remaining items to fix.

If none, say so and stop.

Otherwise break the fixes into smaller, individually implementable plans and write them to the
`.gitignore`'d `.plans` directory, clearing any existing files there first. Then propose running
those plans in parallel via subagents, on a cheaper/faster model — the planning work is already done.

---

*Adapted for this suite from the `audit-package-surface` workflow in
[nikosdion/pm-skill-demo](https://github.com/nikosdion/pm-skill-demo), MIT licensed,
Copyright (c) 2026 Nicholas K. Dionysopoulos. The MIT permission notice accompanies this adaptation;
full text at <https://github.com/nikosdion/pm-skill-demo/blob/main/LICENSE>.*
