---
name: create-marketplace
description: "Use when the user asks to create, publish, deploy, update, or maintain a Cowork marketplace - a public GitHub repo with a .agents/plugins/marketplace.json catalog that distributes plugins and standalone skills, versioned by per-entry sourceHash fingerprints. Triggers on: 'create a marketplace', 'publish a marketplace', 'deploy a marketplace', 'set up a marketplace repo', 'add a plugin to my marketplace', 'add a skill to my marketplace', 'update marketplace hashes', 'marketplace source hash mismatch'."
metadata:
  triggers: "create marketplace, new marketplace, publish marketplace, deploy marketplace, marketplace repo, marketplace.json, marketplace catalog, add plugin to marketplace, add skill to marketplace, update marketplace hashes, source hash, sourceHash, hash mismatch"
---

# Create a marketplace

A marketplace is a public GitHub repo that distributes Cowork plugins and standalone skills. Its
catalog is a manifest at `.agents/plugins/marketplace.json` - that exact path is what Cowork
fetches from the repo's default branch. Plugins live at `plugins/<name>/` (each with a
`.cowork-plugin/plugin.json`); standalone skills live at `skills/<name>/SKILL.md`. Every entry
carries a `sourceHash` fingerprint of its directory tree; that hash is how clients verify installs
and detect updates, so keeping it current is the core maintenance duty.

## Manifest: the complete field set

The manifest is **strict** at every level - any unrecognized key fails parsing. Full rules and an
annotated example are in `references/schema.md`.

| Key | Required | Purpose |
|-----|----------|---------|
| `name` | yes | marketplace identifier (non-empty string) |
| `interface.displayName` | no | human-facing marketplace title |
| `plugins` | yes | array of entries (may be empty `[]`) |
| `skills` | no | array of entries for standalone skills |

Each entry in `plugins`/`skills` (same shape for both):

| Key | Required | Purpose |
|-----|----------|---------|
| `name` | yes | entry identifier |
| `source` | yes | `{ "source": "local", "path": "./plugins/<name>" }` - path must start with `./` and stay inside the repo |
| `policy` | yes | `{ "installation": ..., "authentication": ... }` - both non-empty strings |
| `category` | yes | catalog grouping shown in the UI (e.g. `"Productivity"`, `"Authoring"`) |
| `sourceHash` | no | `"sha256:<64 hex>"` fingerprint of the entry's directory tree - always publish it |
| `interface` | no | `displayName`, `icon`, `logo`, `brandColor` (entry-level UI metadata) |

## Process

### 1. Decide what the marketplace distributes
- **Plugins** - bundles with a `.cowork-plugin/plugin.json` manifest, optionally grouping skills,
  MCP servers, and apps. Author each with the **`create-plugin`** skill.
- **Standalone skills** - single `SKILL.md` directories. Author each with the **`create-skill`**
  skill (kebab-case directory name equal to frontmatter `name`).

### 2. Scaffold the repo layout
Create a new git repo with this structure:

```
<marketplace-repo>/
|-- .agents/
|   `-- plugins/
|       `-- marketplace.json      # the catalog Cowork fetches
|-- plugins/
|   `-- <plugin-name>/
|       `-- .cowork-plugin/plugin.json
|-- skills/
|   `-- <skill-name>/SKILL.md
`-- scripts/
    |-- update-source-hashes.mjs  # copy from this skill's scripts/
    `-- validate-marketplace.mjs  # copy from this skill's scripts/
