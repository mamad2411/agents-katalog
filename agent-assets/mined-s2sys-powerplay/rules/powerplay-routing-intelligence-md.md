---
name: routing-intelligence
description: PowerPlay orchestrator routing — decision trees for command selection, complexity tiers, domain routing
alwaysApply: false
---

# PowerPlay Routing Intelligence

Used by the orchestrator prompts (`/pp`, `/quick`, `/sec`, `/test`, `/db`) to route plain-language requests to the appropriate command.

---

## Complexity Tiers

| Tier | Time | Triggers |
|------|------|----------|
| **Quick** | 1-2 min | Selected code < 100 lines, OR user says "quick/just/fast" |
| **Standard** | 5-10 min | Typical feature-sized code (100-500 lines), specific scope |
| **Full** | 15-30 min | "entire/complete/all/suite", multiple files, system-level scope |

When in doubt, ask the user: "Quick check or complete analysis?"

---

## Code Review Decision Tree

```
Is this a PR diff (diff format visible)?
  → YES: Use /pr-review (6-step review with Approve/Request Changes decision)
  → NO: Continue

Is the request a spot-check on selected code?
  → User says "quick/fast" OR code < 100 lines: Use /inline-review (severity table only)
  → Otherwise: Use /review (full structured review)

Is the user asking for a full module audit across all dimensions?
  → "audit everything", "all checks", "complete audit": Use /audit-all (security + perf + quality + coverage + docs)
  → No: Stick with /review or /inline-review
```

**Caution**: Do NOT use `/audit-all` for single functions — overhead exceeds value.

---

## Security Command Decision Tree

```
Does the user want a QUICK table of issues?
  → Selected code + no mention of "fix/remediate" → /security-scan (OWASP table, 2 min)

Does the user want FIX CODE?
  → Selected code + "fix", "remediate", "address", "fix these": /security-agent (table + fix code per item)

Is this ARCHITECTURE or DESIGN?
  → "design", "architecture", "zero-trust", "how should": /zero-trust-design (5 steps, identity/auth/network/encryption)

Is this about COMPLIANCE?
  → "compliance", "SOC 2", "HIPAA", "ISO 27001", "PCI": /compliance-audit (gap analysis against standard)

Is this about PENETRATION TESTING?
  → "pentest", "penetration test", "test our security": /pentest-plan (formal scope, methodology, ROE)

Did an INCIDENT happen?
  → "incident", "outage", "breach", "post-mortem": /incident-response (IR playbook + post-mortem template)
```

**Escalation pattern**: Start with `/security-scan`. If Critical/High issues found, follow up with `/security-agent` for remediation code.

---

## Testing Command Decision Tree

```
Is the code very small (< 50 lines) or single method?
  → YES: /add-tests (unit tests only, happy path + edge cases + null + exception)

Is the request "full suite", "complete", "all tests", or code > 200 lines?
  → YES: /generate-tests-complete (unit + integration + boundary + special cases)

Does the code already have tests and user wants to find gaps?
  → "coverage", "gaps", "what's not tested", "find untested": /coverage-gaps (analysis + top 5 test cases)

Is this about integration testing strategy?
  → "integration test", "end-to-end", "E2E", "test data": /integration-test-design (contract, E2E, test data strategy)
```

**Rule**: Use `/add-tests` for a single class or method. Use `/generate-tests-complete` only when the entire feature has no tests.

---

## Performance Command Decision Tree

```
Does the user want a QUICK ISSUE TABLE?
  → "what's slow", "find issues", "quick check": /performance-check (Severity | Location | Issue | Fix table)

Does the user want OPTIMIZED CODE WITH BEFORE/AFTER?
  → "make faster", "optimize", "fix the slow parts": /perf-optimize (analysis + before/after code + % improvement)

Is this SQL-SPECIFIC?
  → "SQL", "stored procedure", "query", "database performance": /optimize-sql (procedure-level: NOCOUNT, NOLOCK, indexes)

Is this WEB PERFORMANCE (bundle, Core Web Vitals)?
  → "bundle", "Lighthouse", "LCP", "INP", "CLS", "Core Web Vitals": /performance-audit (comprehensive web perf analysis)

Is this MEMORY-SPECIFIC?
  → "memory leak", "IDisposable", "event handler leak": /memory-audit (leak detection + patterns)
```

