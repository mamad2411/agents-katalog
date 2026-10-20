---
name: wstg-methodology
description: Run a structured web application assessment using the OWASP Web Security Testing Guide (WSTG v4.2) as the methodology spine — the twelve WSTG categories, the order to work them, and how to drive each phase with farai recon and web tooling. Use whenever the target is a web app or site and you need methodical, standards-mapped coverage rather than ad-hoc probing.
metadata:
  domain: offensive-security
  standards: "WSTG v4.2, OWASP Top 10:2025"
  tier: spine
---

# wstg methodology

the owasp web security testing guide (wstg) is the reference methodology for web
app testing. use it as the *spine*: it decides what to cover and in what order.
each category has an id (`WSTG-<CAT>-<NN>`) you cite in evidence and findings so
coverage is auditable. this skill is the map — load the matching per-topic
playbook for how to actually test each class.

## phases (work top to bottom; loop as you learn)

1. **WSTG-INFO — information gathering.** fingerprint the app, server, framework,
   metafiles, entry points, and surface. map before you poke. drive with the
   `recon` lane: subdomain enumeration, dns, http/tls probing, crawling, content
   discovery. delegate this — it is parallel and non-editing.
2. **WSTG-CONF — configuration & deployment.** tls config, headers, http methods,
   admin/backup files, cloud/storage exposure, cross-domain policy.
3. **WSTG-IDNT — identity management.** account provisioning, enumeration, weak
   username policy, role definitions.
4. **WSTG-ATHN — authentication.** credential transport, default/weak creds,
   lockout, bypass, remember-me, 2fa, password reset.
5. **WSTG-ATHZ — authorization.** directory traversal, privilege escalation, idor,
   and the differential-across-identities test. highest yield.
6. **WSTG-SESS — session management.** cookie attributes, fixation, csrf, logout,
   session timeout, jwt/token handling.
7. **WSTG-INPV — input validation.** injection (sqli, nosql, ssti, command,
   ldap, xxe), xss (reflected/stored/dom), header injection, host header, ssrf.
8. **WSTG-ERRH — error handling.** stack traces, verbose errors, exception leaks.
9. **WSTG-CRYP — cryptography.** weak tls, padding oracle, sensitive data in
   transit/at rest, weak randomness.
10. **WSTG-BUSL — business logic.** workflow bypass, request tampering, race
    conditions, abuse of intended functionality, file-upload logic.
11. **WSTG-CLNT — client-side.** dom xss, js execution, clickjacking, cors,
    websockets, postMessage, client storage, resource manipulation.
12. **WSTG-APIT — api testing.** rest/graphql surface; hand off to
    `owasp-api-top-10` for the API-specific classes.

## how to run it in farai

- **be the orchestrator.** fan out detached subagents per phase/scope with
  non-overlapping ownership (one for recon, others per host or per category),
  keep planning, and synthesize as results arrive. do not test inline.
- **prove, don't assume.** a finding needs a server-side effect, an exact
  request/response pair as evidence, and a reproduction — never a status code
  alone. record the `WSTG-<CAT>` id and the OWASP Top 10:2025 mapping on each
  finding.
- **map coverage.** track which WSTG categories are done / partial / blocked so
  gaps are explicit in the report.

## mapping to owasp top 10:2025

INFO/CONF → A02 misconfiguration · ATHZ → A01 broken access control · ATHN/SESS →
A07 authentication failures · INPV → A05 injection / A06 insecure design · CRYP →
A04 cryptographic failures · BUSL → A06 insecure design · CLNT → A02/A05 · APIT →
API top 10:2023. use `owasp-web-top-10` for the risk-ranked view and the
per-topic playbooks (access-control, authentication, injection, client-side,
business-logic) for technique detail.

reference: https://owasp.org/www-project-web-security-testing-guide/
