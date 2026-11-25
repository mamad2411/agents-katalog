---
name: ssh-claude-auth
description: Fix Claude Code appearing logged-out over SSH on a headless macOS machine — its credentials sit in the login keychain, which stays locked in SSH/headless sessions. Offers two fixes and asks the user to choose: a keychain-free long-lived setup-token, or auto-unlocking the login keychain with a stored password (required on any machine in a cux-rotated fleet, where a setup-token cannot be registered or measured). Use when Claude Code shows unauthenticated over SSH on a Mac, when setting up a Mac mini or headless Mac for remote/CI Claude Code use, when installing `~/.claude/unlock-keychain.sh` for the fleet credential skills, or when `security show-keychain-info` reports the login keychain locked.
---

# Claude Code auth on a headless Mac over SSH

## Problem

Claude Code (subscription / OAuth login) stores its credentials in the macOS **login keychain**, encrypted with the user's macOS login password. A GUI login unlocks it automatically; an SSH / headless session does **not**, so Claude Code looks logged out until the keychain is unlocked. Two facts shape the fix:

- `sudo` cannot help — unlocking is *decryption*, and root has privilege but not the password.
- On macOS the keychain is the credential's *intended* home; `~/.claude/.credentials.json` is not the supported Linux-style alternative you can simply opt into.

**But do not read that second point as "the file never exists on macOS."** It does, and mistaking its presence for a healthy configuration wastes hours. `cswap` degrades to writing `~/.claude/.credentials.json` whenever the keychain is unavailable mid-operation, so a full OAuth credential — `refreshToken` present, complete scopes — can end up living there on a Mac. Observed 2026-08-19: the file was present (mode 600) on both headless fleet receivers and **absent** on the GUI machine, exactly tracking which ones had a locked keychain.

Why it matters here: a credential in that file is invisible to `cux`, which reads only the keychain item. `security find-generic-password -s "Claude Code-credentials"` then returns **44** (`errSecItemNotFound`), which looks identical to a setup-token login but is not — unlocking the keychain and re-activating the slot (`cswap switch <active-slot> --force`) makes cswap write the item back. Distinguish rc **36** (locked — unlock and retry) from rc **44** (no item at all — unlocking changes nothing).

## Step 1 — Confirm the diagnosis

```bash
security show-keychain-info ~/Library/Keychains/login.keychain-db   # locked/timeout error => this skill applies
security find-generic-password -s "Claude Code-credentials" ~/Library/Keychains/login.keychain-db >/dev/null 2>&1 \
  && echo "creds are in the keychain"
```

## Step 2 — Ask the user which approach (do NOT choose for them)

> **First: is this machine part of a cux-rotated Claude fleet?** If it is, **Approach A is
> disqualified** — go straight to Approach B and skip the question. A `setup-token` carries
> `user:inference` alone, so `/api/oauth/usage` answers **403**; `cux add` cannot register the
> login at all (it reads only the `Claude Code-credentials` keychain item, and fails with
> **exit 0**, so the failure is silent). The machine then looks configured while sitting
> permanently outside rotation, invisible to both rotators. Verified against cux 0.3.9 /
> cswap 0.25.0. See `sync-claude-accounts` and `refresh-claude-account`, which both exist to
> keep full OAuth logins working across a fleet and explicitly withdraw the setup-token
> recommendation. Tell the two credential kinds apart by shape — `refreshToken: false` /
> `scopes: ['user:inference']` — never by token prefix (both start `sk-ant-oat01-`).

Use **AskUserQuestion** with the trade-offs below. List Approach A first, labeled "(Recommended)" — unless the machine is in a fleet (above) or the user drives this machine's Claude Code remotely (see caveat), in which case recommend B.

| | A. Long-lived OAuth token | B. Auto-unlock keychain |
|---|---|---|
| Secret stored on disk | A scoped, revocable OAuth token | The **macOS login password**, plaintext |
| Blast radius if leaked | Inference only; revoke anytime | Unlocks the **entire** keychain |
| Touches the keychain? | No — bypasses it | Yes |
| Maintenance | Re-mint ~yearly (token expires) | Re-edit file when Mac password changes |
| Remote Control sessions | ❌ token can't establish them | ✅ works |

**Caveat to surface before they pick:** a `setup-token` credential is inference-only and **cannot establish Remote Control sessions** (driving this machine's Claude Code from claude.ai or mobile). Users who rely on that need Approach B.

## Step 3 — Run the chosen setup script

Invoke scripts by **absolute path**: `bash <skill-base-dir>/scripts/<name>.sh`, where `<skill-base-dir>` is the base directory printed when this skill loads. All scripts read secrets interactively with no echo — **never** pass a password or token on the command line, and never have the user paste one into the conversation.

**Approach A** (requires a Claude Pro / Max / Team / Enterprise subscription):
1. The **user** mints the token themselves: `claude setup-token` (interactive browser OAuth; prints a ~1-year token, does not save it).
2. `bash <skill-base-dir>/scripts/setup-oauth-token.sh` — prompts for the token, stores it `600`, and sources it from `~/.zshrc` as `CLAUDE_CODE_OAUTH_TOKEN`, which Claude Code uses instead of the keychain.
3. If Approach B was ever set up, remove it so the macOS password stops living on disk: `bash <skill-base-dir>/scripts/teardown-keychain-unlock.sh`

**Approach B**:
- `bash <skill-base-dir>/scripts/setup-keychain-unlock.sh` — prompts for the macOS password, then installs the password file (`600`), unlock script (`700`), a login LaunchAgent, and a `~/.zshrc` SSH hook.
- For a lighter variant that stores no password and prompts once per SSH session instead, see [REFERENCE.md](REFERENCE.md).

## Step 4 — Verify

Open a **fresh** SSH session and run `claude` — it should be logged in with no prompt.
- Approach A: `[ -n "$CLAUDE_CODE_OAUTH_TOKEN" ] && echo "token set"`. Note `claude --bare` ignores this variable — use `ANTHROPIC_API_KEY` there.
- Approach B: `bash ~/.claude/unlock-keychain.sh && echo ok`

## Scripts

| `scripts/` | Purpose |
|---|---|
| `setup-oauth-token.sh` | Install Approach A (token file + `~/.zshrc` block) |
| `teardown-oauth-token.sh` | Undo Approach A (falls back to the keychain) |
| `setup-keychain-unlock.sh` | Install Approach B (password file, unlock script, LaunchAgent, `~/.zshrc` hook) |
| `teardown-keychain-unlock.sh` | Undo Approach B, **deleting the stored macOS password** |
| `lib.sh` | Shared helpers; single source of truth for the `# >>> … >>>` block markers |

Switching approaches = run the new setup, then the old teardown. Manual walkthrough, no-stored-password variant, command quick-reference, and common mistakes: [REFERENCE.md](REFERENCE.md)

## Related

Approach B's `~/.claude/unlock-keychain.sh` is a hard dependency of the fleet credential skills —
`cux add` reads the keychain directly and cannot fall back to a file, and the keychain **re-locks
between SSH sessions**, so every remote step must unlock in the *same* invocation as the command
that needs it.

- `sync-claude-accounts` — distributes OAuth credentials across a fleet; calls the unlock script on every receiver
- `refresh-claude-account` — repairs a dead account back to a full OAuth login
- `sync-claude-accounts` — the scheduled agents and alerts over both

All three assume **full OAuth logins**, which is why Approach A is disqualified on fleet machines (Step 2).
