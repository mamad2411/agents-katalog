# Repository guardrails for coding agents

This project processes potentially identifying human genomic data. Automated contributors
must preserve the following boundaries:

1. Never add patient data, genomic run files, credentials, direct identifiers or reports to
   Git. Use synthetic fixtures only.
2. Treat every ISCN string as an expert-reviewable proposal. Do not remove the research-use
   warning or introduce automatic clinical release.
3. Keep assay-specific QC and reportability rules versioned. A caller default is not a
   validated clinical threshold.
4. Any change that can alter biological output needs tests, provenance fields, a changelog
   entry and validation-impact review.
5. Prefer typed adapters and structured contracts over parsing presentation files.
6. Run `make safety`, `make versions`, `make lint`, and `make test` before proposing a change.
7. Do not add a public license, public deployment, cloud upload or external data transfer
   without explicit owner and institutional approval.
8. Before acquiring external data files, check the exact source, access/use conditions and
   technical risks using primary evidence. Distinguish metadata checks from inspection of
   actual file contents, state unresolved risks, and never equate public availability with
   anonymity, malware-free contents or biological validity. This check does not introduce
   an additional approval requirement beyond the existing project rules.

The source of truth for scope and limitations is `docs/ARCHITECTURE.md`,
`docs/EVIDENCE_BASE.md`, and `docs/CLINICAL_VALIDATION.md`. The thesis traceability file is
historical context only and must not be treated as a technical specification.
