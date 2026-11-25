---
name: goreleaser-cli-homebrew-pipeline
description: Tag-triggered GitHub Actions workflow that runs Go tests, uses GoReleaser to build multi-platform CLI binaries, then publishes to GitHub Releases and a Homebrew tap.
category: devops
version: 1.0.0
tags: [go, goreleaser, homebrew, cli, github-actions, release]
source_type: extracted-from-git
source_url: https://github.com/multica-ai/multica.git
source_ref: main
source_commit: 6cd49e132de7632b1f2aaa675c98e8eca9308bb7
source_project: multica
imported_at: 2026-04-18T00:00:00Z
version_origin: extracted
confidence: medium
---

## When to use

- You ship a Go CLI and want `brew install org/tap/cli` as the one-line install path.
- Releases should be cut from semver tags on `main`.

## Steps

1. Create a semver tag on `main` for every release:
   ```bash
   git tag v0.1.13
   git push origin v0.1.13
   ```
2. `.github/workflows/release.yml` triggers on tag push, runs tests, then invokes GoReleaser:
   ```yaml
   on: { push: { tags: ["v*"] } }
   jobs:
     release:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
           with: { fetch-depth: 0 }
         - uses: actions/setup-go@v5
           with: { go-version: '1.26' }
         - run: cd server && go test ./...
         - uses: goreleaser/goreleaser-action@v6
           with:
             version: latest
             args: release --clean
             workdir: server
           env:
             GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
             HOMEBREW_TAP_GITHUB_TOKEN: ${{ secrets.HOMEBREW_TAP_GITHUB_TOKEN }}
   ```
3. `.goreleaser.yml` defines per-platform builds + archives + the tap target:
   ```yaml
   builds:
     - id: cli
       main: ./cmd/mycli
       ldflags:
         - -s -w
         - -X main.version={{.Version}}
         - -X main.commit={{.ShortCommit}}
         - -X main.date={{.Date}}
       goos: [linux, darwin, windows]
       goarch: [amd64, arm64]
       env: [CGO_ENABLED=0]
   archives:
     - formats: [tar.gz]
       format_overrides:
         - goos: windows
           formats: [zip]
   brews:
     - repository:
         owner: org
         name: homebrew-tap
         token: "{{ .Env.HOMEBREW_TAP_GITHUB_TOKEN }}"
       commit_author:
         name: goreleaserbot
   ```
4. Document the release cadence rule: by default bump patch (`v0.1.12 → v0.1.13`) unless user asks for minor/major.

## Example

```bash
git tag v0.1.14
git push origin v0.1.14
# → Actions runs tests
# → GoReleaser produces darwin/linux/windows × amd64/arm64 archives
# → Publishes to GitHub Releases
# → Updates homebrew-tap/Formula/mycli.rb with new version + SHAs
# → Users can now: brew upgrade org/tap/mycli
```

## Caveats

- `HOMEBREW_TAP_GITHUB_TOKEN` must be a PAT with `contents:write` on the tap repo (not the default `GITHUB_TOKEN`).
- The Homebrew formula needs `sha256` for each archive; GoReleaser computes them automatically.
- Don't cut a release from a worktree with a dirty working tree — GoReleaser refuses by default.
