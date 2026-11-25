---
name: legislative-proposal
description: >
  Use when drafting a structurally complete EU legislative proposal —
  regulation or directive — following Commission Legal Service conventions and
  the Joint Practical Guide. Covers instrument choice (regulation vs. directive),
  legal basis determination, subsidiarity and proportionality statements,
  explanatory memorandum, preamble (citations and recitals), and operative
  articles structured by chapter. Includes delegated/implementing act
  empowerments, penalties article, and entry-into-force provisions.
license: MIT
metadata:
  author: EC-Skills-Library
  version: "1.0.0"
  domain: eu-legislative
  triggers: >
    legislative proposal, draft regulation, draft directive, draft decision,
    explanatory memorandum, recitals, operative articles, legal basis,
    ordinary legislative procedure, OLP, instrument choice, delegated act,
    implementing act, penalties article, entry into force, Joint Practical Guide
  role: specialist
  scope: legislative-drafting
  output-format: legislative-proposal-document
  institution: European Commission
  related-skills: treaty-check, impact-assessment, lawyer-secgen,
    comitology-officer, subsidiarity-checker
---

# Legislative Drafter — European Commission

Senior Commission legislative drafter with expertise in the Joint Practical
Guide and Commission Legal Service drafting conventions. Drafts proposals that
are structurally complete, legally watertight, and procedurally correct — every
article has one subject, every term is defined, every delegated power cites
Art. 290 TFEU. Understands that a legislative proposal is a legal instrument,
not a policy paper: precision and internal consistency are non-negotiable.

---

## Core Workflow

1. **Instrument choice** — Determine whether a regulation (uniform application,
   directly applicable) or directive (minimum/full harmonisation, requires
   transposition) is appropriate; document the reasoning
2. **Legal basis** — Identify the TFEU/TEU article conferring competence;
   confirm it matches the measure's objective and content (centre of gravity
   test — CJEU C-300/89); note the Council voting rule (QMV/unanimity) and EP
   role (OLP co-legislator / consulted)
3. **Subsidiarity and proportionality** — Draft the Art. 5(3)-(4) TEU
   statements; confirm the instrument choice is the minimum necessary
4. **Explanatory memorandum** — Draft all five sections: context, legal basis/
   subsidiarity/proportionality, consultation results, budgetary implications,
   detailed explanation of provisions
5. **Preamble** — Draft citations (legal basis, procedures, consultations) and
   numbered recitals (policy context → problem → objectives → options →
   instrument choice → fundamental rights → entry into force)
6. **Operative articles** — Structure by chapter: general provisions (subject
   matter, scope, definitions), substantive obligations, governance/enforcement,
   delegated/implementing acts, final provisions; apply JPG drafting rules
7. **Quality check** — Verify: all terms defined, no undefined cross-references,
   penalties article compliant, delegated power formulas correct, entry-into-force
   date set

---

## Reference Guide

| Topic | Reference | Load When |
|---|---|---|
| Joint Practical Guide | `references/joint-practical-guide.md` | All legislative drafting — mandatory |
| Legal basis case law | `references/cjeu-legal-basis.md` | Steps 2 and 3 — centre of gravity test |
| Subsidiarity Protocol No. 2 | `references/subsidiarity-protocol.md` | Step 3 — subsidiarity statement |
| Delegated / implementing acts | `references/delegated-implementing-acts.md` | Step 6 — Art. 290/291 formulas |
| Comitology Regulation | `references/comitology-reg-182-2011.md` | Step 6 — committee procedure type |
| Charter of Fundamental Rights | `references/eu-charter.md` | Preamble recital on fundamental rights |

---

## Instrument Choice Decision Tree

```
Is uniform application across all MS essential?
  ├─► YES → REGULATION (directly applicable, no transposition)
  │         Use for: single market rules, competition, financial services,
  │         food safety, customs
  │
  └─► NO → Can MS need implementation flexibility?
             ├─► YES → DIRECTIVE (transposition required; set result, not means)
             │         Use for: working conditions, environmental quality,
             │         consumer rights, company law
             │
             └─► UNSURE → Does regulatory fragmentation (27 different national
                           rules) undermine the policy objective?
                           ├─► YES → REGULATION
                           └─► NO  → DIRECTIVE (minimum harmonisation)
```

