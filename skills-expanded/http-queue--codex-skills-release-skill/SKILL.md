---
name: release
description: Publish an http-queue release using this repo's make target. Use when asked to cut, publish, or create a release, tag a semver version like 0.1.1, push multi-arch Docker images to GHCR, or create the matching GitHub release notes from the diff log.
---

# release

## When to use

Use this skill for repo releases only. The canonical path is `make release VERSION=<X.Y.Z>`.

## Preconditions

Before running the release:

1. Confirm the version is bare semver like `0.1.1`.
2. Confirm the current branch is `main`.
3. Confirm the working tree is clean. Do not include unrelated local changes in a release.
4. Confirm Docker is authenticated to GHCR.
5. Confirm `gh auth status` succeeds.

If any precondition fails, stop and report the blocker instead of working around it.

## Workflow

1. Inspect current state:
   - `git status --short`
   - `git branch --show-current`
   - `git tag --sort=-version:refname | head`
2. If the tree is clean and the user has supplied a version, run:

```bash
make release VERSION=<X.Y.Z>
```

3. Do not manually recreate the release steps unless the Makefile is broken. The Makefile already:
   - runs `go test -race ./...`
   - validates semver and branch
   - checks local and remote tag collisions
   - builds and pushes multi-arch images to `ghcr.io/mkoziy/http-queue`
   - creates and pushes the annotated git tag
   - creates the GitHub release with notes from the git diff log

## Verification

After a successful release, report:

- the released version
- the pushed image tags:
  - `ghcr.io/mkoziy/http-queue:<X.Y.Z>`
  - `ghcr.io/mkoziy/http-queue:latest`
- the git tag name
- the GitHub release URL if available from command output

## Don't

- Don't release from a dirty worktree.
- Don't bypass `make release` with hand-run git, docker, or gh commands unless fixing the release pipeline itself.
- Don't guess a version. Use the exact version the user requested.
