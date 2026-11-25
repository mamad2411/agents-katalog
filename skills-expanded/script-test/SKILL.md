---
name: script-test
description: Generate a companion verification script that exercises a target script with known inputs and asserts expected outputs. Uses the fm-debug infrastructure to report pass/fail results back to the agent. At Tier 1 the developer runs the test script manually. At Tier 3 the agent deploys, runs, and reads results autonomously. Triggers on phrases like "test this script", "write a test", "verification script", "assert results", or "prove this works".
---

# Script Test

Generate a FileMaker test script that exercises a target script with known inputs, captures the results, and reports pass/fail via the Agentic-fm Debug infrastructure.

---

## Step 1: Determine the automation tier

Read `agent/config/automation.json` and check `project_tier` (preferred) or `default_tier`.

- **Tier 1** — test script goes to clipboard; the developer runs it manually and the agent reads `agent/debug/output.json`
- **Tier 3** — the agent deploys the test script, runs it via the companion, and reads results autonomously

---

## Step 2: Understand the target script

Identify the script to test. Read the human-readable version from `agent/xml_parsed/scripts_sanitized/` and determine:

1. **Parameter format** — what does it expect? (JSON, plain text, empty)
2. **Exit Script result** — what does it return? (JSON, value, empty)
3. **Side effects** — does it modify records, navigate layouts, create records?
4. **Preconditions** — what state must exist for it to work? (records in found set, specific layout, specific field values)

If the developer has provided expected inputs and outputs, use those. Otherwise, derive test cases from the script logic.

---

## Step 3: Design the test cases

Create a test plan with concrete test cases:

```
## Test plan: [Target Script Name]

### Test 1: Happy path
- Input: JSONSetElement ( "{}" ; [ "invoiceID" ; "INV-001" ; JSONString ] )
- Expected result: { "success": true }
- Expected side effect: Invoices::Status = "Sent"

### Test 2: Empty parameter
- Input: ""
- Expected result: { "success": false, "error": "missing parameter" }
- Expected side effect: none

### Test 3: Record not found
- Input: JSONSetElement ( "{}" ; [ "invoiceID" ; "NONEXISTENT" ; JSONString ] )
- Expected result: { "success": false, "error": "not found" }
- Expected side effect: none
```

Present the test plan to the developer for confirmation before generating.

---

## Step 4: Generate the test script

Build a test script as fmxmlsnippet that:

1. **Sets up preconditions** — navigate to the correct layout, ensure test data exists
2. **Calls the target script** with each test case input via `Perform Script`
3. **Captures the result** — `Get ( ScriptResult )` immediately after `Perform Script`
4. **Asserts the expected outcome** — compares actual vs expected
5. **Reports results** via Agentic-fm Debug

### Test script structure (HR format)

```
# PURPOSE: Test script for [Target Script Name]
Allow User Abort [ Off ]
Set Error Capture [ On ]

# Build results array
Set Variable [ $results ; "[]" ]
Set Variable [ $testCount ; 0 ]
Set Variable [ $passCount ; 0 ]

# --- Test 1: Happy path ---
Set Variable [ $testName ; "Happy path" ]
Set Variable [ $input ; JSONSetElement ( "{}" ; [ "invoiceID" ; "INV-001" ; JSONString ] ) ]
Set Variable [ $expected ; JSONSetElement ( "{}" ; [ "success" ; True ; JSONBoolean ] ) ]

Perform Script [ "Target Script" ; Parameter: $input ]
Set Variable [ $actual ; Get ( ScriptResult ) ]
Set Variable [ $errData ; JSONSetElement ( "{}" ;
    [ "lastError" ; Get ( LastError ) ; JSONNumber ] ;
    [ "lastErrorDetail" ; Get ( LastErrorDetail ) ; JSONString ] ;
    [ "lastErrorLocation" ; Get ( LastErrorLocation ) ; JSONString ]
) ]

# Assert
Set Variable [ $pass ; JSONGetElement ( $actual ; "success" ) = JSONGetElement ( $expected ; "success" ) ]
Set Variable [ $testCount ; $testCount + 1 ]
Set Variable [ $passCount ; $passCount + If ( $pass ; 1 ; 0 ) ]
Set Variable [ $results ; JSONSetElement ( $results ;
    [ $testCount ; JSONSetElement ( "{}" ;
        [ "test" ; $testName ; JSONString ] ;
        [ "pass" ; $pass ; JSONBoolean ] ;
        [ "expected" ; $expected ; JSONRaw ] ;
        [ "actual" ; $actual ; JSONRaw ] ;
        [ "errData" ; $errData ; JSONRaw ]
    ) ; JSONRaw ]
) ]

# --- (repeat for each test case) ---

# Report results via Agentic-fm Debug
Perform Script [ "Agentic-fm Debug" ; Parameter: JSONSetElement ( "{}" ;
    [ "label" ; "Test results: Target Script" ; JSONString ] ;
    [ "vars"  ; JSONSetElement ( "{}" ;
        [ "testCount" ; $testCount ; JSONNumber ] ;
        [ "passCount" ; $passCount ; JSONNumber ] ;
        [ "allPassed" ; $testCount = $passCount ; JSONBoolean ] ;
        [ "results"   ; $results  ; JSONRaw ]
    ) ; JSONRaw ]
) ]

Exit Script [ JSONSetElement ( "{}" ;
    [ "testCount" ; $testCount ; JSONNumber ] ;
    [ "passCount" ; $passCount ; JSONNumber ] ;
    [ "allPassed" ; $testCount = $passCount ; JSONBoolean ]
) ]
```

