---
name: security-questionnaire
description: Use this skill when the user asks to answer a vendor security questionnaire, procurement security assessment, enterprise due diligence form, or privacy impact questionnaire. Trigger phrases include "fill this security questionnaire", "answer this DPA", "security assessment", "vendor due diligence", "responder cuestionario de seguridad", "evaluación de seguridad", "DPIA", "SIG questionnaire", "CAIQ". Produces answers structured around what the company actually does, with explicit gaps and roadmap items, without overclaiming.
---

# security-questionnaire

> **Anchor:** Three answers: yes, no, roadmap. "Maybe" is not an answer.

## When to use

Use this skill when the user needs to fill a structured security or privacy questionnaire for a prospect, customer, regulator, or partner. Works for:

- Vendor security assessments (SIG, CAIQ, custom spreadsheets).
- Enterprise procurement due diligence on data handling.
- Privacy impact assessments (DPIA, PIA).
- Questionnaires attached to master service agreements.
- Recurring annual security reviews from existing customers.

Do not use when:

- The user is responding to an RFP with a compliance matrix. Use `rfp-response`.
- The user is writing an internal policy. This skill consumes policy; it does not author policy.
- The user is drafting a contract clause. That is legal work, not security-questionnaire work.

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

- **ES.** Rioplatense register with formal controls-and-compliance vocabulary. Keep standard terms in English: control, policy, MFA, SSO, SOC 2, ISO 27001, HIPAA, DPA, DPIA, CAIQ, SIG, RPO, RTO, pentest, incident response, least privilege, encryption at rest, encryption in transit.
- **EN.** Direct US business register. Avoid "industry-leading" and other marketing hedges that a security reviewer will mark down.
- Control IDs and policy titles stay in their original language.

## Method

### Step 1. Read the questionnaire as a risk assessment, not marketing

The reviewer's job is to find risk, not to be impressed. Read the questionnaire looking for:

- **Binary controls.** Is MFA enforced. Yes or no. Not "we are rolling out".
- **Operating controls.** Running monitoring, rotating keys, reviewing access. Yes if it actually runs, not if a policy says it should.
- **Paper controls.** Do you have a written policy. Yes if the policy exists and is dated.
- **Evidence controls.** Can you produce the log, the report, the attestation.

Mark each question with its type. A paper-control question and an operating-control question look the same but are answered differently.

### Step 2. Map questions to frameworks where possible

If the company has a control register (see step 8), map each question to the control ID that answers it. This does three things:

- Forces consistency. The same control cannot be claimed differently across two questions.
- Makes review faster. The answer is already written once.
- Flags gaps. Questions that do not map to a control are the work.

### Step 3. Use three response categories

Every question gets one of:

- **Yes.** The control is in place, operating, and there is evidence.
- **No.** The control is not in place.
- **Roadmap.** The control is not in place, but there is a committed plan, a target date, and an owner.

Do not create a fourth category for wishful thinking. "We plan to", "we are considering", "we may" are all roadmap at best, no at worst.

For "partial" answers, split the question into sub-questions and answer each one with yes, no, or roadmap.

### Step 4. Back every yes with evidence

For every yes, name the evidence.

- **Policy document.** Title, date, location.
- **Configuration.** Where the reviewer or auditor can verify.
- **Runbook.** Name of the runbook and where it lives.
- **Log or report.** Sample available on request.
- **Third-party attestation.** Auditor, date, scope.

If you cannot name evidence, the answer is not yes. It is no or roadmap.

### Step 5. Do not overclaim

Three common failure modes:

- **Claiming frameworks that are not certified.** "SOC 2 aligned" is not SOC 2. Either say "SOC 2 Type II certified, report available under NDA" or do not say SOC 2.
- **Claiming controls that only one team runs.** If only the platform team enforces MFA and the sales team does not, the answer is no, with a scope note.
- **Claiming "industry best practice"** as a substitute for specifics. Reviewers discount this to zero.

When unsure, err toward understatement. The downside of overclaiming is reviewed contracts, lost deals, or breach notification. The downside of understatement is a comment in the response.

### Step 6. Write gap disclosures proactively

If the company does not meet a common expectation, write the gap clearly, in its own row, with:

- **Gap.** What the reviewer will want that you do not have.
- **Why.** Stage, priority, or risk acceptance reasoning.
- **Mitigation.** Compensating control, contract language, or process in place.
- **Roadmap.** Committed plan or explicit acceptance that there is no plan.

Reviewers trust gap-disclosing vendors more than no-gap-seeming vendors. Polished, gap-free answers look like the vendor did not read the questionnaire.

### Step 7. Keep the voice and the terms consistent

Across a 300-row questionnaire, inconsistency is the thing a reviewer flags.

- Use the same name for the same control across rows.
- Use the same names for environments (production, staging) across rows.
- Use the same names for roles across rows.
- Do not say "we" in one row and "the platform" in the next.

### Step 8. Build and maintain the control register

Every questionnaire answered improves the control register. Each answer goes back into the register keyed by control ID, with a note on which customer needed which framing.

Next questionnaire is 5x faster.

### Step 9. Review as a skeptic

Before sending, read the response top to bottom as a skeptical reviewer.

- Is any "yes" unbacked by evidence.
- Does any row contradict another row.
- Does any answer sound like a sales pitch.
- Does any answer claim coverage of a control the company cannot demonstrate.

Every one of those becomes an action item before submission.

## Templates

- `templates/en/questionnaire-response.md`: full questionnaire response structure.
- `templates/en/control-register.md`: reusable control register keyed by control ID.
- `templates/es/questionnaire-response.md`: estructura completa de respuesta al cuestionario.
- `templates/es/control-register.md`: registro de controles reutilizable indexado por ID.

## Related skills

- `rfp-response`: use it when the security questions are part of a full RFP with a compliance matrix.
- `vendor-evaluation`: the buyer-side mirror, for scoring a vendor's security posture.
- `red-team-review`: run it on the security posture before an external review finds the gaps.

## Anti-patterns

This skill must never produce:

- Answers that claim certifications the company does not hold.
- "Yes" answers without evidence pointers.
- "We are in the process of" as a yes or no.
- Different answers to the same underlying control in different rows.
- Marketing language ("industry-leading", "enterprise-grade") in a security answer.
- A response that lacks a gap disclosure section when real gaps exist.
- A response that collapses ambiguity into a yes to get the deal unstuck.
- A response that treats a written policy as equivalent to an operating control.

## Checklist before delivery

- [ ] Every answer is yes, no, or roadmap.
- [ ] Every yes has an evidence pointer.
- [ ] Every roadmap item has a target date and an owner.
- [ ] Every no or roadmap is disclosed, not buried.
- [ ] Gap disclosure section exists if real gaps exist.
- [ ] Same control is referenced consistently across rows.
- [ ] Marketing language is absent.
- [ ] Skeptical re-read has been done.
- [ ] Control register updated with new or refined answers.
- [ ] No buzzwords from the voice rules appear.
