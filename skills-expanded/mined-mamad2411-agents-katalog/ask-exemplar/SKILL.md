---
name: ask-exemplar
description: Consult the accepted standard and strongest supported exemplars for a decision, plan, design, completed artifact, or diff, then return a source-grounded recommendation or evaluation.
compatibility: Needs a tool that can search or retrieve web pages. Without one, the skill reports Evidence Gaps instead of Standard or Exemplar claims.
---

# ask-exemplar

Consult current external evidence before choosing or judging a Target. Every run is a
Consultation: it is source-grounded and does not change the Target. A standalone run
returns a Decision Brief; an Embedded Evaluation returns only Top Fixes.

## Workflow

1. **Resolve the Target.** Infer whether it is open or completed. Use Guidance for
   an open Target and Evaluation for a completed Target. Ask one question only when
   an unresolved ambiguity would change the research. Identify the domain, mandatory
   requirements, and the user's hard constraints. For Guidance, identify the options.
   For Evaluation, read the completed artifact or diff and its project context.
2. **Research external evidence.** Search or revalidate current online sources on every invocation.
   Prefer primary sources such as formal standards, official documentation, shipped
   work, direct measurements, and an Exemplar's published principles. Classify the
   Standard Finding as `formal requirement`, `dominant convention`, `contested
   practice`, or `no Standard`. Use `undetermined` only when an Evidence Gap prevents
   classification. Select one or two Exemplars for evidence, relevance, and
   transferability. A person, organization, product, or method can be an Exemplar, but
   reputation alone is not evidence. Record the supporting sources as the Verified
   Source Set.
3. **Derive observable criteria.** Convert the supported evidence into criteria that
   can be checked against the Target. Separate mandatory requirements, conventions,
   and Exemplar traits. Place a source link next to each material claim. For code,
   UI, documentation, API, CLI, scope, reliability, tests, short writing, or agent-skill
   Targets, read [REFERENCE.md](REFERENCE.md). Do not let any criterion depend on
   simulated advice from a famous person.
4. **Apply the criteria.** Remove options that violate mandatory requirements or the
   user's hard constraints, then use conventions and Exemplars to rank the Feasible
   Options. State the tradeoff and Confidence for each material finding. A fix that
   violates a mandatory requirement or a hard constraint is not a fix; name the
   tension instead.
   - In Guidance, compare the options and select one by default. Make the
     Recommendation conditional only when one unresolved choice changes the
     preferred option.
   - In Evaluation, check the completed Target against each criterion, give one
     concrete fix per gap, and rank the deduplicated Top Fixes by leverage. Also
     check whether a maintained community tool, library, pattern, or idiom can
     replace custom work in the Target; a supported replacement is a Top Fix
     candidate, and its dependency and maintenance cost is a tradeoff.
5. **Return the Decision Brief.** Use the format below in the conversation unless the
   user asks for a file. Under Embedded Evaluation, return only the Top Fixes instead.

## Evidence rules

- Use credible secondary sources only as provisional context when primary evidence is
  unavailable. Label the Evidence Gap and lower Confidence.
- When online access is unavailable, report the Evidence Gap and make no claim about the
  current Standard or strongest supported Exemplar. Use available local sources only as
  provisional context, set Confidence to `low`, and give the reason.
- Call an Exemplar the best in the world only when the evidence proves that claim.
  Otherwise call it the strongest supported Exemplar for this Target and state the
  Coverage Limit.
- Stop research when current evidence is sufficient to classify the Standard Finding
  and support one or two relevant Exemplars. State important limits instead of implying
  an exhaustive search.
- Reuse a Verified Source Set only in the current conversation or parent workflow, and
  only when the domain and Standard Finding have not changed. Recheck time-sensitive
  claims before reuse.
- Use `high`, `medium`, or `low` Confidence and give a short reason. Do not use a numeric
  score for Confidence.

## Decision Brief

```markdown
## Decision Brief

### Standard Finding
<classification, evidence, and Confidence>

### Exemplars
<one or two selections, why each fits, evidence, and Confidence>

### Observable criteria
<criteria and comparison with the Target>

### Recommendation
<preferred Feasible Option, tradeoffs, and Confidence>

### Evidence limits
<Evidence Gaps and Coverage Limits, or "None material">
```

For Evaluation, make the criteria section a table with `criterion`, `bar`, `current`,
and `fix` columns, state the highest-leverage change in the Recommendation section,
and close the brief with a `### Top Fixes` section. Each Top Fixes item contains the
finding, concrete fix, Confidence, and tradeoff. REFERENCE.md shows a filled example.

## Embedded Evaluation

When a parent workflow requests Embedded Evaluation, remain report-only and return only
the numbered **Top Fixes** list. Each item contains the finding, concrete fix,
Confidence, and tradeoff. Do not edit files, commit, or push; the parent workflow
controls all changes. When there are no material fixes, return exactly `No Top Fixes.`

## Self-check

An Evaluation is useful only when it surfaces what correctness, simplification, and
maintainability reviewers structurally cannot: a missing standard tool, pattern, or an
unmet external bar. A Guidance run is useful only when its criteria come from cited
evidence instead of restating what the user already knows. When a run fails this test,
return to step 2 and research the domain's primary sources, or state that no external
bar applies.
