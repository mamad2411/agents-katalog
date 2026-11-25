---
name: sync-library
description: Keep your agentstack central library (~/.agentstack/lib) consistent across machines by versioning it as a git repo — commit the index and path-source skill bodies, exclude the content store cache and any resolved secrets.
---

# Sync the central library

Use when you want your agentstack central library — the skills and MCP servers
you reference by name — to be the same on every machine (laptop, desktop, a
fresh box).

## The idea

The library lives at `~/.agentstack/lib/`. Version it as a git repo and
push/pull it across machines. git is the right tool here: versioned,
offline-friendly, no daemon, and it diffs cleanly.

**Never fetch a skill from another machine by hand (scp/rsync/ssh).** A raw
copy skips the content scan (prompt-injection gate), records no provenance,
and has no checksum — an unauditable fork the lockfile can't reproduce. If a
skill you need lives on another device, sync the library (below); the skill
then resolves by name everywhere.

## The built-in way (preferred)

agentstack ships a wrapper that does the whole flow — and refuses to push if a
server definition holds a literal secret in **any** field (headers, env, url,
args), can't be parsed (the gate fails closed rather than skipping it), or if
one is still buried in an outgoing commit. `--allow-secrets` overrides,
deliberately:

```bash
# first machine — set it up and push:
agentstack more lib sync --init --remote <your-remote>
agentstack more lib sync                     # commit local changes, pull, push

# a fresh machine — clone the library into place:
agentstack more lib sync --init --remote <your-remote>

agentstack more lib sync --status            # working-tree changes + ahead/behind
```

## What travels vs. what doesn't

- **Travels:** `library.toml` (the index), `skills/` (path-source bodies),
  `servers/` (definitions with `${REF}` placeholders only).
- **Stays local:** the content **store / cache** lives *outside* the library
  (`~/.agentstack/store`), so it never travels; resolved secret values are never
  in the library at all.

Git-source skills carry `git:<url>@<rev>#<subpath>` provenance, so they
re-resolve identically on any machine — only path-source content needs to move.

## Doing it by hand (equivalent)

If you'd rather run git yourself:

```bash
cd ~/.agentstack/lib
git init && git add library.toml skills servers
git commit -m "library snapshot"
git remote add origin <your-remote>
git push -u origin main
# other machines: git clone <your-remote> ~/.agentstack/lib   (or `git pull`)
```

Nothing extra to `.gitignore` — the store cache is already a sibling directory,
not inside the repo.

## Secrets stay per-machine

Server definitions travel with `${REF}` placeholders, never values. On a new
machine, set the secrets locally and let doctor tell you what's missing:

```bash
agentstack secret set <NAME>
agentstack doctor
```

## Keep it clean

- Don't commit the store cache — it bloats history and re-fetches anyway.
- The index is name-keyed and sorted, so cross-machine edits rarely conflict; if
  they do, it's an ordinary git merge of `library.toml`.
