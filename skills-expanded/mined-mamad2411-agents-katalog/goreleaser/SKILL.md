---
name: goreleaser
description: >
  Configure and use GoReleaser for release automation. Use this skill when
  creating or editing .goreleaser.yaml files, setting up release pipelines,
  building cross-platform binaries, publishing to package managers (Homebrew,
  Scoop, AUR, nFPM packages), creating Docker images, or automating changelog
  generation. Supports Go, Rust, Zig, TypeScript (Bun/Deno), and Python
  (PyInstaller/UV/Poetry) projects. Also use when asked about releasing
  software, creating GitHub releases, or automating binary distribution.
version: 1.0.0
---

# GoReleaser Skill

GoReleaser automates the release process for software projects. It builds binaries, creates archives, publishes to package managers, builds Docker images, and generates changelogs.

## Quick Reference

| Task | Reference File |
|------|----------------|
| Build configuration | `references/builds.md` |
| Archives (tar.gz, zip) | `references/archives.md` |
| Docker images | `references/docker.md` |
| Linux packages (deb/rpm) | `references/nfpm.md` |
| Homebrew/Scoop/AUR | `references/homebrew.md` |
| Signing & notarization | `references/signing.md` |
| Changelog generation | `references/changelog.md` |
| CI/CD integration | `references/ci.md` |
| Template variables | `references/templates.md` |
| Complete examples | `references/examples.md` |

## Essential Commands

```bash
# Initialize new config
goreleaser init

# Validate configuration
goreleaser check

# Test build locally (no publish)
goreleaser release --snapshot --clean

# Create release (usually run in CI)
goreleaser release
```

## Configuration File

GoReleaser uses `.goreleaser.yaml` (or `.goreleaser.yml`). Enable schema validation:

```yaml
# yaml-language-server: $schema=https://goreleaser.com/static/schema.json
version: 2

# Project name (defaults to directory name)
project_name: myapp
```

## Minimal Go Configuration

```yaml
# yaml-language-server: $schema=https://goreleaser.com/static/schema.json
version: 2

builds:
  - main: ./cmd/myapp
    binary: myapp
    goos: [linux, darwin, windows]
    goarch: [amd64, arm64]
    ldflags:
      - -s -w
      - -X main.version={{.Version}}

archives:
  - formats: [tar.gz]
    format_overrides:
      - goos: windows
        formats: [zip]

changelog:
  sort: asc
  filters:
    exclude:
      - "^docs:"
      - "^test:"
```

## Build Targets

### Go (default)
```yaml
builds:
  - builder: go  # optional, default
    main: ./cmd/app
    goos: [linux, darwin, windows]
    goarch: [amd64, arm64]
    goarm: ["6", "7"]  # for ARM builds
```

### Rust
```yaml
builds:
  - builder: rust
    targets:
      - x86_64-unknown-linux-gnu
      - x86_64-apple-darwin
      - aarch64-apple-darwin
```

### Zig
```yaml
builds:
  - builder: zig
    targets:
      - x86_64-linux-gnu
      - x86_64-macos
      - aarch64-macos
```

### Prebuilt Binaries
```yaml
builds:
  - builder: prebuilt
    prebuilt:
      path: dist/myapp_{{ .Os }}_{{ .Arch }}/myapp{{ .Ext }}
```

## Common Patterns

### Version Injection (Go)
```yaml
builds:
  - ldflags:
      - -X main.version={{.Version}}
      - -X main.commit={{.Commit}}
      - -X main.date={{.Date}}
```

### CGO Disabled
```yaml
builds:
  - env:
      - CGO_ENABLED=0
```

### Multiple Binaries
```yaml
builds:
  - id: cli
    main: ./cmd/cli
    binary: myapp
  - id: server
    main: ./cmd/server
    binary: myapp-server
```

## Publishing

### Homebrew Tap
```yaml
brews:
  - repository:
      owner: myorg
      name: homebrew-tap
    homepage: https://example.com
    description: "My application"
```

### Docker Images
```yaml
dockers_v2:
  - dockerfile: Dockerfile
    images:
      - "ghcr.io/myorg/myapp:{{ .Tag }}"
      - "ghcr.io/myorg/myapp:latest"
```

### GitHub Release
```yaml
release:
  github:
    owner: myorg
    name: myrepo
  draft: false
  prerelease: auto
```

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `GITHUB_TOKEN` | GitHub API access |
| `GITLAB_TOKEN` | GitLab API access |
| `GITEA_TOKEN` | Gitea API access |
| `GORELEASER_KEY` | Pro license key |

## Workflow

1. **Initialize**: `goreleaser init` creates `.goreleaser.yaml`
2. **Configure**: Edit config for your needs (see reference files)
3. **Validate**: `goreleaser check` verifies configuration
4. **Test**: `goreleaser release --snapshot --clean` tests locally
5. **Release**: Tag and push, CI runs `goreleaser release`

## When to Load References

- **Setting up builds**: Load `references/builds.md` for complete build options
- **Configuring Docker**: Load `references/docker.md` for multi-arch images
- **Linux packages**: Load `references/nfpm.md` for deb/rpm/apk packages
- **Package managers**: Load `references/homebrew.md` for Homebrew/Scoop/AUR/etc.
- **CI setup**: Load `references/ci.md` for GitHub Actions/GitLab CI
- **Template syntax**: Load `references/templates.md` for available variables
- **Complete examples**: Load `references/examples.md` for copy-paste configs