---

## Refactoring Command Decision Tree

```
Is this a SMALL, FOCUSED refactor on selected code?
  → "extract method", "simplify this", "one change": /refactor-inline (single transformation, output code only)

Is this a LARGE, MULTI-STEP refactor?
  → "large refactor", "plan a refactor", multiple files affected: /refactor-large (step-by-step plan with risks)

Is this MODULE-LEVEL with dependency analysis?
  → "dependency", "module", "refactor this module": /refactor-module (dependency map + refactoring plan)

Is this a VERSION UPGRADE?
  → "upgrade", "migrate", "new version", ".NET 9", "Angular 18": /migrate-version (breaking changes + migration steps)
```

---

## Database Command Decision Tree

```
Is this an EXISTING STORED PROCEDURE or QUERY?
  → /optimize-sql (SET NOCOUNT ON, SARGable WHERE, indexes, eliminate cursors)

Is this an EXISTING SCHEMA REVIEW?
  → "review schema", "is this design ok", "check database design": /database-design (normalization, indexes, constraints)

Is this SCHEMA DESIGN from REQUIREMENTS?
  → "design schema", "new database", "create tables", requirements-based: /data-model (from scratch design + migration skeleton)
```

---

## Cloud & Infrastructure Decision Tree

```
Is this AWS architecture?
  → "AWS", "Lambda", "S3", "DynamoDB": /aws-design (serverless/DB/API/storage/monitoring architecture)

Is this Azure resource provisioning?
  → "Azure", "App Service", "Functions", "Bicep": /azure-setup (Bicep IaC + deployment guide)

Is this containerization?
  → "Docker", "container", "Dockerfile": /docker-containerize (multi-stage Dockerfile + docker-compose)

Is this Kubernetes deployment?
  → "Kubernetes", "K8s", "Helm", "manifests": /kubernetes-deploy (K8s manifests: namespace, deploy, svc, ingress)

Is this IaC (Terraform/Bicep)?
  → "IaC", "Terraform", "infrastructure code": /iac-generate (Terraform or Bicep modules)
```

---

## UI & Design Decision Tree

```
Is this a NEW ANGULAR COMPONENT?
  → "Angular", "component", "standalone": /ng-component (Angular 17+ standalone + service + template)

Is this an ACCESSIBILITY AUDIT?
  → "WCAG", "accessibility", "contrast", "a11y": /design-audit (accessibility violations + fixes)

Is this DESIGN TOKENS or SYSTEM?
  → "design system", "tokens", "theme": /design-system (tokens file + documentation)

Is this a COMPONENT LIBRARY?
  → "component library", "Material", "Chakra", "Tailwind": /component-library (patterns + theme setup)

Is this a DATA TABLE?
  → "table", "sortable", "paginated": /table-design (sortable/filterable/paginated table + virtualization)

Is this CHARTS or VISUALIZATION?
  → "chart", "visualization", "graph", "D3", "Recharts": /chart-design (D3/Recharts/Chart.js example)

Is this STORYBOOK setup?
  → "Storybook", "stories", "visual regression": /storybook-setup (Storybook + Chromatic setup)

Is this RESPONSIVE DESIGN?
  → "responsive", "mobile", "breakpoints": /responsive-design (responsive audit across breakpoints)

Is this ANIMATION or MOTION?
  → "animation", "motion", "GPU", "performance": /motion-design (animation GPU acceleration + a11y + perf)
```

---