```

Copy both scripts from this skill's `scripts/` directory into the new repo's `scripts/` - they are
standalone (no dependencies; run under `node` or `bun`) and become the repo's maintenance tooling.

### 3. Author the manifest and entries
Write `.agents/plugins/marketplace.json` with a top-level `name`, optional
`interface.displayName`, and one entry per package. Keep `source.path` relative (`./plugins/<name>`
or `./skills/<name>`). Do not fill in `sourceHash` by hand - the script computes it in the next
step. Never commit installer provenance into source roots: remove any tracked
`.cowork-skill.json`, `.cowork-plugin/install.json`, `.codex-plugin/install.json`, and
`.DS_Store` before hashing (they are excluded from the fingerprint, but they are noise).

### 4. Compute source hashes - required before every push

```bash
node scripts/update-source-hashes.mjs           # rewrite every sourceHash in place
node scripts/update-source-hashes.mjs --check   # verify; exits non-zero listing stale entries
```

Run the update, then the check, and commit the content change and the manifest hash update
**together**. Never hand-edit a `sourceHash`.

### 5. Validate - required before declaring done

```bash
node scripts/validate-marketplace.mjs
```

This applies the same strict rules the product's parser applies (schema, `./` paths inside the
repo, required `policy`/`category`, unique names), plus content checks: every plugin entry has a
`.cowork-plugin/plugin.json`, every skill entry has a `SKILL.md` whose frontmatter `name` equals
its directory name, and every `sourceHash` matches a fresh recompute. Fix every error.

### 6. Deploy: push to a public GitHub repo
Push to a **public** GitHub repository. Cowork fetches
`.agents/plugins/marketplace.json` from the default branch via the GitHub API (with a
`raw.githubusercontent.com` fallback), then fetches entry sources from the same repo/ref. There is
no separate publish step - the push is the release.

### 7. Connect it in Cowork
Users add a deployed marketplace in the Cowork desktop app under **Settings -> Tool Access ->
Marketplace -> "Add marketplace"** - paste the `owner/repo` slug or the GitHub URL. Cowork
validates the manifest before saving, so a repo that fails step 5 will be rejected here too.

## Hashing and versioning discipline

`sourceHash` is the sha256 fingerprint of an entry's directory tree, computed exactly like
Cowork's `computeSourceRootHash`: a `"cowork-source-root-v1\0"` seed, a sorted directory
traversal, `file\0<posix-path>\0<bytes>\0` framing per file, `symlink\0<path>\0<target>\0` per
symlink, ignoring `.git`, `.DS_Store`, `.cowork-skill.json`, `*.incoming-*`, `*.backup-*`, and
`.cowork-plugin/install.json` / `.codex-plugin/install.json`. The bundled
`scripts/update-source-hashes.mjs` reproduces this byte-for-byte.

Clients use the published hash two ways:

- **Install verification.** On plugin install, Cowork recomputes the hash of the fetched source
  and compares it to the manifest's `sourceHash`. A stale hash makes installation **fail** with
  `Marketplace source hash mismatch` - this has happened in production when content was pushed
  without rerunning the hash script. Treat a stale hash as a broken release.
- **Update detection.** When the published hash differs from the installed one, users see
  "Update available". The `sourceHash` **is** the version signal; a `version` field in
  `plugin.json` is for humans and changes nothing by itself.

Therefore: after **any** change to any plugin or skill directory - even one byte - rerun
`update-source-hashes.mjs` and publish the new hash in the **same push** as the content change.

## Maintaining a marketplace

For every content change (add/edit/remove a plugin or skill):

1. Edit the package with `create-plugin` / `create-skill` and validate it with that skill's
   validator.
2. Adding a package: append its entry to the manifest. Removing one: delete the entry and the
   directory together.
3. `node scripts/update-source-hashes.mjs` then `node scripts/update-source-hashes.mjs --check`.
4. `node scripts/validate-marketplace.mjs` - must PASS.
5. Commit content + manifest together; push. Installed clients see "Update available" on their
   next catalog refresh.

## Troubleshooting

- **"Marketplace source hash mismatch" on install** - the published `sourceHash` does not match
  the repo content. Rerun `update-source-hashes.mjs`, commit, push. Also check for stray files in
  the source root that differ between the repo and what GitHub serves (uncommitted changes,
  wrong branch).
- **Manifest parse errors** - the schema is strict: an unknown key anywhere, a missing
  `policy`/`category`, a `source.path` not starting with `./` (or escaping the repo root), or a
  malformed `sourceHash` all reject the whole manifest. `validate-marketplace.mjs` pinpoints the
  entry and key.
- **GitHub rate limits** - Cowork fetches unauthenticated; the GitHub API allows ~60
  requests/hour per IP before returning 403s (a raw-URL fallback softens manifest fetches). If
  adds/installs fail transiently with fetch errors, wait and retry; keep marketplaces public so
  the raw fallback works.

## Resources
- **`references/schema.md`** - the full manifest schema: every field the parser reads, path
  rules, policy conventions, and a complete annotated example.
- **`scripts/update-source-hashes.mjs`** - recompute (default) or `--check` every `sourceHash`;
  copy it into new marketplace repos.
- **`scripts/validate-marketplace.mjs`** - the full-repo validator from step 5; copy it into new
  marketplace repos.
