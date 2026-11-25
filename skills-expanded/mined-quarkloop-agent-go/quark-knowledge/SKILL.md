# Quark Knowledge

Use this profile for document understanding, indexing, retrieval,
grounded answers, and citation-focused workflows.

Keep the agent as coordinator:

- read source files through approved tools,
- call document service functions for mechanical parsing, OCR, layout, pages,
  tables, and images when the file needs them,
- use opaque runtime media references for image-bearing Gateway embeddings;
  never inline binary source data in agent-authored payloads,
- use the runtime/model LLM path for document classification, schema inference,
  field normalization, chunk decisions, fact extraction, entity extraction,
  relation extraction, and citation selection,
- call Run State service functions to track generic batch/run progress and
  auditable references when available,
- call Gateway and indexer service functions with agent-produced chunks,
  facts, entities, relations, citations, embeddings, and provenance,
- call citation service functions to resolve spans or verify grounding when
  evidence needs mechanical verification, coverage scoring, or rendered source
  references,
- use Core service functions for audit artifacts, policy checks, approvals, and
  approval-gated workspace mutation plans when the user explicitly asks to
  reorganize or write into their directory,
- answer only from retrieved context when the user asks about indexed sources.

Do not move semantic extraction into document, Run State, citation, core, or
indexer services. Do not let one service call another service. The agent is the
coordinator.
