---
name: college-decision
description: >
  Use when you want to send a question to the College of Commissioners and get
  the resulting document back. This is a single-command workflow: it runs the
  full College deliberation (all 21 Commissioners speak, the President calls the
  vote) and then, if the College ADOPTS, drafts the full legislative instrument
  as a COM(YYYY) NNN final document — explanatory memorandum, recitals, and
  operative articles by chapter. If the College refers the dossier back or
  withdraws it, no COM document is produced; the deliberation record and the
  conditions/reasons are returned instead. This is the College mirror of the
  self-contained /dpia skill: one call yields both the on-screen decision summary
  and the full referenced document. Invoke with a question or dossier for the
  College.
license: MIT
metadata:
  author: EC-Skills-Library
  version: "1.0.0"
  domain: eu-simulation
  triggers: >
    ask the college, college decision, question to the college, adopt and draft,
    get the COM document, college to proposal, COM final draft, college adopt
    and draft, full draft COM, college produce proposal, decision then document,
    college deliberation with document, adopt the proposal and give me the text
  role: workflow
  scope: college-decision-to-legislative-document
  output-format: college-decision-with-com-document
  institution: European Commission
  related-skills: college-deliberation, legislative-proposal, legislative-cycle
---

# College Decision — Deliberation to COM Document

Composes two existing capabilities into one question→document flow:

1. **College deliberation** — the full College of Commissioners meeting protocol
   (all 21 Commissioners speak, the President reads the room and calls the vote).
2. **Legislative drafting** — only if the College adopts, the adopted dossier is
   turned into a structurally complete `COM(YYYY) NNN final` legislative document.

This skill does not redefine either capability. It orchestrates the College
protocol from `knowledge/agents/college-deliberation.md` and applies the drafting
conventions of the `legislative-proposal` skill for the emitted document. Use
`/college-deliberation` when you only want the meeting record; use this skill when
you want the meeting record **and** the instrument.

The value of the two-step design is that the document is a *consequence of the
vote*, not a foregone conclusion: a College that refers a dossier back has not
adopted anything, so no COM document exists yet — and this skill must not invent
one.

---

## Core Workflow

1. **Run the College deliberation** — follow the full protocol in
   `knowledge/agents/college-deliberation.md`: President opens (question framed,
   treaty basis noted, decision threshold set) → lead Commissioner presents →
   EVP coordination layer → each of the 21 Commissioners speaks once → President
   reads the room → formal vote if needed → outcome.

2. **Branch on the outcome:**
   - **ADOPTED** → proceed to step 3.
   - **REFERRED BACK** → stop. Return the deliberation record and the specific
     conditions the lead DG must address, with a return deadline. Do **not**
     draft a COM document — nothing has been adopted.
   - **WITHDRAWN** → stop. Return the deliberation record and the reasons. Do
     **not** draft a COM document.

3. **Draft the COM document (ADOPTED only)** — turn the adopted dossier into a
   full `COM(YYYY) NNN final` legislative instrument using the drafting
   conventions of `legislative-proposal`: instrument choice (regulation vs.
   directive) → legal basis (cite the full TFEU/TEU article **before** drafting
   operative articles) → subsidiarity and proportionality statements →
   explanatory memorandum (all five sections) → preamble (citations + numbered
   recitals) → operative articles by chapter (JPG structure) → delegated/
   implementing act empowerments → penalties article → entry into force. The
   document must be internally consistent with the position the College actually
   adopted, including any conditions or amendments the President attached to the
   adoption.

---

## Reference Guide

| Resource | Path | Load when |
|---|---|---|
| College deliberation protocol + 21-member roster | `knowledge/agents/college-deliberation.md` | Step 1 — every session; full protocol and roster |
| All 21 Commissioner personas | `knowledge/commissioners/*.md` | Step 1 — each Commissioner's speaking turn |
| Conflict escalation rules | `knowledge/agents/college-deliberation.md` | Step 1 — when two positions are irreconcilable |
| Legislative drafting conventions | eu-legislative `legislative-proposal` skill | Step 3 — instrument choice, legal basis, JPG structure, recitals, empowerments |

Step 3 applies the drafting conventions of the eu-legislative `legislative-proposal`
skill — which loads the Joint Practical Guide, the legal-basis case law, and the
Subsidiarity Protocol from its own plugin. This skill reaches across plugins the
same way `/legislative-cycle` chains phases from other plugins; it does not
duplicate those reference files here.

---

## Constraints

### MUST DO
- **Voice all 21 Commissioners** — every member of the College speaks; the
  difficult voices are the most instructive. A Commissioner whose portfolio has
  no stake gives a brief "no objection from a [X] perspective", not silence.
- **Ground every position in mandate** — a Commissioner speaking outside their
  portfolio is not realistic.
- **Make the President active** — the President frames the debate, names the
  fault lines in the consensus assessment, and takes responsibility for the call.
- **Cite the legal basis before drafting operative articles** — a proposal
  without a correct legal basis is void (CJEU C-300/89 Titanium Dioxide); cite
  the full TFEU article including paragraph and subparagraph.
- **Define every term used in the operative part** — the definitions article
  must cover all terms; no undefined term may remain in the finalised text.
- **Follow the JPG chapter structure** — general provisions → substantive
  obligations → governance/enforcement → delegated/implementing acts → final
  provisions.
- **Include a penalties article** where the instrument creates obligations, using
  the effective/proportionate/dissuasive formula.
- **Use the correct Art. 290/291 formulas** — delegated-act empowerments cite
  Art. 290 TFEU with a specific duration; implementing-act empowerments cite
  Art. 291 TFEU and Regulation (EU) No 182/2011.
