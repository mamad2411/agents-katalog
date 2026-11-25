---
name: leaddocket-settlements
description: >
  Track and retrieve financial Settlement records on Leads in LeadDocket.
  Covers creating new settlement records for a lead, fetching by settlement ID,
  and listing all settlements for a lead. Use for syncing settlement data with
  accounting systems, case management platforms, or reporting dashboards.
---

# LeadDocket — Settlements

All endpoints require API key authentication. Base URL: `https://{instance}.leaddocket.com`.

A **Settlement** represents the financial resolution of a case — recording the gross settlement amount, attorney fees, expenses, and net client recovery tied to a specific lead.

---

## Get a settlement by ID

```http
GET /api/settlements/{id}
```

Returns `SettlementApi`.

---

## Get all settlements for a lead

```http
GET /api/settlements/getbyleadid/{id}
```

Returns array of `SettlementApi`.

---

## Add a new settlement for a lead

```http
POST /api/settlements
Content-Type: application/json

{
  "LeadId": 1234,
  "GrossSettlement": 250000.00,
  "AttorneyFee": 83333.33,
  "Expenses": 12500.00,
  "SettlementDate": "2026-06-15",
  "Notes": "PI case resolved at mediation"
}
```

`SettlementAddApi` fields:

| Field | Required | Description |
|-------|----------|-------------|
| `LeadId` | Yes | Lead to associate settlement with |
| `GrossSettlement` | Yes | Total settlement amount |
| `AttorneyFee` | No | Attorney fee portion |
| `Expenses` | No | Case expenses |
| `SettlementDate` | No | Date of settlement (YYYY-MM-DD) |
| `Notes` | No | Settlement notes |

Returns `200 OK` with `SettlementApi`.

---

## SettlementApi response fields

```json
{
  "Id": 456,
  "LeadId": 1234,
  "GrossSettlement": 250000.00,
  "AttorneyFee": 83333.33,
  "Expenses": 12500.00,
  "NetClientRecovery": 154166.67,
  "SettlementDate": "2026-06-15",
  "Notes": "PI case resolved at mediation",
  "CreatedDate": "2026-06-16T10:22:00Z"
}
```

`NetClientRecovery` is calculated by LeadDocket: `GrossSettlement - AttorneyFee - Expenses`.

---

## Best Practices

- **Check for existing settlements**: Call `GET /api/settlements/getbyleadid/{id}` before adding to avoid duplicates in automated workflows.
- **Decimal precision**: Send financial amounts as decimals with 2 places. LeadDocket stores currency to cent precision.
- **SettlementDate**: Use `YYYY-MM-DD` format. This is the date the settlement occurred, not the recording date.
- **Sync to case management**: Store the returned `Id` in your external system to reference or avoid re-creating the record.
