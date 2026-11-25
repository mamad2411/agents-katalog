---
name: academic-citation
description: Verify, format, and insert scholarly citations with OmniScholar. Use for APA, IEEE, GB/T 7714 and other styles, citation-network evidence, bibliography generation, candidate discovery, or verified citation insertion.
license: MIT
---

# Academic citation

Follow the user's language and requested citation style. Never invent references, identifiers, pages, or evidence.

## Keep retrieval and formatting separate

1. Determine whether the user needs evidence discovery, identity verification, formatting, a bibliography, or insertion into prose.
2. Retrieve and verify sources with `literature_search`, `literature_get`, and when relevant `literature_graph`. A retrieved candidate is not yet proof that it supports a claim.
3. Use `ai4scholar_citation_candidates` only as a paid candidate-retrieval workflow. Review relevance and stable identifiers before selecting anything.
4. Use `ai4scholar_cite` only for a known Google Scholar result ID returned by the provider contract. Do not guess an ID from a title, cluster, URL, or citation text.
5. Verify author order, title, venue, year, volume, issue, pages, DOI, and style punctuation against source evidence.
6. Separate verified references from candidates requiring manual confirmation.
7. Preserve the user's wording and evidence strength; citation insertion must not strengthen the claim.

If citation formatting is unavailable or the provider returns no contractual result ID, format locally only from verified metadata and label fields that remain incomplete. If no verification provider is configured, ask for a DOI/PMID/arXiv ID or use a read-only Zotero record; never turn an unverified title into a formal citation.