### Assertion patterns

Use these comparison patterns depending on what's being tested:

| Assertion type | Pattern |
|---|---|
| Exact match | `$actual = $expected` |
| JSON key match | `JSONGetElement ( $actual ; "key" ) = "expectedValue"` |
| Not empty | `not IsEmpty ( $actual )` |
| Error code | `JSONGetElement ( $errData ; "lastError" ) = 0` |
| Contains | `Position ( $actual ; "substring" ; 1 ; 1 ) > 0` |

### Look up the Agentic-fm Debug script ID

```bash
grep "Agentic-fm Debug" "agent/context/{solution}/scripts.index"
```

Also look up the target script's ID for the `Perform Script` step reference.

### Validate

```bash
python3 agent/scripts/validate_snippet.py agent/sandbox/Test_{ScriptName}.xml
```

---

## Step 5: Deploy and run

### Tier 3 (autonomous)

1. **Deploy the test script** — load clipboard via `POST {companion_url}/clipboard`, create the script via Tier 3 raw AppleScript (Cmd+N → Rename → Cmd+V → Cmd+S)
2. **Run the test** — `POST {companion_url}/trigger` with `{ "fm_app_name": "...", "script": "Test_{ScriptName}", "target_file": "SolutionName" }`
3. **Read results** — wait 2–3 seconds, then read `agent/debug/output.json`

### Tier 1 (developer-assisted)

Present the test script on the clipboard:

> The test script is on your clipboard. To install and run it:
>
> 1. In Script Workspace, press **Cmd+N** to create a new script
> 2. Rename it to **Test_{ScriptName}**
> 3. **Cmd+V** — paste the test script
> 4. **Cmd+S** — save
> 5. Run the test script
> 6. Let me know when it's done — I'll read `agent/debug/output.json` directly.

---

## Step 6: Interpret results

Read `agent/debug/output.json` and parse the test results:

```json
{
  "vars": {
    "testCount": 3,
    "passCount": 2,
    "allPassed": false,
    "results": [
      { "test": "Happy path", "pass": true, ... },
      { "test": "Empty parameter", "pass": true, ... },
      { "test": "Record not found", "pass": false, "expected": "...", "actual": "..." }
    ]
  }
}
```

For each failing test:
1. Compare `expected` vs `actual` to identify the discrepancy
2. Check `errData` for any FM error that occurred
3. Explain the failure and whether it indicates a bug in the target script or a flaw in the test case

Present a summary:

```
## Test Results: [Target Script]

✅ 2/3 tests passed

| Test | Result | Notes |
|---|---|---|
| Happy path | PASS | |
| Empty parameter | PASS | |
| Record not found | FAIL | Expected error response, got empty string |

### Failing test analysis
Test 3 failed because the target script exits without a result when
the find returns 0 records. The script should Exit Script with an error
JSON when Get(FoundCount) = 0.
```

---

## Step 7: Clean up

After testing is complete:

- **Tier 3**: optionally delete the test script from Script Workspace (or leave it for future regression testing — ask the developer)
- **Tier 1**: inform the developer they can delete the test script if no longer needed

If a bug was found, suggest using `script-debug` or `script-refactor` to fix it.

---

## Constraints

- **Test scripts must not modify production data destructively** — if the target script creates or modifies records, the test script should work on test records or restore original values after each test
- **Each test must be independent** — a failing test should not affect subsequent tests
- **Name test scripts with `Test_` prefix** — e.g., `Test_Process Invoice` — so they're easy to identify and clean up
- **Always include error data capture** in the assertion — even passing tests should record `$errData` so unexpected errors are visible
