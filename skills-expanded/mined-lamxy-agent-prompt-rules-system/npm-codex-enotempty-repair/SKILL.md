---
name: npm-codex-enotempty-repair
description: Fix npm global install failures for @openai/codex when ENOTEMPTY rename conflicts occur in the global node_modules path.
argument-hint: 'optional: explicit npm global prefix path'
---

# npm Codex ENOTEMPTY Repair

Use this Skill when the user reports an error like:

- `npm ERR! code ENOTEMPTY`
- `rename .../@openai/codex -> .../@openai/.codex-*`

## Goal

Recover from stale temporary directories left by failed npm reify moves, then reinstall Codex CLI cleanly.

## Procedure

### Step 1: Resolve global prefix and inspect paths

```sh
npm prefix -g
npm root -g
```

Expected affected paths:

- `<PREFIX>/lib/node_modules/@openai/codex`
- `<PREFIX>/lib/node_modules/@openai/.codex-*`
- `<PREFIX>/bin/codex`
- `<PREFIX>/bin/.codex-*`

### Step 2: Remove stale temp directories first

```sh
PREFIX="$(npm prefix -g)"
find "$PREFIX/lib/node_modules/@openai" -maxdepth 1 -type d -name '.codex-*' -exec rm -rf {} + 2>/dev/null || true
find "$PREFIX/bin" -maxdepth 1 -type f -name '.codex-*' -delete 2>/dev/null || true
```

### Step 3: If uninstall fails, continue with hard cleanup

```sh
npm uninstall -g @openai/codex || true

PREFIX="$(npm prefix -g)"
rm -rf "$PREFIX/lib/node_modules/@openai/codex"
rm -f "$PREFIX/bin/codex"
find "$PREFIX/lib/node_modules/@openai" -maxdepth 1 -type d -name '.codex-*' -exec rm -rf {} + 2>/dev/null || true
find "$PREFIX/bin" -maxdepth 1 -type f -name '.codex-*' -delete 2>/dev/null || true
```

### Step 4: Reinstall and verify

```sh
npm install -g @openai/codex@latest
command -v codex
codex --version
```

## Reporting Checklist

After running the repair, report:

- whether stale `.codex-*` directories were found and removed;
- whether uninstall failed or succeeded;
- whether reinstall succeeded;
- final `codex --version` output.

## Notes

- This issue is usually local filesystem state, not a package version issue.
- If reinstall still fails, capture and include the latest npm debug log path from output.
