---
name: frontend-compliance
description: Audits the frontend/ Vite + React SPA against privacy, security and consent obligations — browser storage of personal data, build-baked env vars, consent and cookie handling, security headers, masking of identity documents, RTL/Arabic localisation of notices. Use for any compliance question scoped to the web client.
---

# Frontend compliance

Surface: `frontend/` — Vite + React SPA, built to static assets, served by nginx from
`frontend/Dockerfile`. Graded **separately** from backend and CI/CD.

The frontend's compliance role is narrower than people expect and sharper than they expect. It
cannot be the enforcement point for authorisation — but it is the only enforcement point for
consent, and it is where personal data most easily leaks into places nobody is watching: browser
storage, URLs, analytics, console logs, and the JS bundle itself.

## What to check

### F-01 Build-baked secrets
Everything passed as `VITE_*` is compiled into the public bundle. `frontend/sample_env` declares
`VITE_SECRET_KEY` and `VITE_PLATFORM_KEY`, and `Deploay-DEV.yml` feeds them from GitHub secrets
into `docker build --build-arg`. **Anything treated as a secret there is not one.** Determine what
`VITE_SECRET_KEY` actually does; if it guards anything server-side, that is a finding against
`OWASP-ASVS` (secret management) and `SA-NCA-ECC`.
Check: `grep -rn "VITE_" frontend/src | grep -iE "secret|key|token"` and inspect `frontend/build/`.

### F-02 Personal data in browser storage
Search `localStorage`, `sessionStorage`, IndexedDB and cookies for guest PII, identity-document
data, tokens and tenant identifiers. Passport numbers, CNIC, dates of birth or document images
must not persist client-side beyond the interaction. Sources: `SA-PDPL-IR`, `EU-GDPR`, `ISO-27701`.

### F-03 Token handling
Where the JWT lives (`localStorage` vs memory vs httpOnly cookie), whether it is cleared on logout
and on tab close, and whether the 60-minute lifetime plus 5-minute renewal window from
`TOKEN_LIFETIME_MINUTES` is honoured client-side. Sources: `OWASP-ASVS` session management,
`SOC2-TSC` CC6.

### F-04 Identity-document display and masking
The schema holds `passport_number`, `passport_front_attachment_id`, `passport_back_attachment_id`,
`cnic`. Check which screens render them in full, whether they appear in list views and exports,
and whether presigned S3 URLs for document scans are short-lived and not logged or shared.
This is the single highest-sensitivity item on this surface. Sources: `SA-PDPL-LAW`, `SA-PDPL-IR`.

### F-05 Consent and cookie notice
Is there a consent mechanism at all, and does it gate anything non-essential? For EU-facing booking
flows the ePrivacy rule is consent **before** the write, with refusal as easy as acceptance.
Sources: `EU-EPRIVACY`, `EU-GDPR`, `US-CCPA` (opt-out signals). Note the Digital Omnibus may change
the cookie regime — check the registry entry before designing a banner.

### F-06 Privacy policy, terms, and data-subject entry points
Are privacy policy, terms, contact-for-DSR, deletion request and data export reachable from the UI
in every locale served? An export/deletion process with no UI entry point is a `gap`, not a
`partial`. Sources: `SA-PDPL-IR`, `EU-GDPR` Arts 12–22, `ISO-27701`.

### F-07 Security headers
`frontend/Dockerfile` writes the nginx config inline with an SPA fallback and **no** CSP, HSTS,
X-Content-Type-Options, X-Frame-Options or Referrer-Policy. Grade each header as its own row.
Sources: `OWASP-ASVS`, `OWASP-TOP10`, `PCI-DSS` 6.4.3 if any payment page script runs here.

### F-08 Payment surface
Determine whether card fields are ever rendered by our code or only by a gateway iframe/redirect
(Stripe, Moyasar, KuickPay, Apple Pay are all present in the backend). If our page hosts fields or
scripts on a payment page, PCI scope expands sharply — see `pci-dss-scoping`.

### F-09 Logging and error output
`VITE_DROP_CONSOLE` exists — verify it is actually on in production builds and that no PII or token
reaches the console, an error tracker, or a third-party script. Sources: `SA-PDPL-IR`, `OWASP-ASVS`.

### F-10 Client-side authorisation
`frontend/src/root/Components/Permissions/` suggests permission-driven UI. Confirm it is *only*
UX — every hidden control must also be denied server-side. A UI-only restriction is a BOLA/BFLA
finding on the backend, recorded here as a cross-reference. Sources: `OWASP-API-TOP10`.

### F-11 Localisation of legal text
`LanguageProvider.jsx` and `language.js` indicate multi-locale support. Arabic/RTL notices,
consent text and DSR instructions must exist in the languages the tenant serves — a Saudi guest
notice only in English is a weak position under `SA-PDPL-IR`.

### F-12 Third-party scripts
Inventory every external script, font, analytics and map provider loaded by the SPA. Each is a
processor and a supply-chain risk. Sources: `OWASP-TOP10` A03:2025, `PCI-DSS` 11.6.1.

## Grading notes

- Frontend rows are frequently `n/a` for tax and reporting obligations (ZATCA, NTMP, Shomoos, FBR
  are backend duties) — record them `n/a` with that reason rather than omitting them.
- Never mark a frontend row `compliant` because the backend handles it. Cross-reference instead.
- Evidence is a path under `frontend/src/`, with a line number.
