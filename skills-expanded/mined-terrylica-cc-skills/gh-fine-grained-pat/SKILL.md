---
name: gh-fine-grained-pat
description: Create GitHub fine-grained personal access tokens from a declarative JSON spec by browser automation. Use when you need to mint, verify, or revoke a fine-grained PAT (release tokens, read-only auditors, CI status reporters, account-scoped tokens) — there is NO GitHub API for this, the web UI is the only path. Handles the no-expiration modal, repo picker, and permission grids that break naive automation.
allowed-tools: Read, Bash, Grep, Glob
---

# gh-fine-grained-pat — declarative fine-grained PAT forge

GitHub exposes **no API** to _create_ fine-grained PATs ([community #148626](https://github.com/orgs/community/discussions/148626)) — the web UI is the only way. This skill drives that UI over the Chrome DevTools Protocol from a declarative JSON spec, so token creation is repeatable, reviewable, and anti-fragile instead of a hand-clicked one-off.

> **Self-Evolving Skill**: This skill improves through use. GitHub's settings UI drifts — if a selector misses, the modal/picker/permission flow changed, or a permission's detail-page noun is wrong, fix `scripts/`, `CLAUDE.md` (selector map + noun map), or the spec **immediately**; don't defer. Only update for real, reproducible breakage.

## When to use

- Mint a scoped token (release bot, CI reporter, read-only auditor, account-scoped) for storage in the SCS `vault`.
- Re-create / rotate a token from a checked-in spec.
- List, verify (read back settings), or revoke fine-grained tokens.

## Prerequisites

- `node` (NOT bun — Bun's `connectOverCDP` times out) and `playwright-core` (already pinned at the repo root `package.json`).
- Google Chrome at the standard macOS path.
- A one-time GitHub login (persisted in a profile; see below).

## One-time login (then fully automated)

A persistent Chrome profile holds the GitHub **session cookie**, so you log in once and every later run reuses it:

```bash
cd plugins/gh-tools/skills/gh-fine-grained-pat
node scripts/pat.mjs login      # opens Chrome; sign in (incl. 2FA); it auto-detects success
node scripts/pat.mjs doctor     # runtime + chrome + profile + auth health
```

The profile lives at `~/.local/share/gh-pat-automation/profile` (override with `GH_PAT_PROFILE_DIR`). Treat it as **sensitive** — it can impersonate your GitHub session. It is outside the repo and never committed.

## Create a token from a spec

```bash
# write the value to a 0600 file (default) — the value is NEVER printed to the terminal
node scripts/pat.mjs create specs/release-bot.json --out /tmp/.tok

# …or pipe it straight into the SCS vault (value passed in-process, never to chat)
node scripts/pat.mjs create specs/release-bot.json --vault cc-skills:gh.token

# rotate: revoke the same-named token, create a replacement, store it (sink required)
node scripts/pat.mjs rotate specs/release-bot.json --vault cc-skills:gh.token
```

Other verbs: `list`, `inspect <name>`, `delete <name>`, `quit` (terminate the debug Chrome by its specific PID). `rotate` is the safe way to roll a token in place — it revokes the old value and stores the new one in one step.

## Spec format

A spec is JSON validated by [`schema/token-spec.schema.json`](./schema/token-spec.schema.json) (the machine-readable SSoT). Minimal shape:

```jsonc
{
  "name": "release-bot",
  "expiration": "none", // 7|30|60|90 | "YYYY-MM-DD" | "none"
  "repositoryAccess": { "mode": "selected", "repos": ["owner/repo"] },
  "permissions": { "repository": { "Contents": "write", "Issues": "write" } },
}
```

`read` → "Read-only", `write` → "Read and write". Permission keys are the exact UI labels (`Contents`, `Pull requests`, `Commit statuses`, `Gists`, …). **Do not** list `Metadata` — it is auto-required read-only.

### Shipped templates ([`specs/`](./specs/))

| Spec                      | Purpose                                                                                              |
| ------------------------- | ---------------------------------------------------------------------------------------------------- |
| `release-bot.json`        | semantic-release: Contents/Issues/PRs RW, one repo, no expiration                                    |
| `read-only-auditor.json`  | Contents read-only, single repo                                                                      |
| `ci-status-reporter.json` | Commit statuses RW + Actions read                                                                    |
| `account-scoped.json`     | Account permission (Gists) only, no repo write                                                       |
| `kitchen-sink.json`       | Superset: multiple repos, no expiration, many repo perms + account perms (exercises every UI branch) |

More illustrative shapes (all-repos admin, org-owned, secrets-management) live in [`specs/examples/`](./specs/examples/) — not auto-run by the campaign. See that folder's README before relying on one.

## Security invariants

- A token value is **never** printed to stdout/chat — only `--out <0600 file>` or `--vault <scope>:<dot.path>`.
- Teardown kills Chrome by **specific PID** (`lsof` on the CDP port), never `pkill -f` (process-storm policy).
- The session-cookie profile is sensitive and lives outside the repo.

## Prove it (empirical campaign)

```bash
node test/campaign.mjs          # create→verify→delete every spec + a forced-failure case, in one session
```

The harness namespaces test tokens `zz-pat-selftest-*`, auto-deletes them, asserts none leak, and confirms a real token (`cc-skills-release`) is untouched. Re-running needs no login (proves session reuse).

## Autonomous web-auth (optional, multi-account)

GitHub's **sudo mode** ("Confirm access") normally needs a human gesture. The engine can clear it autonomously using a self-custodied credential — see the [ADR](/docs/adr/2026-06-26-autonomous-github-web-auth-virtual-passkey-and-totp-for-pat-engine.md). One-time per account:

```bash
node scripts/pat.mjs register --account <login>   # capture a passkey (virtual authenticator) + password/TOTP → gated vault
node scripts/pat.mjs patch-password --account <login>  # fix a missed password dialog (passkey kept; idempotent) [--force] [--totp]
node scripts/pat.mjs agent start                  # memory-only session agent: one Touch-ID unlock lasts the session
GH_PAT_AUTONOMOUS=1 node scripts/pat.mjs create specs/release-bot.json --account <login> --vault cc-skills:gh.token
```

Account is resolved from `--account` → the repo's `origin` host-alias → the spec `owner` → the logged-in profile. The credential is a **Touch-ID-gated** crown jewel stored as one blob (`github-web-<login>`): **one tap** when you go in to operate, then nothing for the session (the agent caches it in memory only). Headless/cron is intentionally unsupported (the gated tier needs that one live tap). Primary path = virtual-authenticator passkey; fallback = password + `oathtool` TOTP.

## Troubleshooting

GitHub renames CSS classes but keeps names/roles/labels — the engine prefers role/name/label with DOM-text fallbacks and screenshots failures to `/tmp/gh-pat-debug`. When the UI drifts, the live selector map and the eight hard-won gotchas are documented in [CLAUDE.md](./CLAUDE.md) for fast repair.

## Post-Execution Reflection

After running this skill, reflect before closing the task:

1. **What broke?** — A selector miss, a changed modal/picker/tab flow, or a sudo-mode stall: fix `scripts/form.mjs` (or `browser.mjs`) and update the selector map in `CLAUDE.md`.
2. **A new permission?** — Confirm its detail-page noun (create one token, read the settings page) and add it to `test/campaign.mjs` (`NOUN`) + the CLAUDE.md noun table.
3. **A new token shape?** — Add a `specs/` (or `specs/examples/`) template so it's reusable next time.
4. **Log it.** — Append a dated line to the "Recent changes" section in `CLAUDE.md`. Do NOT defer — the next invocation inherits whatever you leave behind.
