# productivity/file-organizer — skill payload

> Machine-readable contract: [`../file-organizer.manifest.json`](../file-organizer.manifest.json).

## What this skill does

Classifies every file in a directory tree by content type — documents,
images, code, archives, media — and proposes a target layout. Returns a
**dry-run plan** (source → destination) by default; only commits the
moves when `applyChanges: true`. The plan itself is the reversal
manifest.

## When to use it

- A Downloads folder, project workspace, or shared drive has degraded
  into chaos and needs taming.
- You want to *see* what a reorganisation would look like before
  committing.

## When **not** to use it

- The directory is under version control — let git handle structure,
  don't sprinkle moves into history.
- The files are governed (legal hold, regulatory archive) — don't move
  anything programmatically.

## Determinism and risk

Determinism: **medium** — type classification is heuristic. Risk:
**medium** — moves files when applied. Dry-run default mitigates this.

## How it composes

Leaf skill. Pairs well as a follow-up to any bulk-download workflow.
