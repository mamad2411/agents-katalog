---
name: release
description: Prepare and publish a ccxray release — bump version, update CHANGELOG, commit, tag, push, and npm publish.
license: MIT
metadata:
  author: ccxray
  version: "1.0"
---

# Release

Publish a new version of ccxray to npm.

**Input**: Optionally specify a version bump: `patch`, `minor` (default), `major`, or an exact version like `1.6.0`.

---

## Workflow

### 1. Determine version

Read current version from `package.json`. Apply the requested bump (default: `minor`):

```bash
node -e "const v=require('./package.json').version; const [a,b,c]=v.split('.').map(Number); console.log(a+'.'+( b+1)+'.0');"
```

Semver guide:
- **patch** — bug fixes only, no new features
- **minor** — new features, backwards-compatible (default)
- **major** — breaking changes

### 2. Collect changes since last tag

```bash
git describe --tags --abbrev=0
git log <last-tag>..HEAD --oneline --no-merges
```

Keep only user-visible changes (`feat:`, `fix:`). Exclude `chore:`, `ci:`, `docs:`, `test:`, and version bump commits.

### 3. Draft CHANGELOG entry

Format (match existing style in `CHANGELOG.md`):

```markdown
## X.Y.Z

### Added
- **Feature name**: one-line description

### Fixed
- **Bug name**: one-line description
```

**⚠ STOP HERE. Show the proposed version and CHANGELOG draft to the user. Wait for confirmation before making any changes.**

### 4. Update files

After user confirms:

**`CHANGELOG.md`** — insert new section at the top (after `# Changelog`):

```
## X.Y.Z
...
```

**`package.json`** — update `version` field.

### 5. Run tests

```bash
npm test
```

Stop and report if any tests fail.

### 6. Commit and tag

```bash
git add CHANGELOG.md package.json
git commit -m "X.Y.Z"
git tag vX.Y.Z
```

### 7. Push

```bash
git push origin main
git push origin vX.Y.Z
```

### 8. Publish to npm

**⚠ STOP HERE. Confirm with user before publishing — npm publish is irreversible.**

```bash
npm publish
```

Verify output contains `+ ccxray@X.Y.Z`.

---

## Output on success

```
## Released: ccxray@X.Y.Z

✓ CHANGELOG.md updated
✓ package.json bumped to X.Y.Z
✓ Tests passed (N pass)
✓ Committed and tagged vX.Y.Z
✓ Pushed to origin
✓ Published to npm
```
