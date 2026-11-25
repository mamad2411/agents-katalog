---
name: leaddocket-lead-relationships
description: >
  Associate contacts with leads as related parties, and assign users to lead
  roles on a specific lead, in LeadDocket. Use when adding co-plaintiffs,
  family members, witnesses, or other related contacts to a lead, or when
  programmatically assigning attorneys, paralegals, and intake staff to leads.
  For reading lead role definitions see leaddocket-lead-roles; for reading
  users see leaddocket-users.
---

# LeadDocket — Lead Relationships

All endpoints require API key authentication. Base URL: `https://{instance}.leaddocket.com`.

---

## Add a related contact to a lead

Associates an existing contact with a lead in a specified relationship capacity.

```http
POST /api/leads/addrelatedcontact?leadid={leadId}&contactid={contactId}&relationship={text}&additionalplaintiff={bool}
```

| Param | Required | Description |
|-------|----------|-------------|
| `leadid` | Yes | LeadDocket Lead ID |
| `contactid` | Yes | LeadDocket Contact ID |
| `relationship` | Yes | Relationship description (e.g., "Spouse", "Co-Plaintiff", "Witness") |
| `additionalplaintiff` | No | `true` marks contact as an additional plaintiff. Default `false`. |

Returns `200 OK`.

> The contact must already exist. If the contact doesn't exist yet, create it first using `leaddocket-contacts` (`POST /api/contacts`).

---

## Update a lead role user on a lead

Assigns a specific user to a specific lead role on a lead.

```http
PATCH /api/leads/updateleadroleuser?leadid={leadId}&leadRoleId={roleId}&assignToUserId={userId}
```

| Param | Required | Description |
|-------|----------|-------------|
| `leadid` | Yes | LeadDocket Lead ID |
| `leadRoleId` | Yes | Lead role ID (from `GET /api/leadroles`) |
| `assignToUserId` | Yes | User ID to assign (from `GET /api/users`) |

Returns `200 OK`.

---

## Common workflow: Lead intake with related contact

```
1. Create or find the primary contact
   POST /api/contacts → { Id: 101 }

2. Create or find a related contact (e.g., spouse)
   POST /api/contacts → { Id: 102 }

3. The intake creates the lead (via UI or another process)
   → Lead Id: 500

4. Add the related contact to the lead
   POST /api/leads/addrelatedcontact
     ?leadid=500&contactid=102&relationship=Spouse&additionalplaintiff=false

5. Assign the intake attorney to the lead
   GET /api/leadroles → find "Attorney" role Id: 3
   GET /api/users → find attorney user Id: 42
   PATCH /api/leads/updateleadroleuser?leadid=500&leadRoleId=3&assignToUserId=42
```

---

## Best Practices

- **Contact must pre-exist**: `addrelatedcontact` links existing contacts — it does not create new ones. Always create the contact first.
- **Relationship is free text**: Use consistent naming conventions (`"Spouse"`, `"Parent"`, `"Attorney-in-Fact"`) — LeadDocket stores whatever string you send.
- **Lead roles**: Get role IDs from `GET /api/leadroles`. Get user IDs from `GET /api/users` or `GET /api/users/byrole?leadRoleId={id}`. See `leaddocket-lead-roles` and `leaddocket-users`.
- **Re-assigning**: Calling `updateleadroleuser` again with a different `assignToUserId` replaces the previous assignment.
