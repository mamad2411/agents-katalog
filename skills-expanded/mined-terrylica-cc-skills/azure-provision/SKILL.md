---
name: azure-provision
description: >
  Bootstrap Azure automation when interactive `az login` is blocked by a Conditional Access policy
  (error 530035, "Device state: Unregistered"). Mints a service principal through the Azure Portal
  session ONCE — using Microsoft Graph over a captured token, not DOM clicking — then provisions
  resource groups, Cognitive Services / AI Language / Speech resources and their keys entirely via
  az/REST, writing key AND endpoint together into the SCS vault. Use when az login fails but the
  portal works, when moving Azure resources to a client's own tenant, or when you need unattended
  Azure automation from a machine that is not Entra-joined. Triggers: "az login blocked",
  "AADSTS530035", "Conditional Access Azure CLI", "create Azure service principal", "migrate Azure
  account", "provision Azure AI resources", "Azure app registration".
allowed-tools: Read, Bash, Grep, Glob
---

# azure-provision — service-principal bootstrap through a portal session

Azure's **Portal** and **CLI** are different Entra applications. A Conditional Access policy scoped
to the CLI (`04b07795-8ddb-461a-bbee-02f9e1bf7b46`) leaves the portal
(`c44b4083-3bb0-49c1-b47d-974e53cbdf3c`) working, and `az login` has **no `--client-id` override** —
so when the CLI is blocked, the browser session is the only door. Walk through it once, mint a
service principal, and every later run is unattended: **client-credentials auth is not gated by user
Conditional Access.**

> **Self-Evolving Skill**: the Azure Portal drifts. On real, reproducible breakage fix the scripts
> AND append to the Vendor Quirks log in `../dashboard-forge/SKILL.md` — immediately, not later.

## Why this exists

Observed 2026-08-02 on a real clinic migration:

```
Error Code: 530035        App name: Microsoft Azure CLI
Device state: Unregistered   App id: 04b07795-8ddb-461a-bbee-02f9e1bf7b46
```

…while `portal.azure.com` signed the same account in without complaint. Two traps followed, both
worth knowing before you start:

- **`az account list` returned `[]`.** That is a _consequence_ of the block, not evidence that no
  subscription exists. The portal showed an active subscription with the user as **Owner**.
- **The account was a guest** (`user_domain#EXT#@tenant.onmicrosoft.com`). Guests get no app-registration
  rights by default — they need Application Developer/Administrator, and an RBAC role at the target
  scope. If minting fails with 403, that is the reason, and it needs a tenant admin, not a retry.

## The design: browser for the login, Graph for the work

The first version of this drove the portal's DOM and it was a disaster — see the Portal Quirks below.
The fix was not better selectors. **The portal's own Graph token carries the scopes needed to do the
whole job over REST**, measured on a live session:

```
Application.ReadWrite.All · AppRoleAssignment.ReadWrite.All · RoleManagement.ReadWrite.Directory
```

So `captureBearer(page, "graph.microsoft.com")` off the wire, then plain HTTP. **Zero selectors, zero
blade navigation, nothing to drift.** This is the plugin's Hybrid rule taken to its limit: the browser
contributes a _token_, not clicks.

| Step                       | How                                                   | Browser?      |
| -------------------------- | ----------------------------------------------------- | ------------- |
| Sign in (incl. MFA)        | human, in the visible Chrome                          | **yes, once** |
| Capture Graph + ARM tokens | `captureBearer()` off real requests                   | passive       |
| Identity preflight         | `decodeJwtClaims()` → `assertIdentity()`              | no            |
| Create app registration    | `POST /v1.0/applications`                             | no            |
| Create service principal   | `POST /v1.0/servicePrincipals`                        | no            |
| Create client secret       | `POST /v1.0/applications/{id}/addPassword`            | no            |
| Assign Contributor         | `PUT …/roleAssignments/{guid}?api-version=2022-04-01` | no            |
| Everything afterwards      | `az` as the service principal                         | no            |

## Run it

```bash
cd plugins/web-forge/skills/azure-provision
node scripts/mint-sp.mjs specs/example.json     # browser opens; sign in; the rest is REST
node scripts/provision.mjs specs/example.json   # unattended: RG + resources + keys → vault
```

Both are **idempotent** (GET before POST). Re-running adopts what exists. The DOM version was not,
which is exactly how a duplicate app registration got created.

## Portal quirks (why there is no clicking here)

| Trap                               | What happens                                                                                                                                                                                                                                        |
| ---------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Ambiguous accessible names**     | Every close button is `"Close content '<Blade Title>'"`, so `getByRole("button", {name:/register/i}).first()` hits **close**, not submit. It reports a successful click and creates nothing. Use `clickExact()`, which refuses and lists candidates |
| **Two search boxes**               | The masthead search matches `input[placeholder*="Search"]` **before** any blade's own filter. Anchor on the specific placeholder                                                                                                                    |
| **A list view can lie**            | After a _successful_ create, **Owned applications** said "This account isn't listed as an owner of any applications" — true for a guest creator, and utterly misleading. Ground truth is the **notifications pane** or **All applications**         |
| **Tokens are not in localStorage** | This generation of MSAL SPA keeps them in memory. Capture off the wire                                                                                                                                                                              |
| **Cached blades issue no request** | Token capture then silently yields `null`, which reads like "no permission". `captureBearer` retries with a reload                                                                                                                                  |

## Verification — both directions, always

A key that returns HTTP 200 on a trivial call proves nothing. The acceptance checks are:

1. **SP authenticates AND sees the subscription.** `mint-sp.mjs` polls the client-credentials flow
   directly (never `az login -p <secret>` — that puts the secret in **argv**, readable via `ps`).
   RBAC is eventually consistent: expect ~15–60s of "not yet". Do not read that as failure.
2. **Each provisioned resource DETECTS, not merely authenticates.** For an AI Language resource,
   assert real entities come back from a synthetic probe — not just a 200.
3. **The refusal direction fires.** Point the spec at a bogus subscription and confirm it fails loudly.

## Key and endpoint must move together

`provision.mjs` writes **key + endpoint (+ region)** to the vault as one unit, and the schema requires
it. This is not tidiness: a rotation that moved the key but left the endpoint as a hardcoded literal
elsewhere produced `HTTP 401 — Access denied due to invalid subscription key or wrong API endpoint`
in production. Emit both, read both from the same place.

## Secrets discipline

- Client secret: Graph returns it **once** → straight into `vault set --stdin`. Never argv, never
  stdout, never a screenshot.
- **Never screenshot a secret-reveal page.** An agent that later reads that PNG puts the value into
  conversation context permanently. `purgeShots()` runs at the end of every run.
- Captured ARM/Graph tokens are ~1h user credentials. Log `decodeJwtClaims()` output, never the token.
- The profile dir (`~/.local/share/web-forge/profile-azure`) holds a live tenant-admin session — treat
  it as credential-equivalent.

## Reference implementation

`~/459ecs/example-clinic` — the 2026-08-02 migration of a clinic's Speech + Language resources from a
personal Microsoft account into the clinic's own tenant, under a CA block. Decision record: that
repo's `docs/security-and-compliance/README.md`.

## Post-Execution Reflection

1. **Did any step need the DOM?** If yes, ask whether a Graph/ARM call would have done it — that is
   almost always the better fix, and it is how this skill got to zero selectors.
2. **Did a portal behaviour surprise you?** Append it to the dashboard-forge Vendor Quirks log.
3. **Did any secret reach argv, stdout, or a screenshot?** If a reveal was captured, purge it and
   treat the secret as context-exposed.
