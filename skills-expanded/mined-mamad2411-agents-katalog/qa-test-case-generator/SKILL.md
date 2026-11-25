---
name: qa-test-case-generator
description: "**WORKFLOW SKILL** — Generate detailed test cases from test scenarios. USE FOR: expanding high-level test scenarios into step-by-step executable test cases; producing test cases with precise steps, data, and expected results; generating BDD/Gherkin format; creating data-driven test case variants; building regression suites from scenario lists. DO NOT USE FOR: reading Jira stories (use qa-test-planner); writing automation code; executing tests. INVOKES: file tools (write test case documents)."
argument-hint: "Provide test scenarios, a scenario list, or describe the feature to test"
---

# QA Test Case Generator

Act as a senior QA engineer who specializes in writing detailed, executable test cases. Take high-level test scenarios and expand them into precise, step-by-step test cases ready for manual execution or automation scripting.

## When to Use

- User provides test scenarios and wants detailed test cases
- User has a feature description and wants executable test steps
- User needs test cases in a specific format (table, Gherkin, structured)
- User wants data-driven variants generated from a base test case
- User asks to expand a scenario list into full test cases

## Relationship to qa-test-planner

The `qa-test-planner` skill produces **test scenarios** (what to test). This skill takes those scenarios and produces **test cases** (exactly how to test it). They can be chained:

```
Jira Story → [qa-test-planner] → Test Scenarios → [qa-test-case-generator] → Test Cases
```

## Procedure

### Phase 0 — Preparation (Required)

1. **Read test data knowledge** 
 
   - Review the `./docs/test-data-knowledge.md` document to know how to incorporate specific test data into the test cases, such as student accounts, environment URLs, and login credentials. This will allow you to create test cases that are directly actionable and relevant to the testing context.

   - Review the relevant functional flow instructions in `./docs/test-flows-guidance.md` to ensure that the designed test cases accurately reflect the expected user journeys and system behaviors.

### Phase 1 — Understand the Scenarios

1. **Review input.** Accept scenarios in any of these forms:
   - Structured scenarios from `qa-test-planner` (TS-{ID} format)
   - A bullet list of things to test
   - A feature description the user wants test cases for
   - Existing test cases to expand or improve

2. **Identify the application context.** Determine:
   - **Application type**: Web UI, API, mobile, desktop, data pipeline
   - **Domain**: E-commerce, healthcare, education, finance, etc.
   - **Key entities**: What objects/data are involved (orders, users, products, etc.)

3. **Confirm output format.** Ask if not obvious:

   | Format | Best For |
   |--------|----------|
   | Structured (default) | Manual execution, review |
   | Gherkin / BDD | Automation with Cucumber/SpecFlow |
   | Markdown table | Documentation, spreadsheet import |
   | Checklist | Quick smoke/sanity testing |

### Phase 2 — Design Test Cases

4. **Expand each scenario into one or more test cases.** Apply these principles:

   **a) Atomic steps.** Each step must be a single user action or system verification. Never combine two actions in one step.
   
   - Bad: "Log in and navigate to the order page"
   - Good: Step 1: "Navigate to login page" → Step 2: "Enter credentials" → Step 3: "Click Sign In" → Step 4: "Navigate to Orders"

   **b) Observable expected results.** Every step that changes state must have a verifiable expected result.
   
   - Bad: "System processes the order"
   - Good: "Order confirmation page displays with order ID, items, and total in CAD"

   **c) Specific test data.** Never use placeholders like "valid data." Always specify exact values.
   
   - Bad: "Enter valid credentials"
   - Good: "Enter username: `testuser@institution.edu`, password: `Test@1234`"

   **d) Independent test cases.** Each test case should be executable without relying on another test case's outcome, unless explicitly marked as a dependent chain.

