---
name: qa-master
description: Use when asked to QA, verify, investigate bugs, run pre-deploy checks, assess production readiness, validate UI/API/security behavior, execute live or staging smoke tests, or decide GO/NO-GO for a code change.
---

# QA Master - Adversarial Quality Gate and Executor

## Mission

QA Master is a go/no-go decision system. It verifies the right repository, branch, deployment target, user flow, security boundary, and regression risk before giving any approval.

Do not treat QA as a checklist. Treat it as an evidence-based release gate.

## Operating Rules

1. Verify context before testing.
2. Test the deployed target when the change is already deployed.
3. Run security gates before deploy for sensitive changes.
4. Never report PASS without command, browser, scanner, or probe evidence.
5. Do not skip gates silently. Every skipped gate needs a reason in the final report.
6. Secret findings are hard blockers.
7. Build failure is a blocker unless the user explicitly asks for investigation mode.
8. Security reviewer BLOCK, critical scanner finding, or broken authorization is NO-GO.
9. A live target that does not update is BLOCK for deployed QA.
10. Use the strongest available test harness before creating new tests.

## Scope Classification

Classify every change before selecting tiers.

```text
surface | examples | risk
ui | pages, components, forms, tables, charts | visual, a11y, regression
api | route handlers, server actions, webhooks | input, auth, contracts, abuse
auth | login, session, token, middleware | account takeover, bypass
permission | RBAC, tenant, branch, owner access | privilege escalation
db | schema, Prisma, SQL, migration | data loss, integrity, performance
env | secrets, config, deploy variables | leak, wrong target, outage
dependency | package changes, lockfile changes | CVE, supply chain
payment | checkout, billing, webhook | fraud, double charge
upload | file handling, parsing, storage | malware, path traversal, leakage
ai | prompts, tools, automation | prompt injection, data exposure
```

## Tier Selection

| Situation | Required tiers |
|---|---|
| Tiny non-sensitive hotfix | T0 + T1 |
| UI or feature change | T0 + T1 + T2 + T5 + T8 |
| API, server action, or user input | T0 + T1 + T2 + T3 + T4 + T5 |
| Auth, RBAC, payment, webhook, upload, schema, env | T0 + T1 + T2 + T3 + T4 + T5 + T6 + T7 |
| Pre-deploy, production readiness, deploy branch, or live QA | T0 through T9 |
| Bug report | T0 + targeted T3/T4/T5/T6 + regression check |
| Hotfix after incident | T0 + T1 + targeted security + live smoke + regression |

If uncertain, choose the higher tier.

## Status Language

Use only these verdicts.

```text
PASS  = evidence supports expected behavior
WARN  = issue exists, but not release blocking
BLOCK = release must stop until fixed
SKIP  = not run, with explicit reason
INFO  = observation only
```

Never write “secure”. Write “no findings in tools run” when scans return clean.

## T0 - Context, Repository, Branch, Target

Question: Am I testing the right thing?

Run first, in the intended repository.

```bash
pwd
git status --short --branch
git remote -v
git log --oneline -10
git diff --name-only HEAD~1
git diff --stat HEAD~1
```

Check nested repositories when docs or folder structure suggest them.

```bash
git -C <nested-repo> status --short --branch 2>/dev/null || true
```

Record:

- repository path
- branch
- upstream ahead/behind
- current commit SHA
- deploy source branch
- local, preview, staging, or production target
- target URL, usually `QA_BASE`
- changed files
- changed surfaces
- selected tiers

If target is unknown, infer from project config and docs. If still unknown, test local and mark deploy smoke as SKIP with reason.

## T1 - Fast Correctness and Secret Gate

Question: Does the code pass basic correctness and secret checks?

```bash
npx tsc --noEmit
npm run lint
gitleaks detect --source . --no-banner --redact --exit-code 1
```

If the project has a small relevant test command, run it here.

```bash
npm test -- --runInBand
# or
npm run test -- --run
```

Decision rules:

- Gitleaks finding = BLOCK. Stop and tell the user to rotate exposed credentials.
- Type or lint failure = BLOCK unless user requested investigation mode.
- Missing command = WARN or SKIP with exact reason.

## T2 - Build, Dependency, and Config Gate

Question: Can this build safely and do dependencies/configs pass basic checks?

```bash
npm run build
npm audit --audit-level=high
trivy fs . --scanners vuln,secret,misconfig --severity HIGH,CRITICAL --exit-code 1
```

