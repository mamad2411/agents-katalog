---
name: team-management
description: A language-agnostic guide for implementing secure, scalable team and organization management using SSOJet APIs.
---

# SSOJet Team Management (Language-Agnostic, B2B-Ready)

## Context

The user is already authenticated using **SSOJet OIDC (Authorization Code flow)**.

This skill guides developers to implement **secure, scalable team and organization management** using SSOJet APIs, following **best coding practices** and working across **any language or framework** (Next.js, Golang, .NET, Node.js, etc.).

## Goal of This Skill

Enable developers to build **B2B SaaS team management** by correctly handling:

* User ↔ Tenant relationships
* Multi-organization users
* Role-based access
* Secure backend-only management APIs

## Core Architecture Rules (Mandatory)

1. **Language-agnostic**
   * Describe flows, not frameworks
   * Use pseudocode when needed
   * Avoid framework-specific assumptions

2. **Separation of concerns**
   * Frontend → UI only
   * Backend → auth, tenant, team logic
   * Management APIs are never called from the client

3. **Token safety**
   * User access token → identity & context
   * Management token → admin operations only
   * Never expose management tokens

4. **Explicit tenant context**
   * No “default tenant”
   * Tenant ID must be selected and passed explicitly

5. **Client Identification**
   * All Management API calls **MUST** include `client_id` as a query parameter.
   * Format: `?client_id=<management_client_id>`

## Step-by-Step Instructions

### 1️⃣ Obtain a Management Token (Backend Only)

Use **Client Credentials Grant** with `sys_owner` scope.

```json
{
  "client_id": "<client_id>",
  "client_secret": "<client_secret>",
  "grant_type": "client_credentials",
  "scope": "sys_owner"
}
```

**Best practices**
* Cache token until expiry
* Refresh automatically
* Never return this token to frontend
* **Token Endpoint:** `POST /api/v1/oauth2/token`
* **Base URL:** Ensure your API calls use the `/api/v1` prefix (e.g., `https://api.ssojet.com/api/v1`).

### 2️⃣ Identify the Logged-In User

From the user’s **OIDC access token**, extract:
* `sub` → user ID
* Basic identity claims (email, name)

Do **not** assume tenant membership from the token alone.

### 3️⃣ Fetch User’s Tenants (Source of Truth)

To get **all organizations the user belongs to**, call:

```http
GET /users/{userId}/tenants
```

