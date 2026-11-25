---
name: fix-openapi-spec
description: Use when asked to identify and fix errors in an OpenAPI specification that are preventing it from running as mock or test
---

# Fix OpenAPI Spec

Use this skill when the task is to diagnose an OpenAPI specification that is preventing it from running as mock or test.

## Reading Rule

- Read this entire `SKILL.md` before taking any action.
- Do not assume the workflow is complete until the end of the file has been read.
- Any later instruction that refers to scripts or path resolution is mandatory and overrides earlier assumptions.

## Canonical Paths

Use these exact paths and file names everywhere in this workflow.

- Editable spec copy: `<spec-name>-updated.<ext>`
- Actions log: `fix-log-<spec-name>-<current-date>.md`

## Script Location Rule

- The loop-test and validation scripts live in the skill bundle directory.
- Resolve script paths from the fix-openapi-spec skill directory (this directory), not from the current working directory.
- On MacOS or Linux, use the bash scripts:
  - **`scripts/run_loop_test.sh`** - runs the loop test
  - **`scripts/validate_spec.sh`** - validates a spec
- On Windows, use the PowerShell scripts:
  - **`scripts/run_loop_test.ps1`** - runs the loop test
  - **`scripts/validate_spec.ps1`** - validates a spec

## Workflow State Machine

Phase 1 -> Phase 2 -> Phase 3 -> Phase 4 validation -> STOP for user approval -> Phase 4 fixes only if explicitly approved

- Phase 2 is mandatory and must not be skipped just because the spec parses as YAML or OpenAPI.
- Do not stop after syntax checks, file copy creation, or structural validation; always run the loop test on the `-updated` spec unless a tool failure, sandbox restriction, or explicit user interruption prevents it.

## Docker Execution Rule

- Assume Docker is available and the Docker engine is running.
- Do not ask the user about Docker availability before attempting `scripts/run_loop_test.sh`, `scripts/run_loop_test.ps1`, `scripts/validate_spec.sh`, or `scripts/validate_spec.ps1`.
- Always run the script once before concluding that validation or loop testing is unavailable.
- If the script fails, inspect the output to determine whether the failure is Docker-specific. Docker-specific failures include Docker not being installed, Docker not being on `PATH`, Docker Desktop being unavailable, the Docker daemon / engine not running, or Docker access being denied due to permissions.
- If the Docker-specific failure appears permission-related, retry using your environment’s built-in privilege escalation mechanism, if one is available.
- Do not retry with privilege escalation for Docker failures that escalation cannot fix, such as Docker not being installed, Docker not being on `PATH`, Docker Desktop being unavailable, or the Docker daemon / engine not running.
- If the final script result is still a Docker-specific failure or permission related failure,
  - If privilege Escalation has been denied by an auto-reviewer, then display the following message: `Please provide explicit approval to use Specmatic docker image and license file`
  - Otherise, stop and ask the user exactly: `Please confirm if docker engine is running and accessible`
- Do not claim that validation or loop testing is unavailable unless the script was run and the final result was a Docker-specific failure.
 
## Script Execution Rule

- If a script reports that an action is required from the user, report this verbatim to the user. Do not move ahead until the user has responded with the required information or action.

## Working area

Ignore any old test files or log files that existed before this conversation. You'll work with the output of the relevant commands as per the workflow state machine.

### Phase 1: Setup

1. Create a copy of the input spec path for edits named `<spec-name>-updated.<ext>` in the same directory as the source spec.
  - Note: Always edit the `-updated` copy, not the original spec.
2. Create a single append-only actions log file named `fix-log-<spec-name>-<current-date>.md` in the spec directory, with the following initial content:
  ```
  # Actions log for <spec-file>

  ```
### Phase 2: Auto-fix obscure errors

1. Run the loop test script against the editable copy.
2. Immediately after the loop test ends, append a structured entry to `fix-log-<spec-name>-<current-date>.md` with this format:
  ```
  ## <title>
  **Timestamp**: <timestamp>
  **Action**: Loop test run
  **Result**: [pass|fail] - <brief description of the result>

  ```
3. If the loop test passes, go to step 5, the final check. All failed tests are considered "must-fix" errors.
4. If the loop test fails, attempt to fix one of the errors following the guidelines for addressing errors, and then go back to step 1.
5. If any must-fix errors remain to be addressed, go back to step 1 and repeat the process until all must-fix errors have been addressed.
6. Final check: once all the tests are passing, go back to step one and run the loop test again to make sure that there are no errors left.