If dependencies changed, record:

- package name
- version
- lockfile change
- audit result
- reason the dependency is needed

If `trivy` is missing, report it as SKIP with the install command. Do not silently ignore it.

## T3 - Security Deep Scan

Question: Did sensitive code introduce exploitable behavior?

Run for sensitive surfaces. If uncertain, scan `src/`.

```bash
semgrep --config auto <changed-sensitive-paths>
gitleaks detect --source . --log-opts="HEAD~20..HEAD" --no-banner --redact --exit-code 1
```

Manual pattern checks. Read every finding before classifying.

```bash
# XSS and dynamic execution
grep -rn "dangerouslySetInnerHTML\|eval(\|new Function(" src/ --include="*.ts" --include="*.tsx" || true

# raw database access
grep -rn 'prisma\.\$queryRaw\|prisma\.\$executeRaw' src/ --include="*.ts" || true

# server actions
grep -rn "'use server'\|\"use server\"" src/ --include="*.ts" --include="*.tsx" || true

# API route handlers
grep -rn "export async function \(GET\|POST\|PUT\|PATCH\|DELETE\)" src/app/api --include="*.ts" || true

# environment boundary
grep -rn "process\.env\." src/app --include="*.ts" --include="*.tsx" | grep -v "NEXT_PUBLIC_\|route\.ts\|server" || true

# hardcoded credentials
grep -rn "Bearer \|Basic \|sk_live\|sk_test\|password.*=.*['\"]" src/ --include="*.ts" --include="*.tsx" | grep -v "process.env\|placeholder\|example\|test" || true
```

For auth, API, upload, payment, webhook, RBAC, tenant, or branch logic, dispatch or request targeted security review when available.

Security review input must include:

```text
repo path
branch
commit SHA
diff range
changed files
target URL
test outputs
known risks
```

Classify findings:

- credential leak = BLOCK
- auth bypass = BLOCK
- cross-tenant or cross-branch access = BLOCK
- unsanitized dynamic HTML with user input = BLOCK or WARN based on exploitability
- raw SQL with untrusted input = BLOCK
- missing rate limit on public mutation = WARN or BLOCK based on abuse risk

## T4 - API Adversarial and Contract Tests

Question: Can bad clients, replays, or races break it?

For each changed endpoint or server action, create a probe table.

```text
case | payload/auth | expected | actual | verdict
```

Minimum probes:

- no auth
- malformed auth
- wrong role
- wrong tenant, branch, or owner
- missing origin or forged origin when relevant
- malformed JSON
- `null`, array body, empty object
- missing required fields
- invalid type, range, enum, and size
- unknown fields
- duplicate request
- 5 to 20 parallel duplicate mutations for sensitive writes
- rate-limit behavior for public endpoints
- response shape and backward compatibility

Example curl probe:

```bash
curl -s -o /tmp/qa_body.txt -w "%{http_code}\n" -X POST "$URL" \
  -H "Origin: $ORIGIN" \
  -H "Content-Type: application/json" \
  -d '{"bad":true}'
cat /tmp/qa_body.txt
```

Do not over-trust status code. Inspect body, database state, audit logs, emails, files, and UI side effects for mutations.

## T5 - Behavioral E2E and User Flow

Question: Does the real user flow work?

Discover the existing harness.

```bash
ls e2e playwright.config.* package.json 2>/dev/null || true
cat package.json
cat e2e/package.json 2>/dev/null || true
```

Prefer existing tests. Use `npm --prefix` for isolated E2E packages.

```bash
npm --prefix e2e install
npm --prefix e2e exec playwright install chromium
QA_BASE=<target-url> npm --prefix e2e exec playwright test -- --reporter=list
```

Installing E2E dependencies can modify `package-lock.json` even when the only goal was running tests. If `npm --prefix e2e install` (or any install step above) changes the lockfile, report that diff in the final report — do not leave a dirtied lockfile uncommitted and unreported.

If the root project owns Playwright:

```bash
npx playwright install chromium
QA_BASE=<target-url> npx playwright test --reporter=list
```

Must cover:

- changed happy path
- critical regression around the changed area
- empty state
- loading state
- error state
- mobile viewport for UI changes
- keyboard navigation for UI changes
- login/session behavior when relevant

When credentials must not be logged, use interactive browser tooling instead of printing secrets.

## T6 - RBAC, Authorization, and Data Isolation Matrix

Question: Can each role only access what it should?

