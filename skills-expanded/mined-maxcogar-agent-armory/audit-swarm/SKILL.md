\---

name: audit-swarm

description: "Spawn a parallel swarm of 7 specialized production code auditors (security, error handling, validation, performance, architecture, production readiness, test coverage). Each subagent writes findings to a file, then a synthesizer consolidates results into a prioritized report. Use when auditing code for production readiness, reviewing a feature before deployment, performing comprehensive code quality assessment, or any time you want a thorough multi-domain audit. Triggers on 'audit my code', 'production readiness check', 'review this for deployment', 'code quality audit', 'is this production ready', or any request for comprehensive code review across multiple quality dimensions."

disable-model-invocation: true

argument-hint: "\[scope — files, directories, or feature description]"

\---



\# Audit Swarm



Spawn a parallel swarm of specialized production code auditors. Each subagent focuses on one audit domain, writes findings to a file, and a synthesizer consolidates the results.



\## Arguments



`$ARGUMENTS` specifies the audit scope. Examples:

\- `backend/` — audit the entire backend directory

\- `src/api/auth.ts src/api/users.ts` — audit specific files

\- `the new payment integration` — audit a described feature (you determine which files)

\- (empty) — audit the full project



\## Setup — Mandatory Before Dispatch



Before dispatching subagents, YOU must gather the context they all need. Do not skip any of these steps.



\### 1. Read the Plan



If there is a planning doc, architecture doc, spec, or CLAUDE.md that describes what the code should do — read it. The subagents need to know what was intended, not just what exists. Check for:

\- `docs/planning/` or `docs/plans/`

\- `CLAUDE.md`, `ARCHITECTURE.md`, `README.md`

\- Any spec or design doc referenced in `$ARGUMENTS`



If no planning docs exist, note that in the shared context — the subagents will audit against engineering standards only, without spec compliance.



\### 2. Search CORE Memory



Use the `core-memory` MCP tool to search for:

\- Past architectural decisions related to this code

\- Previous audit findings or reviews for this project

\- Historical context on why certain patterns were chosen

\- Known issues or incidents related to this area

\- Team decisions about coding standards and conventions



Include relevant CORE results in the shared context block. Past decisions prevent subagents from contradicting established architectural choices or repeating previously-identified issues.



\### 3. Determine the Audit Target



If `$ARGUMENTS` names files or directories, those are the target. If it describes a feature, identify the relevant files using grep, file listing, and codegraph if available. If empty, the target is the full project source.



\### 4. Create the Output Directory



Create `docs/audits/YYYY-MM-DD/` (today's date). If that directory already exists (multiple audits same day), append a sequence number: `docs/audits/YYYY-MM-DD-2/`.



\### 5. Build the Shared Context Block



Every subagent receives this same preamble:



```

\## Audit Target

\[List of files/directories being audited]



\## Project Context

\[Language, framework, what the project does, deployment target]



\## Plan / Spec Summary

\[Key requirements from planning docs, or "No planning docs found — audit against engineering standards only"]



\## Relevant Past Decisions (from CORE)

\[Architectural decisions, past review findings, known issues, or "No relevant CORE context found"]



\## Scope

\[What the user asked to be audited — their exact words from $ARGUMENTS]

```



\## Dispatch



Read each subagent prompt file from this skill's directory, then spawn all 7 in parallel using `Task`.



Each `Task` call includes:

1\. The full subagent prompt text (read from file)

2\. The shared context block (built above)

3\. The output file path to write findings to



\## Supporting Files



Each subagent prompt lives in this skill's directory. Read them before dispatching:



\- `${CLAUDE\_SKILL\_DIR}/security-auditor.md` — Security domain (OWASP, auth, injection, XSS, CSRF, secrets, crypto). Output: `docs/audits/YYYY-MM-DD/01-security.md`

\- `${CLAUDE\_SKILL\_DIR}/error-handling-auditor.md` — Error handling domain (async catches, error types, logging, degradation). Output: `docs/audits/YYYY-MM-DD/02-error-handling.md`

\- `${CLAUDE\_SKILL\_DIR}/validation-auditor.md` — Type safety \& validation domain (schemas, type guards, sanitization, boundaries). Output: `docs/audits/YYYY-MM-DD/03-validation.md`

\- `${CLAUDE\_SKILL\_DIR}/performance-auditor.md` — Performance domain (queries, caching, async, memory, connections). Output: `docs/audits/YYYY-MM-DD/04-performance.md`

\- `${CLAUDE\_SKILL\_DIR}/architecture-auditor.md` — Architecture domain (SOLID, layer separation, coupling, testability). Output: `docs/audits/YYYY-MM-DD/05-architecture.md`

\- `${CLAUDE\_SKILL\_DIR}/production-readiness-auditor.md` — Production infrastructure domain (logging, health checks, shutdown, config). Output: `docs/audits/YYYY-MM-DD/06-production-readiness.md`

\- `${CLAUDE\_SKILL\_DIR}/test-coverage-auditor.md` — Test coverage \& documentation domain (unit/integration tests, edge cases, API docs). Output: `docs/audits/YYYY-MM-DD/07-test-coverage.md`

\- `${CLAUDE\_SKILL\_DIR}/synthesizer.md` — Consolidation instructions (read after all 7 subagents complete). Output: `docs/audits/YYYY-MM-DD/00-consolidated-report.md`



\## After All Subagents Complete



Once all 7 subagents have finished and written their findings files:



1\. \*\*Read all 7 findings files.\*\*



2\. \*\*Synthesize.\*\* Read `${CLAUDE\_SKILL\_DIR}/synthesizer.md` and follow its instructions to produce the consolidated report at `docs/audits/YYYY-MM-DD/00-consolidated-report.md`.



3\. \*\*Report to user.\*\* Summarize: how many findings at each severity level, which domains had the most critical issues, and the recommended fix priority. Point the user to the consolidated report.



\## File Layout After Completion



```

docs/audits/YYYY-MM-DD/

├── 00-consolidated-report.md    # Synthesized findings + priority

├── 01-security.md               # Security auditor findings

├── 02-error-handling.md         # Error handling findings

├── 03-validation.md             # Validation findings

├── 04-performance.md            # Performance findings

├── 05-architecture.md           # Architecture findings

├── 06-production-readiness.md   # Production readiness findings

└── 07-test-coverage.md          # Test coverage findings

```

