---
name: atdd-bdd-testing
description: >-
  Derive acceptance tests collaboratively from user stories and acceptance criteria,
  test-first, per ISTQB CTFL v4.0 §4.5 (Collaboration-based Test Approaches). Use when:
  "ATDD," "BDD," "acceptance criteria," "acceptance test," "受入基準," "受入テスト,"
  "user story testing," "Given/When/Then," "Three Amigos," "Cucumber/SpecFlow/Behave,"
  or turning a story into executable specs. Produces user stories + acceptance criteria
  (design mode) and executable acceptance tests (implementation mode). Not for:
  low-level input partitioning of a single field — use equivalence-partitioning /
  boundary-value-analysis. Related: equivalence-partitioning, test-strategy-doc.
license: MIT
metadata:
  version: "1.0"
  istqb: "CTFL v4.0 §4.5 (§4.5.1–4.5.3)"
  iso25010: [functional-suitability]
  mode: [design, implementation]
---

# ATDD / BDD Acceptance Testing

Turn a user story into acceptance tests written BEFORE the code, agreed by business,
dev, and test together — so "done" means the criteria pass, not "it compiles."

## Objective

Acceptance criteria and acceptance tests derived collaboratively and test-first. Per
CTFL v4.0 §4.5, collaboration-based approaches add **defect avoidance** through
communication (on top of the defect *detection* the other techniques give). The failure
mode this prevents: acceptance criteria written after implementation (rubber-stamping),
or ambiguous stories that pass review and then fail the user.

## Organization-specific inputs (fill these in)

- **Story & acceptance-criteria format**: which template/standard the team uses.
- **BDD tooling**: Cucumber / SpecFlow / Behave / pytest-bdd — or none (plain tests);
  where step definitions live and their reuse conventions.
- **Definition of Done**: does it require all acceptance tests green?
- **Three Amigos**: who represents business, development, and testing in refinement.

## Context Discovery

- Is there a user story with acceptance criteria already, or does it need writing?
- Which criteria format fits — scenario-oriented (Given/When/Then) or rule-oriented?
- Is a BDD framework present in the repo (detect Cucumber/SpecFlow/Behave/pytest-bdd)?
- Are there non-functional acceptance criteria (performance, security) to include?

## Instructions

1. **Collaborative user story writing** (§4.5.1): apply the **3 C's** — *Card* (the
   story medium), *Conversation* (how the software will be used), *Confirmation* (the
   acceptance criteria). Refine with the Three Amigos so the story is shared, not
   author-owned. (INVEST is a widely-used industry heuristic for good stories —
   independent/negotiable/valuable/estimable/small/testable — applied here as practice.)

2. **Write acceptance criteria** (§4.5.2) in one of the two CTFL formats, per criterion:
   - **Scenario-oriented** — `Given <context> When <event> Then <outcome>` (the BDD
     format).
   - **Rule-oriented** — a bulleted verification list, or a tabulated input→output
     mapping.
   Cover positive, negative, and any non-functional criteria — not just the happy path.

3. **Derive tests test-first** (ATDD, §4.5.3): create the acceptance test cases from the
   criteria BEFORE the story is implemented. They may be run manually or automated.

4. **Make them executable** (implementation): map each Given/When/Then to step
   definitions (Cucumber/Behave/SpecFlow/pytest-bdd) or plain tests. Keep steps at the
   behavior level and reusable — not brittle UI click-by-click scripts.

5. **Trace**: every acceptance criterion maps to at least one acceptance test; the story
   is done only when all pass. Feed edge/negative criteria from the black-box techniques.

## Output Format

### design mode

User story + acceptance criteria in both CTFL formats:

```
Story: As a <role>, I want <capability>, so that <benefit>.

Acceptance criteria — scenario-oriented (BDD):
  Scenario: Refund within window
    Given an order delivered 5 days ago
    When the customer requests a refund
    Then the refund is approved

Acceptance criteria — rule-oriented:
  - Refund allowed only within 30 days of delivery
  - Refund denied for consumable goods once opened
```

### implementation mode

Executable spec (Gherkin-syntax feature + step skeleton; adapt to the repo's runner):

```gherkin
Feature: Refunds
  Scenario: Refund within window
    Given an order delivered 5 days ago
    When the customer requests a refund
    Then the refund is approved
```

```python
# steps (pytest-bdd / behave style)
@given("an order delivered 5 days ago")
def delivered_order(): ...
@then("the refund is approved")
def refund_approved(ctx): assert ctx.response.status == "approved"
```

> Note: ISTQB v4.0 names **BDD** and the **Given/When/Then** format; "**Gherkin**" is the
> common industry syntax/tooling name for that format and is not a syllabus term.

## Anti-Patterns

- **Criteria written after the code** — rubber-stamping, not ATDD. **Guard:** ATDD is
  test-first; acceptance criteria and tests come before implementation.
- **Happy-path only** — no negative or edge criteria. **Guard:** add negative and
  boundary criteria (pair with equivalence-partitioning / boundary-value-analysis).
- **Given/When/Then theater** — imperative, UI-coupled steps that break constantly.
  **Guard:** keep scenarios declarative and behavior-level; reuse step definitions.
- **Solo-authored stories** — skipping the Conversation. **Guard:** the 3 C's require a
  Three-Amigos conversation; a story written alone misses shared understanding.
- **Calling the syntax "Gherkin" as if ISTQB does** — **Guard:** attribute Given/When/
  Then + BDD to CTFL §4.5.2; treat "Gherkin" as industry tooling, cited as such.

## Related Skills

- `equivalence-partitioning`, `boundary-value-analysis` — supply the negative/edge
  acceptance criteria the happy-path scenarios miss.
- `test-strategy-doc` — decides where collaboration-based approaches fit in the strategy.

## References

- ISTQB CTFL v4.0 Syllabus §4.5 (Collaboration-based Test Approaches): §4.5.1
  Collaborative User Story Writing (3 C's), §4.5.2 Acceptance Criteria (scenario-oriented
  Given/When/Then / BDD, and rule-oriented), §4.5.3 Acceptance Test-Driven Development
- "Gherkin" — industry syntax for the Given/When/Then format (not a CTFL term);
  INVEST (Wake, 2003) — industry heuristic cited in the syllabus bibliography
