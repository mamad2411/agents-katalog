---
description: "CB - Production-readiness audit: code + infra + deployment + accessibility"
---

# Production Readiness Audit

Audit this codebase for production-readiness. Covers code quality,
security, data governance, infrastructure, deployment, and
accessibility. Answer: is this ready for production? If not, what
specifically is wrong?

## Context

Before starting, determine from the repo:
- What does this app do? (read README, entry points)
- How is it deployed? (check for CI workflows, platform configs:
  `staticwebapp.config.json`, `netlify.toml`, `vercel.json`,
  Dockerfiles)
- Are there production URLs? (check README, config files, workflow
  files for domain names / deployment targets)
- Are there related repos or APIs? (check config for API base URLs,
  imports from other packages)
- Repo age: run `git log --reverse --format='%aI' | head -1` to get
  the first commit date, then calculate days from that date to TODAY
  (not to the latest commit)

If the user provided arguments, use them to fill in known context.

## Output

Produce a SINGLE report at
`.claude/memories/{reponame}_full_audit_{YYYY-MM-DD}.md` where
`{reponame}` is the repository name (from `git remote get-url origin`,
strip the org/host prefix and `.git` suffix) and `{YYYY-MM-DD}` is
today's date. Do NOT create intermediate files -- write the final
report directly.

## Audit Phases

Execute these phases in order. Each phase feeds the next.

### Phase 1: Structural scan

Use code-index MCP tools:
- `get_project_summary()` -- full codebase overview
- `get_analysis_playbook(focus="quality")` -- tool sequence
- `find_hotspots()` -- risk hotspots by change frequency x complexity
- `find_ownership_risks()` -- bus factor
- `find_cognitive_complexity()` -- top complex functions
- `find_bloated_functions()` -- functions exceeding multiple thresholds
- `find_deep_nesting()` -- nesting depth violations
- `find_duplicates()` -- structural duplicates
- `find_unhandled_errors()` -- missing error handling
- `find_testability_issues()` -- hard-to-test code
- `find_nested_loop_patterns()` -- potential O(n^2)+
- `find_circular_deps()` -- circular imports
- `analyze_coupling()` -- module coupling metrics
- `find_dead_code()` -- unreferenced symbols
- `find_temporal_coupling()` -- hidden co-change dependencies

Also collect the Codebase Profile metrics from the code-index tools:
- `get_project_summary()` -- total files, symbols, languages, LOC
- `find_hotspots()` -- commits, repo age, activity pattern
- `find_ownership_risks()` -- contributors, bus factor

For each section, record not just the raw data but the interpretation:
- Hotspots: concentration risk, expected defect rate vs baseline
- Bloated/complexity: totals out of total analyzed (e.g. "88 of 962")
- Duplicates: group by pattern (modal handlers, getters, etc.)
- Nesting: count functions exceeding depth 3, note worst depth
- Architecture: note module system (ES modules, script tags, none),
  explain zero-coupling or zero-temporal-coupling when it's a monolith
  side effect rather than good design

Record all numbers. These feed the Structural Analysis section.

### Phase 2: Automated audits (run in parallel)

Spawn these agents simultaneously:

1. **Security audit** (Audit Security agent)
2. **Data governance audit** (Audit Data Governance agent)
3. **Observability audit** (Audit Observability agent)
4. **Resilience audit** (Audit Resilience agent)
5. **Dependencies audit** (Audit Dependencies agent)
6. **Documentation audit** (Audit Documentation agent)

### Phase 3: Manual inspection

These are patterns the automated agents often miss. Check each
explicitly:

**Architecture:**
- State management pattern (blob vs. proper resources?)
- API design (REST resources vs. opaque storage?)
- Multi-user concurrency (optimistic locking? ETags? last-write-wins?)
- Build pipeline (bundler? minification? or raw source deployed?)
- Module system (ES modules? script tags? single file?)

**Security -- targeted checks:**
- `postMessage` handlers: check every `addEventListener("message"` for
  `event.origin` validation
- `innerHTML` / template literal HTML: count assignments, check if
  user/external input reaches them unescaped
- Auth token storage: localStorage vs sessionStorage, CSP presence
- Dev/localhost bypasses that ship to production
- Client-side authorization checks (role/admin checks in JS that
  should be server-side)
