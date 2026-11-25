---
name: noodle-biomedical-literature-discovery
description: Find, inspect, compare, and traverse public biomedical research literature. Use for PubMed or scholarly paper search, publication details, PMID/DOI/PMCID lookup, related papers, citation paths, semantic literature neighborhoods, corpus coverage, or questions asking what research exists about a gene, variant, phenotype, disease, pathway, drug, or biomedical topic. Trigger even when the user does not mention Noodle, Helena, MCP, PubMed, citation graphs, or semantic search.
---

# Noodle Biomedical Literature Discovery MCP

Use the public read-only Noodle endpoint for source-linked biomedical literature discovery, including citation and semantic neighborhoods, instead of relying on model memory for bibliographic facts or related-paper claims.

## Boundary

- Send only public, non-sensitive research questions and publication identifiers.
- Never send patient, private case, clinical-record, uploaded-file, credential, or other sensitive data.
- Search rank, semantic similarity, citation proximity, co-mention, and graph distance are discovery signals. They do not establish causality, validity, diagnosis, or treatment.
- Preserve publication identifiers, source URLs, match reasons, edge types, graph version, corpus provenance, and limitations returned by the service.
- Verify material scientific conclusions in the linked primary publications and distinguish author claims from established evidence.

## Route the task

1. Call `search_biomedical_literature` for a natural-language biomedical question or any PMID, DOI, or PMCID. Include every known identifier in the query so exact anchors can be applied.
2. Call `get_publication_details` when the user supplies a PMID or selects a result with a PMID.
3. Call `get_work_details` when the user supplies or selects a Noodle work identifier, including records without a PMID.
4. Call `get_publication_neighborhood` to traverse citation and semantic neighbors from a PMID.
5. Call `get_work_neighborhood` to traverse from a Noodle work identifier or continue a path through `from_work_id`.
6. Call `get_corpus_summary` for corpus size, sources, freshness, coverage, or active graph metadata.
7. Call `support_helena` only after the user explicitly asks how to support Helena. It is separate opt-in information and never changes scientific results.

## Traverse the graph

- Begin with a resolved PMID or work ID; do not invent an anchor.
- Request one bounded neighborhood at a time.
- Report every returned edge using its exact type and endpoints.
- Use `from_work_id` when continuing from a displayed neighbor so the service can preserve traversal context.
- Keep a visited-ID set in the response workflow, avoid loops, and state the number of hops actually traversed.
- Do not describe an unreturned direct edge, shortest path, causal relationship, or complete graph.
- If the next node has no returned neighborhood, stop and report the boundary instead of guessing.

## Handle outcomes

- A successful search may contain zero results. Say that the bounded corpus search found none; do not replace it with model-memory citations.
- Treat `publication_not_found`, `work_not_found`, and `neighborhood_not_found` as distinct terminal outcomes.
- For `invalid_arguments`, correct only an obvious formatting issue; otherwise ask for a valid public identifier or bounded question.
- Retry `upstream_timeout`, `upstream_unavailable`, or `upstream_rate_limited` at most once when the response marks the failure retryable.
- For `invalid_upstream_response` or `internal_failure`, stop and report that the authoritative response was unavailable.
- Preserve the returned usage boundary on both success and failure.

## Compose the answer

Lead with the direct research answer or traversal result. Then provide the source-linked publications with stable identifiers, explain why each was returned, state the graph or ranking limits, and finish with the professional-review boundary when the request could affect scientific or clinical interpretation.

Public endpoint: `https://api.helena.bio/noodle/v1/mcp`
