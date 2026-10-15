---
name: lex-scripta-structurer
description: Convert informal conversations, meeting transcripts, planning notes, requirement drafts, and policy prose into a Lex Scripta document with parent statements, nested conditions, exceptions, action items, open items, assumptions, and risks. Use when natural language must be preserved but rewritten into an indentation-based structure that an AI or rules engine can interpret without guessing missing facts.
license: MIT
metadata:
  author: Lex Scripta Contributors
  version: "1.0.0"
---

# Lex Scripta Structurer

## Use this skill when

Activate this skill when the input contains one or more of the following:

- a casual conversation that needs to become a structured document
- meeting notes or transcripts
- planning or product notes
- requirement drafts
- policy prose
- decision logs
- mixed action items, conditions, and unresolved questions

Use it when the user wants a document that stays readable to humans but can also be interpreted as a rule tree by an AI system.

## Core model

The document is built as an indentation-based logic tree.

- A top-level line expresses the governing rule, decision, objective, or obligation.
- One indentation level equals one logical child.
- Child lines narrow scope, add conditions, define exceptions, record dependencies, or specify approval paths.
- One line contains one claim.
- Explanation belongs outside the rule body unless the explanation itself changes execution logic.

## Hard constraints

- Do not invent missing dates, owners, approvals, thresholds, or legal effect.
- If a fact is absent, mark it as `[Unspecified]` or `[Needs confirmation]`.
- Do not hide conflicts by silently choosing one version.
- Keep terminology stable. One concept should have one label.
- Avoid vague language such as `as soon as possible`, `as appropriate`, or `if needed` unless the source itself is vague. If it is vague, preserve the meaning and flag the ambiguity in `Open Items` or `Evidence / Notes`.
- Do not merge multiple decisions into one sentence.
- Keep explanatory notes outside the Lex Scripta Body.

## Transformation workflow

1. Separate operational content from chatter.
2. Extract statements that imply a rule, decision, action, dependency, question, or exception.
3. Classify each extracted statement.
4. Identify the parent statement for each child statement.
5. Rewrite each statement into a single clear claim without changing its meaning.
6. Build the indentation tree.
7. Move unresolved items, assumptions, and conflicts into their own sections.
8. Audit the result with the checklist in [references/OUTPUT-CHECKLIST.md](references/OUTPUT-CHECKLIST.md).

## Statement placement rules

Place the following in the Lex Scripta Body:

- decisions
- obligations
- prohibitions
- conditions
- exceptions
- action items
- dependencies
- approval rules
- recording or evidence obligations

Place the following outside the Lex Scripta Body:

- unresolved questions
- assumptions
- background explanation
- reasons that do not change execution logic
- explicit conflicts between speakers or versions

## Output format

Produce the document in this exact section order:

1. `Purpose`
2. `Defined Terms`
3. `Lex Scripta Body`
4. `Open Items`
5. `Assumptions`
6. `Evidence / Notes`
7. `Risks / Conflicts`

Render `Lex Scripta Body` inside a fenced `text` block to preserve indentation.

Use this skeleton:

````md
# <Document Title>

## 1. Purpose
<One or two sentences>

## 2. Defined Terms
- <term>: <definition>
- If none, write `- None.`

## 3. Lex Scripta Body
```text
<Parent statement>
    <Child condition or scope>
        <Exception, approval rule, or detailed constraint>
```

## 4. Open Items
- <Question or missing fact>
- If none, write `- None.`

## 5. Assumptions
- <Working assumption>
- If none, write `- None.`

## 6. Evidence / Notes
- <Source interpretation note or contextual note>
- If none, write `- None.`

## 7. Risks / Conflicts
- <Conflict, risk, or unresolved tension>
- If none, write `- None.`
````

## Missing-information policy

Transform the input even when information is incomplete.

Never block the output because of missing details. Instead:

- keep the logic that is already supported by the source
- mark absent facts explicitly
- move unresolved questions into `Open Items`
- move ambiguous interpretation notes into `Evidence / Notes`

## Conflict policy

Resolve competing statements only when the source clearly establishes priority.

Use this priority order:

1. explicit agreement over tentative suggestion
2. later confirmed decision over earlier draft
3. direct instruction over implied preference

If priority is still unclear, preserve the conflict in `Risks / Conflicts`.

## Time normalization

If a reliable reference date is present, convert relative time into a concrete date or date range.

If not, keep the original phrasing and mark the missing anchor in `Open Items`.

Example:

- `next month` -> keep as `next month` and add `[Reference date needed]` if no anchor exists
- `within two weeks of hire` -> keep as relative timing because the anchor is intrinsic to the rule

## Quick example

Source:

```text
We need the beta out next month.
Email-only sign-up for now.
Phone verification can wait.
Enterprise customers may need a company email check.
Minji owns design.
Backend goes first.
Exact date next meeting.
```

Output shape:

````md
# Beta Release and Signup Flow

## 1. Purpose
Turn rough planning notes into a structured release and onboarding document.

## 2. Defined Terms
- Enterprise customer: A customer account expected to use a company-managed email domain.

## 3. Lex Scripta Body
```text
The beta release is targeted for next month.
    The exact release date must be confirmed in the next meeting.

The initial signup flow follows a minimum-information rule.
    Only email is collected at signup.
    Phone verification is excluded from the initial beta scope.
        Enterprise customers may require a company email verification step.

Minji owns the design work.
Backend implementation is sequenced before dependent work.
```

## 4. Open Items
- The reference date for `next month` is [Unspecified].

## 5. Assumptions
- None.

## 6. Evidence / Notes
- `Email-only sign-up for now` was normalized into a minimum-information rule.

## 7. Risks / Conflicts
- None.
````

## Further reading

- [Detailed reference](references/REFERENCE.md)
- [Examples](references/EXAMPLES.md)
- [Output checklist](references/OUTPUT-CHECKLIST.md)
- [Reusable output template](assets/output-template.md)
