---
name: credential-cache-file-for-mcp-subprocess
description: Write decrypted per-source credentials to a session-scoped .credential-cache.json on disk so MCP stdio subprocesses can read them without the parent passing secrets via env (which shows up in ps).
category: agent-sdk
version: 1.0.0
version_origin: extracted
tags: [credentials, mcp, subprocess, filesystem-ipc]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/lukilabs/craft-agents-oss.git
source_ref: main
source_commit: 61f7d48a5b4fd0a8094f002c9e3aea5f3824dcfb
source_project: craft-agents-oss
source_path: packages/session-mcp-server/src/index.ts
imported_at: 2026-04-18T00:00:00Z
---

# Credential cache file for MCP subprocesses

## When to use
- Spawning MCP subprocesses that each need per-source credentials (GitHub token, Slack bearer, etc.).
- Don't want secrets in `env` (visible via `ps -e`, leakable through logging).
- Secrets rotate or expire; the subprocess must re-read on each call rather than snapshot at start.

## How it works
1. Parent (Electron main) maintains the encrypted credential store.
2. When a session starts and a source is activated, parent decrypts the relevant credential and writes it to:
   ```
   <workspaceRoot>/sources/<sourceSlug>/.credential-cache.json
   ```
3. File format:
   ```jsonc
   { "value": "<secret>", "expiresAt": 1732000000000 }
   ```
4. Permissions: restrict to user (`0600`). Clean up on session end.
5. Subprocess reads this file per tool call (not per session start) - handles rotation and expiry naturally.
6. Subprocess checks `expiresAt`; if expired, sends a `__CALLBACK__` stderr message asking the parent to refresh.
7. Keep file *outside* the session dir (under `sources/`) so the same cache is shared across sessions that use the same source.

## Example
```ts
// Parent
function refreshCache(workspaceRoot, sourceSlug, cred) {
  const path = join(workspaceRoot, 'sources', sourceSlug, '.credential-cache.json');
  writeFileSync(path, JSON.stringify({ value: cred.accessToken, expiresAt: cred.expiresAt }));
  chmodSync(path, 0o600);
}

// Subprocess
function getCredential(workspaceRoot, sourceSlug) {
  const p = join(workspaceRoot, 'sources', sourceSlug, '.credential-cache.json');
  if (!existsSync(p)) return null;
  const { value, expiresAt } = JSON.parse(readFileSync(p, 'utf8'));
  if (expiresAt && Date.now() > expiresAt) {
    console.error(`__CALLBACK__${JSON.stringify({ type:'credential_expired', sourceSlug })}`);
    return null;
  }
  return value;
}
```

## Gotchas
- Always `chmod 0600` - writing credentials world-readable is the dumb version of this.
- Don't rely on `.gitignore` to keep these out of repos; they're under workspace dirs that users may zip and share.
- On Windows, permission bits don't map cleanly; combine with ACL or keep the parent dir write-protected.
- Add to session cleanup: delete stale caches on session close.
- Subprocess reading per tool call has a small perf cost but wins on rotation safety.
