---
name: rfp-response
description: Use this skill when the user asks to respond to a government, enterprise, or institutional RFP, tender, or vendor questionnaire that requires structured compliance answers. Trigger phrases include "respond to this RFP", "RFP response", "draft the tender", "compliance matrix", "respuesta a licitación", "responder este pliego", "vendor questionnaire", "enterprise deal questionnaire". Produces a compliance-first response structured around the procurement document, not the vendor's pitch.
---

# rfp-response

> **Anchor:** Answer the question they asked, in the format they asked. Pitch separately.

## When to use

Use this skill when the user is preparing a response to a structured procurement document. Works for:

- Government or public-sector tenders (RFP, RFI, RFQ, pliego de licitación).
- Enterprise procurement packages with vendor questionnaires.
- Industry-specific compliance responses bundled with sales proposals.
- Rewrites of a prior response that lost or was marked non-compliant.

Do not use when:

- The user is preparing a custom dev proposal with flexible scope. Use `proposal-scoping`.
- The user is filling a security assessment. Use `security-questionnaire`.
- The user is writing a pitch deck. This skill is not that.

## Voice rules (apply to all outputs)

- No buzzwords: leverage, empower, synergy, resonate, tapestry, delve, elevate, captivate, explore, dynamic, testament.
- No em dashes.
- No filler openings.
- Decision-oriented over descriptive.
- High-context, no overexplaining.
- Standard sentence case for formal outputs.
- ES outputs match the register of the handbook: direct, self-aware, no reverence for process, comfortable naming failure.
- EN outputs use direct US business register. Do not soften bluntness into corporate-speak.
- Language switches based on audience, not author.

## Bilingual handling

- **ES.** Rioplatense register with formal procurement vocabulary where required by the buyer. Public-sector Spanish often demands specific legal and procedural language; keep it. Do not simplify contract vocabulary to sound friendlier.
- **EN.** Direct US business register. Public-sector procurement in the US, UK, or EU has its own register; match the buyer.
- Language follows the RFP's official language. Bilingual buyers get bilingual responses, not mixed sections.

## Method

### Step 1. Read the RFP as a compliance instrument

An RFP is a contract being assembled in public. The buyer is signaling what it will sign. Read it looking for:

- **Mandatory requirements.** Often called "must", "shall", "obligatorio", "excluyente". Failure to meet one is disqualification.
- **Desirable requirements.** "Should", "preferred", "deseable". Affects scoring.
- **Evaluative requirements.** Subjective but scored. "Approach to X", "quality of Y".
- **Format requirements.** Page limits, file types, naming conventions, language, order.
- **Deadlines and submission rules.** Non-negotiable.

Mark each requirement with a tag before writing anything.

### Step 2. Build the compliance matrix first

Before any prose, assemble a matrix. Every requirement in the RFP is one row.

Columns:

- **Requirement ID.** From the RFP, or your own if none exists.
- **Source.** Section and page in the RFP.
- **Requirement text.** Verbatim or tight paraphrase.
- **Type.** Mandatory, desirable, evaluative, format.
- **Response.** Meet, partially meet, do not meet, clarification needed.
- **Evidence.** Document, attachment, or section of the response where the answer lives.
- **Owner.** Person responsible for that answer.

If any mandatory row is "do not meet", the bid is either pulled or converted to a partnership bid with a disclosed gap.

### Step 3. Decide whether to bid

After the compliance matrix, run a bid/no-bid. The bid is only worth making if:

- All mandatory requirements are met or can be met with evidence.
- Evaluative requirements favor the vendor's strengths.
- The effort to respond is proportional to the expected value.
- The vendor has or can obtain the reference engagements the RFP requires.

If any of those is false, produce a no-bid note with the reason, not a weak response.

### Step 4. Split compliance answers from the narrative

Two separate parts of the document:

1. **Compliance section.** One answer per requirement. No narrative. No pitch. "Yes, met. Evidence: appendix 3."
2. **Technical approach.** The narrative. Where the vendor argues why its approach is right, backed by evidence.

Mixing them is the most common way to write a long response that fails to answer the questions.

### Step 5. Write the technical approach as decisions

The technical approach is not a vendor profile. It is a chain of decisions tied to the buyer's problem.

Structure each section around:

- **The buyer's need.** As stated in the RFP.
- **The vendor's decision.** What is being proposed.
- **The rationale.** Why this decision over alternatives.
- **The evidence.** Prior work, references, data.
- **The risks.** Named openly.

### Step 6. Team and references

- **Team.** Roles, not headshots. Time commitment per role. Replaceability.
- **References.** Same-sector engagements, delivered by the named team where possible. Each reference has a contactable name.

Do not inflate the team. Do not include names of people who will not work on the engagement.

### Step 7. Pricing

Match the format the RFP demands. If the RFP asks for fixed price, deliver fixed price. If the RFP asks for T&M with rate card, deliver that.

For each price element:

- What it covers.
- What it does not cover.
- What triggers a change order.

If pricing in the RFP's format will fail commercially, state the problem in the clarifying questions phase (step 8), not inside the price.

### Step 8. Use the clarifying questions window

Most RFPs allow written questions before the deadline. Use this window deliberately.

- Ask about anything that, if interpreted wrong, disqualifies the bid.
- Ask about formatting or interpretation issues.
- Do not ask questions that signal weakness unless a weak signal is cheaper than a wrong interpretation.

Questions become public across all bidders. Write them with that in mind.

### Step 9. Review in the order the evaluator will

Before submission, read the response in the evaluator's order:

1. Compliance matrix.
2. Mandatory documents.
3. Technical approach.
4. Team and references.
5. Pricing.

If the first two pages do not make the case that this bid is compliant and serious, the rest does not matter.

## Templates

- `templates/en/compliance-matrix.md`: requirement-by-requirement matrix.
- `templates/en/full-response.md`: full RFP response structure.
- `templates/es/compliance-matrix.md`: matriz de cumplimiento por requerimiento.
- `templates/es/full-response.md`: estructura completa de respuesta a licitación.

## Related skills

- `proposal-scoping`: use it instead when the engagement has flexible scope, not a fixed procurement document.
- `security-questionnaire`: use it for the security assessment that often ships alongside the RFP.
- `vendor-evaluation`: the mirror of this skill, for when you are the buyer scoring vendors.

## Anti-patterns

This skill must never produce:

- An RFP response without a compliance matrix.
- A response that starts with company history before addressing the buyer's problem.
- Answers that exceed the page or word limit.
- Inflated team bios that include people who will not work on the engagement.
- "Partnership" language used in place of a concrete commitment.
- A single long prose section that mixes compliance answers with narrative.
- Pricing that hides change triggers.
- A response submitted in the wrong language.
- A response that ignores format instructions.

## Checklist before delivery

- [ ] Every requirement in the RFP appears in the compliance matrix.
- [ ] No mandatory requirement is unanswered or unmet.
- [ ] Compliance section and technical approach are separate.
- [ ] Team section names real people who will do the work.
- [ ] References are same-sector and contactable.
- [ ] Pricing matches the format the RFP demands.
- [ ] Format rules (length, file type, language, order, naming) are obeyed.
- [ ] Submission deadline and channel are confirmed.
- [ ] No buzzwords from the voice rules appear.
