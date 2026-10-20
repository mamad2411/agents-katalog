# Evidence-Governed Answering

Domain: ViDocs/Memorix
Lifecycle: Intake
Owner: Vioxniv
Skill Type: Policy/Guardrail

<aside>
🧩

This is an **Intake** skill. Complete Examples + Verification before promoting.

</aside>

## Summary

- Policy skill: responses and decisions should be **evidence-governed** (links, citations, or artifacts) when making claims about Vidoxlabs systems.

## When to Use (Triggers)

- Producing conclusions, recommendations, or changes that affect operational/engineering truth
- Writing documentation that will be treated as canonical

## Inputs

- The question/request
- Available sources (Notion pages, Skills References, repos, logs)

## Outputs

- Answer or decision with supporting evidence (or explicitly noted gaps)

## Procedure / Steps

1. Identify what claims are being made.
2. Find sources that support each claim (internal docs preferred).
3. If evidence is weak or missing, state uncertainty and propose the minimum verification step.
4. Record sources in the page body and/or link them via **Evidence**.

## Guardrails

- Do not present guesses as facts.
- Prefer “unknown / needs verification” over fabrication.

## Examples

### Good

- “Based on X doc + Y log, the system does Z.”

### Bad

- “The system does Z” without support.

## Verification

- Spot-check at least one primary source for any high-impact claim.

## Sources / Evidence (Optional)

- Link the supporting pages, logs, PRs, or reference rows.