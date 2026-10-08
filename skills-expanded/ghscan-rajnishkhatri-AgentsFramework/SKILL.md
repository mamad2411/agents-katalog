---
name: agentsframework-playwright
type: skill
description: >-
  Concrete Playwright E2E playbook for THIS repository (the AgentsFramework
  `agent` monorepo: Next.js 15 + React 19 frontend, CopilotKit/AG-UI chat,
  WorkOS AuthKit, Python agent backend, deployed on Google Cloud Run). Use this
  whenever the work involves running or writing frontend E2E tests here, signing
  in for tests against WorkOS, running the T1/T2/T3 tiers, pointing tests at the
  Cloud Run deployment, the GoalJudge registry batch, or verifying a run via
  Cloud Logging / Langfuse. It supplies the exact commands, env vars, service
  URLs, selectors, and the repo's hard-won gotchas. Trigger on phrases like
  "run the e2e tests", "test:e2e:t3", "playwright auth", "test against Cloud
  Run", "GoalJudge batch", "frontend/e2e", or any task editing files under
  `frontend/e2e/`. For the underlying methodology (how streaming/auth/cloud
  testing works in general), defer to the `playwright-agentic-e2e` skill — this
  one is the workspace binding layer on top of it.
license: Complete terms in LICENSE.txt
---

# AgentsFramework Playwright Playbook

This is the **workspace binding layer**. For the *why* — how to test streaming
agent UIs, the auth patterns, non-determinism, cloud verification — read the
companion **`playwright-agentic-e2e`** skill. This file gives you the *what*
for this repo: exact commands, env vars, URLs, selectors, and the lessons this
codebase has already paid for.

Source of truth in-repo:
- `frontend/e2e/README.md` — the suite's own guide (tiers, quick start, layout)
- `docs/Architectures/PLAYWRIGHT_TESTING_ARCHITECTURE.md` — the architecture & rationale
- `docs/guides/FRONTEND_VALIDATION.md` — the SS-numbered manual checklist specs mirror
- `docs/style-guides/STYLE_GUIDE_FRONTEND.md` — the F-R rules and FE-AP anti-patterns

## The three tiers (this repo's exact mapping)

| Tier | Cut point | Command | Needs |
| --- | --- | --- | --- |
| **T1** SSE-mocked | `page.route("**/api/run/stream")` | `pnpm test:e2e:t1` | nothing (per-commit safe) |
| **T2** BFF integration | Node mock middleware on `:8765` | `pnpm test:e2e:t2` | `MOCK_MIDDLEWARE=1` (set by the script) |
| **T3** full-stack | nothing mocked | `pnpm test:e2e:t3` | WorkOS creds + `E2E_AUTHENTICATED=1` |

All Playwright commands run from `frontend/`. The package manager is **pnpm**
(there's a `pnpm-lock.yaml`; `npm run …` also works for the scripts). One-time:
`pnpm install && pnpm exec playwright install --with-deps`.

Other scripts: `test:e2e:matrix` (5-browser cross-browser), `test:e2e:visual`
(chromium visual regression), `test:e2e:headed`, `test:e2e:visual:auth` (visual
with `E2E_BYPASS_AUTH=1`).

## Filled-in config block

This is the `playwright-agentic-e2e` config block, completed for this repo:

```yaml
frontend_dir:        frontend
test_dir:            e2e
package_manager:     pnpm
base_url_local:      http://localhost:3000
base_url_remote:     https://agent-frontend-w65nrxwkiq-uc.a.run.app   # Cloud Run frontend

auth_library:        workos-authkit              # @workos-inc/authkit-nextjs
session_cookie_name: wos-session                 # HttpOnly; tests never read the JWT
auth_gate_env:       E2E_AUTHENTICATED
storage_state_path:  e2e/.auth/state.json        # git-ignored
fake_session_env:    E2E_FAKE_SESSION            # mints a sealed iron-session cookie locally

stream_endpoint:     /api/run/stream
stream_transport:    fetch                        # fetch-stream — page.route() DOES intercept it
stream_protocol:     ag-ui (SSE)                  # AG-UI events over text/event-stream

composer_selector:   "[data-testid='composer'], textarea[aria-label='Compose message'], textarea"
send_selector:       "[data-testid='send-button'], button[aria-label='Send']"
message_selector:    "article div[aria-live='polite']"   # the streamed content DIV (FE-AP-5)
```

GCP topology (for verification): project **`agent-prod-gcp-dev`**, region
**`us-central1`**; services **`agent-frontend`** and **`agent-backend-combined`**.
GoalJudge shadow config object:
`gs://agent-prod-gcp-dev-agent-facts/ops/goal_judge_config.json` — **do not
overwrite it.**

## Running against Cloud Run (T3)

```bash
cd frontend
export BASE_URL=https://agent-frontend-w65nrxwkiq-uc.a.run.app
export E2E_AUTHENTICATED=1
export E2E_USER_EMAIL=...          # from repo-root .env / your secret store, never inline
export E2E_USER_PASSWORD=...       # likewise
pnpm exec playwright test e2e/full-stack/   # or a specific spec
```

`globalSetup` (`e2e/global-setup.ts`) signs in once via WorkOS AuthKit and writes
`e2e/.auth/state.json`; the `authenticatedPage` fixture reuses it. The conditional
`webServer` starts nothing because `BASE_URL` is remote.

Credentials live in the **repo-root `.env`** (auto-loaded by global-setup). Read
the gotchas reference before debugging an auth failure — the #1 cause here was a
*stale on-disk `.env`*, not bad credentials. Never print secret values and never
paste the literal password into a command (a classifier blocks it).

## GoalJudge registry batch

The canonical full-stack example: drive each GoalJudge registry prompt through the
real chat on Cloud Run and capture the result. Spec:
`frontend/e2e/full-stack/goaljudge-batch.spec.ts`. Plan:
`docs/plans/goaljudge_gcp_playwright_batch.plan.md`.

```bash
# one case (smoke), then the whole 22-case subset:
GJ_CASE_FILTER=GJ-010 pnpm exec playwright test e2e/full-stack/goaljudge-batch.spec.ts
pnpm exec playwright test e2e/full-stack/goaljudge-batch.spec.ts     # all of GJ-001…GJ-022
# cap size: GOALJUDGE_BATCH_LIMIT=5
```

Cases come from `e2e/fixtures/goaljudge_registry.ts` (`walkthroughCases()` =
GJ-001…GJ-022, numeric-sorted, **includes B-variants** like GJ-001B/GJ-003B;
`filterCases({caseFilter, limit})`). Regenerate the JSON with
`python scripts/export_goaljudge_registry_json.py`. Each run appends a row to
`cache/goaljudge_eval/ui_batch.jsonl`.

The **thread bridge** is the key mechanism: the spec rewrites the outbound
`/api/run/stream` body to set `thread_id = gj:{case_id}:{trace_id}` so the backend
can join the UI run to the registry case. **FE-AP-7**: it throws if the body
contains a client-generated `trace_id` — the server owns trace ids;
`trace_id = uuid5(NAMESPACE_DNS, case_id)` is derived deterministically, not sent.

## Post-run verification

Two independent signals — the DOM capture **and** the backend. A blank DOM does
**not** prove backend failure here (observed: backend completed all cases, but
only ~half surfaced a final answer in the live region — a frontend stream→DOM gap).

Use the companion skill's `verify_run.py` on the capture (it encodes the
status-prefix strip and last-write dedup this repo needs):

