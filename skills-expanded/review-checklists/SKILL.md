---
name: review-checklists
description: "Review checklists by kind of change: interface work, API endpoints, database migrations and queries, background jobs, authentication and permissions, infrastructure and CI, dependencies, tests, documentation, mobile apps and animation, each listing the defects most often missed, to use with the `review` method. Read when reviewing a change of that kind."
---

# Review checklists by kind of change

Each kind of change hides the same defects because the diff looks fine: the
migration that locks the table, the endpoint that checks the role but not the
owner, the job that runs twice, the workflow that pastes a pull request's title
into a shell. Settle each item on the lists for what the change touches, with
the method in `review`. An item is a question, not a finding: report only what
the change gets wrong. The skill in brackets holds the rule and the fix.

## 1. Which lists apply

Take them from `git diff --name-only`: pages and styles (2, and 3 when
anything animates), routes and handlers (4, and 7 for sign-in or permissions),
migrations and queries (5), workers and schedulers (6), workflows, Dockerfiles
and infrastructure (8), manifests and lockfiles (9), tests (10), docs (11),
mobile code (12), claims of speed (13). Most changes need two or three.

## 2. Interface (`ui`, `ui-audit`, `frontend-*`)

- Every state of each view that loads data: empty, loading, error, one item
  and hundreds; errors shown where they happen (`frontend-errors`).
- Keyboard: Tab reaches every control, Enter or Space works it, Escape closes
  overlays, focus is visible and returns to the trigger; icon buttons have a
  name, inputs a label (`frontend-accessibility`).
- 360, 768 and 1440px: nothing past the right edge, the primary action in view
  on a phone, wide tables scrolling in their own box (`ui-layout`).
- Tokens, not raw colours or spacing (`ui_check` flags colours outside them);
  both themes checked (`ui-themes`); the direction in `DESIGN.md` kept (`ui`).
- Placeholders marked; no invented figures, testimonials or logos (`ui-audit`).
- Text through the translation layer, no sentences glued from pieces, dates,
  numbers and money through `Intl` (`i18n`).
- No user data in `dangerouslySetInnerHTML`, `v-html`, `{@html}` or `innerHTML`
  unsanitised; user URLs only `http`, `https` or `mailto` (`frontend-security`).
- Forms keep input after a failed submit, block double submits and map server
  errors to fields (`frontend-forms`); filters, sort and page live in the URL
  when a reload should keep them (`frontend-state`).
- Images sized (width, height, `srcset`, `sizes`), lazy below the fold but never
  the largest; no heavy library for a small widget (`frontend-performance`).

## 3. Animation (`motion-audit`)

- With reduced motion, nothing moves beyond fades and nothing stays hidden
  (`motion-comfort`).
- No content hidden in the base CSS: without JavaScript or in print the page is
  complete (`motion-reveal`).
- Loops stop off screen and in a hidden tab (`motion-performance`).
- Only `transform` and `opacity` animate; no `transition: all`, no animated
  size, position or blur (`motion-performance`).
- One IntersectionObserver for reveals, each block unobserved once shown; no
  scroll listeners or scroll hijacking (`motion-reveal`).
- Feedback 80 to 160ms, nothing blocking the user past 400ms (`motion-timing`).
- No parallax on text, no zoom or spin tied to scroll (`motion-comfort`).
- `preview` with `motion: true`: the timeline matches the intent, nothing is
  hidden after scrolling, the reduced-motion pass is still.

## 4. API endpoints (`backend-api`, `backend-security`, `backend-errors`)

- Every input validated at the boundary (body, query, path, headers read), with
  lengths, ranges, array sizes and a body size limit.
- The parsed body never saved as it is: nobody sets `role`, `ownerId` or
  `price` by adding it to the JSON.
- Authorisation per object: the record loaded scoped to the caller or tenant
  (`WHERE id = $1 AND owner_id = $2`), not by id and then a role check
  (`backend-auth`).
- `201` for a create, `404` where `403` would reveal the record exists, `409`
  for conflicts, never `200` with an error inside.
- One error format; the unexpected becomes a generic `500` with a request id;
  no stack trace or SQL in responses, no token or personal record in logs
  (`backend-observability`).
- Lists paginated in the query (default 25, maximum 100); sort and filter
  fields from an allow-list, never pasted into SQL.
- A create that must not repeat takes an `Idempotency-Key`; concurrent edits
  carry a version and get `409` when stale.