Guidelines for addressing errors:
- Classify every failure before moving on:
  - `Spec Issue`: the run points to a concrete schema, example, enum, `$ref`, `required`, or constraint defect in the spec.
  - `Specmatic Bug`: the error is unclear (does not identify a concrete spec defect or provide enough information to point directly to where the issue is), or if it appears that Specmatic cannot handle a value / feature in the spec that is perfectly legimiate (e.g. valid regex syntax, valid OpenAPI syntax, etc)
  - Treat any opaque error as a `Specmatic Bug`. "Opaque" means the message does not identify a concrete spec defect or does not provide enough information to fix the spec confidently.
  - If relaxing or removing a valid constraint is used to make the workflow pass, log it as a `Specmatic Bug`.
  - A status mismatch is not opaque merely because the final summary only shows `R0002`. Before classifying it as `Specmatic Bug`, inspect the raw temp test log around the full request/response transcript. Look both above and below the failed scenario summary. Only classify as opaque if no response body or adjacent transcript contains a concrete contract path or rule violation.
  - If Specmatic-generated traffic fails against the same specification, classify it as `Specmatic Bug` unless the failing constraint is itself invalid OpenAPI, invalid syntax, or demonstrably conflicts with another schema rule such as enum/example values.


- If the issue is classified as a `Specmatic Bug`, log it immediately when first observed in `fix-log-<spec-name>-<current-date>.md`, using this format:
  ```
  ## <title>
  **Timestamp**: <timestamp>
  **Action**: Issue Classification
  **Error**: <error message that prompted this bug classification>
  **Classification**: Specmatic Bug
  **Reason**: <why this is considered a Specmatic Bug instead of a concrete spec defect>
  **Logs**: <log snippet showing the issue that prompted the fix>

  ```

- If the issue is classified as a `Spec Issue`, log it immediately when first observed in `fix-log-<spec-name>-<current-date>.md`, using this format:
  ```
  ## <title>
  **Timestamp**: <timestamp>
  **Action**: Issue Classification
  **Error**: <error message that prompted this bug classification>
  **Classification**: Spec Issue
  **Reason**: <why this is considered a Spec Issue instead of a Specmatic Bug>
  **Logs**: <log snippet showing the issue that prompted the fix>

  ```

- Do not wait for the bug to be resolved before logging it.
- Form a hypothesis about the cause of the error, and whether there is an allowed fix which you have not yet tried that will resolve it. Even if the error seems unclear or opaque, form a hypothesis anyway, make your best guess, based on the error message, field names, and schema context.
- If allowed fixes are available to be tried as per the "Allowed fixes" section,
  - attempt the fixes in order of preference as outlined,
  - Immediately after applying a fix, append a structured entry to `fix-log-<spec-name>-<current-date>.md` with the format:
  ```
  ## Fix: <summary of the fix>
  **Timestamp**: <timestamp>
  **Action**: Fix applied
  **Fix**: <description>
  **Reason**: <why you think this fix should resolve the issue>
  **Logs**: <log snippet showing the issue that prompted the fix>

  ```
  - Then go back to Step 1 of this phase and run the loop test again to see if the fix resolved the issue.

- However if there are no more allowed fixes left to try and the issue remains unresolved, consider the issue addressed and log a "Specmatic Bug" entry in the following format:
  ```
  ## Unfixable: <summary of the bug>
  **Timestamp**: <timestamp>
  **Action**: Dropping issue as unfixable
  **Classification**: Specmatic Bug
  **Reason**: <Why you concluded that this was unfixable>
  **Logs**: <log snippet showing the issue that prompted this conclusion>

  ```
- When logging a failed loop run, include the most specific inner contract error found in the response body. Do not log only the outer status mismatch if the response body contains a deeper rule violation.

  For example, log:
  `REQUEST.QUERY.path.to.something <error>` or `RESPONSE.BODY.path.to.something <error>` or

  instead of:
  `confirm-payment-source returned 400 instead of 200`.

### Phase 3: Report on auto-fix phase

Prepare a console report for the user. Do not mention mechanics such as test execution details, mock startup details, or pass/fail runtime chatter.

1. Read fix log at `fix-log-<spec-name>-<current-date>.md` in order to identify Specmatic bugs and applied fixes. Do not depend on memory.
2. If it contains `Classification**: Specmatic Bug`, the final response MUST include a `Specmatic bugs:` section.
3. If it contains `Fix applied`, the final response MUST include a `Fixes applied:` section.
4. Specmatic bugs section should be followed by the Fixes applied section if both exist, else just the one that exists should be printed.
5. If any Specmatic bugs exist, the final response MUST say to send:
    - original spec
    - updated spec
    - fix log