- External scripts: SRI (integrity) attributes present?
- Security headers: check `staticwebapp.config.json`, `netlify.toml`,
  `_headers`, `vercel.json` for CSP, HSTS, Permissions-Policy,
  X-Frame-Options, X-Content-Type-Options

**Data governance -- targeted checks:**
- PII inventory: grep for email, name, address, phone, postcode,
  subject, tenant fields. Trace where they are stored (localStorage,
  IndexedDB, cookies, URL params, API calls, third-party services)
- Consent mechanism: search for "consent", "privacy", "cookie", "gdpr"
- Data deletion: what does logout/reset clear? What persists?
- Third-party data sharing: Google Fonts (IP leak), CDN loads,
  external API calls with user data in params
- Data files: are there CSVs, JSONs, or JS data blobs with real
  addresses, names, or other PII? Verify if addresses are real by
  checking one against a public API (PDOK, Google Maps, etc.)

**Infrastructure -- targeted checks:**
- What is the deploy directory? Is it the repo root? (publish = ".")
- Are internal files (scripts/, docs/, README, .github/, .gitignore)
  publicly accessible?
- CI/CD: are there quality gates (tests, lint, type-check) before
  deploy? Or straight to production on push?
- Environment separation: can you switch between dev/staging/prod
  without editing source?
- Stale deployment configs from previous platforms?
- For Azure: check for duplicate resources, Free tier in production,
  Function App settings (FTPS, health check, CORS, managed identity)

**Accessibility (WCAG 2.2 AA):**
- Focus styles: is `outline: none/0` applied globally?
- Skip link present?
- ARIA roles: tabs, dialogs, alerts used correctly?
- Live regions for dynamic content updates?
- Table semantics: scope, caption?
- Modal focus trapping?
- Heading hierarchy (starts with h1?)
- Motion: prefers-reduced-motion respected?
- Form errors: aria-invalid, aria-describedby?

### Phase 4: Production verification (read-only only)

If production URL(s) are known, run ONLY read-only checks:

```bash
# Security headers
curl -sI https://[PRODUCTION_URL]/ | head -20

# Webroot exposure -- check each internal path
curl -sI https://[PRODUCTION_URL]/README.md
curl -sI https://[PRODUCTION_URL]/scripts/
curl -sI https://[PRODUCTION_URL]/.gitignore
curl -sI https://[PRODUCTION_URL]/.github/
# Add more paths based on what you find in the repo

# Stale/duplicate deployments (if Azure SWA names are known)
curl -sI https://[STALE_SWA_URL]/
```

Do NOT test any write paths (login, save, edit, API POST/PUT/DELETE).
The production environment may have fragile persistence (blob storage,
no idempotency). Read-only HTTP checks only.

Record all curl results in the report.

### Phase 5: Consolidation

Build the final report using the template at
`.claude/templates/production-audit-report.md`. Follow its structure
exactly. Fill in all sections from the data collected in Phases 1-4.

Key points:
- Findings grouped by category, not by severity bucket
- Each finding gets an ID: `{CAT}-{S}{N}` (e.g., SEC-C1, RES-H2)
- Production verification results include discrepancy analysis
  (repo config vs. actual production behavior)
- Manual checklist items marked as VERIFIED / SKIPPED / FAIL
- Positive findings listed separately

## Categories

Use these for grouping. Only include categories that have findings.

- Architecture and Structure (ARC)
- Security (SEC)
- Data Governance / GDPR (DG)
- Observability and Logging (OBS)
- Resilience and Error Handling (RES)
- Code Quality (CQ)
- Accessibility (A11Y)
- Dependencies (DEP)
- Infrastructure and Deployment (INF)
- Documentation (DOC)

## Rules

- Severity labels: CRITICAL / HIGH / MEDIUM / LOW
- ID prefix per category (e.g., SEC-H1, RES-C2, DOC-M3)
- Deduplicate across phases: if security agent and manual inspection
  find the same issue, merge into one entry
- Preserve file:line references
- Do not invent findings -- only report what you observe
- Do not propose solutions -- findings and evidence only
- Verify claims where possible (curl production URLs, check if
  addresses in data files are real, confirm header presence)
- If a finding from automated scan is contradicted by production
  verification, note both and adjust severity
- For WCAG findings, note the conformance level (A or AA)