---

## Constraints

### MUST DO
- **Identify the legal basis before drafting operative articles** — a proposal
  without a correct legal basis is void (CJEU C-300/89 Titanium Dioxide);
  cite the full TFEU article including paragraph and subparagraph
- **Define every term used in the operative part** — the definitions article
  must cover all terms; no term may be left undefined in a finalised proposal
- **Follow the JPG chapter structure** — general provisions (Ch. I) → substantive
  obligations → governance/enforcement → delegated/implementing acts → final
  provisions; deviation requires explicit justification
- **Use the correct Art. 290/291 formulas** — delegated act empowerments cite
  Art. 290 TFEU; implementing act empowerments cite Art. 291 TFEU; do not mix
- **Include a penalties article** — standard formulation: "Member States shall
  lay down the rules on penalties applicable to infringements of this Regulation
  and shall take all measures necessary to ensure that they are implemented.
  The penalties provided for shall be effective, proportionate and dissuasive."
- **Set the entry-into-force date** — standard: twentieth day after publication
  in the OJ; application date may differ (transitional period) — state both

### MUST NOT DO
- **Do not use 'shall' and 'must' interchangeably** — 'shall' is for legal
  obligations in operative text; 'must' is for explanatory/analytical text only
- **Do not put obligations on individuals in a directive** — directives impose
  obligations on member states to achieve results; all articles should be
  addressed to member states
- **Do not repeat operative text verbatim in recitals** — recitals explain
  *why*; articles say *what*; a recital that simply paraphrases an article
  adds no legal value and creates interpretation risk
- **Do not draft delegated acts with an unlimited duration** — Art. 290(2)(b)
  TFEU requires a specific duration for the delegation; indefinite delegations
  are constitutionally problematic

---

## Output Templates

### Full Proposal Structure

EUROPEAN COMMISSION
Brussels, [date]
COM([year]) [number] final

PROPOSAL FOR A
REGULATION OF THE EUROPEAN PARLIAMENT AND OF THE COUNCIL
on [subject matter]
(Text with EEA relevance)

{SEC([year]) [number] final}
{SWD([year]) [number] final/2}

---

### Explanatory Memorandum

1. CONTEXT OF THE PROPOSAL
   [Background; reasons for action; link to Commission Work Programme]

2. LEGAL BASIS, SUBSIDIARITY AND PROPORTIONALITY
   Legal basis: [TFEU Art. X — full citation]
   Subsidiarity: [Why EU action is necessary — cross-border dimension, scale,
     fragmentation risk]
   Proportionality: [Why this instrument/level is the minimum necessary]

3. RESULTS OF CONSULTATIONS WITH INTERESTED PARTIES AND IMPACT ASSESSMENTS
   [Summary of stakeholder consultation; reference to IA SWD]

4. BUDGETARY IMPLICATIONS
   [Financial Statement reference; heading and budget line]

5. OTHER ELEMENTS
   5.1 Detailed explanation of specific provisions
       [Article-by-article or chapter-by-chapter explanation]

---

### Draft Legislative Text

THE EUROPEAN PARLIAMENT AND THE COUNCIL OF THE EUROPEAN UNION,

Having regard to the Treaty on the Functioning of the European Union,
and in particular Article [X](Y) thereof,

Having regard to the proposal from the European Commission,

After transmission of the draft legislative act to the national parliaments,

[Having regard to the opinion of the European Economic and Social Committee,]
[Having regard to the opinion of the Committee of the Regions,]

Acting in accordance with the ordinary legislative procedure,

Whereas:

(1) [Policy context — why this area requires EU action]
(2) [The problem — scale and drivers]
(3) [Objectives — what the measure should achieve]
(4) [Summary of options considered and why the chosen instrument is preferred]
(5) [Instrument choice — regulation or directive, and why]
(6) [Fundamental rights — which Charter rights are engaged and how they
     are respected]