6. Do not substitute validation/test summaries for these sections.

The format for the Specmatic bugs section is:

```
Specmatic bugs:
- <bug title>: <brief description of the bug>
- <bug title>: <brief description of the bug>

Please send the following files to the Specmatic team for analysis:
- <original spec file>
- <updated spec file>
- <fix log file>
```

The format for the list of fixes applied is:

```
Fixes applied:
- <item fixed>: <brief description of the fix>
- <item fixed>: <brief description of the fix>
```

### Phase 4: Address load time errors and warnings

Note: Even if the user asks to fix the spec, they really want control over what gets fixed, and how the fix is done. So Phase 4 validation may be run automatically, but Phase 4 fixes must never be applied automatically.

1. Run the validate command on the `<spec-name>-updated.<ext>` spec.
2. If there are no errors or warnings, report to the user that the spec is now valid and can be used for testing and mocking with Specmatic, and end the process.
3. If there are errors or warnings, do NOT fix any errors or warnings. Do not infer approval from the original request, or from prior sessions. Only proceed if the next user message explicitly approves fixing the listed Phase 4 issues or requests specific fixes. Instead, list them out (not just the ids, include the descriptions if Specmatic provided it), and ask the user if they want to address spec defects on the `-updated` copy.
4. For each load-time error or warning that the users wants to address:
  - Classify and log the error following the same classification and logging contract as in Phase 2.
6. Apply allowed fixes to the `-updated` copy based on the error messages and classification, following the same guidelines for allowed fixes as in Phase 2.
7. Repeat this phase until all actionable load-time errors are addressed.
8. If you conclude that an issue cannot be fixed using allowed fixes, log it as a "Specmatic Bug" following the same contract as in Phase 2, consider it addressed.

## Disallowed fixes

The following changes are not allowed:
- Widening a JSON schema from `additionalProperties: false` to `additionalProperties: true`
- Dropping a property from a JSON schema completely. At most you may make properties optional or mandatory
- Changing descriptions, titles, summaries, and other metadata (these are never parsed by Specmatic)
- Avoid changing the request or response datatype
- Remove a security scheme from an API

## Allowed fixes

Guidelines for fixing constraints and examples:
- If you feel that an obscure must-fix error is related to a constraint (datatype is still correct but constraint such as regex, minLength, maximum, etc is broken), attempt the following fixes in order of preference:
  - If the constraint syntax is invalid, fix the syntax and re-attempt the loop test.
  - If the loop test fails, then based on the field name and schema context, make an educated guess, update the constraint, and re-attempt the loop test.
  - Final option, remove the constraint and re-attempt the loop test.
- When an enum does not match the schema constraint, remove the constraint.
- When an example value does not match schema, update the example value to something meaningful based on the datatype and field name.
- If you get an error saying expected X status but got 400, it means the mock didn't like the request. You will find details adjacent to that message saying why the 400 was returned by the mock.
- For regexes, Specmatic uses the dk.brics.automaton.Regexp library, which supports a specific regex syntax found in `references/briks-automaton-regex-rules.md`.

### When a scenario fails with HTTP status mismatch

  If a loop test reports `R0002: HTTP status mismatch`, do not classify it as opaque until you inspect the request/response transcript for
  that same failed scenario.

  Specmatic often prints the detailed contract failure inside the mock response body, before the final `Unsuccessful Scenarios` summary.
  Search upward from the failed scenario or from `Specification expected status ... but response contained status 400` for the nearest
  preceding:

  - `Response at ...`
  - `X-Specmatic-Result: failure`
  - `Error from contract <spec-file>`
  - `>> REQUEST...`
  - `R1003`, `R000x`, `OAS00xx`, or any schema path

  If the response body contains a concrete `>> REQUEST...` or `>> RESPONSE...` path, treat that as the primary failure, not the outer
  `R0002` status mismatch.

  Example:
  - Outer error: `Specification expected status 200 but response contained status 400`
  - Response body detail: `>> REQUEST.BODY.payment_source.card.network_token.cryptogram`
  - Classification: Spec Issue if the path points to a concrete schema constraint that can be fixed.

## Logging Contract (Mandatory)

- After every loop test run: append one loop-run entry to `fix-log-<spec-name>-<current-date>.md`.
- After every applied fix: append one fix entry to `fix-log-<spec-name>-<current-date>.md`.
- For every observed `Specmatic Bug` or `Spec Issue`: append one matching classification entry to `fix-log-<spec-name>-<current-date>.md`.
