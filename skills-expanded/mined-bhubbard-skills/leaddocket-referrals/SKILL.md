---
name: leaddocket-referrals
description: >
  Manage Referral Sources in LeadDocket — the attorneys, firms, medical
  providers, and organizations that send leads. Covers listing all referrals,
  fetching by ID or external code, adding new referral sources, editing
  existing ones, deleting, listing referral groups and practice areas, and
  syncing referrals with external case management systems via Case Tracker Code
  and External Code. Use for referral network management, cross-system sync,
  and CRM integrations.
---

# LeadDocket — Referrals

All endpoints require API key authentication. Base URL: `https://{instance}.leaddocket.com`.

A **Referral Source** represents an external party (attorney, firm, medical provider, marketing channel) that sends leads to the firm.

---

## List all referral sources

```http
GET /api/referrals/list
```

Returns array of `ReferralSourceApi`.

---

## Get a referral source by ID

```http
GET /api/referrals/{id}
```

Returns `ReferralSourceApi`.

---

## Get by external code

```http
GET /api/referrals/getbyexternalcode?externalCode={code}
```

Returns the first matching `ReferralSourceApi`. Useful for looking up a referral source using an ID from your external CRM.

---

## List referral groups

```http
GET /api/referrals/listgroups
```

Returns array of `ReferralGroupApi`. Groups are used to organize referral sources.

---

## List practice areas used on referral sources

```http
GET /api/referrals/listpracticeareas
```

Returns array of strings (unique practice area names). Use to populate dropdowns in intake forms.

---

## Add a new referral source

```http
POST /api/referrals
Content-Type: application/json

{
  "Name": "Smith & Associates",
  "FirstName": "John",
  "LastName": "Smith",
  "Email": "john@smithlaw.com",
  "Phone": "555-987-6543",
  "PracticeArea": "Personal Injury",
  "ReferralGroupId": 5,
  "ExternalCode": "EXT-4521"
}
```

`ReferralSourceAddApi` — returns `200 OK` with the created referral.

---

## Edit an existing referral source

```http
PUT /api/referrals/{id}
Content-Type: application/json

{
  "Name": "Smith & Associates LLP",
  "Email": "contact@smithlaw.com",
  ...all fields...
}
```

Returns `200 OK` with updated `ReferralSourceApi`.

---

## Delete a referral source

```http
DELETE /api/referrals/{id}
```

Returns `200 OK`.

---

## Associate with external systems

```http
# Set Case Tracker Code (primary case management system ID)
PUT /api/referrals/updatecode?id={referralId}&code={cmsCode}

# Set External Code (any external system identifier)
PUT /api/referrals/updateexternalcode?id={referralId}&externalCode={extCode}
```

Both return `200 OK`. Use `getbyexternalcode` to look up by the stored external code later.

---

## Best Practices

- **Deduplicate on add**: Call `listall` and check by `Name` or `ExternalCode` before adding — there's no built-in duplicate prevention.
- **Use External Code for CRM sync**: Store your CRM's contact/firm ID as `ExternalCode` to enable bidirectional lookups without storing LeadDocket IDs in your external system.
- **Case Tracker Code vs. External Code**: Case Tracker Code is specifically for the primary case management system (e.g., Filevine). External Code is for any other external system.
- **Practice areas**: Fetch `listpracticeareas` to keep intake dropdowns in sync with what's configured in LeadDocket.
