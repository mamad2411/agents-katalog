---
name: cybersecurity-check
description: >-
  Runs a comprehensive, EU-focused security and GDPR/DSGVO compliance check
  across a project's backend, frontend, and deployment configuration, then
  reports the results as one table (check, area, status, evidence,
  recommendation). Covers application security (OWASP-style: SSRF, injection,
  auth, access control, headers, secrets, rate limiting, ...), GDPR (Art.
  5–49: legal basis, special-category data, data subject rights,
  international transfers, DPIA, DPA/AVV, breach handling,
  retention/deletion), ePrivacy/cookie & tracking consent, email
  authentication (SPF/DKIM/DMARC), mobile-app specifics, and applicability of
  adjacent EU regulations (AI Act, Accessibility Act, NIS2, DSA, PSD2). Use
  this whenever the user asks for a "security check", "cybersecurity check",
  "security audit", "sicherheitscheck", "pentest-light", "security readiness
  review", "DSGVO check", "GDPR compliance check", or asks about any specific
  item this covers (SSRF, open redirects, webhook replay, email
  verification, staging data, SPF/DKIM/DMARC, consent-gated tracking,
  DPA/AVV, deletion concept, privacy policy, data subject rights, DPIA, EU AI
  Act transparency, accessibility) — even if they only name one or two and
  not "security check" explicitly. Also trigger before a production/store
  launch when the user asks "are we ready to go live" or similar readiness
  questions.
---  

# Cybersecurity & GDPR Check

A structured, evidence-based check of a project's backend, frontend, and deployment against
application-security best practice and EU data-protection law — not a live penetration test and
not legal advice. It investigates the codebase, configuration, and (where relevant) live
DNS/HTTP endpoints, and reports one table the user can act on.

## Ground rules

- **Evidence or it didn't happen.** Every row needs a concrete pointer — a `file:line`, a grep
  match, a command's actual output, or (for things code can't answer) an explicit note that this
  needs a human/legal decision. Don't mark something ✅ because it "looks fine" or "is standard" —
  either you found the safeguard in the code/config, or you didn't.
- **This is static investigation, not runtime testing, and not a legal opinion.** A ✅ on a
  security check means the code contains the safeguard as far as you could read it. A ✅ on a
  GDPR check means the documentary/technical evidence for compliance exists — it is not a lawyer's
  sign-off. Say both caveats once, up front, in the report so the user doesn't over-trust the
  result. Never phrase a finding as "this is GDPR-compliant" — phrase it as "the evidence for X is
  present/absent."
- **Some checks are not code problems.** SPF/DKIM/DMARC live in DNS, not the repo. DPA/AVV
  coverage, a DPIA, a retention policy, and EU-regulation applicability are legal/organizational
  facts a codebase can't fully prove or disprove — code review can only surface *evidence* (a
  documented DPA list, a retention-policy doc) or its *absence*. Be honest about which kind of
  check you're doing, per-row, using the status legend below.
- **Don't invent scope you can't check, and don't silently drop scope either.** If the project has
  no webhook receivers, or isn't in scope for NIS2, say so — mark the row `➖ N/A` with a one-line
  reason. Every check in this skill gets a row in the output; none are quietly skipped.
- **Never actually attack anything.** Confirming a webhook endpoint replays old signed payloads
  means reading the validation code — not firing a replayed request at a live server. Read-only
  investigation, plus passive external checks explicitly called out as safe (DNS lookups, response
  header checks against the project's own already-public endpoints).
- **Be genuinely thorough — this skill exists because "mostly checked" isn't good enough for
  health/personal data in the EU.** Don't stop at the first few checks in each file because the
  table is getting long; a check that's tedious to verify is usually exactly the one worth getting
  right.

## Workflow

1. **Map the surface.** Identify the backend framework/language, frontend framework/platform (web
   vs. mobile — this determines whether `mobile-eu-extra.md`'s mobile section applies), deployment
   setup (Docker/cloud/reverse proxy), auth provider, data categories processed (especially any
   Art. 9 special-category data — health, biometric, etc.), production domain(s), and every
   third-party service that receives personal data (AI providers, hosting, email, analytics,
   payment). Skim `README.md`/dev-setup/compliance docs first — most projects already document
   much of this and it saves a lot of exploration.
2. **Work through all four reference files** — every check in each one gets a row in the final
   table, marked ✅/❌/⚠️/➖ as appropriate:
   - `references/security.md` — application & infrastructure security (OWASP-style: injection,
     auth, access control, misconfig, headers, secrets, rate limiting, SSRF, open redirect,
     webhook replay, SPF/DKIM/DMARC, email verification, staging data, logging, backups)
   - `references/gdpr.md` — GDPR Art. 5–49: legal basis, special-category data, records of
     processing, DPIA, DPO, privacy by design, data subject rights, retention/deletion,
     international transfers, DPA/AVV coverage
   - `references/eprivacy-tracking.md` — cookie/tracking consent (ePrivacy Directive, national
     implementations like TTDSG), dark-pattern-free consent UI, mobile ad identifiers
   - `references/mobile-eu-extra.md` — mobile-app-specific security (secure storage, deep links,
     permissions), plus applicability assessment for the AI Act, Accessibility Act, NIS2, DSA, and
     PSD2 (most projects will be `➖ N/A` for several of these — that's a valid, reportable
     outcome, not something to skip evaluating)
3. **Investigate, don't assume.** Use Grep/Read/Bash freely: search for the actual pattern (HTTP
   client usage, redirect handling, webhook controllers, tracking SDK init, DNS records, consent
   screen logic) rather than inferring from framework defaults or the presence of a nicely-named
   file. A framework being "secure by default" doesn't mean this project didn't override that
   default; a `PrivacyPolicy.md` existing doesn't mean its contents match what the code does —
   spot-check that too if time allows.
4. **Report as one table** in the format below, most severe failures first within each area,
   followed by a short prioritized punch list of what to fix first.

## Output format

Start with 3-4 sentences: what was checked (confirm all four reference files were worked through),
what couldn't be reached (no staging environment to inspect, no DNS access, no visibility into a
signed contract's actual existence, etc.), and the two caveats from Ground rules (static
investigation only; not legal advice).

Then ALWAYS use this exact table — one row per check across all four reference files, none
omitted:

| # | Check | Bereich | Status | Befund | Empfehlung |
|---|---|---|---|---|---|
| 1 | ... | Security/GDPR/ePrivacy/Mobile/EU-Recht | ✅/❌/⚠️/➖ | file:line, command output, or doc reference | only if not ✅ |

(Match the table's actual language to the conversation's language — the column names above are
illustrative, not a fixed vocabulary. Keep "Befund"/"Evidence" concrete: a path+line, a command
and its output, or "not found — searched X, Y, Z". Group rows by area with a subheading or an
"Area" column, whichever reads more clearly for the number of rows involved.)

Status legend:
- ✅ Pass — safeguard/evidence found and verified in code/config/docs
- ❌ Fail — checked, safeguard or evidence is missing or broken
- ⚠️ Needs manual/legal review — code can't answer this (a signed contract's existence, legal text
  accuracy, a DNS record you don't have access to check, a DPIA judgment call)
- ➖ N/A — this check's surface/regulation doesn't apply here (state why in one clause — for the
  EU-regulation applicability checks in particular, the *reasoning* is the actual deliverable)

End with a short **prioritized punch list**: every ❌, ordered by how bad the exposure/legal risk
would be if left unfixed, each with the one-line fix. Follow it with a **needs-review list**: every
⚠️, since those are exactly the items a human (often a lawyer, for the GDPR ones) needs to close
out — don't let them get lost at the bottom of a long table.
