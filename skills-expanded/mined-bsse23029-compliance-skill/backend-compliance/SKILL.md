---
name: backend-compliance
description: Audits the backend/ Express API against privacy, security, tax and hospitality-reporting obligations — tenancy isolation, authn/authz, identity-document handling, encryption, retention and deletion, audit trails, payment and webhook integrity, outbound processors, AI calls. Use for any compliance question scoped to the server.
---

# Backend compliance

Surface: `backend/` — Express on Node 20, MySQL/Postgres, generated + project-specific CRUD APIs,
integration layer under `Services/Integrations/`. Graded **separately** from frontend and CI/CD.

This is where nearly every obligation lands: it holds the identity documents, it is the party that
must transmit to Shomoos and NTMP, it issues the ZATCA-compliant invoice, it is the PDPL
controller-side actor, and it is the one talking to OpenAI.

## What to check

### B-01 Tenant isolation
Multi-tenant PMS: cross-tenant read or write is the worst failure available. Check every generated
CRUD path (`Src/Apis/GeneratedApis/`, `Src/Apis/ProjectSpecificApis/`) enforces tenant scoping in
the query layer, not just in a middleware that some route can skip. Examine
`Services/Middlewares/PermissionCheck/`, `QueryResolver/` and `Services/Integrations/Database/`.
Sources: `OWASP-API-TOP10` (BOLA/BFLA), `SA-NCA-CCC` (data separation between tenants),
`SOC2-TSC` CC6, `ISO-27002`.

### B-02 Object-level authorisation
For each endpoint that takes an id, verify the record is checked against the caller's tenant *and*
role — not merely that a valid JWT was presented. Generated CRUD is exactly where this rots.
Sources: `OWASP-API-TOP10` API1/API3/API5, `OWASP-ASVS`.

### B-03 Authentication and session
`argon2` and `bcrypt` are both present — determine which is live and whether legacy hashes remain.
Check JWT signing algorithm and secret sourcing, `TOKEN_LIFETIME_MINUTES=60` and
`TOKEN_RENEWAL_THRESHOLD_SECONDS=300` behaviour, refresh/rotation (`AuthSessionRefresh`),
revocation on logout and on permission change, and the admin OTP flows (`AdminCodeVerify`,
`AdminCodeReset`). Sources: `OWASP-ASVS`, `SA-NCA-ECC`, `SOC2-TSC` CC6.

### B-04 Identity documents — the sharpest item
`passport_number`, `passport_issuing_country`, `passport_expiry_date`,
`passport_front_attachment_id`, `passport_back_attachment_id`, `cnic`, `date_of_birth`,
`nationality`, `address`. For each: encryption at rest (column-level or storage-level), who can
read it (which roles, which endpoints, which exports), whether it appears in logs, whether S3
presigned URLs are short-lived, and how long it is kept after checkout.
Sources: `SA-PDPL-LAW`, `SA-PDPL-IR`, `ISO-27701`, `EU-GDPR` Art. 9-adjacent sensitivity, `ISO-27018`.

### B-05 Lawful basis and disclosure register
Saudi properties must transmit guest identity data to MOI (Shomoos) and occupancy/financial data to
the Ministry of Tourism (NTMP). These are legal obligations — record them as the lawful basis, and
record every other disclosure (payment gateways, SMS/WhatsApp, email, OTA, AI) with its basis.
Sources: `SA-MOI-SHOMOOS`, `SA-MT-NTMP`, `SA-PDPL-IR`; see `ksa-hospitality-reporting`.

### B-06 Cross-border transfer
Where does data physically go? Azure region, S3 `S3_REGION`, OpenAI (US), Firebase, SMS/WhatsApp
providers, email. Each egress out of the Kingdom needs a lawful transfer route and, for continuous
or large-scale sensitive transfers, a documented risk assessment.
Sources: `SA-PDPL-TRANSFER`, `SA-PDPL-TRA-GUIDE`, `SA-CST-CCRF`, `EU-GDPR` Ch. V.

### B-07 Retention and deletion
Is there a retention schedule per data class, and does anything enforce it? Check the cron layer
(`Services/Integrations/CronJobs/`) for any purge job. Tax records have a **minimum** retention
that conflicts with privacy minimisation — resolve explicitly per field rather than deleting a
folio wholesale. Deletion must reach backups, `Uploads/`, S3, logs and `WorkflowData/`.
Sources: `SA-PDPL-IR`, `SA-VAT`, `EU-GDPR` Art. 17, `ISO-27701`.

### B-08 Data-subject rights machinery
Access, correction, deletion, portability/export — is there an implementation, an SLA, an audit
trail of requests, and identity verification of the requester? Sources: `SA-PDPL-IR`, `EU-GDPR`,
`US-CCPA`.

