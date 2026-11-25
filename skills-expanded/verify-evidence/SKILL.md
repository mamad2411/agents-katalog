---
name: verify-evidence
description: Check a claim about an AI system against supplied evidence with the agent-evidence MCP tools, or replay the conformance vectors. Use when asked whether a report, receipt or "done" claim is backed by evidence.
---

Use the `agent-evidence` MCP tools; they are offline and read-only.

1. To decide a claim, call `verify_claim` with the case, the consumer policy and the artifacts the case names. Report the `decision` and `reason` verbatim. `supported` means the pinned policy's checks passed, and the application still owns authorization.
2. To see the three decisions, call `verify_sample` with `contradicted`, `not_established` or `supported`.
3. To check a conformance claim, call `list_vector_corpora`, then `run_vectors` for a corpus, and `explain_vector` for any vector.
4. To define a term, call `lookup_term`. To check that an artifact has a digest its SBOM or attestation names, call `check_artifact_digest`.

5. To canonicalize JSON before it is signed, call `canonicalize_json`; to check a DSSE envelope against keys you trust, call `verify_dsse`. A refusal names the crate's variant; quote it.

Never state a verdict the tool did not return, and quote an error as an error.