## Integration & Events Decision Tree

```
Is this EVENT-DRIVEN or CQRS/EVENT SOURCING?
  → "event-driven", "CQRS", "event sourcing", "saga": /event-driven-design (CQRS + event sourcing + saga patterns)

Is this MESSAGE QUEUE setup?
  → "message queue", "RabbitMQ", "Kafka": /message-queue-setup (topic/exchange design + implementation)

Is this WEBHOOK implementation?
  → "webhook", "HMAC", "signature verification": /webhook-implementation (webhook publisher + verification + retries)

Is this API COMPOSITION?
  → "API composition", "gateway", "aggregate": /api-composition (composition gateway design)
```

---

## Signal Words → Command Mapping

| User Says | DO Use | DO NOT Use | Why |
|-----------|--------|-----------|-----|
| "quick review" | /inline-review | /audit-all | Too fast for heavyweight audit |
| "full audit" | /audit-all | /review | Need all dimensions |
| "fix the security" | /security-agent | /security-scan | Scan doesn't include fixes |
| "add a test" | /add-tests | /generate-tests-complete | Single class doesn't need full suite |
| "complete test suite" | /generate-tests-complete | /add-tests | Entire feature needs comprehensive tests |
| "is this SQL ok?" | /optimize-sql | /database-design | Checking syntax/perf, not design |
| "design the schema" | /database-design | /optimize-sql | Schema design scope, not tuning |
| "containerize this" | /docker-containerize | /kubernetes-deploy | Dockerfile first, K8s is deployment |
| "deploy to K8s" | /kubernetes-deploy | /docker-containerize | Already containerized, need manifests |
| "what's slow here?" | /performance-check | /perf-optimize | Identify issues, don't optimize yet |
| "make this faster" | /perf-optimize | /performance-check | Want fixes, not just analysis |
| "PR review" | /pr-review | /review | PR has specific expectations |
| "spot check" | /inline-review | /audit-all | Lightweight, not comprehensive |
| "why is it slow?" | /explain-deep | /performance-check | Understanding, not optimization |
| "think through" | /think-through | /review | Meta-reasoning, not code analysis |

---

## Multi-Intent Handling

When a request spans 2+ categories:

1. **Execute the primary intent fully** (don't attempt both)
2. **After completion, suggest the next command:**
   - "Next: run `/[command]` to `[what it adds]`. Select the code and type it to continue."
3. **Only suggest if it genuinely adds value**
   - Don't suggest `/performance-check` after a simple typo fix
   - DO suggest `/add-tests` after fixing a bug in untested code
   - DO suggest `/refactor-large` after finding complex code in a `/review`

---

## Routing Confidence Rules

**Clear single match** → Route without asking
- User: "optimize this SQL" + has SQL code → /optimize-sql (no question needed)

**Two equally plausible categories** → Ask ONE clarifying question
- User: "review this" + ambiguous code → "Is this a [code quality check] or [security audit]?"
- Keep question to one sentence maximum

**Ambiguous or missing context** → Default routing
- No category match + has code → default to `/review`
- No category match + is a concept → default to `/think-through`
- Is a question about PowerPlay itself → suggest `/explain-deep`

---

## Category Shortcuts Quick Reference

Use these when routing `/sec`, `/test`, or `/db`:

**`/sec` routes:**
- Code only, no "fix" → OWASP scan table
- Code + "fix/remediate" → Full OWASP audit with fix code
- Architecture/design → Zero-trust design
- Compliance mention → Compliance audit

**`/test` routes:**
- Small code (< 50 lines) → unit tests only
- Large code or "full suite" → complete test file
- "coverage gaps" or has existing tests → gap analysis

**`/db` routes:**
- Stored procedure/query text → SQL optimization
- Existing schema (CREATE TABLE) → schema review (normalization, indexes, constraints)
- Requirements description → schema design from scratch

---

**Last Updated**: 2026-04-09