- Rate limits on sign-in, sign-up, reset and whatever sends email or costs
  money; a timeout on every query and outbound call.
- Server-side fetches of user URLs refuse private and metadata addresses.
- No field renamed or removed without a transition; OpenAPI or the shared
  types changed with it.
- Tests for another user's id, bad input and the main path (`backend-testing`).

## 5. Database (`database-migrations`, `database-queries`, `database-indexes`, `database-transactions`)

- A new migration, never an edit of one already run anywhere shared; one
  concern; a down migration or a stated reason for none.
- Big Postgres tables: most `ALTER TABLE` forms take an `ACCESS EXCLUSIVE`
  lock, a type change rewrites the table, `SET NOT NULL` scans it;
  `lock_timeout` set.
- Live tables: indexes built `CONCURRENTLY` (outside a transaction, so that
  migration opts out of one), foreign keys and checks added `NOT VALID`, then
  validated separately.
- Renames and drops split across releases (expand, then contract); backfills in
  batches, outside the schema migration, safe to run twice.
- `NOT NULL` by default, `ON DELETE` chosen per foreign key, unique constraints
  where the business needs them; money in integer minor units, `timestamptz`
  for time (`database-schema`, `backend-data`).
- Parameterised queries; no query per item in a loop or lazy relation in a
  template; only the columns needed.
- Large or live lists paged by keyset, ordered by the sort column then the id.
- An index for each new filter and sort; foreign key columns indexed, which
  Postgres does not do by itself.
- No read, decide, write: a conditional update or `SELECT ... FOR UPDATE`, with
  unique constraints deciding races.
- Writes that belong together in one transaction, no network call inside it,
  jobs queued after the commit.

## 6. Background jobs (`backend-jobs`)

