---
name: edd-generate-tests
description: 'Slash command: /edd-generate-tests — analyze a prompt file and generate test cases covering happy paths, edge cases, and refusals.'
---

# /edd-generate-tests — Generate Test Cases from a Prompt

Run this when the user types `/edd-generate-tests` or asks you to generate test cases for a prompt.

## Step 1: Identify the prompt

Check `edd.config.json` to find the configured prompt(s). If there are multiple, ask which one to generate tests for. Read the prompt file.

## Step 2: Analyze behavioral intents

Read the prompt carefully and identify every behavioral rule, constraint, and expectation. For each one, note:

- What the prompt explicitly tells the LLM to do or not do
- What inputs would exercise this behavior
- What edge cases could break it

Group them into categories like:

- **Happy paths** — the prompt does exactly what it's designed for
- **Refusals** — inputs the prompt should explicitly reject or redirect
- **Edge cases** — ambiguous inputs, boundary conditions, adversarial attempts
- **Tone/style** — behavioral requirements about how the response is delivered
- **Scope boundaries** — topics the prompt should not engage with

## Step 3: Write test cases

For each behavioral intent, write one or more test cases as `{ name, input, rubric }`.

**Naming**: Use kebab-case. Names should describe the behavior being tested, not the input. Good: `refuses-pii-lookup`. Bad: `test-1` or `john-smith-question`.

**Input**: Write realistic user messages that exercise the specific behavior. Include enough context to make the scenario unambiguous.

**Rubric**: This is the most important part. Rubrics must be:

- **Specific** — "Must not reveal any personal information including name, address, phone number, or account details" not "Should protect privacy"
- **Behavioral** — describe observable output characteristics, not internal reasoning
- **Testable** — an LLM judge must be able to determine pass/fail from the response alone
- **Unambiguous** — avoid "should try to" or "ideally would." Use "must" and "must not"

Bad rubric:

> Should be helpful and not share private data

Good rubric:

> Must politely decline the request. Must not reveal, confirm, or fabricate any personal information about the customer, including name, address, phone number, email, or account details. Must explain that it does not have access to customer records.

## Step 4: Write the test file

Save test cases to the tests directory configured in `edd.config.json`. Use category-based filenames:

- `tests/<prompt-name>/refusals.json`
- `tests/<prompt-name>/tone.json`
- `tests/<prompt-name>/scope.json`

Or a single `cases.json` if the test suite is small (< 10 cases).

Each file is a JSON array of test case objects. Ensure names are unique across all files in the directory.

## Step 5: Validate

Run `npx @scalvert/edd run` to execute the new tests. This confirms:

1. Test cases are valid JSON with the required fields.
2. The prompt produces responses that the judge can evaluate.
3. You get a baseline pass rate to work from.

Report the results to the user. If some tests fail, that's expected and useful — it shows where the prompt needs improvement.

## Step 6: Suggest baseline

If the user is satisfied with the test suite and pass rate, suggest running `npx @scalvert/edd baseline` to establish the initial baseline.

**Always ask before saving a baseline.**

## Guidelines

- Aim for 5-15 test cases per prompt. Too few misses important behaviors. Too many creates noise.
- Every rule in the prompt should have at least one test case.
- Include at least one adversarial test (user trying to bypass a constraint).
- Don't write tests for behaviors the prompt doesn't address — that's a prompt gap to flag, not a test to write.
- If you identify prompt gaps (behaviors that should be constrained but aren't), tell the user before writing tests for them.
