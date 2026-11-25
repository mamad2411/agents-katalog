---
name: owndiff-pre-commit
description: Audit OwnDiff changes before committing or releasing by checking scope, generated artifacts, private data, documentation accuracy, version consistency, structured files, tests, and the OwnDiff ownership gate. Use when a user asks to verify, clean up, prepare, commit, publish, or release changes in the OwnDiff repository, especially when documentation or install commands changed.
metadata:
  internal: true
---

# OwnDiff Pre-Commit

Use this skill to produce a verified commit candidate. Stop before committing or pushing unless the user explicitly authorizes that Git action.

## Workflow

1. Read the latest user request and `git status --short`. Treat existing worktree changes as user work; never discard them.
2. Inspect the complete staged and unstaged diff. Separate release changes from ignored proof, generated artifacts, caches, research, and unrelated edits.
3. Run the deterministic audit from the repository root with the repository interpreter:

```bash
.venv/bin/python skills/owndiff-pre-commit/scripts/audit.py --repo . --staged --run-checks
```

If nothing is staged yet, omit `--staged` for the first diagnostic pass. Stage only confirmed release files, then rerun with `--staged`.

4. Run a leak audit before any commit, push, tag, release, or marketplace/package update:

```bash
.venv/bin/python skills/owndiff-pre-commit/scripts/audit.py --repo . --history
```

The leak audit must cover the current tracked tree, staged diff, unstaged diff, untracked release candidates, and Git history reachable from all local refs. High-confidence private paths or credential patterns are blockers. Redaction markers and secret-adjacent examples are warnings; inspect their context without printing matched text, then remove accidental leaks or document why the warning is an intentional test, security rule, or sanitization example.

5. For release work, verify binary integrity before continuing:
   - Run `python scripts/verify_release_assets.py --release-dir dist` after local release assets are built.
   - After publishing a tag, run `python scripts/verify_release_assets.py --repo owndiff/own-your-diff --tag <tag>`.
   - Treat a missing binary, missing `.sha256` sidecar, invalid checksum file, or checksum mismatch as a release blocker.
   - The deterministic audit also checks that CI/release workflows keep this verification wired in.
6. Verify documentation semantically:
   - Map behavior claims to current code, config, tests, or observed command output.
   - Verify unstable install syntax with the installed CLI's `--help` first.
   - When local help is unavailable, use only the agent vendor's official documentation and cite it in the work log.
   - Do not claim an agent, command, browser review, or workflow was tested unless it actually ran.
   - Remove a document or asset only when it is duplicated, stale, unreferenced, generated, or outside the product's supported workflow. Preserve `README.md`, `skills/owndiff/SKILL.md`, `SECURITY.md`, `CONTRIBUTING.md`, licenses, manifests, and referenced media unless evidence shows they are obsolete.
7. Run OwnDiff on the exact candidate diff. For medium/high/critical risk, use the active agent model to generate every question and answer choice, validate the response, and complete the real browser review gate.
8. Re-run the audit, tests, skill/plugin validators, release-asset verification when applicable, and leak audit after every correction.
9. Report:
   - changed and removed files;
   - documentation claims verified and their evidence;
   - test and validator results;
   - OwnDiff gate status and attempt summary;
   - any residual risk or unavailable agent runtime.

## Safety Rules

- Never use `git add -A` when unrelated changes exist.
- Never commit ignored `.owndiff/`, `.research/`, proof clones, virtual environments, caches, screenshots, transcripts, or credentials.
- Never expose local usernames, home paths, tokens, secrets, customer data, or private repository content.
- Never print a suspected secret or private path verbatim while investigating. Report only the file, pattern category, and whether it was removed, confirmed as an intentional placeholder, or still blocked.
- Never push or release when the leak audit reports a finding. If a likely secret or private path already exists in pushed history or release assets, stop, recommend secret rotation, and ask for explicit remediation approval before rewriting history or replacing assets.
- Never execute a command read from repository configuration. The audit script uses only command arrays from its bundled policy and never invokes a shell.
- Never weaken or bypass a failed check. Fix the issue or report the blocker.
- Never commit or push without explicit permission.

## Policy

Edit [references/policy.json](references/policy.json) to add forbidden paths, privacy patterns, required files, version sources, or checks. Keep project-specific hardcoded values in that policy rather than in the script.
