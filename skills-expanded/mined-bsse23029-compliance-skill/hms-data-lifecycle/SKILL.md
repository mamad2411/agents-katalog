---
name: hms-data-lifecycle
description: The guest and staff personal-data map for this hotel system — what each PMS module collects, why, who can see it, which external party receives it, where it rests, how long it is kept and how it is deleted. Use to build or refresh the data inventory, to answer a DSR, or before assessing any module against a privacy regime.
---

# HMS data lifecycle

Every privacy regime in this stack — `SA-PDPL-IR`, `EU-GDPR`, `ISO-27701`, `US-CCPA` — asks the
same eight questions of every field. Answer them once, per module, and most of the privacy grid
fills itself in.

## The eight questions

For each data element in each module:

1. **Collected where** — which screen, API, import or integration
2. **Why** — the purpose, and the lawful basis for it
3. **Who can access** — which roles, which endpoints, which exports and reports
4. **Which service receives it** — internal modules and external processors
5. **Where stored** — table, object storage, cache, log, backup, and the **region** of each
6. **How long retained** — and what enforces that
7. **Can the guest have it deleted** — and what legally blocks deletion (tax, Shomoos records)
8. **Can the guest export it** — in what format

## Data classes used across the grids

| Class | Examples in this schema | Sensitivity |
|---|---|---|
| `identity-doc` | `passport_number`, `passport_issuing_country`, `passport_expiry_date`, `passport_front_attachment_id`, `passport_back_attachment_id`, `cnic` | **Highest.** Government identity documents plus scanned images |
| `guest-pii` | name, `email`, `phone_no`, `address`, `date_of_birth`, `nationality` | High |
| `stay-data` | reservation, room, dates, occupancy, preferences, special requests | Medium — special requests can carry health or religious data by accident |
| `payment` | gateway tokens, last-4, transaction ids; PAN if ever present | High — see `pci-dss-scoping` |
| `credential` | password hashes, JWTs, OTPs, API keys | High |
| `staff-pii` | employee records, shift data, performance | High — employment data has its own expectations |
| `audit` | API logs, error logs, change history | Medium — often contains PII by accident |
| `commercial` | rates, contracts, corporate agreements | Confidential, not personal |

## Module → data map

Build this in `compliance/modules/backend.yaml` from the real repo, not from a generic PMS list.
The starting inventory from the codebase:

- **Guest identity and profile** — `BookingUsers/`, `Profile/`, guest APIs. Holds `identity-doc`
  and `guest-pii`. The most exposed module in the system.
- **Reservations and check-in** — booking, check-in grouped CRUD, availability, quoting.
- **Catalog, pricing, packages** — `CatalogCrud`, `CatalogPricingCrud`, `CustomPricing_rules`,
  `CustomPackages`, `HotelPackageStudio` (frontend). Mostly `commercial`.
- **Billing and payments** — `AdminBookingCheckout`, `AdminBookingPayment`,
  `Services/Integrations/Payments/`, folio and invoice paths. `payment` plus fiscal obligations.
- **Services and locations** — `CustomServices`, `ServiceLocationFacets`, `ServiceLocations`,
  `CrudCities`, `CrudLandmarks`, `LocationTypesCrud`, `RegionCountriesCrud`.
- **Tenancy and provisioning** — `TenantProvisioningGroupedCrud`, `TenantConfigs`,
  `TenantAssignmentsGroupedCrud`, `ServiceManagerProvisioning`, `TenantManagerCandidates`.
  Cross-tenant boundary lives here.
- **Users, permissions, auth** — `CustomUsersGroupedCrud`, `CustomPermissionGroupsGroupedCrud`,
  `AuthSessionRefresh`, `AdminCodeVerify`, `AdminCodeReset`, `ValidationEmail`,
  `ValidationDuplicate`. `credential` and `staff-pii`.
- **Config and governance** — `ConfigConstraints`, `HmsConfigKeysEnabledForCrud`,
  `HmsConfigPossibleValuesCrud`, `CustomConfigPossibleValues`, frontend `Governance/`.
- **Logging and observability** — `ApiLogsCrud`, `Services/Middlewares/ApiLogger/`,
  `Errorlog.js`, frontend `ServerLogs/`. `audit`, frequently contaminated with PII.
- **Notifications** — Email, Push, SMS, WhatsApp channels. Four egress paths for `guest-pii`.
- **Files and uploads** — `multer`, `Uploads/`, S3 via `@aws-sdk/client-s3`. Where passport scans
  live.
- **Cron and lifecycle jobs** — `Services/Integrations/CronJobs/`. Where retention enforcement
  should live, if it exists.
- **AI** — OpenAI and LM Studio. What leaves the Kingdom in a prompt.

## Retention conflicts — resolve at field level

Deletion requests and tax/regulatory retention collide constantly in a PMS. Do not resolve them
wholesale in either direction:

| Data | Constraint |
|---|---|
| Issued invoices and folio lines | Statutory retention (`SA-VAT`, ZATCA archival). Cannot be deleted on request |
| Shomoos transmission records | Legal-obligation processing; retain the record of disclosure |
| Passport scans | No lasting purpose after the stay and any statutory retention — the strongest candidate for aggressive deletion |
| Marketing consent state | Retain the *evidence of consent decision* even after withdrawal |
| Audit logs | Retain for security, but minimise PII inside them |

The right answer is usually: keep the fiscal record, delete or anonymise the identity payload
around it. That requires the schema to separate them — check whether it does.

## Output

A per-surface module inventory in `compliance/modules/`, with data classes attached. That inventory
is the row source for `compliance-grid`.
