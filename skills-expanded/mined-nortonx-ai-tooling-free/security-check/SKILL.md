---
name: security-check
description: "Audit code against the OWASP Top 10 (injection, XSS, CSRF, auth and sessions, data exposure, misconfiguration, vulnerable dependencies, API security) and write a findings report with severity, location, proof of concept and fix. Args: [<path>]"
argument-hint: "[<path>]"
---

<!-- Note: $ARGUMENTS is substituted by Claude commands only. In Copilot,
     the user must include their argument inline in the prompt; the skill
     body sees the literal text "$ARGUMENTS" unsubstituted. -->

## Arguments

`[<path>]`

- Optional. A file or directory to scope the audit; omit to audit the whole project.
- **Examples**: `/security-check`, `/security-check src/api`

> Copilot CLI note: `$ARGUMENTS` does not substitute in skills; include the argument inline in your prompt.

# Security check: $ARGUMENTS

Audit the code against the OWASP Top 10 and report the findings. Read the relevant code (route
handlers, authentication, database access, configuration, dependencies) before asserting anything: a
finding without evidence in the code is noise and costs the trust of whoever has to fix it.

## Language and style

Write the report in the language of the user's request. Use active voice, short sentences, one idea per
paragraph, no decorative emoji, and **explain why** each risk matters, not only what it is. Keep code
identifiers in backticks with their original spelling.

## OWASP Top 10

1. **Injection**: SQL, NoSQL, OS commands, LDAP, XPath
2. **Authentication and sessions**: weak passwords, insecure credential storage, session fixation, missing session timeout
3. **XSS**: reflected, stored, DOM-based, missing output encoding
4. **Insecure direct object reference (IDOR)**: unauthorized access, missing access controls
5. **Security misconfiguration**: insecure defaults, unnecessary features enabled, missing security headers, verbose errors
6. **Sensitive data exposure**: unencrypted data, weak encryption, leaks in logs or URLs
7. **CSRF**: missing or weak CSRF tokens
8. **Vulnerable dependencies**: outdated libraries, missing security patches
9. **Logging and monitoring**: missing audit trails, inadequate error logging
10. **API security**: missing rate limiting, weak authentication, excessive data exposure

## Report

For each finding, give these fields:

- **Severity**: Critical / High / Medium / Low
- **Location**: affected file(s) and line(s)
- **Proof of concept** (when applicable)
- **Remediation steps**

### Structure

1. Executive summary of the security posture
2. Critical and high findings (fix immediately)
3. Medium and low findings (plan for upcoming sprints)
4. Long-term security recommendations

At the end, if the report uses 5 or more technical acronyms, add a short glossary table with the
meaning of each one. Omit the obvious ones (SQL, API) and keep the domain-specific ones (IDOR, CSRF).
