---
name: business-analyst
description: Analyze and maintain requirements, user stories, and test cases. Use when asked to "find gaps", "check consistency", "write user stories", "review requirements", "check traceability", "write acceptance criteria", or "audit test coverage".
---

# Requirements Analysis
Reading and understanding what the product must do — and what it must not do.
- Parse business requirements documents and identify scope boundaries
- Flag ambiguous, contradictory, or missing requirements
- Distinguish functional requirements (what the system does) from non-functional requirements (how it performs)
- Identify assumptions that need explicit confirmation from stakeholders

# Gap Detection
Finding what is specified but not built, built but not specified, or specified inconsistently across documents.
- Cross-reference requirements, user stories, and test cases to find coverage holes
- Identify modules or features with requirements but no stories (and vice versa)
- Check that test cases exist for each acceptance criterion
- Flag broken cross-references, stale links, and wrong file/section references
- Produce structured gap reports: severity (critical / inconsistency / naming), location, and recommended fix

# User Story Writing
Translating requirements into actionable development units.
- Follow the "As a … I want … So that …" format with a clear role, goal, and rationale
- Write acceptance criteria as explicit, testable conditions (Given/When/Then or checklist style)
- Ensure each story is independent, negotiable, valuable, estimable, small, and testable (INVEST)
- Assign story IDs that follow the project's existing naming convention (e.g. US-MP-001)
- Link each story back to its requirement source

# Traceability
Keeping requirements, stories, and tests aligned as the product evolves.
- Maintain a traceability matrix: requirement → user story → test case
- When a requirement changes, identify which stories and tests are affected
- When a test is added or removed, check whether the originating story and requirement are still covered
- Flag orphaned tests (no story), orphaned stories (no requirement), and untested stories

# Acceptance Criteria Review
Ensuring that "done" is unambiguous before work starts.
- Verify each acceptance criterion is testable (can be confirmed pass/fail)
- Check that criteria cover the happy path, edge cases, and error conditions
- Identify criteria that are too vague ("works correctly", "displays properly") and rewrite them with concrete, measurable expectations
- Confirm criteria do not contradict each other within the same story or across related stories

# Test Case Alignment
Bridging stories and QA plans.
- Map test case IDs to the user story or requirement they verify
- Identify test cases that reference outdated or non-existent requirements
- Check that test case expected results are consistent with acceptance criteria
- Flag test cases marked ✅ Pass whose underlying requirement has since changed

# Scope & Prioritisation
Helping teams decide what to build and in what order.
- Identify MVP-critical requirements vs. nice-to-have features
- Flag scope creep: features that appear in tests or code but not in requirements
- Group related stories into logical delivery increments
- Surface dependencies between stories (e.g. story B cannot be built until story A is done)

# Documentation Hygiene
Keeping the project's specification artefacts clean and navigable.
- Enforce consistent naming conventions across requirement files, story files, and test sections
- Ensure cross-document links (e.g. requirement file references in user stories) are correct and up to date
- Maintain module-level indices (e.g. README tables that map modules to their stories)
- Flag stale issue log entries that reference fixed or superseded documents
