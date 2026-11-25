---
name: leaddocket-lead-roles
description: >
  Manage Lead Role definitions in LeadDocket — the named roles (Attorney,
  Paralegal, Intake Specialist, etc.) that can be assigned to users on leads.
  Covers listing all roles and deleting roles. Use to discover role IDs for
  use in user assignment (leaddocket-lead-relationships) and user lookup
  (leaddocket-users).
---

# LeadDocket — Lead Roles

All endpoints require API key authentication. Base URL: `https://{instance}.leaddocket.com`.

A **Lead Role** is a named position on a lead — such as "Attorney", "Paralegal", "Case Manager", or "Intake Specialist". Users are assigned to leads in a specific role.

---

## List all lead roles

```http
GET /api/leadroles
```

Returns array of `LeadRoleApi`:

```json
[
  { "Id": 1, "Name": "Attorney" },
  { "Id": 2, "Name": "Paralegal" },
  { "Id": 3, "Name": "Intake Specialist" },
  { "Id": 4, "Name": "Case Manager" }
]
```

---

## Delete a lead role

```http
DELETE /api/leadroles/{id}
```

Returns `200 OK`.

> ⚠️ Deleting a lead role removes it from all leads where it was assigned. Use with care — prefer deactivation if the platform supports it.

---

## Common usage patterns

```
# 1. Discover role IDs
GET /api/leadroles
→ [{ Id: 1, Name: "Attorney" }, { Id: 2, Name: "Paralegal" }]

# 2. Find users eligible for that role
GET /api/users/byrole?leadRoleId=1
→ [{ Id: 42, Name: "Maria Garcia" }, { Id: 43, Name: "Tom Chen" }]

# 3. Assign a user to a lead in that role
PATCH /api/leads/updateleadroleuser?leadid=500&leadRoleId=1&assignToUserId=42
```

---

## Best Practices

- **Cache role IDs**: Lead roles rarely change. Cache the list for the day in automation.
- **Cross-reference with assignment**: Role IDs here are the same ones used in `PATCH /api/leads/updateleadroleuser` (see `leaddocket-lead-relationships`) and `GET /api/users/byrole` (see `leaddocket-users`).
- **Roles are firm-specific**: The set of roles varies by firm — always fetch from the API, never hardcode names or IDs.
