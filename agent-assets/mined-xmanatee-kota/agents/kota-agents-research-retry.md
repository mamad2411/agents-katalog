# Research Retry

`research-source-collection` owns source calls in a repository-free run;
`research-retry` owns the task-scoped writer and semantic review. The runtime
persists collection output and the child handoff, journals browser effects, and
owns child deduplication, recovery and publication. Keep candidate selection
stable during recovery. Checkpoint HTTP readings before browser collection; bind
durable browser effects to the source URL and tool so fallback branches cannot
shift their identities.

- Only the collector listens to blocked-research availability. It reads canonical
  published task intent, never editor drafts; the writer validates that same
  contract before editing and against published intent after reconciliation.
  A stale handoff completes without mutation; the invariant
  permits that completion only if the writer has no changes relative to canonical.
  Neither phase selects another task during recovery.
- Browser tools keep their destructive network declarations. Automatic collection
  requires scope policy to allow the actual tool. Denied and confirmation-required
  authority stay parked, with distinct source-authority diagnostics; operators
  resolve authority through the existing scope controls. Do not enqueue approvals
  repeatedly from availability events. Live tool execution rechecks authority.
- Browser profile persistence must be disabled. Missing package/profile capability
  stays distinct from denied authority and a called source that remains inaccessible.
  Public HTTP reads do not require a browser profile.
- Sources cross the ordinary tool middleware and untrusted-output boundaries.
  Handoffs carry bounded, redacted text and source provenance, never credentials or
  mutable browser sessions. The research agent and reviewer consume the same evidence.
- Retry markers describe actual per-source calls. Unchanged access waits 24 hours;
  refreshed browser profile metadata permits an immediate browser retry without
  refreshing unrelated HTTP attempts. Task and inbox edits publish through the
  existing task integration policy.
- An unsuccessful child leaves collected results with their original run. Resume
  that lineage through runtime recovery; do not launch a replacement collection.
