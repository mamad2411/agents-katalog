# Progress Review Helpers

This directory holds the progress-reviewer's implementation helpers.

- Keep `../progress-review.ts` as the public export surface.
- Evidence collectors should stay grouped by source: runs, tasks, events,
  artifacts, git, and operator queues.
- Canonical owner-decision evidence uses the scoped core repository. Evidence
  projections observe decisions and never authorize owner actions.
- Quarantined historical run metadata is excluded with its run identity and
  diagnostic in the review packet. Use the shared metadata enumerator to
  preserve historical normalization and fail closed on invalid runtime authority;
  keep direct metadata lookup strict.
- Action writer helpers belong in `action-writers.ts`; `actions.ts` should
  orchestrate applying reviewed actions without mixing in evidence collection.
