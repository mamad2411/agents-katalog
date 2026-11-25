---
name: kei-directory-sync
description: Set up, run and troubleshoot Kei's per-org Entra (Azure AD) directory sync, which turns a customer's Entra app roles into Kei groups and creates their users as org members. Use when a customer admin or an agent helping one wants to sync Entra or Azure AD groups or users into Kei; configure app roles, the sync app registration, Graph permissions or the federated credential (system:serviceaccount:kei:oidc-bridge, api://AzureADTokenExchange); run `kei directory-sync get|set|enable|disable|report`; read a dry-run report; go live; or debug no groups synced, users skipped, a token or AADSTS error, 403 from Graph, 409 ALREADY_EXISTS, a run stuck in dry run, a cap exceeded, or `kei directory-sync` returning 404. Writing policies against the synced groups is kei-harness-policy; other kei commands are kei-cli.
---

# Kei directory sync (Entra)

Kei can mirror one Entra application's **app-role assignments** into one Kei
organization. Kei's identity service (kei-oidc-bridge) runs the sync every
interval (5 minutes by default):

- **One Kei group per app role.** The group name is exactly the role's
  **value** (case-sensitive), not its display name. Role value `pilot` → Kei
  group `pilot`. An existing Kei group with that name is reused.
- **Members.** Users assigned to the role directly, or **direct** members of an
  Entra group assigned to it, are added to the Kei group. Nested groups are not
  expanded.
- **Users (optional, `--create-users=true`).** Assigned people who have never
  signed in to Kei get a Kei user (`ms:<Entra object id>`) and join the org as
  **`member`**. When they later sign in with Microsoft, the sign-in lands on the
  same user; no duplicate is created. (A Google or email-code sign-in is a
  different login and a different Kei user.)
- **Report.** Every run writes a report: `kei directory-sync report`.

It starts in **dry run**: it reads Entra and records what it *would* do, and
writes nothing else.

Setup happens in two places: the **Azure portal** (Entra admin) and the **`kei`
CLI** (Kei org owner or admin). There is no console UI for it yet.

## Retrieval sources

| Source | How to retrieve | Use for |
| --- | --- | --- |
| Installed CLI | `kei help` (look for the `kei directory-sync` line); `kei directory-sync set --help`, `report --help` | Whether this release has the commands, exact flags |
| Entra sync runbook | the `kei-oidc-bridge` repository, `docs/entra-sync.md` | Full customer runbook, stat meanings, Haikei-ops appendix |
| CLI source | the `kei-cli` repository, `internal/app/directory_sync.go` | Output format, exit codes |
| Azure detail | [references/azure-setup.md](references/azure-setup.md) | Portal clicks, the three ids |
| Report and errors | [references/report-and-errors.md](references/report-and-errors.md) | Every stat, change actions, exact error strings |

The code wins over this file. Never invent a flag: `set` takes only
`--tenant-id`, `--client-id`, `--app-id`, `--dry-run`, `--create-users`,
`--revoke` and `--yes`.

## Before you start

- **CLI version.** `kei directory-sync` is on kei-cli `main` and first ships in
  the release after v0.1.29. If `kei help` has no `kei directory-sync` line, run
  `kei upgrade` once that release is out. `kei directory-sync --help` itself is
  not a help command (it prints `unknown directory-sync command "--help"`); use
  `kei help` or `--help` on a subcommand.
- **Who.** `kei login` as an **owner or admin** of the Kei org that receives
  the users and groups. Members get permission denied. The org comes from the
  login token; there is no `--org` flag.
- **One Kei org per Entra tenant.** A tenant can be connected to only one Kei
  org. A second org gets `409 ALREADY_EXISTS`.

## Part 1: Azure portal (Entra admin)

Details and click paths: [references/azure-setup.md](references/azure-setup.md).

1. **App roles on the customer's app** (the app users sign in to, e.g. the
   `contoso-chat` app registration): create one app role per Kei group, allowed
   member types **Users/Groups**, with value `pilot`, `dev`, and so on. In
   **Enterprise applications → the app → Users and groups**, assign each Entra
   group to its role. **Default Access assignments are ignored**: the sync
   skips them (`default_access_skipped`), so a group assigned to Default Access
   never reaches Kei.
2. **A sync app registration** (e.g. `Kei Entra sync`, single tenant) with
   Microsoft Graph application permissions — of type application, not
   delegated — `Application.Read.All`, `GroupMember.Read.All`,
   `User.Read.All`. Then grant admin consent for the tenant. All three are
   read-only; the sync never writes to Entra.
