---
name: leaddocket-user-management
description: >
  Manage users and teams in LeadDocket at the admin level — inviting new users,
  configuring roles and permissions, setting up lead role assignments, and
  deactivating users. This is a UI-based skill (no write API for user
  management). For reading users and looking them up via API see
  leaddocket-users.
---

# LeadDocket — User & Team Management

User management in LeadDocket is handled through the admin UI. The API supports read-only user operations.

> Support section: [Manage Users](https://support.leaddocket.com/hc/en-us/sections/360009378652-Manage-Users)

---

## Inviting New Users (Admin, in the LeadDocket UI)

1. Navigate to **Settings → Users**
2. Click **Invite User**
3. Enter the user's email address
4. Select their **Role** (admin, standard, etc.)
5. Select their **Lead Roles** (Attorney, Paralegal, Intake Specialist, etc.)
6. Click **Send Invitation**

The user receives an email to set their password and activate their account.

---

## User Types / Permission Levels

| Level | Access |
|-------|--------|
| **Admin** | Full access: settings, users, billing, all leads |
| **Standard** | Access to leads, contacts, tasks per their lead role |
| **Intake Only** | Limited to creating/viewing opportunities |
| **View Only** | Read-only access to leads |

---

## Lead Roles vs. User Types

| Concept | Purpose |
|---------|---------|
| **User Type** | Overall system permission level |
| **Lead Role** | The role a user plays on a specific lead (Attorney, Paralegal, etc.) |

A user can have one system permission level but be assigned to leads in any number of lead roles.

---

## Configuring Lead Roles

1. Navigate to **Settings → Lead Roles**
2. Add/edit/delete role definitions
3. For each role, configure:
   - Role name
   - Whether this role receives lead notification emails
   - Default assignment (auto-assign based on rules)

---

## Deactivating a User

1. Navigate to **Settings → Users**
2. Find the user
3. Click **Deactivate**

Deactivated users cannot log in but their historical lead assignments are preserved. Their leads are **not** automatically reassigned — do this manually before deactivating.

---

## Managing User Assignment on Leads

Use the API to reassign users to leads programmatically:

```http
# Get all lead roles
GET /api/leadroles

# Get all users
GET /api/users

# Get users for a specific role
GET /api/users/byrole?leadRoleId={id}

# Assign user to a lead in a role
PATCH /api/leads/updateleadroleuser?leadid={id}&leadRoleId={rid}&assignToUserId={uid}
```

See `leaddocket-lead-relationships` and `leaddocket-users` for details.

---

## Best Practices

- **Deactivate before the user leaves**: Reassign their leads and deactivate the account on or before the user's last day.
- **Use lead roles for specialization**: Don't rely only on system permissions. Use lead roles (Attorney, Case Manager, Intake Specialist) to route the right work to the right person.
- **Audit assignments monthly**: Run a report of leads without an assigned Attorney or Paralegal and reassign orphaned leads.
- **Test new user access**: After inviting a new user, have them log in and verify they can see the leads and features they need.
