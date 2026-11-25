---
name: mongodb-datetrunc-binsize-zero-guard
description: Guard MongoDB $dateTrunc binSize against 0 when your interval may be auto/unset; coerce to 1 to avoid runtime error
category: backend
version: 1.0.0
source:
  kind: project
  ref: lucida-performance@3ad4cf9
trigger: Building a MongoDB aggregation with `$dateTrunc` whose `binSize` comes from a user-supplied interval mode
tags: [mongodb, aggregation, dateTrunc, pitfall]
linked_knowledge: [binsize-zero-fallback-to-one]
---

# mongodb-datetrunc-binsize-zero-guard

## Rule
`$dateTrunc.binSize` must be `>= 1`. If your interval resolver returns `0` (e.g. "auto"
mode that is resolved later), **coerce to 1 at construction time**, never ship `0` to
MongoDB.

## Pattern
```java
int binSize = (interval == 0) ? 1 : interval;
Document dateTrunc = new Document("$dateTrunc", new Document()
    .append("date", "$timestamp")
    .append("unit", unit)
    .append("binSize", binSize));
```

## Why
MongoDB driver rejects `binSize: 0` with a runtime error that surfaces only when the
aggregation executes — so it slips past unit tests using stubbed intervals. Found in
production via SonarQube/Jenkins build (commit `3ad4cf9`).

## How to apply
Whenever you have a chain `userMode → intervalResolver → $dateTrunc`, add the guard at
the repository/query-builder boundary, not in the resolver (resolver's "auto=0" may be
meaningful elsewhere).
