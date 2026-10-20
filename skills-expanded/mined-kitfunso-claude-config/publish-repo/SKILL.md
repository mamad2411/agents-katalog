---
name: publish-repo
description: "Ship an npm release end to end: version bump, docs, build, test, publish, tag, push. Use when asked to ship this package."
---

# Publish Repo

End-to-end release workflow for npm packages. Handles version bump, docs, build, test, publish, push, and global install.

## Prerequisites

- Must be in a directory with `package.json`
- Must have npm publish access (already logged in)
- Git working tree should be clean or have only the changes to release

## Steps

### 0. Verify state

```bash
git branch
git status
```

Confirm you're on the correct branch (usually `master` or `main`). If not, ask before proceeding.

### 1. Determine version bump

Check the current version from `package.json`. Determine the bump type:

- If the user specifies a version (e.g., "bump to 0.12.0"), use that exactly.
- If the user says "patch", "minor", or "major", bump accordingly.
- If unspecified, infer from the changes in this session:
  - Bug fix or small improvement: **patch** (0.11.1 -> 0.11.2)
  - New feature or capability: **minor** (0.11.1 -> 0.12.0)
  - Breaking change: **major** (0.11.1 -> 1.0.0)
- Confirm the version with the user before proceeding if ambiguous.

### 2. Bump version in ALL manifests

**NEVER use `npm version`: it only bumps `package.json` and `package-lock.json`.** Always bump manually with Edit to catch every manifest.

Search for the old version string across the repo:

```bash
grep -rn '"version".*OLD_VERSION' --include='*.json' . | grep -v node_modules | grep -v package-lock
```

Typical files to bump (edit each one):
- `package.json` (root)
- Any nested `package.json` files (extensions/, plugins/)
- Any `*.plugin.json` or `openclaw.plugin.json` manifests
- MCP server version strings in source code

After bumping all manifests, run `npm install` to sync `package-lock.json` to the new version.

**Verify all manifests match** after bumping, grep again and confirm zero hits for the old version (excluding package-lock.json and node_modules).

### 3. Update CHANGELOG.md

Add a new section at the top, after the `# Changelog` heading:

```markdown
## X.Y.Z (YYYY-MM-DD)

### Fixed / Added / Changed
- **Short title.** Description of the change.
```

Use today's date. Categorize entries as Fixed, Added, or Changed. Keep descriptions concise but specific.

### 4. Update README.md (MANDATORY if pattern exists)

First, check whether the README uses the "What's new in vX.Y.Z" pattern:

```bash
grep -c "What's new in v" README.md
```

If count > 0, adding a new "What's new in vNEW" section is **required**, not optional. Insert immediately above the most recent entry. Use 2-5 bullet points that summarize user-visible behavior, not internal refactors.

**Critical: do not describe features that were reverted in this session.** If you or the user removed functionality between releases, the release notes must reflect what actually shipped, not what was prototyped. Before writing the section, scan the session history for reverts / checkouts / branch deletions; if any named feature was removed, it must not appear in release notes.

After editing, verify the section exists:

```bash
grep -n "What's new in vNEW_VERSION" README.md
```

If grep returns no match after you claim to have updated it, you did not save the file. Re-edit.

Verify the ordering is correct (newest first):

```bash
grep -n "What's new in v" README.md | head -5
```

The line numbers should ascend and versions should descend.

### 5. Update other relevant docs

Check for:
- Plugin/extension READMEs that reference the changed functionality
- Integration guides affected by the changes
- Any doc that references the old behavior

Only update docs that are actually affected. Do not touch unrelated files.

### 6. Build

```bash
npm run build
```

Must succeed before proceeding.

### 7. Test

```bash
npx vitest run
```

Or whatever the test command is (`npm test`, `npx jest`, etc.). ALL tests must pass. If a test fails due to version sync, fix it. If a test fails for other reasons, stop and report.

### 8. Commit

Stage only the changed files (not `git add -A`). Write a commit message:

