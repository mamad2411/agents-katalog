---
name: docker-find-chmod-fast-readability
description: In a Dockerfile RUN layer, use find -not -perm to touch ONLY files missing a permission bit instead of chmod -R — cuts image build time from minutes to seconds on big node_modules trees.
category: build
version: 1.0.0
version_origin: extracted
tags: [docker, chmod, performance, node_modules]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/lukilabs/craft-agents-oss.git
source_ref: main
source_commit: 61f7d48a5b4fd0a8094f002c9e3aea5f3824dcfb
source_project: craft-agents-oss
source_path: Dockerfile.server
imported_at: 2026-04-18T00:00:00Z
---

# chmod smart in Docker (find -not -perm)

## When to use
- You want world-readable app files inside a container so `docker run --user $(id -u):$(id -g)` works for arbitrary host users.
- Your `/app` has hundreds of thousands of files (node_modules - looking at you).
- `chmod -R o+r /app` takes minutes and explodes the layer size.

## How it works
`chmod -R` walks every inode and writes the new mode unconditionally. `find -not -perm` only invokes chmod on files that actually need it:

```dockerfile
RUN find /app -not -perm -o=r -exec chmod o+r {} + && \
    find /app -type d -not -perm -o=x -exec chmod o+x {} +
```

- `-o=r` / `-o=x` = "other has read/execute". `-not -perm -o=r` = "other is missing read".
- `-exec chmod o+r {} +` = batch up arguments (like xargs), one chmod per batch instead of per file.
- Directory pass is separate because you want `o+x` (traversability) not `o+r` on dirs if you're being precise.

## Example
Slow:
```dockerfile
RUN chmod -R o+r /app  # ~3 minutes on 300k files
```

Fast:
```dockerfile
RUN find /app -not -perm -o=r -exec chmod o+r {} + && \
    find /app -type d -not -perm -o=x -exec chmod o+x {} +
# ~15 seconds, and the layer is tiny because most files didn't actually change
```

## Gotchas
- Layer size: `chmod -R` rewrites every file even if mode didn't change, bloating the diff layer. The `find` approach writes only deltas.
- Don't forget BOTH passes - if you only o+r, dirs without o+x make files unreachable.
- `-exec {} +` > `-exec {} \;` by 10-100x because it batches.
- Symlinks: by default `chmod` follows, `find` doesn't; add `-L` if symlink targets matter.
- This trick is especially valuable for images that wrap Node/Bun monorepos.
