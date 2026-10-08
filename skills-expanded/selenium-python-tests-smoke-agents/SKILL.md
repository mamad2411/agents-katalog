# Smoke Test Context

Smoke tests cover fast, high-value framework-readiness checks and the initial Sauce Demo
home-page load check. UI steps must use the framework step context so English
START/PASS/FAIL logs are produced consistently.
After the Sauce Demo loaded-state assertion, capture an explicit screenshot step so
the Allure report has a controlled post-assertion page image.
Tests in the daily 04:00 UTC GitHub Actions run are selected with the `smoke` marker.

When adding a smoke test or changing smoke-test conventions, update this file and the nearest relevant `AGENTS.md` file.