3. **A federated credential on the sync app, and no client secret.**
   **Certificates & secrets → Federated credentials → Add credential**,
   scenario *Kubernetes accessing Azure resources* (or *Other issuer*):

   | Field | Value |
   | --- | --- |
   | Issuer | Haikei's cluster issuer, as published in the runbook: `https://oidc.eks.us-east-1.amazonaws.com/id/7AD200EBD688652018CBF106B042AD88` |
   | Namespace / service account | `kei` / `oidc-bridge` |
   | Subject | `system:serviceaccount:kei:oidc-bridge` |
   | Audience | `api://AzureADTokenExchange` (the default) |

   **Do not create a client secret** and never send one to Haikei. Kei has no
   client-secret option: the sync authenticates only with this federated
   credential (a short-lived token Haikei's cluster rotates).
4. **Copy three ids** (GUIDs, none secret): the **Directory (tenant) id** →
   `--tenant-id`; the **sync app's** Application (client) id → `--client-id`;
   the **app with the app roles** → `--app-id`. Don't swap the two client ids:
   `--client-id` has the federated credential, `--app-id` has the roles.

## Part 2: Kei (org owner or admin)

```sh
kei login

# 1. Configure. The first set creates the config; later sets change only the flags you pass.
kei directory-sync set \
  --tenant-id <tenant GUID> --client-id <sync app GUID> --app-id <app-with-roles GUID>
kei directory-sync set --create-users=true      # optional: create users who never signed in

# 2. Enable. Dry run is on by default, so nothing is written yet.
kei directory-sync enable

# 3. After the next interval (about 5 minutes), read the dry-run report.
kei directory-sync report                       # newest run in full: result, stats, changes
kei directory-sync report --limit 10            # last 10 runs as a table
kei directory-sync get                          # settings + last-run summary

# 4. Go live only when the report is right.
kei directory-sync set --dry-run=false

# Stop at any time. Nothing is removed.
kei directory-sync disable
```

- Booleans take `=true` / `=false` (`--dry-run=false`, not `--dry-run false`).
- `set`, `enable` and `disable` ask for confirmation; `--yes` skips it in
  scripts. `get --json` and `report --json` print the raw API response.
- `enable` needs all three ids. Ids must be GUIDs.
- Defaults: `enabled=false`, `dry_run=true`, `create_users=false`,
  `revoke=false`.
- `get` on an org with no config prints `No directory sync configured.` and
  exits 1.

### Read the dry-run report before going live

Check, in `kei directory-sync report`:

- `result: succeeded` and `dry_run: true`.
- `assignments` matches the role assignments you made; `default_access_skipped`
  is 0.
- `would_create` equals the assigned people who never signed in to Kei, with a
  `create_user` change per person.
- `users_skipped_disabled` / `users_skipped_guest` are the people you expect to
  skip.
- `groups_created` and the `add_member` changes are what you expect.

After `--dry-run=false`, the next report shows `dry_run: false`, and
`users_created`, `org_members_added` and `members_added` match the dry run, with
`member_errors` 0. Field glossary:
[references/report-and-errors.md](references/report-and-errors.md).

## Safety

- **Dry run first, always**, and read the report before `--dry-run=false`.
- **Users are never deleted.** Unassigning someone removes only memberships the
  sync added, and only with revocation on. Manual memberships are never
  removed. Nobody is made an org admin or demoted. No workspace memberships.
- **Revocation is off by default** (`--revoke=true` turns it on for the org).
- **Haikei's ceilings.** Haikei's platform settings for dry run and revoke are
  global ceilings; an org can only be stricter. If Haikei forces dry run, runs
  stay `dry_run: true` even after `--dry-run=false`. If Haikei forbids revoke,
  `--revoke=true` has no effect.
- **Caps per org, per run.** A run fails before writing anything if it would
  create more users than the platform cap (200 by default), or remove more than
  the allowed share (20% by default) of tracked assignments or synced
  memberships (`... cap exceeded`). Haikei sets the caps; ask Haikei to raise
  one, or roll out in batches of groups.
- **One Kei org per tenant** (409 otherwise).
- **Don't rename role values.** Existing assignments keep feeding the old group;
  add a new role instead.

| To | Do |
| --- | --- |
| Back to dry run | `kei directory-sync set --dry-run=true` |
| Stop creating users | `kei directory-sync set --create-users=false` (existing users stay) |
| Stop the sync | `kei directory-sync disable` (users, groups and memberships stay) |
| Undo memberships | Unassign in Entra with revocation on, or remove them in the console |
| Undo users | Remove them from the org in the console; the sync never deletes users |

## Troubleshooting

Start with the newest run's `error` in `kei directory-sync report` (short, never
contains tokens or Graph bodies). Exact strings:
[references/report-and-errors.md](references/report-and-errors.md).

