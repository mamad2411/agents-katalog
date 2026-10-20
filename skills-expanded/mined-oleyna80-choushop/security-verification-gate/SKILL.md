---
name: security-verification-gate
description: "Независимая post-implementation проверка security-патча: diff review, validation commands, регрессии, ship/no-ship verdict и обновление SSOT."
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

# Skill: Security Verification Gate

## Triggers
- "проверь после фиксов"
- "security verifier"
- "ship verdict"

## Objective
Дать независимый verdict по security-pass и зафиксировать фактический остаточный риск перед релизом.

## Workflow
1. Проверить фактический diff по заявленному scope.
2. Run checks per `sdd-protocol.md § Check Suite → Tier Standard`, plus:
   - `npm audit --omit=dev --audit-level=high`
   - `scripts/secret-scan.sh staged` when staged security-sensitive files exist
   - `scripts/secret-scan.sh tracked` for security Work Blocks
3. Для security-sensitive diff выполнить `sdd-protocol.md § Tier Full`
   security checklist:
   - SQL parameterization / injection review;
   - XSS sinks (`dangerouslySetInnerHTML`, dynamic HTML) and sanitization;
   - CSRF/origin/webhook/scheduler guard on mutation endpoints;
   - redirect/file/path allowlisting;
   - no weak randomness for security-sensitive values;
   - no dynamic code execution from user input;
   - sanitized errors and logs;
   - security headers/CSP preserved for browser apps;
   - admin readable CSRF cookie remains protected by CSP;
   - staged diff contains no secrets, credentials, private keys, or full
     connection strings.
4. Apply `sdd-protocol.md § Runtime Proof Matrix` for browser/admin/API/header
   findings. If DNS, deployment state, or live-action approval blocks runtime
   proof, report `blocked` with the blocker and carry it as a separate follow-up
   gate; do not mark runtime proof as pass.
5. Map material findings to OWASP 2021 categories when useful:
   - A01 access control;
   - A02 crypto/secrets;
   - A03 injection;
   - A04 insecure design / missing threat model;
   - A05 security misconfiguration / CSP and headers;
   - A06 vulnerable components;
   - A07 auth/session failures;
   - A08 integrity/supply chain;
   - A09 logging/monitoring;
   - A10 SSRF.
6. Сопоставить исходные findings с единой triage/status-моделью:
   - `confirmed`
   - `partially confirmed`
   - `stale/resolved`
   - `rejected`
   - `needs-more-proof`
7. Явно зафиксировать side effects/regression risks.
8. Передать verdict и closure matrix в Control Tower для SSOT sync.
   Verifier может писать `memory-bank/*` или `docs/tasklist/*` только если
   утвержденный Work Block явно включает эти artifact paths.

## Constraints
- Verifier-mode: не расширять scope implementation в этом шаге.
- Любой follow-up fix — отдельным coder step.
- Если какая-то проверка не запускалась, указывать это явно.

## Output
- Ship verdict: `safe incremental ship` / `needs changes`
- Findings closure matrix
- OWASP/security checklist coverage summary
- Runtime proof matrix status, including blocked follow-up gates
- Security tooling baseline status
- Open blockers
- Next recommended action

## Handoff
- **Success condition**: verdict `safe incremental ship` выдан, нет open blockers.
- **Next**: ssot-sync-closeout
- **Auto-proceed**: 🟢 YES на safe ship; 🔴 вручную на needs changes
- **Hard stop**: NO (только репорт, без деплоя)
