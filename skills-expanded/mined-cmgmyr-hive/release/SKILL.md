---
name: release
description: "Cut a hive release: gate on a clean main and a green full suite, bump and tag with np, let the publish workflow ship @cmgmyr/hive, verify the registry and a fresh global install. Use when asked to release, publish, cut a version, or tag hive."
---

# Release hive

Run every step in order, from the main checkout. Stop at the first failure and say which step failed. The tag push is the point of no return. Nothing before step 5 publishes or pushes. The publish workflow (`.github/workflows/publish.yml`) fires on a `v*` tag, publishes with npm trusted publishing, and creates the GitHub release from `CHANGELOG.md`. You never publish from your machine. Steps 7 and 8 need registry access; nothing needs an npm login, because the workflow publishes.

Flags below were read from `npx np@latest --help` on np 12.1.1. Re-read them if `npx np@latest --version` prints a different major.

## 0. Preconditions

```bash
git branch --show-current            # must print main
git status --porcelain               # must print nothing
git fetch && git status -sb          # must show no ahead or behind
gh auth status                       # must be logged in
```

## 1. Machine slot

Compare `uptime` with `sysctl -n hw.ncpu`. Do not run the suite when the 1-minute load average is above the core count, or while another suite runs. Wait and check again.

## 2. Gate

```bash
mkdir -p .agents/suite-logs
npm run build && npm test > .agents/suite-logs/release-<version>.log 2>&1
grep -E '^ℹ (tests|pass|fail|skipped)' .agents/suite-logs/release-<version>.log
```

Use the step 3 version in the log name, or a date. Require `fail 0`. `test/dispatcher-worktree-pin.test.mjs` "gates under --strict" is a known machine-coupled pair. If only those two fail, record it in step 9 and continue. Any other failure stops the release.

## 3. Pick the version

```bash
git log "$(git describe --tags --abbrev=0 2>/dev/null || git rev-list --max-parents=0 HEAD)"..HEAD --oneline
```

Choose `patch`, `minor`, `major` or an explicit version such as `0.2.0`. Before 1.0, a breaking change is a `minor`.

Prerelease versions such as `1.0.0-rc.1` are not supported. The workflow publishes without `--tag`, and npm refuses a prerelease on `latest`.

## 4. Write the changelog

Write the `CHANGELOG.md` section `## <version> - <date>` and commit it before `np` runs:

```bash
git add CHANGELOG.md
git commit -m "document <version> release"
```

The changelog commit must land before the version bump, tag, and push. Write for a stranger. Include the user-visible changes and keep internal workflow details out of the section.

## 5. Bump, tag and push

```bash
npx np@latest <version> --no-tests --no-publish --no-2fa --no-release-draft --no-cleanup
```

- `--no-tests`: the gate in step 2 already ran the suite; np would rerun it.
- `--no-publish`: np does not publish; the workflow does.
- `--no-2fa`: np does not try to enable 2FA on the package, which needs a publish.
- `--no-release-draft`: np does not create a GitHub release; the publish workflow creates it from `CHANGELOG.md` after npm publish succeeds.
- `--no-cleanup`: np's cleanup runs `npm ci` in this checkout and deletes `node_modules` under the hive servers running from it.

np bumps `package.json` and the lockfile, commits, tags `v<version>`, and pushes the commit and the tag. Pushing the tag starts the workflow.

## 6. Watch the publish run

```bash
sha=$(git rev-parse HEAD)
for i in $(seq 24); do
  id=$(gh run list --workflow publish.yml --commit "$sha" --event push --json databaseId -q '.[0].databaseId')
  [ -n "$id" ] && break
  sleep 5
done
gh run watch "$id" --exit-status
```

The loop waits up to two minutes for the run to appear. If the tag check or the version check fails, the tag is wrong. Delete it, fix `package.json`, and start again from step 0:

```bash
git tag -d v<version> && git push origin :refs/tags/v<version>
```

## 7. Verify the registry

```bash
npm view @cmgmyr/hive version                 # must equal <version>
npm view @cmgmyr/hive dist.attestations       # must print attestation data (provenance)
```

## 8. Install smoke

```bash
P=$(mktemp -d); D=$(mktemp -d)
npm install -g --prefix "$P" @cmgmyr/hive@<version>
HIVE_DATA_DIR="$D" "$P/bin/hive" --version
rm -rf "$P" "$D"
```

Never run `hive setup` here without a scratch `HIVE_BIN_DIR`; it rewrites your real shim.

## 9. Verify the release

```bash
gh release view v<version> --json name,body -q .name
```

The command must print the version. If the publish workflow's release job failed because the changelog section was missing, fix `CHANGELOG.md` on main and re-run the release job for the existing tag:

```bash
gh workflow run publish.yml -f tag=v<version>
```

Read the notes on the page it prints and edit them there if needed.

## 10. Record

Write the version, the commit sha (`git rev-parse HEAD`), the publish run URL and the suite counts wherever this project keeps lane records.

## First release only

Trusted publishing is set up on npmjs.com, in the package's settings, under "Trusted publishing". Enter these values:

- Organization or user, and repository: the two halves of `cmgmyr/hive`, the same slug as this repo's GitHub URL
- Workflow filename: `publish.yml`
- Environment name: leave blank (the workflow declares none)

The npm docs list those fields, `id-token: write`, npm 11.5.1 or later and Node 22.14.0 or later as requirements. They also say provenance is generated automatically and that only cloud-hosted runners are supported. They do not say whether the package must exist before you can register a trusted publisher (https://docs.npmjs.com/trusted-publishers, read 2026-09-20). Do not assume either way.

1. Preview what would ship, from a clean checkout of main: `npm publish --access public --dry-run`.
2. Open the package's settings on npmjs.com. If the trusted publisher can be registered before the package exists, do that and run steps 0 to 9 as written. np needs a version above the one in `package.json`, so the first workflow release is a later version than today's.
3. If it cannot, publish once by hand with your 2FA: `npm version <first version> --no-git-tag-version`, commit it, then `npm publish --access public`. Register the trusted publisher. Then `git tag v<first version> && git push origin v<first version>` is safe: the workflow sees the version on the registry and publishes nothing.

For the 1.0.0 release, package.json is already 1.0.0, so write its changelog section and push the tag by hand. Do not run `np`, which would bump the package to another version.
