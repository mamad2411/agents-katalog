# Session Loop

Owns session turns, context assembly, instruction loading, observation reduction,
compaction, and conversation-local tracking. Provider translation and workflow
execution belong to their respective core boundaries and module adapters.

- Pruning preserves non-reproducible text results and errors; observation
  masking may replace them but retains action and error identity. Both preserve
  recent messages and remove the complete old result envelope, including metadata.
  Text replacement must save space.
- Compaction keeps deterministic working facts alongside model narrative and
  bounded rationale. Verify the model input and retained conversation suffix;
  a canned model answer cannot establish that prior context reached the model.
- Provider signatures stay out of summarizer requests and narrative output.
- Instruction-loader fixtures use isolated temporary trees with explicit scope
  roots. Retain the repository delivery guard through the production loader,
  including referenced documents: truncation can hide operational rules.
  Shorten or scope guidance, or expand adjacent documents in place with `@`
  references, when the guard fails; preserve rule order and authority.
- Owner tests observe context snapshots, model requests, persisted bytes and
  reduction outcomes. Shared observation helpers own envelope handling; callers
  do not export alternate names for those helpers.
