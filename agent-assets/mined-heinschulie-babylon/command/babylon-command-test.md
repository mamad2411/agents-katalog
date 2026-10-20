# Application Validation Test Suite

Execute comprehensive validation tests for frontend, backend, and ADW components, returning results in a standardized JSON format for automated processing.

## Purpose

Proactively identify and fix issues before they impact users. This suite:
- Detects type errors, import failures, and broken Svelte components
- Runs Convex backend tests (convex-test + edge-runtime)
- Runs frontend unit tests (Vitest + jsdom)
- Runs ADW workflow tests
- Verifies builds across the monorepo

## Variables

TEST_COMMAND_TIMEOUT: 5 minutes

## Instructions

- Execute each test in the sequence provided below
- Capture the result (passed/failed) and any error messages
- IMPORTANT: Return ONLY the JSON array with test results
  - IMPORTANT: Do not include any additional text, explanations, or markdown formatting
  - We'll immediately run JSON.parse() on the output, so make sure it's valid JSON
- If a test passes, omit the error field
- If a test fails, include the error message in the error field
- Execute all tests even if some fail
- Error Handling:
  - If a command returns non-zero exit code, mark as failed and immediately stop processing tests
  - Capture stderr output for error field
  - Timeout commands after `TEST_COMMAND_TIMEOUT`
  - IMPORTANT: If a test fails, stop processing tests and return the results thus far
- All file paths are relative to the project root

## Test Execution Sequence

### Backend Tests (Convex)

1. **Convex Backend Tests**
   - Command: `cd apps/web && bun run test:run`
   - test_name: "convex_backend_tests"
   - test_purpose: "Runs all Convex backend tests (convex-test with edge-runtime) and web app unit tests (jsdom) via Vitest"

### Frontend Tests

2. **SvelteKit Type Check (Web)**
   - Command: `cd apps/web && bun run check`
   - test_name: "web_typecheck"
   - test_purpose: "Runs svelte-check against the web app — catches type errors, invalid Svelte 5 runes usage, missing imports, and component prop mismatches"

3. **SvelteKit Type Check (Verifier)**
   - Command: `cd apps/verifier && bun run check`
   - test_name: "verifier_typecheck"
   - test_purpose: "Runs svelte-check against the verifier app — catches type errors, invalid Svelte 5 runes usage, missing imports, and component prop mismatches"

4. **Web Build**
   - Command: `cd apps/web && bun run build`
   - test_name: "web_build"
   - test_purpose: "Full production build of the web app — validates Vite bundling, Paraglide i18n compilation, SvelteKit adapter-node output, and Tailwind CSS processing"

5. **Verifier Build**
   - Command: `cd apps/verifier && bun run build`
   - test_name: "verifier_build"
   - test_purpose: "Full production build of the verifier app — validates Vite bundling, Paraglide i18n compilation, SvelteKit adapter-node output, and Tailwind CSS processing"

### ADW Tests

6. **ADW Workflow Tests**
   - Command: `bun run adw:test`
   - test_name: "adw_tests"
   - test_purpose: "Runs ADW workflow tests (agent-driven workflow integration tests) via Vitest"

## Report

- IMPORTANT: Return results exclusively as a JSON array based on the `Output Structure` section below.
- Sort the JSON array with failed tests (passed: false) at the top
- Include all tests in the output, both passed and failed
- The execution_command field should contain the exact command that can be run to reproduce the test
- This allows subsequent agents to quickly identify and resolve errors

### Output Structure

```json
[
  {
    "test_name": "string",
    "passed": boolean,
    "execution_command": "string",
    "test_purpose": "string",
    "error": "optional string"
  }
]
```

### Example Output

```json
[
  {
    "test_name": "web_typecheck",
    "passed": false,
    "execution_command": "cd apps/web && bun run check",
    "test_purpose": "Runs svelte-check against the web app — catches type errors, invalid Svelte 5 runes usage, missing imports, and component prop mismatches",
    "error": "Error: Type 'string' is not assignable to type 'number' (src/routes/+page.svelte:42)"
  },
  {
    "test_name": "convex_backend_tests",
    "passed": true,
    "execution_command": "cd apps/web && bun run test:run",
    "test_purpose": "Runs all Convex backend tests (convex-test with edge-runtime) and web app unit tests (jsdom) via Vitest"
  }
]
```

## Step Summary

IMPORTANT: You MUST end your output with this exact block. Fill in each field with a single line.

## Step Summary
- status: pass | fail
- action: <one line describing what you did>
- decision: <one line -- key choice and why>
- blockers: <one line, or "none">
- files_changed: <comma-separated list, or "none">