---
name: talkvalue-company
description: "View and manage companies and their associated contacts."
metadata:
  version: 1.0.0
  openclaw:
    category: "productivity"
    requires:
      bins:
        - talkvalue
    cliHelp: "talkvalue path company --help"
---

# TalkValue CLI — Companies

> **PREREQUISITE:** Read ../talkvalue-shared/SKILL.md for auth, global flags, and output formatting.

Companies represent organizations derived from contact email domains. Use company commands to browse company records, update display names, and explore or export the contacts associated with each company.

## company list

List companies in the active organization, with optional search and pagination.

```bash
talkvalue path company list [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--keyword <keyword>` | No | - | Filter by domain or display name |
| `--page <n>` | No | `1` | Page number (1-indexed) |
| `--page-size <n>` | No | - | Results per page |

Output columns: ID, Domain, Display Name, People (count)

### Example

```bash
talkvalue path company list
talkvalue path company list --keyword "acme"
talkvalue path company list --page 2 --page-size 50
talkvalue path company list --format json | jq '.data[].domain'
```

---

## company get

Get details for a single company.

```bash
talkvalue path company get <id>
```

No flags.

### Example

```bash
talkvalue path company get co_01xyz789
talkvalue path company get co_01xyz789 --format json
```

---

## company update

Update a company's display name.

> [!CAUTION]
> Changing the display name affects how the company appears across all views and exports. Confirm the correct company ID before running this command.

```bash
talkvalue path company update <id> --display-name <name>
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--display-name <name>` | Yes | - | New display name for the company |

Output: Updated company object.

### Example

```bash
talkvalue path company update co_01xyz789 --display-name "Acme Corporation"
talkvalue path company update co_01xyz789 --display-name "Acme Corp (Acquired)"
```

---

## company person list

List contacts associated with a company, with optional filtering and pagination.

```bash
talkvalue path company person list <companyId> [flags]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--keyword <term>` | No | - | Filter by name, email, or other searchable fields |
| `--channel-id <id>` | No | - | Filter to people in this channel; repeatable |
| `--event-id <id>` | No | - | Filter to people from this event; repeatable |
| `--company-name <name>` | No | - | Filter by company name |
| `--job-title <title>` | No | - | Filter by job title |
| `--page <n>` | No | `1` | Page number (1-indexed) |
| `--page-size <n>` | No | - | Results per page |
| `--sort <value>` | No | - | Sort expression, e.g. `joinedAt:desc`; repeatable |

Output columns: ID, Name, Primary Email, Company, Job Title, Joined At, Created At

### Example

```bash
# All contacts for a company
talkvalue path company person list co_01xyz789

# Filter by keyword and job title
talkvalue path company person list co_01xyz789 \
  --keyword "acme" \
  --job-title "Engineer"

# Filter to people in two specific channels
talkvalue path company person list co_01xyz789 \
  --channel-id ch_01abc123 \
  --channel-id ch_01def456

# Filter by event and sort by join date descending
talkvalue path company person list co_01xyz789 \
  --event-id ev_01ghi789 \
  --sort "joinedAt:desc" \
  --page 1 \
  --page-size 25

# Export to JSON and extract emails
talkvalue path company person list co_01xyz789 \
  --format json | jq '.data[].primaryEmail'
```

---

## company person export

Export all contacts for a company as CSV.

```bash
talkvalue path company person export <companyId>
```

No flags. Output is always CSV regardless of `--format`.

### Example

```bash
# Save to file
talkvalue path company person export co_01xyz789 > acme-contacts.csv

# Pipe to another tool
talkvalue path company person export co_01xyz789 | cut -d',' -f1,2,3
```

---

## Tips

- Company records are auto-derived from contact email domains. You can't create companies directly — they appear once a contact with a matching domain is added.
- `--channel-id` and `--event-id` on `person list` are both repeatable. Combine them to narrow results across multiple channels or events at once.
- `--sort` accepts `field:asc` or `field:desc` and is repeatable for multi-key sorting, e.g. `--sort "joinedAt:desc" --sort "name:asc"`.
- `company person export` always produces CSV. The `--format` flag has no effect on export commands.
- Use `company list --format json` to get company IDs for scripting or bulk operations.

## See Also

- `../talkvalue-shared/SKILL.md` — Auth, global flags, output formatting, and pagination
- `../talkvalue-person/SKILL.md` — Manage individual contacts directly
- `../talkvalue-channel/SKILL.md` — Channel membership and channel-based segmentation
- `../talkvalue-event/SKILL.md` — Event registration and attendance data
