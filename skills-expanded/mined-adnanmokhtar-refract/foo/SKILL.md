---
name: foo
description: Scan the repo for foo and report what is wrong with it. TRIGGER — "check foo", "foo audit". ANTI-TRIGGER — not for bar, that is /bar.
kind: skill
pack: p
---

# foo

> **Hard rule:** never report a foo finding without a `<path:line>` cite.

## Premise (read first, do not deviate)

Foo is measured, never estimated. A finding with no cite is not a finding.

## When to use

When the project has a foo surface and nobody has audited it.

## Halt conditions

- No foo surface found → halt, say so, do not invent one.

## Procedure

1. Locate the foo surface.
2. Read every entry point.
3. Rank findings by blast radius.

## Output

A ranked table: `| finding | path:line | severity | fix |`.

## Failure modes

- Reporting a foo finding that is really a bar finding.
- Ranking by count instead of blast radius.

## Related

- `bar.md` — the sibling surface.