> **API Reference:** [List User Tenants](../../apis/users.md#list-user-tenants)
>
> "Returns a complete list of all tenants the user is a member of, along with their associated roles and context within each tenant."

**Rules**
* This API is the authoritative source for user–tenant mapping
* Do not rely only on JWT claims
* Backend must call this API using the **management token**

### 4️⃣ Tenant Selection (B2B SaaS Flow)

This is the critical "fork in the road" for B2B apps.

#### Scenario A: User belongs to existing tenants
* **UI:** Show a "Select Organization" screen or dropdown.
* **Action:** specific tenant ID is selected.
* **Persistence:** Store `tenant_id` in the frontend session/cookie.

#### Scenario B: User has no tenants (New Sign-up)
* **UI:** Redirect to an "Onboarding / Create Organization" page.
* **Form:** Ask for "Company Name" and "Workspace URL".
* **Backend Action:**
    1. Call **Create Tenant API** (`POST /tenants`).
       ```json
       {
         "name": "string",
         "display_name": "string",
         "domains": [ "string" ]
       }
       ```
       > **API Reference:** [Create Tenant](../../apis/tenants.md#create-tenant)

    2. Call **Add User to Tenant API** (`POST /tenants/{id}/users`).
       ```json
       {
         "user_ids": ["current_user_id"]
       }
       ```
       > **API Reference:** [Add Users to Tenant](../../apis/tenants.md#add-users-to-tenant)

    3. Call **List All Roles API** (`GET /roles`) to find the `Owner` role ID.
       > **API Reference:** [List All Roles](../../apis/roles.md#list-all-roles)

    4. Call **Assign User Roles API** (`POST /tenants/{id}/users/{uid}/roles`).
       ```json
       {
         "role_ids": ["owner_role_id"]
       }
       ```
       > **API Reference:** [Assign User Roles](../../apis/tenants.md#assign-user-roles)

    5. Auto-select the new tenant and proceed to the dashboard.

### 5️⃣ Multi-Tenant (B2B SaaS) Enforcement

Your system must support:
* One user → multiple tenants
* Different roles per tenant
* Safe tenant switching

**Recommended request context**
```
user_id
selected_tenant_id
role_in_tenant
```

### 6️⃣ Fetch Users of a Tenant (Team Listing)

To list **all users in a selected tenant**, use the endpoint that matches your authentication context:

#### A. Using User Access Token (Recommended for Front-facing APIs)
Use the JWT obtained during the OIDC login flow. This endpoint returns roles specific to the tenant context.
* **Method:** `GET`
* **Endpoint:** `/auth/tenants/{tenantId}/users`
* **Header:** `Authorization: Bearer {User_Access_Token}`

#### B. Using Management Token (System/Service level)
Use this if you are performing administrative tasks without a user context.
* **Method:** `GET`
* **Endpoint:** `/tenants/{tenantId}/users`
* **Header:** `Authorization: Bearer {Management_Token}`

**Display Requirements:**
* Email / Name
* Role (Extracted from the tenant's role list)
* Status (active, pending)

### 7️⃣ Filtering & Status Management

To provide a complete "Team Members" view, combine data from two sources:

1.  **Active Members**: Call the members listing API (above) and filter for `is_active: true`.
2.  **Pending Invitations**: Call `GET /tenants/{id}/invitations?status=pending` using the **Management Token**.

**Implementation Note:** Standardize both responses into a shared model for the UI.

### 8️⃣ Invite New Team Members

Provide a backend endpoint that:
* Accepts email + role
* Verifies inviter’s role (Owner/Admin)
* Calls **Team Member Invite API** with full payload:
    * `invitee`: `{ email: "..." }`
    * `inviter`: `{ user_id: "...", email: "..." }` (Required)
    * `role_ids`: `["..."]`
    * `send_invitation_email`: `true`
    * `expire_in_minutes`: `10080` (7 days)
* Returns invite status

```http
POST /tenants/{tenantid}/invitations
```

> **API Reference:** [Invite Team Member](../../apis/team-invites.md#invite-team-member)
>
> "Generates a new onboarding invitation for a user to join the tenant workspace. This process creates a secure invitation token, associates it with the tenant, and dispatches an invitation email."

### 9️⃣ Remove Team Members

Allow only authorized roles to remove members. The removal logic depends on the member's status:

#### A. Remove Active Member
To remove an active user from the tenant, use the bulk delete endpoint:
* **Method:** `DELETE`
* **Endpoint:** `/tenants/{tenantid}/users`
* **Body:**
  ```json
  {
    "user_ids": ["userId"]
  }
  ```

#### B. Remove Pending Invitation
To cancel or remove a pending invitation, use the invitation delete endpoint:
* **Method:** `DELETE`
* **Endpoint:** `/tenants/{tenantid}/invitations?invitation_id={invitationId}`

**Best practices**
* Prevent accidental self-removal (last owner).
* Provide a clear confirmation dialog in the UI before proceeding.

### 🔟 Fetch Available Roles

Use the **Roles API** to:
* Fetch role list dynamically
* Assign roles during invite/update
* Avoid hardcoded role names

```http
GET /roles
```

> **API Reference:** [List All Roles](../../apis/roles.md#list-all-roles)
>
> "Retrieves a list of all defined roles within the system."

## 🎨 Frontend/UI Implementation Guidelines

To ensure a professional B2B experience, follow these UI patterns:

### 1. Tenant Switcher (Navigation)
* **Location:** Top-left of the sidebar or navbar.
* **Component:** Dropdown menu showing current tenant name + avatar.
* **Actions:**
    * List other available tenants.
    * "Create New Organization" button.
    * "Settings" link for the current tenant.

### 2. Team Members List (Settings Page)
* **Layout:** Table view.
* **Columns:** User Info (Avatar+Name+Email), Role (Badge), Status (Active/Invited), Actions (Three-dot menu).
* **Actions:** "Edit Role", "Remove Member", "Resend Invite" (for pending).

### 3. Invite Member Modal
* **Trigger:** Primary button "Invite Member" on Team page.
* **Fields:**
    * **Email Address** (Input).
    * **Role** (Select/Dropdown) - fetched dynamically from backend.
* **Feedback:** Show success toast notification and refresh the list immediately.

### 4. Empty States
* **Scenario:** No members in the team (other than self).
* **UI:** "You are the only member. Invite your team to collaborate."
* **Call to Action:** Prominent "Invite Member" button.

## Error Handling & Security Guidelines

The agent must always:
* Handle expired management tokens
* Return safe, user-friendly errors
* Log errors without leaking secrets
* Retry only idempotent operations

## Output Expectations

The agent should:
* Explain **why each step exists**
* Clearly separate frontend vs backend responsibilities
* Use pseudocode instead of framework-specific code
* Work identically for Next.js, Golang, .NET, etc.
* Highlight common mistakes (wrong token, missing tenant context)

## What This Skill Must Avoid

❌ Calling management APIs from frontend
❌ Assuming a single tenant per user
❌ Trusting JWT tenant data blindly
❌ Hardcoding roles or tenant IDs

## TL;DR Flow

1. User logs in (OIDC)
2. Backend fetches user tenants → `/users/{userId}/tenants`
3. User selects or creates tenant
4. Backend lists tenant users → `/tenants/{tenantId}/users`
5. Admin manages team (invite / remove / role update)
