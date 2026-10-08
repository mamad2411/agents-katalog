---
name: orphan-etalon-fixture
description: Negative fixture — one references/ etalon is correctly pointed at, but a sibling etalon in the same directory is never named and is dead weight.
---

# orphan-etalon fixture

Read `references/pointed.md` and reproduce it — it holds the complete file for
the shared widget helper.

`references/unpointed.md` sits in the same directory but is never named above:
no paragraph in this body sends the reader to it. `check_orphan_etalon` flags
that file as dead weight — authored, structurally valid, but unreachable from
the skill body, so it can drift silently and never actually gets copied.

## Core rules

- [invariant · desired] The shared widget helper is a single exported function.

Filler prose so the stub detector does not fire on this fixture instead of the
one under test.