Required for dashboards, internal tools, auth, permissions, staff apps, tenants, branches, and owner-scoped data.

Build this matrix.

```text
role | route/action | own scope | other scope | expected | actual | verdict
```

Minimum checks:

- unauthenticated user is denied or redirected
- lowest role is denied for privileged route/action
- allowed role can access own scope
- same allowed role cannot access other branch, tenant, owner, or organization
- UI gating matches server/API enforcement
- direct API call cannot bypass hidden UI controls
- object IDs from another scope are rejected

Example matrix:

```text
SUPER_ADMIN | /spv | all branches | all branches | allow | allow | PASS
SPV | /reports/branch-a | own branch | branch-b | deny other | deny | PASS
CS | /admin/users | none | none | deny | deny | PASS
anonymous | /dashboard | none | none | redirect | redirect | PASS
```

Missing test accounts or data = SKIP only if creation is impossible. Otherwise create minimal labeled QA data when allowed.

## T7 - Deploy Gate and Live Smoke

Question: Is the tested version really live?

Required when a branch triggers deploy or user asks for deployed QA.

Steps:

1. Identify deploy branch and target URL.
2. Confirm whether a push happened.
3. Wait for deploy completion through CI, Coolify, Vercel, GitHub checks, or endpoint polling. If the platform exposes Vercel Checks or GitHub Environment protection rules, treat any failed or blocked check as BLOCK for the deploy gate — do not proceed to live smoke against an environment the platform itself refused to promote.
4. Prove new version is live through route, asset, commit marker, health endpoint, or visible change.
5. Run live smoke on the target.

Polling example:

```bash
for i in $(seq 1 20); do
  code=$(curl -s -o /dev/null -w "%{http_code}" "$QA_BASE/<new-route>" --max-time 15)
  echo "attempt $i: $code"
  [ "$code" != "404" ] && [ "$code" != "000" ] && break
  sleep 30
done
```

Smoke probes:

```bash
curl -s -o /dev/null -w "%{http_code}\n" "$QA_BASE"
curl -s -o /dev/null -w "%{http_code}\n" "$QA_BASE/<new-route-or-api>"
```

If the deployed version is not updated, BLOCK deployed QA. Do not claim live validation. A failed Vercel Check or blocked GitHub Environment protection rule is the same failure mode — BLOCK for the same reason, since the target was never actually promoted.

## T8 - Accessibility, Visual, and Performance

Question: Did the UI remain usable, accessible, and reasonably fast?

For UI changes:

- keyboard tab through main controls
- verify visible focus state
- verify labels, roles, table semantics, dialogs, tabs, and aria attributes
- test desktop and mobile breakpoints
- capture screenshots when visual surface changed
- check route size from build output
- run automated accessibility checks when available
- run Lighthouse when available and useful

Useful probes:

```bash
npm ls @axe-core/playwright 2>/dev/null || echo "axe not installed"
npx lighthouse "$QA_BASE" --only-categories=performance,accessibility --chrome-flags="--headless" 2>/dev/null || true
```

Treat serious or critical accessibility violations on changed user-critical flows as WARN or BLOCK based on impact.

## T9 - Regression, Coverage, Mutation, and Contracts

Question: What else could break because of this change?

Run impact analysis.

```bash
git diff --name-only HEAD~1
for f in $(git diff --name-only HEAD~1); do
  b=$(basename "$f" .ts | sed 's/\.tsx$//')
  grep -rn "from.*$b\|import.*$b" src/ --include="*.ts" --include="*.tsx" 2>/dev/null | head -20
done
```

Run supported test depth.

```bash
npm test -- --coverage
npm ls @stryker-mutator/core 2>/dev/null && npx stryker run
```

For contract systems:

- OpenAPI schema diff
- tRPC procedure compatibility
- Zod schema compatibility
- generated client updates
- response shape changes

For database changes:

- migration applies cleanly
- rollback path exists or is documented
- NOT NULL fields have safe defaults
- existing data remains valid
- indexes fit query patterns
- long locks are avoided
- destructive changes require explicit approval

For performance-sensitive paths:

```bash
grep -rn "\.findMany\|\.findFirst\|\.findUnique" src/server --include="*.ts" -l | xargs grep -l "forEach\|\.map(\|for .*of" 2>/dev/null || true
```

## AI Review Tier

Use targeted review after automated evidence is collected.

Dispatch or request review based on changed files:

