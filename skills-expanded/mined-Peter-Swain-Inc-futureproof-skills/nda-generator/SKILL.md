---
name: nda-generator
description: |
  Drafts tailored unilateral or mutual Non-Disclosure Agreements from
  scratch with jurisdiction-specific carve-outs, DTSA whistleblower
  notice, and a clause strength scorecard plus drafting notes memo. Use
  when a user says "draft me an NDA", "I need a mutual NDA for a vendor
  pitch", "write a confidentiality agreement for an acquisition
  discussion", or "generate an NDA before sharing our roadmap". For
  generating new NDAs, not reviewing inbound ones — route counterparty
  NDA review to contract-review-assistant. Drafting aid only, not legal
  advice.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="nda-generator")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — including previously used entity names, preferred governing law jurisdictions, standard confidentiality periods, and any recurring carve-outs or special clauses the user has established in prior sessions.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- **Parties**: Full legal names of the Disclosing Party and Receiving Party (or both, if mutual)
- **NDA type**: Unilateral (one-way) or Mutual (bilateral)?
- **Purpose**: What is the permitted use of confidential information? (e.g., evaluating a potential acquisition, vendor integration, joint venture exploration, employment onboarding)
- **Jurisdiction**: Governing law and venue for disputes (e.g., State of Delaware, England & Wales)
- **Confidentiality period**: Duration of non-disclosure obligations (e.g., 2 years, 5 years, perpetual for trade secrets)
- **Specific carve-outs or additions**: Any custom exclusions, permitted disclosures, non-solicitation clauses, or residuals provisions required?
- **Recipient format**: Word document outline, Markdown, or structured clause-by-clause output?

If the user's FutureProof context contains previously saved entity details, governing law preferences, or standard clause libraries, surface these as defaults and confirm before proceeding.

## Step 3: Do the Work

Draft the NDA by systematically addressing each structural element against a rigorous legal drafting standard:

### 3.1 Recitals & Definitions

- Draft recitals establishing the business context and relationship between the parties
- Define **Confidential Information** with specificity — include affirmative inclusions (technical data, business plans, financial information, customer lists, ICA profiles, product roadmaps, source code, algorithms) and standard exclusions:
  1. Information already in the public domain (not through breach)
  2. Information independently developed without reference to disclosed materials
  3. Information lawfully received from a third party without restriction
  4. Information already known to the Receiving Party prior to disclosure
  5. Information required to be disclosed by law, regulation, or court order (with notice obligations)

### 3.2 Obligations of Receiving Party

- **Standard of care**: at least the same degree of care used to protect own confidential information, but no less than reasonable care
- **Permitted disclosure**: limit to directors, officers, employees, advisors, and agents with a need to know, bound by equivalent confidentiality obligations
- **No reverse engineering**: prohibition on decompilation, disassembly, or derivation of trade secrets
- **Return/destruction**: obligation to return or certify destruction of all materials upon termination or written request

### 3.3 Term & Survival

- Specify agreement effective date, term of the permitted disclosure period, and survival period for confidentiality obligations post-termination
- Address perpetual protection for trade secrets where jurisdiction supports it

### 3.4 Remedies & Enforcement

- Acknowledge that monetary damages may be inadequate and that the Disclosing Party is entitled to seek injunctive and equitable relief without bond
- Include prevailing party attorney's fees provision where commercially appropriate and jurisdictionally enforceable

### 3.5 General Provisions

- **Governing law & jurisdiction**: per user-specified jurisdiction with exclusive venue selection
- **Assignment**: non-assignable without prior written consent (with or without carve-out for affiliates/successors)
- **Entire agreement & amendment**: standard integration clause; amendments in writing only
- **Severability**: if any provision is held unenforceable, remainder continues in full force
- **Counterparts & electronic signatures**: permit execution in counterparts and via electronic signature where applicable
- **No licence or implied rights**: clarify that no IP licence is granted by disclosure
- **Non-solicitation / non-circumvention**: include only if user requests — draft with enforceable scope limitations (time, geography, activity)

### 3.6 Jurisdiction-Specific Compliance Check

