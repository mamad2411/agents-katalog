---
description: "Spring Boot k6 load-testing contract for optional HTTP scripts, env-based targets, checks, and generated reports."
applyTo: "**/src/test/k6/**/*.js"
---

# Spring Boot k6 Contract

These rules apply when an application ships HTTP load or performance scripts.
They do not apply to JUnit tests. Automated unit, slice, and context-load tests
stay in the testing contract. Do not restate that contract here.

k6 is optional. Add these scripts only when the product needs load or performance
checks.

## When to add k6

- Add k6 when the product needs HTTP smoke, load, or authenticated-path
  performance checks against a running application.
- Do not add k6 to every greenfield app.
- Do not add a k6 Maven dependency.
- Do not run k6 from Maven Surefire or as a substitute for `mvn test`.

## Layout

- Put scripts in `src/test/k6/` of the application module.
- Use one script per scenario (for example smoke, staged load, or an
  authenticated path).
- Keep fixtures such as JSON payloads next to the scripts, not under
  `src/main`.

## Script contract

- Import `k6/http` and declare `export const options` with `vus` plus
  `duration`, or with `stages`.
- Call `check()` on HTTP status, and on important body or header values when
  that is the point of the script.
- Read the target from `__ENV.BASE_URL`, defaulting to `http://localhost:8080`
  for local runs.
- Prefer thresholds `http_req_failed: ['rate < 0.01']` and a duration
  percentile. Set the duration limit to match the endpoint under test; do not
  copy a cookbook 200ms or 500ms number onto a deliberately slow path.
- Do not invent request tags that the script never sets.

## Secrets and authentication

- Load credentials from environment variables only. Never hardcode passwords or
  tokens in scripts.
- Send credentials with an `Authorization` header. Never put `user:pass` in the
  URL.
- When the API uses HTTP Basic (or a similar static header), build it once in
  `setup()` and reuse it in the default function.

## Reports

- Optional HTML summaries go under `src/test/k6/output/`.
- Add `src/test/k6/output/` to `.gitignore` when the project writes k6 reports.
- Never commit generated HTML reports.
- Never place k6 report HTML in `src/main/resources/templates/` or other
  application static/UI paths.

## README

- When k6 scripts exist, the Tests section documents the `k6` CLI prerequisite
  and the `k6 run` command for the scripts in `src/test/k6/` (README contract).

## Forbidden

- Never add k6 because a related sample or starter exists.
- Never run k6 as part of `mvn test`.
- Never hardcode production URLs or credentials in scripts.
- Never put Basic credentials in the request URL.
- Never commit generated k6 HTML reports, including under Thymeleaf `templates/`.
- Never replace JUnit coverage with k6 scripts.
