---
name: administrative-writing
description: Produces formal and institutional documents ready for real use: letters, official correspondence, administrative requests, notices, attestations, memoranda, meeting minutes, formal statements and application documents. Handles the required elements, the register, the signature block and the conventions of the recipient's country. Never invents a fact, a legal reference, a credential or an institution.
license: MIT
metadata:
  category: administrative
  version: 1.0.0
  depends_on: [document-core]
  outputs: [administrative-document, element-checklist, gap-list]
---

# Administrative Writing

These documents are filed, quoted, forwarded, and occasionally produced years
later in a dispute. A missing reference number costs a week. An invented
regulation costs credibility that does not come back.

Governed by `document-core`. This skill adds the required elements, the
register, the country conventions, and the evidence rule at its strictest.

Never merged with technical documentation. The audiences, registers,
structures and failure consequences have nothing in common.

## 1. The evidence rule, at its strictest

`document-core` section 5 forbids inventing facts. Here it is absolute,
because these documents assert things about the real world on someone's
behalf.

Never write, unless taken from a source in front of you:

```
a statute, article, decree, regulation or case reference
a registration, licence, accreditation, tax or company number
an institution's name, department, address or procedure
a person's title, function, qualification or authority
a date, deadline, amount, rate or reference number
a prior exchange, its date or its content
a commitment, guarantee or obligation
```

Legal references are the most dangerous. A plausible article number in a
formal letter is quoted back, relied upon, and discovered to be wrong by the
recipient rather than by you. A citation is copied from the text of the law or
it does not appear.

Missing elements are marked visibly in the draft, never filled and never
silently dropped:

```
[TO PROVIDE: contract reference from your file]
[TO VERIFY: exact department name at the recipient organisation]
[TO CONFIRM WITH COUNSEL: whether this clause applies to a fixed term contract]
```

Anything touching legal effect, entitlement or obligation is marked for a
qualified human. This skill drafts; it does not advise.

## 2. Required elements

Absence of any of these is what gets a document returned, ignored or ruled
inadmissible.

| Element | Rule |
|---|---|
| Sender | full identity and the address a reply reaches |
| Recipient | named person or exact department, with the title they use |
| Place and date | as the recipient's country writes them |
| References | yours and theirs, both, when the exchange has any |
| Subject | one line, factual, naming the object and the action |
| Salutation | matching the recipient's status and the country's convention |
| Body | purpose, facts, request, deadline |
| Closing | the country's convention, matched to the salutation |
| Signature | name, function, and space for a handwritten signature where required |
| Attachments | listed and numbered, matching what is enclosed |
| Copies | listed when anyone else receives it |

The subject line is the field most often wasted. It is what the recipient's
filing system indexes and what a later reader sees first.

| Weak | Usable |
|---|---|
| Request | Request for a certified copy of building permit PC-2024-0871 |
| Follow-up | Second request, invoice 2026-0142 unpaid since 14 May 2026 |
| Contract | Termination of contract 88-2451, effective 30 September 2026 |

## 3. Structure of the body

Four movements, in this order, whatever the document.

```
1. Purpose      why you are writing, in one sentence, first
2. Facts        what happened, in order, each verifiable
3. Request      what you want, specifically, and by when
4. Availability what you provide, and how to reach you
```

Rules:

- The purpose is the first sentence. An administrative reader decides in one
  line whether this is theirs to handle.
- Facts are dated and separable. Anything the recipient can check is easier to
  act on than a characterisation.
- The request is one action, addressed to someone able to take it. Two
  requests are two letters, or a numbered list where each is separately
  answerable.
- A deadline is a date, never a duration. `Within 15 days` starts a dispute
  about when it started.
- No emotion, no accusation, no irony. Facts and a request are more effective
  and survive being read by a third party later.
- Never threaten a consequence you cannot or will not carry out.

Length: one page for a request or a notice. Two pages is already a document
that needs an attachment instead.

## 4. Register

Formal, impersonal, unambiguous. Not archaic and not stiff.

| Avoid | Prefer |
|---|---|
| I am writing to inform you that we have decided to | We have decided to |
| Please be advised that the deadline is approaching | The deadline is 30 September 2026 |
| It would be greatly appreciated if you could kindly | Please send |
| At your earliest convenience | By 15 September 2026 |
| We regret any inconvenience caused | one sentence naming what went wrong, then what you are doing |
| As per our conversation | In our exchange of 4 August 2026 |

Politeness carries no information; precision does. A courteous, precise letter
is more respectful of the recipient's time than an elaborate vague one.

Ambiguity is the defect that matters. Every sentence is checked for a second
reading, because a sentence that can be read two ways will be read the other
way at the moment it counts.

## 5. Country conventions

The output language is the recipient's. So are the conventions, and they are
not translations of each other.

