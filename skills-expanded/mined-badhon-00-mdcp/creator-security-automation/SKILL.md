---
name: creator-security-automation
description: One cross-agent workflow for defensive cybersecurity, website protection, E2E quality assurance, and complete rights-safe YouTube content automation.
---

# MDCP Unified Creator + Security Automation

Use this as the compact entrypoint for creator workflows and defensive application security. Route each request to only the relevant section. The unified MCP tool is named `mdcp`; YouTube's existing dedicated `youtube` tool remains available as a compatibility adapter.

## Fast router
- Website security, vulnerability discovery, hardening → **Defensive security**
- SQL injection, XSS, auth/session, API safety → **Application protection**
- Browser journeys, regression, E2E, accessibility → **Testing**
- YouTube channel growth, ideas, scripts, calendar → **Creator strategy**
- Thumbnails, captions, editing, Shorts, audio → **Production**
- Upload, scheduling, SEO, playlists, analytics → **Publishing**
- Copyright claims, music/footage licensing, reused content → **Rights management**

## Safety boundaries
- Test only owned systems or targets covered by explicit written authorization and a defined scope.
- Default to passive inspection, source review, safe test fixtures and staging environments.
- No credential theft, phishing, persistence, malware, stealth, destructive exploitation, unauthorized scanning, data exfiltration or bypassing access controls.
- Do not run SQL injection/XSS payloads against third-party production systems. Validate defenses in local labs or authorized staging with synthetic data.
- Never evade YouTube Content ID, copyright claims, licensing terms or platform enforcement. Do not disguise copied work as original.
- Do not publish, change visibility, delete, comment, or mutate playlists without specific approval. Uploads default to private.

## Defensive security

### Authorized discovery
1. Confirm asset owner, written authorization, in-scope domains/IPs, exclusions, test window, rate limits and emergency contact.
2. Inventory public routes, APIs, authentication boundaries, dependencies and data classes without collecting unnecessary personal data.
3. Begin with passive TLS/HTTP header review, configuration review, dependency advisories, secret scanning and source-code review.
4. Classify findings by severity, exploitability, impact, evidence, affected component and remediation.
5. Retest fixes in staging; record residual risk and evidence.

### Vulnerability coverage
- Injection: SQL/NoSQL/command/template injection; use parameterized queries and safe APIs.
- Browser: XSS, CSRF, clickjacking, CORS misconfiguration and unsafe DOM sinks.
- Identity: weak authentication, MFA gaps, session fixation, insecure cookies, password reset and account enumeration.
- Authorization: IDOR/BOLA, role escalation, tenant isolation and server-side access checks.
- API: schema validation, rate limiting, mass assignment, excessive data exposure and object-level authorization.
- Infrastructure: TLS, security headers, exposed admin surfaces, secrets, dependency/container issues and least privilege.
- Data: encryption in transit/at rest, retention, backups, logging redaction and privacy controls.

### SQL injection protection
- Bind every user-controlled value; never concatenate user input into SQL.
- Use prepared statements and safe ORM parameter APIs; audit raw-query escape hatches.
- Apply least-privilege database roles, allowlisted dynamic identifiers, safe error handling and regression tests.
- Treat escaping and input validation as defense-in-depth, not substitutes for parameterization.
- Review source statically first; verify with synthetic fixtures in a controlled test database.

### Website protection checklist
HTTPS/TLS; HSTS; CSP; frame protection; nosniff; Referrer-Policy; Permissions-Policy; secure/HttpOnly/SameSite cookies; CSRF protection; server-side authorization; rate limits; dependency patching; secret management; backups; audit logging; alerting; secure error handling; WAF/CDN rules where appropriate.

## E2E and quality testing
Create a test matrix for critical journeys, roles, negative cases, API contracts, accessibility, mobile layouts, browser compatibility, network failures, retries and data cleanup. Prefer Playwright for browser automation. Use staging, synthetic accounts and isolated test data. Capture failure traces with secrets and personal data redacted. Include regression tests for every fixed vulnerability.

## YouTube creator automation

### Full workflow
1. Channel audit and audience/content-pillar strategy.
2. Research topics and viewer intent; build a publishing calendar.
3. Generate brief, hook, script, storyboard, shot list and narration.
4. Prepare rights-cleared footage, images, music, fonts and voice assets.
5. Generate thumbnail concepts and produce a final image using an image tool.
6. Edit video/Shorts: assemble timeline, crop/reframe, captions, audio mix, transitions, color and export.
7. Run QA: aspect ratio, codec, loudness, captions, spelling, thumbnail readability and rights checklist.
8. Generate title, description, chapters, tags and pinned-comment draft.
9. Preview; request approval; upload privately or schedule only after explicit approval.
10. Add to playlists, monitor analytics and produce a concise performance report.

### Automation capabilities and integration boundaries
Use the YouTube Data API for authorized channel metadata, uploads and playlists; YouTube Analytics API for owner-only analytics. Use FFmpeg or a selected editor for deterministic media transforms; use image-generation tools for thumbnails; use speech/transcription tools for narration and captions when configured. Long-running rendering/upload tasks need a durable job queue, worker, object storage and resumable/idempotent jobs. The skill describes orchestration; it does not itself provision those cloud services or grant API permissions.

### Rights and copyright management
Maintain an asset ledger containing source, creator, license/permission, allowed platforms, territories, term, attribution and proof. Use original or properly licensed music, footage, images, fonts and voice. Check for third-party claims through official platform workflows; document licenses and dispute only when there is a good-faith legal basis. Prefer original commentary, analysis, education or transformation with meaningful new expression, but do not assume that any label or edit automatically makes a use fair or lawful. Never promise copyright-free status or guaranteed monetization.

## Token-efficient execution
- Keep this file as the single umbrella entrypoint; load only the matching workflow.
- Use one `mdcp` tool and one operation per call where the host supports it.
- Return bounded findings, top risks and concise evidence; do not dump raw logs or full analytics.
- Cache stable metadata; fetch volatile metrics only when needed.
- Delegate deterministic rendering, test execution and report formatting to configured tools.
- Inference tokens cannot be reduced to zero; savings depend on host, model, tool schemas and task size.

## Expected output
Return: **Scope**, **Actions**, **Findings/artifacts**, **Approvals needed**, **Verification status**, **Next step**. Clearly distinguish a plan from a test actually executed.
