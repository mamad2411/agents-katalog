---
name: leaddocket-users
description: >
  Look up and filter Users in LeadDocket. Covers listing all users, fetching
  by ID, filtering users by lead role, looking up by Case Tracker Code, and
  looking up by Filevine User ID. Use for role assignment automation,
  Filevine integration user mapping, and populating assignment dropdowns in
  external systems. For admin-level user management (invite, permissions) see
  leaddocket-user-management. For lead role definitions see
  leaddocket-lead-roles.
---

# LeadDocket — Users

All endpoints require API key authentication. Base URL: `https://{instance}.leaddocket.com`.

---

## List all users

```http
GET /api/users
```

Returns array of `UserApi`.

---

## Get a user by ID

```http
GET /api/users/{id}
```

Returns `UserApi`.

---

## Get users by lead role

```http
GET /api/users/byrole?leadRoleId={id}
```

Returns array of `UserApi` with that role. Get `leadRoleId` values from `GET /api/leadroles`.

Useful for: "Give me all users who can be assigned as Attorney."

---

## Get user by Case Tracker Code

```http
GET /api/users/getuserbycode/{code}
```

Returns `UserApi`. The Case Tracker Code is the user's ID in the connected case management system.

---

## Get user by Filevine User ID

```http
GET /api/users/getuserbyfilevineuserid/{id}
```

Returns `UserApi`. Use for Filevine bidirectional sync to map Filevine users to LeadDocket users.

---

## UserApi response shape

```json
{
  "Id": 42,
  "FirstName": "Maria",
  "LastName": "Garcia",
  "Email": "maria@lawfirm.com",
  "IsActive": true,
  "Code": "MGARCIA",
  "FilevineUserId": 8812,
  "Roles": ["Attorney", "Intake Specialist"]
}
```

---

## Best Practices

- **Cache the user list**: Users change rarely. Cache `GET /api/users` for a few hours in automation workflows to avoid per-request lookups.
- **Use `byrole` for role-specific assignment**: When building "assign to an attorney" logic, use `byrole` to get only eligible users rather than filtering the full list yourself.
- **Filevine mapping**: Store the cross-reference of `FilevineUserId` → LeadDocket `Id` in your integration layer to avoid repeated lookups.
- **Inactive users**: Check `IsActive: true` before offering users in assignment UIs. The API returns both active and inactive users in `GET /api/users`.