| Element | France | United Kingdom | United States | Germany |
|---|---|---|---|---|
| Date | 11 aout 2026 | 11 August 2026 | August 11, 2026 | 11.08.2026 |
| Place with date | Lyon, le 11 aout 2026 | not used | not used | Berlin, den 11.08.2026 |
| Salutation, named | Monsieur / Madame | Dear Mr Dupont | Dear Mr. Dupont: | Sehr geehrter Herr Dupont |
| Salutation, unknown | Madame, Monsieur | Dear Sir or Madam | To Whom It May Concern: | Sehr geehrte Damen und Herren |
| Closing | full formule de politesse | Yours sincerely / Yours faithfully | Sincerely, | Mit freundlichen Grussen |
| Subject line | Objet, before the salutation | Re, after the salutation | Re, after the salutation | Betreff, before the salutation |
| Attachments | Pieces jointes, numbered | Enc. | Enclosures: | Anlagen |

French correspondence deserves specific attention because its closing carries
the hierarchical relationship and a wrong one is noticed:

- To an institution or a superior, the full form:
  `Je vous prie d'agreer, Madame, Monsieur, l'expression de mes salutations
  distinguees.`
- The salutation used in the closing repeats the opening one exactly.
- Between professional equals, `Cordialement` or `Bien cordialement` is
  sufficient and the full form reads as distant.
- The typographic rules of `writing/resources/typographie-francaise.md` apply
  to any French output: non-breaking spaces before double punctuation,
  guillemets, capitalisation of titles.

When the recipient's country is not in this table, find its convention from a
source. Do not extrapolate. Formal correspondence conventions are not
predictable from a neighbouring country.

## 6. Document types

### Formal letter or request

The four movements of section 3, one page, one request.

### Notice, formal statement or demand

```
The fact, dated
The rule, obligation or agreement it engages, cited from its text
The consequence, if any, stated plainly and without exaggeration
The action required, with a date
```

Never states a legal consequence that has not been verified with someone
qualified. Mark it and stop.

### Attestation or certificate

```
Identity of the person certifying, and the authority under which they do
Identity of the subject
The fact certified, precisely bounded in time and scope
Date and place
Signature
```

Certifies only what the signatory can personally attest. Nothing inferred,
nothing generalised, nothing about a period they did not observe. A phrase
such as *has always been* is not certifiable and does not appear.

### Memorandum

```
To, From, Date, Subject
Purpose, first line
Background, only what is needed to act
Decision or request
Action required, with owner and date
```

Internal, so shorter and more direct, but the required elements do not change:
it will still be forwarded and filed.

### Meeting minutes

```
Meeting, date, time, place
Present, absent, apologies
Agenda
Per item: discussion in substance, decision taken, action with owner and date
Next meeting
Approval status
```

Minutes record decisions and actions, not conversation. Attribution only where
it matters to the decision. Disagreements are recorded as positions, never as
character. Circulated for correction within days, while memory is still
available.

### Application or submission document

```
Every element the receiving body requires, in the order it requires
Their references and identifiers, quoted exactly
A checklist of attachments, matching what is enclosed
Nothing they did not ask for
```

Requirements are taken from the body's own published instructions. Where a
requirement is unclear, it is marked and the body is asked, rather than
guessed. A guessed requirement is the standard reason an application is
returned.

## 7. Before sending

- [ ] Every element of section 2 present.
- [ ] Purpose in the first sentence.
- [ ] Every fact verifiable, every date correct.
- [ ] No invented reference, number, statute, title or institution.
- [ ] Every marked gap either resolved or visibly still marked.
- [ ] The request is one action, addressed to someone able to take it.
- [ ] The deadline is a date.
- [ ] Salutation and closing match, in the recipient's convention.
- [ ] Attachments listed, numbered, and actually enclosed.
- [ ] No sentence readable two ways.
- [ ] Nothing asserted that a qualified professional should assert.
- [ ] Read once as the recipient, and once as a third party reading it in two
      years with no context.

## 8. Protocol

1. Load `document-core`. Identify sender, recipient, purpose and the country
   whose conventions apply.
2. Set the output language to the recipient's.
3. Choose the type from section 6 and list its required elements.
4. Collect the facts. Separate what is sourced from what is assumed.
5. Mark every missing element visibly. Ask for the essential ones in one
   batch, through `project-brief`.
6. Draft the four movements of section 3.
7. Apply the country conventions of section 5.
8. Apply `document-design` for the letterhead, margins and signature block.
9. Run the checklist of section 7, and the eight-point gate with the
   administrative panel.
10. Deliver with the marked gaps listed separately, so none is missed.
11. Where a PDF is required, hand to `pdf-production` and verify the render.

## 9. Auto-critique

Score 0 to 5: every required element present, purpose first, facts verifiable
and dated, one actionable request, deadline as a date, register formal without
padding, country conventions correct, no sentence readable two ways, nothing
invented, gaps marked rather than filled, nothing asserted that requires a
qualified professional.

Threshold: no axis below 3, average at least 4.3. These documents carry
consequences, and the threshold reflects it.

Automatic failure: an invented legal reference, registration number,
institution or credential; an assertion of legal effect made without a
qualified source; or a gap silently filled with a plausible value.

## 10. Interfaces

- Upstream: `document-core`, `project-brief`.
- Downstream: `document-design`, `pdf-production`, `self-critique`.
- Related: `report-writing` for documents that support a decision rather than
  make a request.