5. **Write test cases** using this structure:

   ```
   ┌─────────────────────────────────────────────────────┐
   │ TC-{ID}: {Clear, action-oriented title}              │
   ├─────────────────────────────────────────────────────┤
   │ Scenario:      TS-{ref} (if applicable)              │
   │ Type:          Positive | Negative | Boundary | E2E  │
   │ Priority:      P0 | P1 | P2 | P3                    │
   │ Module:        {Feature area}                        │
   │ Preconditions:                                       │
   │   1. {Required state before test begins}             │
   │   2. {Required data / environment}                   │
   │ Test Data:                                           │
   │   - field: value                                     │
   │   - field: value                                     │
   ├─────────────────────────────────────────────────────┤
   │ # │ Step                      │ Expected Result      │
   │───│───────────────────────────│──────────────────────│
   │ 1 │ {Single user action}      │ {Observable result}  │
   │ 2 │ {Single user action}      │ {Observable result}  │
   │ 3 │ {Verification action}     │ {Verifiable outcome} │
   ├─────────────────────────────────────────────────────┤
   │ Postconditions: {State after test completes}         │
   │ Notes: {Edge cases, environment specifics}           │
   └─────────────────────────────────────────────────────┘
   ```

6. **For Gherkin/BDD format**, use:

   ```gherkin
   @{tag} @{priority}
   Scenario: {Descriptive title}
     Given {precondition / initial state}
       And {additional precondition}
     When {user action}
       And {additional action}
     Then {expected outcome}
       And {additional verification}

   Scenario Outline: {Title with parameterization}
     Given {precondition with <variable>}
     When {action with <variable>}
     Then {outcome with <variable>}

     Examples:
       | variable1 | variable2 | expected |
       | value1    | value2    | result1  |
       | value3    | value4    | result2  |
   ```

### Phase 3 — Generate Variants

7. **Create data-driven variants** when the scenario has combinatorial dimensions:

   - Identify the dimensions (region, role, product, quantity, payment, etc.)
   - Create a **base test case** with parameterized fields
   - Generate a **variants table** showing all combinations to execute:

   | Variant | Region | Product | Programs | Payment | Currency |
   |---------|--------|---------|----------|---------|----------|
   | V1 | Canada | RPECOM | Single | Bill Institution | CAD |
   | V2 | Canada | RPECOM | Multiple | Bill Institution | CAD |
   | V3 | Canada | UsageBased | Single | Bill Institution | CAD |
   | V4 | Canada | UsageBased | Multiple | Bill Institution | CAD |

   - For >3 dimensions, apply **pairwise reduction** and note which combinations are covered

8. **Generate negative test cases** for each positive case:

   | Positive Case | Negative Variant | Input | Expected |
   |---------------|-----------------|-------|----------|
   | TC-01: Valid order | TC-01N1: Empty cart | No items selected | Error: "Please select at least one program" |
   | TC-01: Valid order | TC-01N2: Expired session | Session timeout | Redirect to login with message |
   | TC-01: Valid order | TC-01N3: Unauthorized role | Student role | Error: "Insufficient permissions" |

### Phase 4 — Organize & Deliver

9. **Group test cases** by module/feature area:

   ```
   Feature: {Name}
   ├── Positive Tests
   │   ├── TC-001: ...
   │   └── TC-002: ...
   ├── Negative Tests
   │   ├── TC-003: ...
   │   └── TC-004: ...
   ├── Boundary Tests
   │   └── TC-005: ...
   └── Data-Driven Variants
       └── TC-001-V1 through TC-001-V4
   ```

10. **Produce a summary table:**

    | TC ID | Title | Type | Priority | Scenario Ref | Automated? |
    |-------|-------|------|----------|-------------|------------|
    | TC-001 | ... | Positive | P1 | TS-01 | Candidate |
    | TC-002 | ... | Negative | P2 | TS-01 | Manual |

11. **Provide execution notes:**
    - Recommended execution order (dependencies, data setup)
    - Environment requirements
    - Test data setup/teardown instructions

## Quality Checklist

Before delivering, verify:

- [ ] Every step is atomic (one action per step)
- [ ] Every state-changing step has an expected result
- [ ] Test data is specific — no placeholders like "valid data"
- [ ] Preconditions are complete — a tester can start from scratch
- [ ] Positive and negative paths both covered
- [ ] Data-driven variants use a clear parameterization table
- [ ] Test case IDs are sequential and traceable to scenarios
- [ ] Postconditions document the end state
