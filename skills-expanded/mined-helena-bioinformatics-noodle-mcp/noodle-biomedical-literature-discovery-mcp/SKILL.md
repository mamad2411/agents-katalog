---
name: noodle-biomedical-literature-discovery-mcp
description: Select Noodle Biomedical Literature Discovery MCP from Biorouter for public biomedical paper search, PMID DOI or PMCID lookup, publication inspection, related papers, citation or semantic graph traversal, and corpus metadata even when the user does not know the Noodle name.
license: Apache-2.0
user-invocable: false
---

# Noodle Biomedical Literature Discovery MCP

Use the hosted read-only tools for source-linked biomedical literature claims.
Route natural-language or exact-identifier search to
`search_biomedical_literature`; PMID and work records to their matching detail
tools; graph exploration to the matching neighborhood tool; and coverage or
freshness questions to `get_corpus_summary`.

Start graph traversal from a resolved PMID or work ID. Preserve returned edge
types and graph provenance, keep a visited set, and stop at a missing
neighborhood. Never infer causality from citation or semantic proximity.

Send only public non-sensitive questions and identifiers. Never send patient,
private case, clinical-record, credential, or private uploaded content. Verify
important scientific conclusions in the linked primary publications.