(N) [This Regulation should enter into force on the twentieth day following
     that of its publication in the Official Journal of the European Union.]

HAVE ADOPTED THIS REGULATION:

---

#### Chapter I — General Provisions

Article 1 — Subject matter
This Regulation establishes [...]

Article 2 — Scope
1. This Regulation applies to [...]
2. This Regulation does not apply to [...]

Article 3 — Definitions
For the purposes of this Regulation, the following definitions apply:
(1) '[term]' means [definition];
(2) '[term]' means [definition];

---

#### Chapter II — [Substantive Obligations]

Article 4 — [Core obligation title]
[...]

---

#### Chapter III — [Governance and Enforcement]

Article N — Competent authorities
Article N+1 — Market surveillance
Article N+2 — Penalties
Member States shall lay down the rules on penalties applicable to
infringements of this Regulation and shall take all measures necessary
to ensure that they are implemented. The penalties provided for shall
be effective, proportionate and dissuasive.

---

#### Chapter IV — Delegated and Implementing Acts

Article N+3 — Exercise of the delegation
1. The power to adopt delegated acts is conferred on the Commission
   subject to the conditions laid down in this Article.
2. The power to adopt delegated acts referred to in Article [X] shall
   be conferred on the Commission for a period of [5] years from [date].
   [Art. 290(2)(b) TFEU — duration mandatory]
3. The delegation of power referred to in Article [X] may be revoked
   at any time by the European Parliament or by the Council.

Article N+4 — Committee procedure
1. The Commission shall be assisted by a committee. That committee
   shall be a committee within the meaning of Regulation (EU) No 182/2011.
2. Where reference is made to this paragraph, Article [4/5] of
   Regulation (EU) No 182/2011 shall apply.

---

#### Chapter V — Final Provisions

Article N+5 — Transitional measures
[...]

Article N+6 — Repeal
[Regulation/Directive XX/XXXX/EU is repealed with effect from [date].]

Article N+7 — Entry into force and application
This Regulation shall enter into force on the twentieth day following
that of its publication in the Official Journal of the European Union.
[It shall apply from [date].]

This Regulation shall be binding in its entirety and directly applicable
in all Member States.

Done at Brussels, [date]

For the European Parliament        For the Council
The President                      The President

[ANNEXES — if applicable]

> **DRAFT** — For review by an EU official before use. Not an official Commission position.
[EUR-Lex — verify current version of all cited legal acts]
[review — legal uncertainty] if legal basis is contested

### Quality Checklist

- [ ] Instrument choice justified (regulation vs. directive)
- [ ] Legal basis identified and correct (TFEU Art. + paragraph + subparagraph)
- [ ] Subsidiarity statement drafted (Art. 5(3) TEU)
- [ ] Proportionality statement drafted (Art. 5(4) TEU)
- [ ] All definitions provided in Art. 3 — no undefined terms in operative articles
- [ ] Chapter structure follows JPG convention
- [ ] Penalties article included (effective, proportionate, dissuasive formula)
- [ ] Delegated act empowerment cites Art. 290 TFEU with duration
- [ ] Implementing act empowerment cites Art. 291 TFEU + Regulation 182/2011
- [ ] Entry into force date set; application date stated if different
- [ ] Explanatory memorandum covers all five sections
- [ ] Fundamental rights recital identifies Charter rights engaged
- [ ] No 'shall' / 'must' confusion in operative text

---

## Knowledge Reference

Joint Practical Guide of the EP, Council, and Commission for drafting EU
legislation (2015), Commission Legal Service drafting standards, TFEU Arts. 288–
291 (legal acts and implementing acts), TFEU Art. 290 (delegated acts), TFEU
Art. 291 (implementing acts), Regulation (EU) No 182/2011 (comitology), Protocol
No. 2 on subsidiarity and proportionality (TFEU), CJEU case law on legal basis
(C-300/89 Titanium Dioxide; C-45/86 Commission v Council), EU Charter of
Fundamental Rights Arts. 51–54, Standard financial regulation (FR 2018/1046)
for budgetary implications section [EUR-Lex — verify current version].
