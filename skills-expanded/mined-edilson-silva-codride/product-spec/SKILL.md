---
name: product-spec
description: Expand a validated requirement into a full PRD
---

You're acting as a product specialist helping a human take an issue's requirement to its final stage, ready for build.

If this doesn't already have a GitHub issue and refined requirement behind it, and the task is small/well-understood, `product-quick-spec` produces the same output (FR-XX + BDD feature file) in one step — consider redirecting there instead of forcing this staged process on something that doesn't need it.

Your goal is to take an initial requirement and understand it deeply.

The user's request should point to the requirement to expand — a GitHub issue number, or the requirement text itself. If neither is given, ask which one they mean rather than guessing.

1. **Validate the current requirements.** Review what you were given and confirm it contains the essentials:
   - WHY we're doing this
   - WHAT is being built
   - HOW it's being built — less important than the other two, but good to have a sense of it

   If the initial requirements aren't enough to move on to a PRD, ask the user clarifying questions and update the requirement artifact/issue before proceeding. Don't assume anything — ask.

2. **Check the project's master docs** to identify any specific rule to follow, or whether this request violates a master doc. If it does, ask for clarification and only proceed if the user says to.

3. **Build your understanding of the key PRD elements:**

   - **Product overview**: problem statement and market opportunity, target users and personas, product vision and goals, success metrics and KPIs
   - **Functional requirements**: core features and capabilities, user stories or use cases, user flows and interactions, technical specs, API requirements (if applicable). Number each discrete requirement `FR-01`, `FR-02`, ... — this numbering carries through to the acceptance criteria below and to the feature file in step 6.
   - **Acceptance criteria (BDD)**: for each `FR-XX`, write the scenarios that define "done" as `Given/When/Then`:
     ```
     Given [starting state]
     When [the user does something]
     Then [expected outcome]
     ```
     Keep scenarios concrete and testable — they become the contract `engineer-work` implements against and `engineer-coverage` checks against. Cover the happy path plus the edge cases that actually matter (don't pad with trivial ones). Skip this for requirements too small to need it.
   - **Non-functional requirements**: performance benchmarks, security/compliance needs, scalability requirements, accessibility standards
   - **Design and UX**: UI/UX guidelines, wireframes or mockups, design-system references, platform-specific considerations
   - **Technical considerations**: architecture overview, integration requirements, data requirements, third-party dependencies
   - **Project details**: risks and mitigation strategies, release criteria and rollout plan
   - **Constraints and assumptions**: technical constraints, business constraints, key assumptions being made

   Don't overthink this. If the issue doesn't call for some of these, skip them — less is more, but don't drop important details.

4. Present your understanding to the user, along with any clarifications needed. Iterate until you have 100% clarity.

5. Once the user approves, edit the requirement artifact/issue/file, enriching it with what was discovered.

6. **Save (or update) `docs/business-context/features/<slug>.md`** — this is what makes the feature visible to `product-sync-github`; without it, the PRD only lives on the issue and never gets tracked there. Use a kebab-case slug derived from the feature title. Format:

   ````markdown
   # [Feature Title]

   **Status**: Planned
   **Priority**: [Critical | High | Medium | Low]
   **Scope**: [MVP | Phase 2 | Phase 3 | ...]
   **Module**: [if this project groups features by module; omit otherwise]

   [1-2 paragraph product overview]

   ### FR-01: [Requirement title]
   [Description]

   **Acceptance criteria:**
   ```
   Given ...
   When ...
   Then ...
   ```

   ### FR-02: [Next requirement]
   [Same structure]
   ````

   If `docs/business-context/features/` doesn't exist yet, create it. If the file already exists (this feature was specced before), update it rather than duplicating.
