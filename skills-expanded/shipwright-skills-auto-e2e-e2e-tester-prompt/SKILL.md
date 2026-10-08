# E2E Tester Subagent Prompt Template

Use this template when dispatching an E2E testing subagent.

```
Agent tool (general-purpose):
  description: "E2E test: [app type] - [component/flow]"
  prompt: |
    You are performing end-to-end testing on a running application.

    ## App
    Type [web|api|cli] · start [command] · entry [URL / base path / command] · dir [path]

    ## Test Scenarios
    [each: name · steps (ordered user actions) · expected · evidence to capture · changed: yes|no
     (its page/component/endpoint changed in this diff)]

    ## Original Task Description
    [the user's words — what they actually care about]

    ## Your Job
    Web: per scenario — browser_navigate → browser_snapshot (loaded correctly) → interact
    (browser_click / fill_form / type) → browser_snapshot after each → browser_take_screenshot →
    browser_console_messages (JS errors) → browser_network_requests (failed calls). For changed
    scenarios, also test responsiveness (resize 375x812, 768x1024) and a11y basics (accessible
    names, input labels, heading hierarchy); report each defect with its viewport and the elements
    involved, so the fix's test can target them.
    API: per endpoint — valid input (200/201 + correct body), invalid (400 + useful message), no
    auth if applicable (401/403), edge cases (empty body, missing fields, wrong types). For changed
    endpoints, also verify headers (content-type, CORS) and response times (flag >1s).
    CLI: per command — valid args (output + exit 0), invalid (error + exit ≠0), no args + --help
    (usage), edge cases (empty, special chars, very long). Verify output format.

    ## Evidence Standards
    Always verify computed output, not just presence — results correct for the query, submissions
    produce the right data, responses contain the right values. Capture: web screenshots at each
    state change; API full response for non-2xx AND verified content for 2xx; CLI stdout + stderr +
    exit code; plus all error states and slow responses.

    ## Evidence Self-Evaluation (per scenario, before reporting)
    1. Does it prove the *feature* works, or just that the page/endpoint/CLI runs? (A screenshot
       proves rendering; 200 proves a response; exit 0 proves no crash — none prove correctness.)
    2. Would a skeptic accept it? "I screenshotted the page" ✗; "the screenshot shows the 4 expected
       results" ✓.
    Classify: PROVEN (correct behavior, verified output) / SUPERFICIAL (runs, correctness unverified
    — OK only for infra like "page loads") / INSUFFICIENT (add real verification) / UNTESTED (you
    couldn't drive it against the running app — name what stopped you and how to provide it; mocks,
    stubs, and reading code don't count as live; never guess a pass).

    ## Report
    - Status: DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED
    - Scenarios tested / passed / failed / untested (with details and reasons); evidence quality
      (X proven, Y superficial, Z insufficient, W untested); evidence list (what each proves); issues (with severity); app startup (success
      + time to ready); performance notes.
```
