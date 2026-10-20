# Web Application Security Testing Skill

This comprehensive security testing framework enables Claude to assist with OWASP Top 10 assessments, injection vulnerability detection, API security analysis, and authentication testing across authorized targets.

## Key Capabilities

**Injection Testing**: The skill covers SQL injection, XSS, command injection, SSRF, and SSTI with systematic detection methodologies. It details how to discover injection points across parameters, headers, JSON bodies, and GraphQL queries, then provides payload libraries organized by database type and attack technique.

**API Security**: The framework includes checks for broken authentication, authorization flaws (BOLA/IDOR), input validation bypasses, and data exposure. GraphQL-specific tests address introspection abuse and circular query DoS vectors.

**Authentication Analysis**: Testing procedures cover session token entropy and management, OAuth/OIDC flows, JWT validation weaknesses (including `alg:none` attacks), and credential handling practices.

**Security Headers & CORS**: The skill provides assessment templates for checking Strict-Transport-Security, Content-Security-Policy, X-Frame-Options, and CORS misconfiguration scenarios like arbitrary origin reflection and null origin acceptance.

## Critical Authorization Requirement

The documentation emphasizes: "**Authorization Required**: All testing must be performed on authorized targets only. Confirm scope and written authorization before testing."

## Report Structure

Findings are documented with severity ratings, CVSS scores, CWE/OWASP mappings, step-by-step reproduction instructions, and specific remediation guidance—enabling clear communication with development teams.
