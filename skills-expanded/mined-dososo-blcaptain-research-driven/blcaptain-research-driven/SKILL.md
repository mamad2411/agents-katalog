---
name: blcaptain-research-driven
description: Improves research quality when accuracy matters; work depends on external facts such as documentation, APIs, pricing, licenses, standards, current events, research, or source code; a question is complex or multi-part; confidence is low; or sources conflict. Excludes casual chat, pure formatting, mechanical edits, and trivial facts already known with high certainty.
license: Apache-2.0
---

# Research-Driven Investigation

**Investigate; do not merely retrieve.**

Treat a plausible answer as the start of inquiry, not its end. Build a conclusion that survives attempts to disprove it. Maximize correctness without promising certainty. Expose uncertainty instead of filling gaps.

## Protect the Two Highest-Priority Behaviors

### Try to disprove before supporting

1. State the strongest competing explanation or answer.
2. Predict what evidence would appear if that alternative were true.
3. Search for counterexamples, boundary failures, changed assumptions, and contrary primary sources.
4. Revise or narrow the conclusion when contrary evidence survives scrutiny.

Do not call a search complete after collecting only supporting material.

### Stop only after convergence

Stop when every applicable condition holds:

- [ ] Cover every material sub-question or name it as an open gap.
- [ ] Trace every key fact to an appropriate primary source when one exists.
- [ ] Corroborate every key conclusion with at least two genuinely independent sources.
- [ ] Test the strongest credible alternative or counterexample.
- [ ] Reconcile meaningful conflicts or state why they remain unresolved.
- [ ] Mark each conclusion with a certainty grade.
- [ ] Observe diminishing returns: the latest search round changes no conclusion, certainty grade, or material caveat.

Continue when any applicable item remains false. Stop earlier for a trivial or low-impact task when one authoritative source directly answers the whole question and no meaningful conflict, ambiguity, or freshness risk exists. State that reduced scope.

## Use Three Levers

| Lever | Make it operational | Avoid |
|---|---|---|
| Thorough | Decompose the question into mutually exclusive, collectively exhaustive sub-questions; track coverage; apply the explicit STOP conditions. | Collecting many links without proving coverage. |
| Deep | Prefer the closest primary source; inspect definitions, mechanisms, boundaries, version history, and counterexamples; ask why the fact holds. | Repeating summaries that merely agree. |
| Correct | Cross-verify material claims; test alternatives; distinguish source independence; grade certainty. | Treating consensus, rank, or confidence as proof. |

## Run the Seven-Step Investigation

### 1. Frame and decompose

- Restate the exact question, intended decision, audience, time boundary, and required precision.
- Separate facts to establish from judgments to make.
- Split the question into MECE sub-questions.
- Add boundary questions for version, jurisdiction, date, environment, population, and excluded cases.
- Mark dependencies and what could change the answer.
- Calibrate effort to impact, uncertainty, reversibility, and freshness.

Use the coverage and overlap tests in [references/techniques.md](references/techniques.md) for complex decomposition.

### 2. Survey the landscape

- Map the terrain before narrowing the search.
- Identify authoritative source families, disputed areas, vocabulary, versions, and likely blind spots.
- Name the best available primary source and an independent corroborating source for each sub-question.
- Read [references/tool-mapping.md](references/tool-mapping.md) before relying on platform-specific tool names.
- Keep the survey broad but brief; use it to plan depth, not to form the final conclusion.

### 3. Trace to primary sources

- Search one sub-question or hypothesis at a time.
- Open the underlying source; do not treat a search snippet as evidence.
- Follow citations upstream until reaching the closest authoritative origin available.
- Record the exact passage, table, behavior, date, version, and scope that support or weaken the claim.
- Ask why the observed fact holds; identify its mechanism, definition, assumptions, and failure boundary.
- Separate observed fact, source interpretation, and your inference.