| Symptom | Cause | Fix |
| --- | --- | --- |
| No groups synced / a group is missing; `assignments` is 0 or `default_access_skipped` > 0 | Groups assigned to **Default Access** instead of a role; wrong `--app-id` (e.g. the sync app's id instead of the app with the roles); role value not what you expected (the group name is the case-sensitive **value**), or the role is disabled | Assign each group to a defined app role and remove Default Access; check `--app-id` is the client id of the app with the roles; check the role value |
| `service principal for app … not found in tenant …` | `--app-id` is not an app in this tenant (a typo, or another tenant's app) | Set `--app-id` to the app with the roles |
| Users not created; `unknown_users` > 0 | `create_users` is off | `kei directory-sync set --create-users=true` |
| Users skipped; `users_skipped_disabled` or `users_skipped_guest` > 0 | The Entra account is **disabled** (or Graph didn't return `accountEnabled`), or the user is a **guest** (`userType=Guest`) | Expected. Enable the account in Entra; guests are not created by default, ask Haikei |
| A person missing from a group; `member_errors` > 0 | Member of a nested group only, or signed in at the same moment as the sync and isn't in the org | Add them to the assigned group directly; an org admin adds them to the org |
| `token: entra returned 400 …` / `401 invalid_client`; an `AADSTS…` federated-credential error in Entra's sign-in logs | Entra rejected the federated sign-in: issuer, subject or audience doesn't match exactly, or `--client-id` / `--tenant-id` is wrong | On the sync app's federated credential, check the issuer, subject `system:serviceaccount:kei:oidc-bridge` and audience `api://AzureADTokenExchange` exactly (no trailing slash or space). Check `--client-id` is the **sync** app and `--tenant-id` your tenant. Don't add a secret |
| 403 from Graph (`graph: … status 403`) | A Graph permission is missing, delegated instead of application, or not admin-consented | Add `Application.Read.All`, `GroupMember.Read.All`, `User.Read.All` as application permissions (not delegated) and grant admin consent |
| `set` fails with `ALREADY_EXISTS` (HTTP 409), or a run fails with `tenant already synced by org …` | Another Kei org already syncs this tenant | Use the org that already has it, or disable it there and ask Haikei to release the tenant |
| Report shows `dry_run: true` after `--dry-run=false` | Haikei's platform dry-run ceiling forces every org into dry run | Ask Haikei to lift it; nothing to change on your side |
| `--revoke=true` removes nothing | Haikei's revoke ceiling is off | Ask Haikei |
| `creation cap exceeded` / `removal cap exceeded` / `revocation cap exceeded` | The run hit a per-run cap; nothing was written | Check the Entra assignments are intended; ask Haikei to raise the cap, or roll out in batches |
| `kei directory-sync` gets 404 (HTTP 404 on `set`/`report`, or `get` says `No directory sync configured.` even after a `set`) | Kei's console proxy doesn't allow the directory-sync routes yet (the allowlist isn't deployed) | A first `set` creates the config, so a 404 on `set` is never "not configured"; nothing to fix locally, ask Haikei |
| `unknown command` / no `directory-sync` in `kei help` | The installed kei predates the commands | `kei upgrade` to a release after v0.1.29 |
| No new runs in the report | The sync is disabled, or Haikei hasn't enabled it for the platform | `kei directory-sync get` to check `enabled`, then ask Haikei |

## Then: policies on the synced groups

Synced groups are ordinary Kei groups, referenced as **`group:<role value>`**,
e.g. `group:pilot`. Write policies only after the first live run:

```sh
kei policy create --workspace WS --group group:pilot --allow shell:git
```

Load **`kei-harness-policy`** for policy patterns and **`kei-cli`** for the rest
of the CLI (`kei groups members list GROUP_ID` to see who the sync added).

## Validation commands

```sh
kei help | grep directory-sync      # the commands exist in this release
kei directory-sync set --help       # exact flags
kei directory-sync get              # config + last-run summary (exit 1 if none)
kei directory-sync report --json    # newest run, raw
```

## Realistic usage boundaries

- Entra only (`provider: entra`). One app's roles into one org; one org per
  tenant.
- No client-secret auth, no console UI, no `delete` (disable instead; the
  config goes with the org), no nested-group expansion, no workspace
  memberships, never writes to Entra, never deletes users.
- Ceilings, caps, the interval, guests and disabled-user creation are Haikei's
  platform settings; customers can't change them with `kei`.
- Run reports are written only by Kei's service; users can't post them. Kei
  keeps the newest 100.
- Agents: never run `set`, `enable` or `--dry-run=false` without the admin's
  go-ahead, and never ask for or handle an Entra client secret.
