# Version Sync Skill

Detect and synchronize Node.js version specifications across project files.

## Trigger Phrases

- "version mismatch"
- "upgrade node"
- "sync versions"
- "update node version"
- "version drift"
- "check node versions"
- "node version conflict"

## Commands

### Check Version Status

```bash
npx tsx scripts/index.ts check
```

Scans the current project for Node.js version specifications and reports any mismatches.

### Update All Versions

```bash
npx tsx scripts/index.ts update <version>
```

Updates all version files to the specified target version.

**Options:**
- `--dry-run` - Preview changes without modifying files

## Supported Files

| File | Pattern | Example |
|------|---------|---------|
| `.nvmrc` | First line number | `22` |
| `package.json` | `engines.node` | `">=22.0.0"` |
| `Dockerfile` | `FROM node:<version>` | `FROM node:22-slim` |
| `.github/workflows/*.yml` | `node-version` or `NODE_VERSION` | `node-version: '22'` |
| `docker-compose.yml` | `image: node:<version>` | `image: node:22-alpine` |

## Best Practices

1. Always run `check` first to understand current state
2. Use `--dry-run` before applying updates
3. Commit version changes separately for clear git history
4. Test after updating to ensure compatibility
