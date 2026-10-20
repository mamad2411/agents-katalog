# Autonomy Health Reviewer

This workflow consumes typed `autonomy.health.signal` events and converts
concrete failures or repeated health patterns into bounded follow-up actions.

- Keep this workflow deterministic and code-only in v1.
- Do not expose raw prompts, tool payloads, secrets, or cost ranking context
  through review artifacts, attention digests, or improver inputs.
- A single warning remains review evidence; it does not become a durable issue.
  Admit an error/critical outcome immediately, a warning after repeated
  observation, or any later update/clear for an existing durable issue.
  Module recoveries retain an operation-specific recovery boundary even before
  failure backfill arrives; informational clears must reach this owner too.
  Retaining that history requests no investigation.
  Later failures after operation recovery are admitted immediately, including
  recovery evidence carried in the same review batch.
  Module observation times come from the occurrence, never the audit or review;
  cited occurrence facts reconcile older audit-stamped history without deleting it.
  Legacy clear timestamps record review delivery, not operation success; only
  attributed recovery evidence establishes the boundary for later failures.
  Absent or partial attribution keeps unmatched failure references unresolved;
  aggregate operation labels cannot establish which operations failed. Operation
  recovery cannot clear unmatched references or another operation's failure. Generated tasks and question links retire
  only when the complete review batch resolves the issue.
- The improver owns the AI disposition and the shared generated-work
  materializer owns any resulting task or owner question. No disposition is
  required to create work.
- An explicit source clear resolves the stable generated-work proposal without
  another AI decision. Successful finalization reduces retained observations
  against the freshest canonical issue state and stages decision and attention
  events with that transition. Task retirement events remain in the same run
  transaction. Task retirement remains a separate repository writer. Successful
  finalization applies pending question dismissals from the retained review
  artifact and stages their notification events. A question revision changed
  after review or a terminal owner response is preserved; crash replay recognizes
  matching completed dismissals without rewriting question history.
- Coalesce unstarted batches by incident identity and scope, retaining each
  attributed observation and its chronology. Prepare full reviews in the shared
  blocking worker and hand off artifacts; finalization still owns the fresh-state
  reduction. Avoid hardcoded workflow-name allowlists.
- Treat health signals as explicit `present` / `changed` / `cleared`
  observations. The durable autonomy-issue projection owns current lifecycle
  and cross-source links; absence from a batch or bounded audit never clears an
  issue or dismisses its owner question.