### B-09 Audit trail and log integrity
`Services/Middlewares/ApiLogger/`, `ApiLogsCrud`, `Services/Integrations/Database/Errorlog.js`.
Check: are privileged actions (rate override, folio edit, refund, permission change, guest-data
export) logged with actor, tenant, before/after; are logs tamper-evident; are they retained long
enough; and — the inverse risk — do they contain PII, tokens or card data they should not.
Sources: `SA-NCA-ECC`, `SOC2-TSC` CC7, `PCI-DSS` 10, `ISO-27002`.

### B-10 Payments and PCI scope
`Services/Integrations/Payments/` — Stripe, Apple, Chase/Authorize.net, KuickPay, plus a Moyasar
webhook route. Establish for each: does any PAN/CVV touch our process, memory, logs or DB? Are
webhooks signature-verified and replay-protected (`Src/Routes/webhooks.js`,
`moyasarWebhook.js`, `appleWebhook.js`, `Payments/routes/PaymentWebhook.js`)? Are refunds
authorised and logged? See `pci-dss-scoping`. Sources: `PCI-DSS`, `VENDOR-STRIPE`, `VENDOR-MOYASAR`.

### B-11 E-invoicing correctness
Saudi: cryptographic stamp, UUID, hash chain, QR, XML to spec, clearance/reporting per phase and
wave. Pakistan: real-time reporting through a licensed integrator, and the 72-hour cancel/edit
window after which only the Commissioner IR can approve a change — this constrains how mutable a
folio may ever be. Sources: `SA-ZATCA-EINV-REG`, `SA-ZATCA-SPEC`, `SA-ZATCA-SECURITY`,
`PK-FBR-DIGITAL-INVOICING`, `AE-EINV`.

### B-12 Outbound processors
`Notifications/implementations/` has Email, Push, SMS and WhatsApp channels; `Mailer/sendEmail.js`;
`geoip-lite`; Firebase. For each: what personal data is sent, is it minimised to purpose, is there
a DPA, and where does that processor store it. Sources: `SA-PDPL-IR`, `ISO-27701`, `EU-GDPR` Art. 28.

### B-13 AI calls
`Services/Integrations/AI/OpenAi/queryOpenAi.js` and `AI/LMStudio/`. What is in the prompt — does
guest PII leave the Kingdom to a US model provider? Is there prompt-injection exposure where model
output drives an action? Is AI use disclosed where guest-facing? See `ai-governance`.
Sources: `OWASP-LLM-TOP10`, `SA-PDPL-TRANSFER`, `EU-AI-ACT` Art. 50, `SA-SDAIA-AI`, `ISO-42001`.

### B-14 Secrets and configuration
`sample_env` exposes the shape: DB credentials, a second `SECURITY_DB_*`, S3 keys, Stripe secret
key, KuickPay, Authorize.net signature key. Check for hardcoded secrets in the repo, secrets in
logs, key rotation, and whether `Uploads/`, `data/` or `WorkflowData/` hold anything sensitive in
version control. Sources: `SA-NCA-ECC`, `OWASP-ASVS`, `SOC2-TSC` CC6.

### B-15 Transport and storage encryption
TLS at the edge is not the question — check container-to-database, container-to-S3, backups, and
whether anything sensitive is written to disk unencrypted. Sources: `SA-NCA-ECC`, `SA-NCA-CCC`,
`PCI-DSS` 4, `ISO-27017`.

### B-16 Input validation and injection
`Services/Middlewares/ParameterValidation/` and the dynamic query/CRUD layer are the places where a
generated API meets user input. Check parameterisation across `mysql`, `mysql2` and `pg` paths, file
upload handling (`multer`, `Uploads/`), and the dynamic route resolver (`dynamicRoutes.js`).
Sources: `OWASP-ASVS`, `OWASP-TOP10`.

### B-17 Rate limiting, abuse and availability
`express-rate-limit` and `helmet` are present — verify they are applied to the guest-facing and
auth endpoints, not just mounted. Sources: `OWASP-API-TOP10` API4, `SOC2-TSC` A1.

### B-18 Backup and restore
Existence, encryption, region, retention, and a **tested** restore. An untested backup is a `gap`
under both continuity and PDPL availability duties. Sources: `ISO-22301`, `SOC2-TSC` A1, `SA-NCA-ECC`.

### B-19 Distribution and device integrations (not yet present — assess on arrival)
No OTA, channel-manager, POS or door-lock integration exists in the repo today. When one lands it
brings its own contract: guest data flowing to a third-party distributor, rate and availability
integrity, and physical-access data. Use the vendor's own API documentation as the authoritative
source, with `HOSP-OPENTRAVEL` and `HOSP-HTNG` for the interface conventions. Record this as a
standing `n/a — not implemented` row so the question is revisited rather than forgotten.

## Grading notes

- Evidence is a path under `backend/` with a line number. "The middleware exists" is not evidence
  that it is applied to the route in question — check the route wiring.
- Generated CRUD deserves its own rows. The risk profile of `GeneratedApis/` is not the same as
  hand-written endpoints, and a single scoping bug there is systemic.