- **Make the document reflect the adopted position** — any conditions or
  amendments the College attached to the adoption must appear in the COM text.

### MUST NOT DO
- **Do not emit a COM document unless the outcome is ADOPTED** — a referred-back
  or withdrawn dossier has produced no instrument; fabricating one misrepresents
  the procedure.
- **Do not manufacture consensus** — if the dossier genuinely divides portfolios,
  the deliberation must show it; artificial unanimity is not useful.
- **Do not skip the EVP layer** — the EVP assessments shape how individual
  Commissioners position themselves.
- **Do not repeat operative text verbatim in recitals** — recitals explain *why*;
  articles say *what*.
- **Do not use 'shall' and 'must' interchangeably** — 'shall' for legal
  obligations in operative text; 'must' only in explanatory text.

---

## Output Template

### Part A — College Decision Summary

COLLEGE OF COMMISSIONERS — [Meeting reference, e.g., PV(2026)2400]
Subject: [Dossier title]
Simulated date: [DD Month YYYY]
Decision sought: [Adopt for transmission to EP/Council / Note / Other]

**Outcome:** [ADOPTED / REFERRED BACK / WITHDRAWN]
**Vote:** [In favour N — Against N — Abstain N; threshold 11/21] *(state "consensus, no formal vote" if adopted without a vote)*
**Key tensions:** [Portfolio A vs Portfolio B on [issue] — nature of disagreement; or "none material"]
**Conditions attached:** [any amendments/conditions the President attached to adoption, or "none"]

> The full deliberation record (all 21 contributions, EVP assessments, President's
> consensus reading) is available on request — run `/college-deliberation` for the
> verbatim meeting record. This skill summarises the decision and, on adoption,
> produces the instrument below.

*If the outcome is REFERRED BACK:* list the specific conditions the lead DG must
address and the return deadline. **Stop here — no COM document.**

*If the outcome is WITHDRAWN:* state the reasons. **Stop here — no COM document.**

---

### Part B — Full draft · COM(YYYY) NNN final

*(This part appears only when the outcome is ADOPTED.)*

EUROPEAN COMMISSION
Brussels, [date]
COM([year]) [number] final

PROPOSAL FOR A
[REGULATION / DIRECTIVE] OF THE EUROPEAN PARLIAMENT AND OF THE COUNCIL
on [subject matter]
(Text with EEA relevance)

{SEC([year]) [number] final}
{SWD([year]) [number] final}

---

#### Explanatory Memorandum

1. CONTEXT OF THE PROPOSAL
   [Background; reasons for action; link to Commission Work Programme; the College
   decision that authorised this proposal]

2. LEGAL BASIS, SUBSIDIARITY AND PROPORTIONALITY
   Legal basis: [TFEU Art. X(Y) — full citation]
   Subsidiarity: [why EU action is necessary — cross-border dimension, scale,
     fragmentation risk]
   Proportionality: [why this instrument/level is the minimum necessary]

3. RESULTS OF CONSULTATIONS WITH INTERESTED PARTIES AND IMPACT ASSESSMENTS
   [Summary of stakeholder consultation; reference to IA SWD]

4. BUDGETARY IMPLICATIONS
   [Financial Statement reference; heading and budget line]

5. OTHER ELEMENTS
   5.1 Detailed explanation of specific provisions
       [Article-by-article or chapter-by-chapter explanation]

---

#### Draft Legislative Text

THE EUROPEAN PARLIAMENT AND THE COUNCIL OF THE EUROPEAN UNION,

Having regard to the Treaty on the Functioning of the European Union,
and in particular Article [X](Y) thereof,

Having regard to the proposal from the European Commission,

After transmission of the draft legislative act to the national parliaments,

Acting in accordance with the ordinary legislative procedure,

Whereas:

(1) [Policy context — why this area requires EU action]
(2) [The problem — scale and drivers]
(3) [Objectives — what the measure should achieve]
(4) [Summary of options considered and why the chosen instrument is preferred]
(5) [Instrument choice — regulation or directive, and why]
(6) [Fundamental rights — which Charter rights are engaged and how respected]
(N) [This [Regulation/Directive] should enter into force on the twentieth day
     following that of its publication in the Official Journal of the European
     Union.]

HAVE ADOPTED THIS [REGULATION / DIRECTIVE]:

---

##### Chapter I — General Provisions

Article 1 — Subject matter
Article 2 — Scope
Article 3 — Definitions

##### Chapter II — [Substantive Obligations]

Article 4 — [Core obligation]

##### Chapter III — [Governance and Enforcement]

Article N — Competent authorities
Article N+1 — Penalties
[Member States shall lay down the rules on penalties applicable to infringements
of this [Regulation/Directive] ... effective, proportionate and dissuasive.]

##### Chapter IV — Delegated and Implementing Acts

Article N+2 — Exercise of the delegation [Art. 290 TFEU — with duration]
Article N+3 — Committee procedure [Art. 291 TFEU + Regulation (EU) No 182/2011]

##### Chapter V — Final Provisions

Article N+4 — Transitional measures
Article N+5 — Entry into force and application
[This [Regulation/Directive] shall enter into force on the twentieth day following
that of its publication in the Official Journal of the European Union.]

[This Regulation shall be binding in its entirety and directly applicable in all
Member States. / This Directive is addressed to the Member States.]

Done at Brussels, [date]

For the European Parliament        For the Council
The President                      The President

[ANNEXES — if applicable]

---

[EUR-Lex — verify current version of all cited legal acts]
[review — legal uncertainty] if the legal basis is contested
[model knowledge — verify] for any claims about specific current dossiers or
Commissioner political positions.

> **DRAFT** — Simulation output. Not an official Commission position.
