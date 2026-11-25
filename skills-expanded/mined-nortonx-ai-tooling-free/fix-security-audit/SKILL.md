---
name: fix-security-audit
description: "Detect the JS/TS package manager, audit dependencies, and fix vulnerabilities safely, least-invasive first, with backup, re-audit, and full test/lint/format/e2e verification. Works with npm, pnpm, yarn, deno, bun. Args: [<path-to-project>]"
argument-hint: "[<path-to-project>]"
---

<!-- Note: $ARGUMENTS is substituted by Claude commands only. In Copilot,
     the user must include their argument inline in the prompt; the skill
     body sees the literal text "$ARGUMENTS" unsubstituted. -->

## Arguments

`[<path-to-project>]`

- Optional. Path to the project root to audit. Defaults to the current working directory.
- **Examples**: `/fix-security-audit`, `/fix-security-audit ./packages/api`

> Copilot CLI note: `$ARGUMENTS` does not substitute in skills; include the argument inline in your prompt.

# Fix security audit

Detect the package manager a JS/TS project uses, audit its dependencies for known vulnerabilities, and resolve them **safely**: applying the least-invasive fix first, backing up before any change, re-auditing after each step, and re-running the project quality gates before declaring success. Never break the user dependency tree silently.

Run every command in the project root (from `$ARGUMENTS` if given, else the current directory). Commands below are written shell-agnostically: discard stderr as your shell allows (such as redirecting to null in PowerShell or POSIX shells) and do not chain with `&&`.

## Step 1: Detect the package manager

Check signals in order; **first match wins**. Report which manager was detected and the signal that decided it.

| Signal (checked in order) | Manager |
|---|---|
| `packageManager` field in `package.json` (corepack) | trust it (`npm` / `pnpm` / `yarn`) |
| `deno.json`, `deno.jsonc`, or `deno.lock` present | deno |
| `bun.lock` or `bun.lockb` present | bun |
| `pnpm-lock.yaml` present | pnpm |
| `yarn.lock` **and** `.yarnrc.yml` present | yarn berry (v2+) |
| `yarn.lock` present (no `.yarnrc.yml`) | yarn classic (v1) |
| `package-lock.json` present, or nothing matched | npm |

If **multiple** lockfiles exist, prefer the `packageManager` field; otherwise pick the most specific lockfile and **warn the user about the ambiguity**: do not guess silently. If no JS/TS project is found at all, stop and say so.

## Step 2: Audit (read-only)

Run the audit command for the detected manager and summarize findings by severity (critical / high / moderate / low).

| Manager | Audit command |
|---|---|
| npm | `npm audit` |
| pnpm | `pnpm audit` |
| yarn classic | `yarn audit` |
| yarn berry | `yarn npm audit` |
| bun | `bun audit` |
| deno | No native audit command. Best-effort: run `deno outdated` and report it, and **state plainly that Deno has no vulnerability audit**: do not fabricate a clean result. |

If the audit reports **zero vulnerabilities**, report clean and stop: there is nothing to fix.

## Step 3: Present the plan and get approval (GATE: do not skip)

Before touching anything, show the user:

- The detected package manager and why.
- The vulnerability summary by severity.
- The exact commands you intend to run, in order (the least-invasive-first strategy from Step 5).
- The backup you will take (Step 4).

**Wait for explicit approval. Do not mutate the dependency tree, lockfile, or `package.json` until the user says go.**

## Step 4: Back up

Copy `package.json` and the detected lockfile to `*.bak` siblings (e.g. `package-lock.json` -> `package-lock.json.bak`, `package.json` -> `package.json.bak`). These are the rollback point. Keep them until the run succeeds; if any later step fails, **restore from `.bak`**. On success, remove the `.bak` files and note their disposition in the report.

## Step 5: Fix, least invasive first

Stop escalating the moment a re-audit comes back clean. Re-audit after **every** mutation.

**5.1: Non-breaking auto-fix:**

| Manager | Command |
|---|---|
| npm | `npm audit fix` |
| pnpm | `pnpm audit --fix` |
| yarn classic | `yarn upgrade <pkg>` for each flagged package |
| yarn berry | `yarn up <pkg>` for each flagged package |
| bun | `bun update <pkg>` for each flagged package |
| deno | `deno outdated --update` for affected modules (best-effort) |

Re-audit. If clean, jump to Step 6.

**5.2: Forced / pinned fix (warn first):** If vulnerabilities remain, **warn the user that this step can introduce breaking, semver-major changes**, then proceed only with approval:

- npm: `npm audit fix --force`
- npm / pnpm: add an `overrides` block in `package.json` pinning the patched transitive version, then reinstall.
- yarn / bun: add a `resolutions` block in `package.json` pinning the patched version, then reinstall.

Re-audit again.

**Do NOT offer `--omit=dev` / `--prod` here.** Production-only scoping does not fix anything: it only hides dev-only advisories. Offer it **only** in Step 5.3.

**5.3: Last resort (`--omit=dev` / `--prod`):** Only if vulnerabilities still remain **and** no patched version exists for them. Explain clearly that this merely excludes dev-only dependencies from the audit rather than fixing the issue, and that the advisory still applies to your dev toolchain. Require explicit approval before running it (`npm audit --omit=dev`, `bun audit --prod`, etc.).

## Step 6: Verify the audit

Re-run the Step 2 `<manager> audit` command and capture the final vulnerability state (clean, or residual advisories that have no available fix).

## Step 7: Run project quality gates

Detect each gate from `package.json` scripts (or the Deno/Bun equivalent) and run those that exist. **Silently skip any gate that does not exist**: a missing script is not a failure.

| Gate | Where to look |
|---|---|
| lint | `lint` script -> `<manager> run lint`; or `deno lint` |
| format | `format` / `format:check` script; or `deno fmt --check` |
| unit tests | `test` script -> `<manager> test`; or `deno test`, `bun test` |
| e2e | `test:e2e` / `e2e` script (Playwright/Cypress) -> `<manager> run <script>` |

If any gate **fails after a fix was applied**, restore from `.bak` (Step 4), report exactly which gate failed with its output, and stop. Do not leave a half-broken tree.

## Step 8: Report

Output a markdown summary:

- **Package manager**: detected manager + the signal that decided it.
- **Vulnerabilities**: before -> after counts by severity.
- **Commands run**: the exact commands, in order.
- **Dependencies changed**: name + `old -> new` version for each, from the lockfile diff.
- **Gates**: which ran, passed, failed, or were skipped (and why skipped).
- **Escalations used**: whether `--force`, `overrides`/`resolutions`, or `--omit=dev` were used, and why.
- **Final status**: clean, or residual advisories with no available fix (list them).
- **Backups**: `.bak` files removed on success, or retained because the run was rolled back.

## Rules

- **Never mutate before Step 3 approval.** Audit and detection are read-only; everything after needs the go-ahead.
- **Never run `--force` without the Step 5.2 warning** about breaking changes.
- **Never offer `--omit=dev` / `--prod` before Step 5.2 escalation is exhausted**, and never as a fix: only as a last-resort scope reduction, with a warning.
- **Re-audit after every mutation**: do not assume a fix worked.
- **Restore from `.bak` if any quality gate fails** after a change. Leave the tree in a known-good state.
- **Skip missing gates** instead of erroring.
- Run from the project root; respect the `$ARGUMENTS` path if provided.
- Keep commands shell-agnostic and cross-platform: do not hardcode POSIX stderr redirection or `&&` chaining in what you instruct the user; adapt to PowerShell or bash as needed.
