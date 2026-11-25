---
name: clinical-evidence-search
description: "Use OpenEvidence for clinical questions: queries, citations, drug interactions, and guideline lookups. Always cite sources and flag the educational-only caveat."
---

# Clinical evidence search

- Use **`open_evidence_search`** for clinical / drug / guideline questions. Set `evidenceLevel` to `meta-analysis` or `rct` when the user wants the strongest signal; use `any` only for broad scoping.
- Use **`open_evidence_get_citation`** to resolve any citation id before quoting a specific claim — never paraphrase a study you have not opened.
- Use **`open_evidence_drug_interactions`** for medication interaction checks (≥ 2 drugs). Report each pair with severity and the OpenEvidence citation behind it; do not collapse the list into a one-line yes/no.
- Use **`open_evidence_guideline_lookup`** to find society guidelines (ACC/AHA, ESC, NICE, USPSTF, …); pass the issuing body in `society` when the user asked for one specifically.
- **OpenEvidence is US-only and not available in the EU/UK.** If the user's locale is European, fall back to `academic_search` (PubMed) and label the limitation explicitly.
- **Educational use only.** Every reply that includes clinical content must end with: *Not medical advice; verify against your local guidelines and a qualified clinician.* Surface citations inline (journal, year, evidence level, DOI / PubMed id).
- For non-clinical research (math, CS, etc.) prefer **`academic_search`** — it is free, broader, and not subject to OpenEvidence's TOS.
