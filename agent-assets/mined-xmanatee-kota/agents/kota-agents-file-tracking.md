# File Tracking

This directory contains kernel infrastructure for tracking file modifications
and watching filesystem changes.

- `file-tracker.ts` records read/write timestamps to detect stale reads.
- `file-watcher.ts` manages active filesystem watchers with debouncing.
- `file-watcher-core.ts` provides low-level watcher primitives and types.

These are shared kernel utilities used by core/tools, core/workflow, and
modules that perform file operations. They are not module-owned.