```
chore: bump to vX.Y.Z, update changelog and readme

<the attribution lines the session's system reminder supplies>
```

### 9. Publish to npm

```bash
npm publish
```

Wait for confirmation. If it fails (auth, version conflict), report and stop.

### 10. Tag and push

```bash
git tag vX.Y.Z
git push origin <branch>
git push origin vX.Y.Z
```

### 11. Create GitHub Release (MANDATORY if `gh` is available and the repo has a GitHub remote)

The CHANGELOG entry is the source of truth: extract it and ship it as the release body so anyone landing on the GitHub Releases page sees the same notes that ship in the repo.

First, confirm `gh` is installed and the repo has a GitHub remote:

```bash
gh release list --limit 1 2>/dev/null && git remote -v | grep -i github
```

If neither command produces output, the repo has no GitHub remote, skip this step and note it in the final report. Otherwise:

Extract the new version's CHANGELOG section (everything between `## X.Y.Z` and the next `## ` heading):

```bash
awk '/^## X\.Y\.Z/{flag=1; next} /^## /{flag=0} flag' CHANGELOG.md > <scratchpad>/vX.Y.Z-notes.md
wc -l <scratchpad>/vX.Y.Z-notes.md
```

(`<scratchpad>` is the session scratchpad; /tmp outside Claude Code.)

If the file is empty or only a few lines, the CHANGELOG section is missing, go fix Step 3 first.

Create the release with a one-line headline title that captures the user-visible win, and the extracted CHANGELOG body:

```bash
gh release create vX.Y.Z \
  --title "vX.Y.Z: <one-line headline>" \
  --notes-file <scratchpad>/vX.Y.Z-notes.md \
  --latest
```

Use `--latest` only if this version is the newest stable. If shipping a backport / hotfix to an older line, omit `--latest` so the highest semver stays the GitHub default. Add `--prerelease` for alpha/beta/rc tags.

**Headline format:** start with the version, then a brief user-visible reason ("vX.Y.Z: fixed Y leak", "vX.Y.Z: added Z transport"). Don't paraphrase the CHANGELOG body in the title; the body has the detail.

**Verify the release landed:**

```bash
gh release view vX.Y.Z 2>&1 | head -10
```

If the previous N releases also have missing notes (common when a project skips this step for several patches), backfill all of them in the same session by running this step once per missing tag.

### 12. Install globally (if applicable)

If the package is a CLI tool (has a `bin` field in package.json):

```bash
npm install -g <package-name>@X.Y.Z
```

Verify:

```bash
<cli-command> --version
```

### 13. Close related issues/PRs

If any commits reference `Closes #N` or `Fixes #N`, verify the issues/PRs were closed. If not, close them manually with a comment.

### 14. Post-publish doc audit (MANDATORY)

After npm publish, before reporting success, verify documentation is consistent with what actually shipped:

```bash
# CHANGELOG has an entry for the new version at the top
grep -n "^## " CHANGELOG.md | head -3

# README "What's new" includes the new version (if that pattern exists)
grep -n "What's new in v" README.md | head -3

# No stale references to the previous version in manifests
grep -rn '"version".*"OLD_VERSION"' --include='*.json' . | grep -v node_modules | grep -v package-lock

# GitHub Release exists for the new version (if gh is available)
gh release view vX.Y.Z --json tagName,name,isLatest 2>&1 | head -5
```

If CHANGELOG or README missed the new version, create a follow-up docs commit IMMEDIATELY. Do not defer. The user should never have to point out missing release notes.

If `gh release view` returns "release not found", run Step 11 now. The release notes are the user-facing artifact most likely to be missed because it's the only step that lives outside the local repo; never skip it on the assumption "the tag is enough."

If release notes describe features the user rejected or reverted during the session, rewrite them before pushing the commit. Shipped software must match published description.

## Rules

- Do not amend previous commits. Always create new commits.
- Report what was published at the end: package name, version, npm URL, tag, **and GitHub Release URL**.
