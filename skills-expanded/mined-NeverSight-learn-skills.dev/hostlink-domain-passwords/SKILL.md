---
name: hostlink-domain-passwords
version: 1.0.0
description: "HostLink Domain Passwords: Manage passwords associated with a domain."
metadata:
  openclaw:
    category: "hostlink"
    requires:
      bins: ["hostlink"]
    cliHelp: "hostlink domain-passwords --help"
---

# domain-passwords

> **PREREQUISITE:** Run `hostlink set-token <token>` to authenticate before using any command.

Manage passwords (credentials) associated with a domain. One domain can have multiple password entries.

> **API Note:** Uses GraphQL resource `DomainPassword`.  
> Queries/mutations: `listDomainPassword`, `addDomainPassword`, `updateDomainPassword`, `deleteDomainPassword`.

```bash
hostlink domain-passwords <command> [flags]
```

## Commands

| Command | Description |
|---------|-------------|
| `hostlink domain-passwords list <domain_id>` | List all passwords for a domain |
| `hostlink domain-passwords get <id>` | Get a password entry by ID |
| `hostlink domain-passwords add` | Add a password to a domain |
| `hostlink domain-passwords update <id>` | Update a password entry by ID |
| `hostlink domain-passwords delete <id>` | Delete a password entry by ID |

---

## list

```bash
hostlink domain-passwords list <domain_id> [--json]
```

```bash
hostlink domain-passwords list 42
hostlink domain-passwords list 42 --json
```

### Sample output

```
[10] cPanel | admin | cpanel.example.com:2083 | main hosting panel
[11] FTP | ftpuser | ftp.example.com:21
```

---

## get

```bash
hostlink domain-passwords get <id> [--json]
```

```bash
hostlink domain-passwords get 10
hostlink domain-passwords get 10 --json
```

---

## add

```bash
hostlink domain-passwords add --domain-id <id> --name <label> [flags]
```

| Flag | Description |
|------|-------------|
| `-d, --domain-id <id>` | Domain ID *(required)* |
| `--name <value>` | Name / label *(required)* |
| `--username <value>` | Username |
| `--password <value>` | Password |
| `--host <value>` | Host |
| `--port <n>` | Port |
| `--remark <value>` | Remark |

```bash
hostlink domain-passwords add --domain-id 42 --name "cPanel" --username admin --password secret --host cpanel.example.com --port 2083
```

---

## update

```bash
hostlink domain-passwords update <id> [flags]
```

Supports all the same flags as `add` (except `--domain-id`). At least one flag must be provided.

```bash
hostlink domain-passwords update 10 --password newpassword
hostlink domain-passwords update 10 --host newhost.example.com --port 2096
```

---

## delete

```bash
hostlink domain-passwords delete <id>
```

```bash
hostlink domain-passwords delete 10
```

---

## Output Fields

| Field | Description |
|-------|-------------|
| `domainpassword_id` | Password entry ID |
| `domain_id` | Parent domain ID |
| `name` | Name / label |
| `username` | Username |
| `password` | Password |
| `host` | Host |
| `port` | Port |
| `remark` | Remark |
