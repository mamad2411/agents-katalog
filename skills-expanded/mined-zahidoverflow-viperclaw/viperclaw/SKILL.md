---
name: viperclaw
description: Master ViperClaw Application Security, Architecture & Compliance Audit entrypoint (`/viperclaw`). Guides source-code taint review, client bundle inventory, passive HTTP configuration/header inspection, and SARIF 2.1.0 remediation reporting.
---

# ViperClaw Application Security & Architecture Audit (`/viperclaw`)

Use this skill whenever the user invokes `/viperclaw` or requests a comprehensive codebase security review, configuration/posture audit, or OWASP/CWE remediation workflow.

## 5-Phase Audit & Remediation Workflow

1. **Phase 1 — Input Mode & Trust-Boundary Inventory (`viper-orchestrator`, `viper-threat-model-stride`):**
   - **Repository / Source Path (`/viperclaw ./repo`):** Run `viper_taint_scan` (`viperclaw taint . --db .viperclaw/graph.db`), `viper_harvest_js` (`viperclaw harvest-js . --db .viperclaw/graph.db`), `viper_secrets_scan`, `viper_iac_audit`, `viper_sbom_deps`, and `viper_mcp_audit` to map data flows, secrets, IaC posture, SBOMs, and trust boundaries.
   - **HTTP Endpoint / HAR Capture (`/viperclaw api.example.com` or `./traffic.har`):** Perform strictly non-destructive configuration and contract posture checks:
     - Inspect HTTP headers, TLS/CORS policy, cookie attributes (`HttpOnly`, `Secure`, `SameSite`), and framework signatures with `viper_fingerprint_traffic` (`viperclaw fingerprint`).
     - Inspect public service discovery metadata (`/.well-known/openid-configuration`, `/.well-known/jwks.json`, `/openapi.json`) with `viper_live_scan` and client bundle manifests with `viper_harvest_js`.
     - Do not run destructive fuzzing, high-volume traffic floods, or state-changing mutations against external endpoints.

2. **Phase 2 — Standards & Stack Audit Checklists (`viper-*` skills):**
   - Route to the applicable stack, cloud, and protocol compliance skills under `viper-*` (OWASP ASVS v4.0.3, OWASP Top 10:2025, OWASP API Top 10:2023, RFC 8725, RFC 9700):
     - **Auth, Tokens & Protocol Compliance:** `viper-auth-oauth-jwt`, `viper-oauth-oidc-compliance`, `viper-saml-sso-enterprise`, `viper-session-cookie-audit`, `viper-webauthn-passkey-mfa`.
     - **Access Control, Input Safety & Headers:** `viper-headers-csp-cors`, `viper-openapi-rest-schema`, `viper-multitenant-isolation`, `viper-proxy-parser-alignment`, `viper-taint-sast`.
     - **Application & Language Stacks:** `viper-nextjs-react-rsc`, `viper-fastapi-django-flask`, `viper-nodejs-express-nestjs`, `viper-go-service-audit`, `viper-rust-memory-unsafe`, `viper-java-spring-audit`, `viper-php-laravel-wordpress`, `viper-ruby-rails-audit`.
     - **Cloud, Containers & AI Guardrails:** `viper-aws-iam-cloud-audit`, `viper-gcp-azure-cloud-audit`, `viper-container-k8s-audit`, `viper-iac-terraform-audit`, `viper-terraform-drift-policy`, `viper-cicd-hardening`, `viper-secrets-audit`, `viper-dependency-sbom`, `viper-ai-llm-guardrails`, `viper-mcp-server-audit`, `viper-agent-skill-supplychain`, `viper-diff-pr-review`.

3. **Phase 3 — Control Verification (`viper-browseros-agent`, `viper_jwt_audit`, `viper_diff_oracle`):**
   - Audit token headers/claims against RFC 8725 using `viper_jwt_audit`, inspect browser storage/CSP telemetry via `viper_browser_ingest`, and compare control responses using `viper_diff_oracle`.

4. **Phase 4 — 7-Gate Evidence Quality & CVSS v3.1 Triage (`viper-proof-judge`):**
   - Validate every candidate finding with `viper_verify_and_report` (`viperclaw verify`) to filter false positives, verify scope and reachability, compute exact CVSS v3.1 scores, and emit SARIF 2.1.0 + Markdown reports.

5. **Phase 5 — Root-Cause Remediation & Regression Tests (`viper-remediation-patch-verifier`):**
   - Synthesize minimal, idiomatic fixes paired with positive and negative unit tests, then re-run `viper_taint_scan` to verify zero remaining unmitigated flows.