For persistent work, copy [assets/research-log-template.md](assets/research-log-template.md) and fill it while investigating.

### 4. Cross-verify

- Corroborate each key conclusion with at least two genuinely independent sources.
- Trace source ancestry; reject circular citation, mirrored content, or repeated claims from a shared origin as independent support.
- Compare sources that use different methods when possible.
- Resolve disagreements by checking scope, date, definitions, methods, incentives, and source ancestry.
- Downgrade the conclusion when independent corroboration remains unavailable.

### 5. Actively disprove

- Steelman the strongest alternative before rejecting it.
- Predict what evidence would appear if that alternative were true.
- Search using contrary phrasing and failure-oriented terms.
- Seek counterexamples, boundary cases, version differences, and the strongest opposing evidence.
- Downgrade, narrow, withdraw, or replace a conclusion when it does not survive the challenge.

### 6. Identify gaps and iterate

- Name every unresolved sub-question, conflict, access limit, and untested boundary.
- Reframe weak questions in light of new evidence.
- Loop through survey, primary-source tracing, cross-verification, and disconfirmation as findings demand.
- Track what each new round changes.
- Apply the STOP checklist; continue only when another round could materially change the result.

### 7. Synthesize with graded certainty

- Answer the decision first.
- Show the minimum reasoning needed to make the answer auditable.
- Attach sources to the claims they support.
- Grade each material conclusion as Confirmed, Probable, Speculative, or Unknown.
- State versions, dates, assumptions, exceptions, and open questions plainly.
- Reapply the STOP checklist before finalizing.

## Grade Certainty

| Grade | Assign only when |
|---|---|
| Confirmed | At least two genuinely independent primary sources agree, material conflicts are resolved, and active disconfirmation found no surviving contradiction within the stated scope. |
| Probable | Credible evidence supports the claim, but full independent primary-source corroboration or one meaningful boundary test remains incomplete. |
| Speculative | Only reasoning or weak, indirect evidence supports the claim, and plausible alternatives remain open. |
| Unknown | Available evidence cannot determine the answer; keep the gap open instead of guessing. |

Do not convert source confidence, model confidence, or repeated wording into a higher grade. State scope beside the grade when a conclusion depends on a version, date, environment, or population.

## Present the Result

Use this compact structure unless the user requests another format:

1. **Conclusion:** State the decision-relevant answer and certainty grade.
2. **Why:** Give the decisive facts and reasoning.
3. **Countercheck:** State the strongest alternative tested and what happened.
4. **Boundaries:** Name versions, dates, assumptions, exceptions, and unresolved gaps.
5. **Sources:** Link each material claim to the closest supporting source.

## Avoid Research Failure Modes

- **Shallow stop:** Do not stop at the first plausible answer.
- **Single-source conclusion:** Do not treat one source as corroboration.
- **Confirmation bias:** Do not gather only supporting material; hunt for the strongest contrary evidence.
- **Secondary as authority:** Do not prefer commentary when an accessible primary source can answer the question.
- **Circular corroboration:** Do not count pages that repeat one upstream claim as independent confirmation.
- **Speculation as fact:** Do not hide an inference, unresolved conflict, or guess behind confident prose.
- **Boil the ocean:** Do not overresearch low-impact questions after the STOP conditions hold.
- Do not claim exhaustive coverage without a decomposition and a coverage check.
- Do not confuse "no contradiction found" with proof that none exists.
- Do not guarantee correctness; make the remaining uncertainty visible.

## Load Supporting Material Only When Needed

- Read [references/techniques.md](references/techniques.md) for detailed decomposition, source selection, independence checks, active disconfirmation, conflict resolution, and stopping tests.
- Read [references/tool-mapping.md](references/tool-mapping.md) before mapping the method to Claude Code, Codex, or Gemini CLI.
- Copy [assets/research-log-template.md](assets/research-log-template.md) when a durable investigation record will improve coordination, resumption, or review.
