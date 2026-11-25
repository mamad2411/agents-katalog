---
name: tigris-iam
description: Use when managing IAM policies, users, and permissions in a Tigris organization
---

# Tigris IAM (Identity and Access Management)

## Policies

Policies define permissions for access keys using AWS IAM-compatible JSON documents.

### `tigris iam policies list` (alias: `l`)

List all policies in the current organization.

```bash
tigris iam policies list
tigris iam policies list --json
```

| Flag       | Alias | Description                            | Default |
| ---------- | ----- | -------------------------------------- | ------- |
| `--format` | `-f`  | Output format (`json`, `table`, `xml`) | `table` |
| `--json`   |       | Output as JSON                         |         |

### `tigris iam policies get [arn]` (alias: `g`)

Show details for a policy including its document and attached users. If no ARN is provided, shows interactive selection.

```bash
tigris iam policies get
tigris iam policies get arn:aws:iam::org_id:policy/my-policy
tigris iam policies get --json
```

| Flag       | Alias | Description                            | Default |
| ---------- | ----- | -------------------------------------- | ------- |
| `--format` | `-f`  | Output format (`json`, `table`, `xml`) | `table` |
| `--json`   |       | Output as JSON                         |         |

### `tigris iam policies create <name>` (alias: `c`)

Create a new policy with a name and policy document. The document can be provided via file path, inline JSON, or stdin.

```bash
tigris iam policies create my-policy --document policy.json
tigris iam policies create my-policy --document '{"Version":"2012-10-17","Statement":[...]}'
cat policy.json | tigris iam policies create my-policy
```

| Flag            | Alias | Description                                                                  |
| --------------- | ----- | ---------------------------------------------------------------------------- |
| `--document`    | `-d`  | Policy document (JSON file path or inline JSON). Reads from stdin if omitted |
| `--description` |       | Policy description                                                           |

### `tigris iam policies edit [arn]` (alias: `e`)

Update an existing policy's document. If no ARN is provided, shows interactive selection.

```bash
tigris iam policies edit --document policy.json
tigris iam policies edit arn:aws:iam::org_id:policy/my-policy --document policy.json
cat policy.json | tigris iam policies edit arn:aws:iam::org_id:policy/my-policy
```

| Flag            | Alias | Description                                                                      |
| --------------- | ----- | -------------------------------------------------------------------------------- |
| `--document`    | `-d`  | New policy document (JSON file path or inline JSON). Reads from stdin if omitted |
| `--description` |       | Update policy description                                                        |

### `tigris iam policies delete [arn]` (alias: `d`)

Delete a policy. If no ARN is provided, shows interactive selection.

```bash
tigris iam policies delete
tigris iam policies delete arn:aws:iam::org_id:policy/my-policy --force
```

| Flag      | Description              |
| --------- | ------------------------ |
| `--force` | Skip confirmation prompt |

### Policy Document Format

Policies use AWS IAM JSON format:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject"],
      "Resource": ["arn:aws:s3:::my-bucket/*"]
    }
  ]
}
```

### Example Policies

**Read-only access to a bucket:**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:ListBucket"],
      "Resource": ["arn:aws:s3:::my-bucket", "arn:aws:s3:::my-bucket/*"]
    }
  ]
}
```

**Write to a specific prefix:**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:PutObject"],
      "Resource": ["arn:aws:s3:::my-bucket/uploads/*"]
    }
  ]
}
```

**Full bucket admin:**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:*"],
      "Resource": ["arn:aws:s3:::my-bucket", "arn:aws:s3:::my-bucket/*"]
    }
  ]
}
```

## Users

Manage organization members and invitations.

### `tigris iam users list` (alias: `l`)

List all users and pending invitations in the organization.

```bash
tigris iam users list
tigris iam users list --json
```

| Flag       | Alias | Description                            | Default |
| ---------- | ----- | -------------------------------------- | ------- |
| `--format` | `-f`  | Output format (`json`, `table`, `xml`) | `table` |
| `--json`   |       | Output as JSON                         |         |

### `tigris iam users invite <email>` (alias: `i`)

Invite users to the organization by email. Comma-separate for bulk invitations.

```bash
tigris iam users invite user@example.com
tigris iam users invite user@example.com --role admin
tigris iam users invite user1@example.com,user2@example.com
```

| Flag     | Alias | Description                        | Default  |
| -------- | ----- | ---------------------------------- | -------- |
| `--role` | `-r`  | Role to assign (`admin`, `member`) | `member` |

### `tigris iam users revoke-invitation [id]` (alias: `ri`)

Revoke pending invitations. If no invitation ID is provided, shows interactive selection. Comma-separate for multiple.

```bash
tigris iam users revoke-invitation
tigris iam users revoke-invitation invitation_id --force
tigris iam users revoke-invitation id1,id2,id3 --force
```

| Flag      | Description              |
| --------- | ------------------------ |
| `--force` | Skip confirmation prompt |

### `tigris iam users update-role [id]` (alias: `ur`)

Update user roles in the organization. If no user ID is provided, shows interactive selection. Comma-separate for multiple users.

```bash
tigris iam users update-role --role admin
tigris iam users update-role user_id --role member
tigris iam users update-role id1,id2 --role admin
tigris iam users update-role id1,id2 --role admin,member
```

| Flag     | Alias | Description                                                                                                                                           |
| -------- | ----- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--role` | `-r`  | Role(s) to assign (`admin`, `member`), comma-separated. Each role pairs with the corresponding user ID. If one role is given, it applies to all users |

### `tigris iam users remove [id]` (alias: `rm`)

Remove users from the organization. If no user ID is provided, shows interactive selection. Comma-separate for multiple.

```bash
tigris iam users remove
tigris iam users remove user@example.com --force
tigris iam users remove user@example.com,user@example.net --force
```

| Flag      | Description              |
| --------- | ------------------------ |
| `--force` | Skip confirmation prompt |

## Roles

| Role     | Description                                                                          |
| -------- | ------------------------------------------------------------------------------------ |
| `admin`  | Full access to all organization resources and settings                               |
| `member` | Limited access — can use buckets and objects but cannot manage organization settings |
