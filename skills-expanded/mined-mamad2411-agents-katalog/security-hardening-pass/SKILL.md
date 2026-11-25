---
name: security-hardening-pass
description: Выполнение scoped security-фиксов в web-runtime (chat/contact/storage/config) с минимальным риском регрессий и обязательной проверкой совместимости с текущим deploy-контуром.
user-invocable: true
allowed-tools:
  - Read
  - Bash(git *)
  - Bash(ls *)
  - Bash(find *)
  - Bash(grep *)
  - Bash(cat *)
  - Bash(npm *)
  - Bash(npx *)
  - Bash(curl *)
  - Bash(fuser *)
  - Bash(node *)
  - Bash(rg *)
  - Bash(jq *)
---

# Skill: Security Hardening Pass

## Triggers
- "устрани security findings"
- "сделай hardening"
- "закрой P0/P1"

## Objective
Реализовать подтвержденные hardening-фиксы в узком scope, сохранив стабильность production runtime.

## Workflow
1. Зафиксировать scope правок по файлам до начала edits.
2. Triage external findings against the current tree as `confirmed`,
   `partially confirmed`, `stale/resolved`, `rejected`, or `needs-more-proof`.
3. Внести P0/P1 изменения с backward-compatible default behavior.
4. Избегать архитектурных поворотов без отдельного решения (Redis migration, encryption-at-rest, etc.).
5. Run checks per `sdd-protocol.md § Check Suite → Tier Standard`, plus:
   - `npm audit --omit=dev --audit-level=high`
   - `scripts/secret-scan.sh tracked` when the script exists
6. For browser/admin hardening, verify security headers and CSP expectations.
   Admin CSRF uses a readable double-submit cookie, so any CSRF/admin rendering
   change must preserve CSP and output-encoding assumptions.
   Code-level config evidence is not runtime evidence; apply
   `sdd-protocol.md § Runtime Proof Matrix` when the relevant deployed runtime
   is available, and mark unavailable runtime evidence as `blocked`.
7. Review error/log output:
   - auth failures must not reveal whether a secret, token, route, or resource
     existed unless the API contract requires it;
   - 5xx responses must not include stack traces, SQL/provider messages,
     internal paths, secrets, or connection strings;
   - logs must not include tokens, passwords, API keys, `DATABASE_URL`, full
     headers, full bodies, row payloads, or client-private message bodies.
8. Сформировать остаточные риски и deferred backlog.

## Constraints
- Не ломать текущий reverse-proxy/TLS termination flow.
- Не включать strict policies, которые могут блокировать no-Origin/internal traffic, без explicit решения.
- Любые env-зависимые ужесточения делать через feature/env flags с безопасным default.
- Do not treat CSP/header reports as accepted until checked against the current
  `web/next.config.ts` and `admin/next.config.ts`.
- Do not add dependencies, CI jobs, secret-scanning tools, or SAST tools inside
  this skill unless the Work Block explicitly approves dependency/tooling
  changes.

## Output
- Changed files
- AC status
- Commands run + pass/fail
- Residual risks + deferred items

## Handoff
- **Success condition**: все P0/P1 фиксы применены, проверки пройдены, residual risks задокументированы.
- **Next**: security-verification-gate
- **Auto-proceed**: 🟢 YES
- **Hard stop**: NO
