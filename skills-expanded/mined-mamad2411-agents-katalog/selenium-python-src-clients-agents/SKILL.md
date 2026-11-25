# Client Guidance

Clients own WebDriver sessions and expose high-level page access. Keep browser
construction delegated to `webdriver/`; keep page-specific behavior in page objects.
`UIClientPool` must remain suitable for multiple named sessions without sharing a

Named UI steps should use the client step context so the execution log identifies
START, PASS, and FAIL states.
Use the dedicated screenshot-step method when a test needs explicit control over
where a screenshot appears in the Allure report.
Automatic screenshots after every named UI step must remain configurable and disabled
by default for normal local, CI, and pipeline runs.
Screenshot capability flags should be accepted by clients and preserved by the
client pool so future multi-session tests can control evidence consistently.

When adding new elements, update this `AGENTS.md` and the parent framework guidance.
