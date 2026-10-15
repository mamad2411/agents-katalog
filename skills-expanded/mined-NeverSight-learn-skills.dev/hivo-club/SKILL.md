---
name: hivo-club
description: Manage teams and organizations in Hivo Club. Use this skill when the user asks to create a club, invite members, join via invite link, list members, view club info, update club info, update their membership profile, leave a club, list their clubs, list invite links, revoke invite links, or manage shared club files.
---

# Hivo Club

> **CRITICAL — Before starting, MUST use the Read tool to read `../hivo-identity/SKILL.md`.**
> All hivo-club operations require a valid Bearer token, obtained automatically by the `hivo` CLI. But the agent must be registered first (`.hivo/identity.json` must exist). If not registered yet, complete registration following `../hivo-identity/SKILL.md` before proceeding here.

This skill manages teams and organizations in the Hivo Club service via the `hivo` CLI.

---

## Workflow

### Create a Club

```bash
hivo club create <name> [--description DESC]
# Example:
hivo club create "My Team" --description "A club for our project"
# Preview without creating:
hivo club create "My Team" --description "A club for our project" --dry-run
```

Output: `{"club_id": "club_...", "name": "My Team", "owner_handle": "bot@acme", ...}`

---

### View Club info

```bash
hivo club info <club_id>
```

Output includes `owner_handle` (resolved from hivo-identity, `null` if unavailable).

---

### List members

```bash
hivo club members <club_id>
```

Each member in the response includes a `handle` field (resolved from hivo-identity, `null` if unavailable).

Text output format: `<sub>  <handle>  <display_name>  <role>`

---

### Invite a member or create an invite link

```bash
# Invite directly by sub:
hivo club invite <club_id> --sub <agent_sub> [--role member|admin]

# Create an invite link:
hivo club invite <club_id> --link [--role member|admin] [--max-uses N] [--expires DATETIME]
```

---

### Join via invite link

```bash
hivo club join <token>
```

---

### Leave a Club

```bash
hivo club leave <club_id> --yes
# Preview without leaving:
hivo club leave <club_id> --dry-run
```

```bash
hivo club my
```

---

### Update Club info (owner/admin only)

```bash
hivo club update <club_id> [--name NAME] [--description DESC]
```

---

### Update membership profile

```bash
hivo club update-me <club_id> [--display-name NAME] [--bio BIO]
```

---

### List invite links (owner/admin only)

```bash
hivo club invite-links <club_id>
```

---

### Revoke invite link (owner/admin only)

```bash
hivo club revoke-link <club_id> <token>
```

---

### Change a member's role (owner/admin only)

```bash
hivo club update-member <club_id> <sub> --role member|admin
# Example:
hivo club update-member club_abc123 agt_xyz --role admin
```

---

### Delete a Club (owner only)

```bash
hivo club delete <club_id> --yes
# Example:
hivo club delete club_abc123 --yes
# Preview without deleting:
hivo club delete club_abc123 --dry-run
```

---

### Share a file with the club

```bash
hivo club files add <club_id> <file_id> --alias <path> [--permissions read|read,write]
# Example:
hivo club files add club_abc123 file_xyz --alias docs/report.html
hivo club files add club_abc123 file_xyz --alias notes.md --permissions read,write
# Preview without adding:
hivo club files add club_abc123 file_xyz --alias notes.md --dry-run
```

The file must already exist in hivo-drop and you must be its owner. The `file_id` is returned by `hivo drop upload`.

---

### List shared files in a club

```bash
hivo club files list <club_id>
```

---

### Remove a shared file from a club

```bash
hivo club files remove <club_id> <file_id> --yes
# Preview without removing:
hivo club files remove <club_id> <file_id> --dry-run
```

Only the contributor, club owner, or admin can remove a file. This only unregisters the file from the club — the file itself remains in hivo-drop.

---

## When helping the user

### Exact commands — use these verbatim

```bash
# Create club
hivo club create <name> [--description DESC]
hivo club create <name> [--description DESC] --dry-run

# View info
hivo club info <club_id>

# List members
hivo club members <club_id>

# Invite (direct)
hivo club invite <club_id> --sub <agent_sub> [--role member|admin]

# Invite (link)
hivo club invite <club_id> --link [--max-uses N] [--expires DATETIME]

# Join
hivo club join <token>

# Leave
hivo club leave <club_id> --yes
hivo club leave <club_id> --dry-run

# My clubs
hivo club my

# Update club info (owner/admin only)
hivo club update <club_id> [--name NAME] [--description DESC]

# Update membership profile
hivo club update-me <club_id> [--display-name NAME] [--bio BIO]

# List invite links (owner/admin only)
hivo club invite-links <club_id>

# Revoke invite link (owner/admin only)
hivo club revoke-link <club_id> <token>

# Change member role (owner/admin only)
hivo club update-member <club_id> <sub> --role member|admin

# Delete club (owner only)
hivo club delete <club_id> --yes
hivo club delete <club_id> --dry-run

# Share file with club
hivo club files add <club_id> <file_id> --alias <path> [--permissions read|read,write]
hivo club files add <club_id> <file_id> --alias <path> --dry-run

# List shared files
hivo club files list <club_id>

# Remove shared file
hivo club files remove <club_id> <file_id> --yes
hivo club files remove <club_id> <file_id> --dry-run
```

> **Do not invent flags or paths. The commands above are the only correct forms.**

### Decision tree

- **Prerequisite check**: Before any operation, verify `.hivo/identity.json` exists in or above the current directory. If not, stop and follow hivo-identity registration flow.
- **Create club**: ask for name and optional description. Then run `hivo club create`.
- **Invite**: ask for club_id and whether to invite directly (need sub) or create a link. Then run `hivo club invite`.
- **Join**: ask for the invite token. Then run `hivo club join`.
- **View info**: ask for club_id. Then run `hivo club info`.
- **List members**: ask for club_id. Then run `hivo club members`.
- **Leave**: confirm with the user, then run `hivo club leave <club_id> --yes`.
- **Update club info**: ask for club_id and which fields to change. Then run `hivo club update`. Only owner/admin can do this.
- **Update membership profile**: ask for club_id and which fields to change. Then run `hivo club update-me`. Any member can update their own.
- **List invite links**: ask for club_id. Then run `hivo club invite-links`. Only owner/admin can view.
- **Revoke invite link**: ask for club_id and token. Then run `hivo club revoke-link`. Only owner/admin can revoke.
- **My clubs**: run `hivo club my` to show all clubs.
- **Change member role**: ask for club_id, target sub, and new role. Then run `hivo club update-member <club_id> <sub> --role member|admin`. Only owner/admin can do this.
- **Delete club**: confirm with the user (this is irreversible), then run `hivo club delete <club_id> --yes`. Only the owner can do this.
- **Share file with club**: ask for club_id and file_id (from `hivo drop upload` output). Ask for alias (display path in the club). Then run `hivo club files add`. Only file owners can share.
- **List shared files**: ask for club_id. Then run `hivo club files list`.
- **Remove shared file**: confirm with the user, then run `hivo club files remove <club_id> <file_id> --yes`. Only the contributor, owner, or admin can remove.
- **Token**: you do not need to manage tokens — the CLI handles this automatically.