```bash
python ~/.claude/skills/playwright-agentic-e2e/scripts/verify_run.py \
  --jsonl cache/goaljudge_eval/ui_batch.jsonl \
  --status-prefix "Using tools:" --id-namespace dns --dedupe --expect-cases 22
```

Cloud Logging — the bridge/marker line is in **`jsonPayload.message`, NOT
`textPayload`** (see the working query in the gotchas reference). Dedupe by run id
before counting. Langfuse — list traces for the saturation user
(`lf.api.trace.list(user_id="synthetic-saturation-user", limit=…)`) and compare
the count to distinct cases.

Known limitation (G3): GoalJudge verdict axes (`goal_met` / `graceful_failure` /
`partial_fraction`) are not emitted as queryable structured fields on GCP — you
can verify the integrity/trace-set layer, but the semantic axes read N/A there.

## The gotchas that already cost time

Read **`references/gotchas.md`** before debugging — it has the full catalog with
fixes. The headlines:

1. **Stale `.env` ≠ bad credentials.** An auth failure was an unsaved/stale
   on-disk `.env`, not WorkOS rejecting the user. Check the file on disk first.
2. **Locale → Afrikaans.** Without a pinned locale, headless Chromium pulls
   `af-ZA` and WorkOS renders Afrikaans; text selectors break. `E2E_BROWSER_CONTEXT`
   (`e2e/fixtures/browser-context.ts`) pins `en-US` — reuse it everywhere.
3. **The live region is the DIV, not the `<article>`** (FE-AP-5). Target
   `article div[aria-live='polite']`; a bare `[aria-live]` matches Next.js's route
   announcer (`div[aria-live='assertive'][role='alert']`) and reads empty.
4. **Wait by text-settle, not by `finished()` or composer state.** On Cloud Run,
   runs were observed frozen at "Using tools: file_io…" with the composer never
   re-enabled; `response.finished()` hangs behind the route intercept. Use
   `waitForResponse` from `e2e/fixtures/helpers.ts`.
5. **Capture text includes the leading status feed.** Strip `Using tools: …`
   before deciding "did this render a real answer" — fully-answered runs also
   start with it (this flips 11/22 into a wrong 21/22).
6. **`E2E_FAKE_SESSION=1` is local-only.** Against Cloud Run the sealed cookie
   must match production `WORKOS_COOKIE_PASSWORD`; don't fake-session prod.

## References

| File | Read it when |
| --- | --- |
| `references/gotchas.md` | Debugging anything; full gotcha catalog + the working `gcloud` query |
| `references/goaljudge-batch.md` | Running/extending the GoalJudge registry batch + verification detail |

## Repo conventions to honor

- **Spec naming is a YES/NO outcome** mirroring `docs/guides/FRONTEND_VALIDATION.md`
  (cite the SS section in the file header).
- **Skip gracefully** when prerequisites are missing (`test.skip(condition, …)`)
  so unauthenticated CI doesn't crash.
- **Only T1 runs in per-commit CI.** T2 is nightly; T3 and the matrix are release
  gate / on-demand (they cost money and hit the live model).
- **Don't commit** `e2e/.auth/state.json` or the `e2e/.auth/debug-*.png` files.
- **Security:** don't read production Secret Manager secrets (classifier-blocked);
  don't `git stash` for A/B comparison (the repo has unrelated stashes — pop
  conflicts ensue).