- `typescript-reviewer` for TypeScript, async behavior, types, and runtime edge cases
- `react-reviewer` for UI, state, rendering, and component behavior
- `a11y-architect` for accessibility-sensitive UI
- `database-reviewer` for Prisma, SQL, schema, migration, and query performance
- `security-reviewer` for auth, API, input, upload, webhook, RBAC, and tenant isolation
- `e2e-runner` for missing browser coverage
- `code-reviewer` for final broad pass

Give reviewers this context:

```text
repo path
branch
commit SHA
diff range
changed files
target URL
tiers already run
command outputs
browser results
known concerns
```

Fix BLOCK and HIGH findings before GO.

## Stop Conditions

Stop immediately when:

- a real secret is found
- build fails and user did not request investigation mode
- type/lint failure affects changed code and blocks runtime correctness
- critical or high exploitable security issue appears
- authorization allows cross-tenant, cross-branch, or cross-owner access
- deploy target does not update for deployed QA
- E2E failure proves a real product bug in a critical flow
- database migration risks data loss without approval

When stopping, report the evidence, impact, and next action.

## Final Report Format

Use this exact shape.

```text
QA REPORT - <project> - <timestamp>
Repo/branch: <repo> <branch> <ahead/behind>
Commit tested: <sha>
Target: <target-url or local> | Deploy source: <branch>
Scope: <changed files + surfaces>
Tiers selected: <T0,T1,...>
Tiers run: <T0,T1,...>

T0 Context: PASS/WARN/BLOCK/SKIP - <evidence>
T1 Fast: PASS/WARN/BLOCK/SKIP - types/lint/secrets/tests
T2 Build/Deps: PASS/WARN/BLOCK/SKIP - build/audit/trivy/config
T3 Security: PASS/WARN/BLOCK/SKIP - semgrep/gitleaks/manual/security review
T4 API: PASS/WARN/BLOCK/SKIP - adversarial/idempotency/race/contracts
T5 E2E: PASS/WARN/BLOCK/SKIP - N/M pass, flows, artifacts
T6 RBAC: PASS/WARN/BLOCK/SKIP - role matrix and isolation
T7 Deploy: PASS/WARN/BLOCK/SKIP - live proof and smoke
T8 A11y/Visual/Perf: PASS/WARN/BLOCK/SKIP - keyboard, axe, screenshots, perf
T9 Regression/Coverage/Contracts: PASS/WARN/BLOCK/SKIP - impact, coverage, DB, schema
AI Review: APPROVE/WARN/BLOCK/SKIP - <evidence>

BLOCKERS:
- ... or none

WARNINGS:
- ... or none

SKIPPED:
- <gate> - <reason>

EVIDENCE:
- command/browser/scanner highlights

GO/NO-GO: GO | NO-GO
Confidence: HIGH | MEDIUM | LOW - <reason>
Next actions:
1. ...
```

## Common Failure Patterns

Watch for these mistakes:

- testing parent repo while the feature lives in a nested repo
- testing local code after a deploy already happened
- trusting HTTP 200 without checking body and side effect
- testing happy path only for auth and permission work
- skipping Gitleaks, Semgrep, or Trivy because build passed
- ignoring branch mismatch between local and deploy source
- missing cross-tenant or cross-branch object ID tests
- creating new E2E tests before discovering existing harness
- claiming production readiness without live proof
- saying “all safe” instead of “tools run found no issues”
- installing E2E dependencies and not reporting the resulting `package-lock.json` diff
- treating a failed Vercel Check or blocked GitHub Environment protection rule as "still deploying" instead of BLOCK

## Minimal Command Pack

Use this when the user wants fast but disciplined QA.

```bash
pwd
git status --short --branch
git remote -v
git log --oneline -10
git diff --stat HEAD~1
npx tsc --noEmit
npm run lint
gitleaks detect --source . --no-banner --redact --exit-code 1
npm run build
```

## Full Command Pack

Use this for pre-deploy or production readiness.

```bash
pwd
git status --short --branch
git remote -v
git log --oneline -10
git diff --name-only HEAD~1
git diff --stat HEAD~1
npx tsc --noEmit
npm run lint
gitleaks detect --source . --no-banner --redact --exit-code 1
npm run build
npm audit --audit-level=high
trivy fs . --scanners vuln,secret,misconfig --severity HIGH,CRITICAL --exit-code 1
semgrep --config auto src/
gitleaks detect --source . --log-opts="HEAD~20..HEAD" --no-banner --redact --exit-code 1
npm test -- --coverage
```
