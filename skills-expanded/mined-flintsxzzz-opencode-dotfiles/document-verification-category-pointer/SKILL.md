---
name: document-verification-category-pointer
description: "Pointer to a library of 7 specialized Document Verification skills. Use when working on document-verification-related tasks."
risk: none
---

# Document Verification Capability Library 🎯

This is a **pointer skill**. The 7 specialized Document Verification skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **check-identity-pack** — Run an AFP 100-point or AUSTRAC safe-harbour identity check over a set of documents, and report exactly what's missing. Use when the user asks to check identity documents, verify someone's ID for onboarding, or assess whether a document pack satisfies Australian identity requirements.
- **detect-ai-text** — Estimate whether a document's prose was written by AI, with the linguistic tells and honest abstention on non-prose. Use when the user asks whether an essay, report, CV, submission, or article was AI-generated — for triage, not proof.
- **extract-document-data** — Extract structured, grounded fields from documents — values cite their page, missing values abstain instead of hallucinating. Use for parsing invoices, payslips, statements, contracts.
- **find-matching-tenders** — Find open AU/NZ government tenders matching what a company does, ranked by fit with why and gap analysis. Use when the user asks to find tenders, bid opportunities, government contracts, or RFPs for their business (or a client's).
- **screen-adverse-media** — Screen a person or organisation for adverse media coverage, PEP status, and sanctions exposure — corroboration-gated, returns "review" never "guilty". Use when the user asks to screen someone before onboarding, partnership, or investment; for AML/CTF flows; or for ongoing counterparty monitoring.
- **verify-citations** — Verify citations and references in a document, report, or article against real sources. Use when the user asks to fact-check, verify references, check citations, or validate evidence in research reports, tender responses, whitepapers, or academic writing.
- **verify-document** — Check whether a document (PDF or image) shows signs of tampering or forgery before you rely on it. Use when the user asks to verify a payslip, invoice, bank statement, ID document, contract, or any document where authenticity matters.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/document-verification/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/document-verification`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
