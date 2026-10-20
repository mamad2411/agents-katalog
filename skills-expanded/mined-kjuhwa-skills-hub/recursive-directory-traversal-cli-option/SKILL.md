---
name: recursive-directory-traversal-cli-option
description: CLI --recursive (-r) flag walks directory trees, batches files for inference, and handles symlink loops + permission errors gracefully.
category: cli
version: 1.0.0
version_origin: extracted
confidence: medium
tags: [magika, cli]
source_type: extracted-from-git
source_url: https://github.com/google/magika.git
source_ref: main
source_commit: 0a8cb9626bbf76c2194117d9830b23e9052a1548
source_project: magika
imported_at: 2026-04-18T00:00:00Z
---

# Recursive Directory Traversal Cli Option

**Trigger:** Scanning entire directory trees from a CLI without forcing users to pipe `find` output through xargs.

## Steps

- Add --recursive / -r flag and treat input args as either files or directory roots.
- Walk directories with std::fs::read_dir / walkdir / tokio::fs::read_dir; collect paths.
- Skip symlinks by default; add --follow-symlinks for opt-in dereferencing.
- Track visited (dev, inode) pairs (file_id on Windows) to break symlink cycles.
- Handle permission-denied per file (warn, continue); don't abort the whole run.
- Sort or stream results predictably so output is reproducible.

## Counter / Caveats

- Walking huge trees can be slow; parallelize directory I/O and inference.
- Symlink cycles are real; the visited-inode check is non-negotiable on *nix.
- node_modules / .git / target should usually be excluded by default — or at least documented.
- Parallel scanning produces non-deterministic output; sort if reproducibility matters.

## Source

Extracted from `magika` (https://github.com/google/magika.git @ main).

Files of interest:
- `rust/cli/src/main.rs:44-45`
- `python/src/magika/cli/magika_client.py:65-68`
- `go/cli/cli.go`