Cross-reference drafted provisions against jurisdiction-specific enforceability considerations:
- **US (state-specific)**: Confirm non-compete/non-solicitation enforceability (e.g., California's restrictions under Business & Professions Code §16600), ensure DTSA (Defend Trade Secrets Act) whistleblower immunity notice is included per 18 U.S.C. § 1833(b)
- **UK**: Confirm compliance with common law confidentiality principles; assess reasonableness of restrictive covenants
- **EU**: Address GDPR implications if Confidential Information includes personal data; include data processing acknowledgement where relevant
- **Other jurisdictions**: Flag any jurisdiction-specific requirements or limitations identified in FutureProof research context

Apply any user-specific `instructions` from FutureProof context — such as preferred clause ordering, tone (aggressive vs. balanced), or mandatory internal compliance language — to customise the draft.

## Step 4: Deliver Output

Produce the following structured deliverables:

### Deliverable 1: NDA Draft Document

Full clause-by-clause NDA in the user's requested format, with:
- Signature blocks for all parties (including title, date, and entity capacity lines)
- Bracketed placeholders `[___]` for any details not yet confirmed
- Clause numbering consistent with professional legal document standards

### Deliverable 2: Drafting Notes Memo

A companion memo (addressed to the user / internal legal team) covering:
- **Jurisdiction risk flags**: any provisions with enforceability uncertainty in the selected jurisdiction
- **Negotiation leverage points**: 3–5 clauses the counterparty is most likely to push back on, with recommended fallback positions
- **Missing information checklist**: any factual inputs still needed to finalise the agreement
- **Deviation log**: where the draft departs from the user's previously saved preferences (if any) and the rationale

### Deliverable 3: Clause Strength Scorecard

| Clause | Strength (1–10) | Risk Level | Notes |
|---|---|---|---|
| Definition of Confidential Information | — | — | — |
| Standard of Care | — | — | — |
| Permitted Disclosures / Exclusions | — | — | — |
| Term & Survival | — | — | — |
| Remedies & Injunctive Relief | — | — | — |
| Return / Destruction | — | — | — |
| Governing Law & Venue | — | — | — |
| Non-Solicitation (if included) | — | — | — |

**Disclaimer**: This NDA is generated as a drafting aid and does not constitute legal advice. The user should have the document reviewed by qualified legal counsel in the applicable jurisdiction before execution.

### Confirm, Deliver as Document, Amend, Distribute

> **Output is a document — never a chat stream.** Follow this sequence:
>
> 1. **Confirm** — before producing output, tell the user what you've prepared and ask for the go-ahead
> 2. **Produce as a document** — not inline in the chat; a structured, self-contained artifact
> 3. **Offer amends** — "Any changes before we send it somewhere?"
> 4. **Distribute via connector** — check `context.connectors` from Step 1; offer the most applicable service (scheduling tool → document store → Slack/Teams → email). If nothing connected, ask the user where they want it.


## Step 5: Propose Experiments

> **Always call save_experiment — never skip.** If no explicit test emerged, create
> a lightweight hypothesis based on the most uncertain choice made this session
> (e.g. format selected, tone chosen, angle taken). That choice is worth testing.


```
FutureProof:save_experiment(skill="nda-generator", experiment={
  hypothesis: "Including a structured Drafting Notes Memo alongside the NDA reduces counterparty redline cycles by shortening internal review time",
  variants: ["control: NDA draft only", "variant: NDA draft + Drafting Notes Memo with negotiation leverage points"],
  measurement: "Number of redline iterations before execution across next 5 NDA transactions",
  expected_impact: "30% reduction in average redline cycles and 20% faster time-to-signature"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="nda-generator",
  query="2024–2025 enforceability trends for NDA non-solicitation clauses, DTSA whistleblower immunity compliance requirements, and emerging AI-specific confidentiality provisions in commercial NDAs",
  reason="Ensure generated NDAs reflect current judicial enforcement patterns, statutory compliance obligations, and evolving market standards for technology-related confidential information"
)
```

## Step 7: Save Session

> **Session summary must be fact-dense:** include the user's stated preferences,
> personal context (company, ICA, industry), what was delivered, any corrections
> given, and end with **"Next session defaults: [3-5 things to pre-fill on next
> connect()]"** so returning users get immediate personalisation.
>
> **Outcomes array:** one concrete fact per item (format, tone, ICA, length,
> constraints). Each outcome should be extractable as a standalone user preference.


```
FutureProof:save_session(skill="nda-generator", session={
  summary: "...[fact-dense: ICA, format, tone, constraints, what was delivered, amends made. End with: Next session defaults: ...]",
  outcomes: [
    "Format: [format chosen]",
    "Tone: [tone and constraints]",
    "ICA: [ICA description]",
    "Deliverable: [what was produced]"
  ],
  metadata: {}
})
```