- Idempotent: two runs have the effect of one (a unique key, a conditional
  update, the provider's idempotency key).
- Carries ids and loads the current state, not a copy taken when queued.
- Queued after the transaction commits (an outbox or an after-commit hook).
- Retried with backoff and jitter only for what can succeed later (timeouts,
  `429`, `5xx`), up to a set number of attempts.
- A time limit per job; one small job per item, not one for a thousand.
- Out of attempts: a dead-letter list with the error, visible to someone.
- Scheduled work runs once across instances, catches up on missed runs, and
  keeps times of day in the business's time zone, stored in UTC.
- On `SIGTERM` a worker finishes its job or hands it back.

## 7. Authentication and permissions (`backend-auth`, `security-auth`)

- Passwords hashed with argon2id, or bcrypt at cost 12 or more, by a library;
  no length cap below 64 characters.
- A new session id at sign-in; sessions ended by sign-out and by a password
  change; cookies `HttpOnly`, `Secure`, `SameSite`.
- JWTs with the algorithm pinned (never `none`), `exp`, `iss` and `aud`
  checked; no token in `localStorage` in a browser app.
- The same answer for known and unknown accounts on sign-in, sign-up and reset;
  rate limits per account and per IP there and on second factors.
- Reset and verification tokens: 32 random bytes, stored hashed, used once,
  expiring (30 to 60 minutes for a reset); a reset ends other sessions.
- Deny by default, checked on the server on every request, owner and tenant in
  the query rather than a role alone.
- OAuth and OpenID Connect: PKCE, `state`, `nonce`, the redirect URI matched
  exactly; accounts linked by verified email only.
- `next` or `returnTo` after sign-in limited to paths on the same site.
- Tests for what must fail: another user's record, a lower role, an expired
  token.

## 8. Infrastructure and CI (`devops-ci`, `devops-containers`, `devops-deploy`, `security-infra`)

- No secret in files, images, logs or `run:` lines; secrets from the platform's
  store; cloud access by OIDC, not long-lived keys.
- `permissions:` at the minimum (`contents: read`); IAM without wildcards.
- Actions pinned to a full commit SHA, base images to a version (and digest),
  tools to a version; no `latest`.
- `pull_request_target` never runs the pull request's code; untrusted text
  (`github.event.pull_request.title`) reaches scripts through `env:`, never
  inside `run:` (`security-supply-chain`).
- Images multi-stage and non-root, a `.dockerignore` keeping out `.git`, `.env`
  and `node_modules`, an exec-form `CMD` so `SIGTERM` reaches the app.
- Liveness and readiness checks, rollouts that wait for readiness, memory and
  CPU limits, a restart policy.
- A rollback path: the previous image kept, a schema the previous version still
  runs against.
- Only the app's port public; databases, caches and admin panels private.
- Validated with the tool (`actionlint`, `hadolint`, `docker build`,
  `terraform plan`, `kubectl apply --dry-run=server`); the report says which
  ran.

## 9. Dependencies (`security-supply-chain`, `research-libraries`)

- Needed at all: the standard library, the platform or an installed package may
  already do it.
- Maintained: the last release and its date, issues answered, more than one
  active maintainer for anything critical.
- A licence the project can use; GPL or AGPL in closed software is the owner's
  decision, never a default.
- Size: the gzipped cost in a frontend bundle; transitive dependencies and
  native builds elsewhere.
- The lockfile changed in the same commit and matching the manifest; one
  package manager's lockfile, not two.
- No new `preinstall` or `postinstall` script without a reason; no look-alike
  of a popular package's name.
- The audit clean or triaged (`npm audit`, `pip-audit`, `cargo audit`,
  `govulncheck`, `osv-scanner`).
- A major bump with its migration guide read and breaking changes handled at
  every call site.

## 10. Tests (`testing`)

- They fail without the change: read each assertion against the old code with
  `git show main:<path>`, or run it on the base.
- They cover the case the change is about, its failure path included.
- Assertions on outcomes, not on which mock was called; none in a callback that
  never runs; async ones awaited.
- Deterministic: no real clock, unseeded randomness, network, order dependence
  or sleeps (`testing-flaky`).
- Nothing deleted, skipped (`.skip`, `xit`, `@Ignore`, `#[ignore]`, `t.Skip`)
  or loosened to pass; snapshots updated for a stated reason.
- Mocks only at boundaries; never the unit under test (`testing-unit`).
- Each test makes its own data, unique enough to run in parallel
  (`testing-data`).
- Names state the behaviour: "refund is refused after 30 days".

## 11. Documentation (`docs`)

- Every flag, default, environment variable, endpoint and command the text
  names exists in the code (grep each one).
- Examples run: the commands exist in the scripts or the Makefile; the code
  compiles against the current API.
- A changelog entry under Unreleased for what users notice; breaking changes
  first, with migration steps (`docs-changelog`).
- New environment variables in `.env.example` and the README (`docs-readme`).
- The API reference or OpenAPI changed with the endpoints (`docs-api`).
- Comments changed with the code; none describes the old behaviour
  (`docs-comments`).
- No invented numbers, no marketing words (`writing`).
- Links resolve; screenshots show the current interface.

## 12. Mobile apps (`mobile`, `mobile-ux`, `mobile-data`, `mobile-release`)

- State survives backgrounding and, on Android, the process being killed; data
  refreshed on resume.
- Offline and slow networks: timeouts, retries, writes queued with idempotency
  keys, no endless spinner (`mobile-data`).
- Permissions asked in context, with a path for a refusal; Android back, safe
  areas and navigation conventions kept (`mobile-ux`).
- Icon buttons labelled, text that grows to the largest size, targets of 44pt
  or 48dp, a sensible screen reader order.
- Tokens in the Keychain or Keystore, not AsyncStorage or SharedPreferences.
- Long lists virtualised (FlashList, `LazyColumn`, `ListView.builder`), images
  sized for their slot (`mobile-performance`).
- Deep links validated before they act; no personal data in logs.
- A new permission or SDK reflected in the privacy manifest and the store forms
  (`mobile-release`).

## 13. Performance claims (`performance`)

- Measured before and after, same machine and workload, both stated.
- Several runs, median and spread, percentiles for latency; not one run or an
  average (`performance-benchmarks`).
- A realistic workload: production-like sizes and concurrency.
- A profile showing the changed code was the hot path (`performance-profiling`).
- Correctness kept: tests pass; a cache has an invalidation rule
  (`backend-caching`).
- The trade named: memory for speed, one input shape against another.
- Micro-benchmarks keep the compiler from removing the work (`black_box`).
- No speed-up claimed in a commit or changelog without its numbers.

## Check it

Lists chosen from every path in the diff, config and CI included; each item
settled against the code; findings in the `review` format (consequence, line,
input, evidence, fix, severity); what could not be checked listed as such.

## Avoid

Pasting a checklist into the report; an item raised as a finding because the
code does not mention it (a job that cannot fail needs no retries); findings
without a line; the interface list alone on a change that ships a migration.
