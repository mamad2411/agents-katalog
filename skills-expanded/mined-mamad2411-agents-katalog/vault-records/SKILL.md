---
name: vault-records
description: Search, identify, and reason about Keeper vault records via Commander - record types and their fields, search by title/type/URL, folders and sharing relationships, and addressing a record safely by title or UID. Use when asked to find a record in the vault, identify the right record before acting, understand a record type's fields, or reason about how a record is shared.
---

# Keeper Vault Records

The Keeper vault is the full record store behind Commander. This skill is how
you find the right record and understand how it is structured and shared -
without ever displaying its secret contents. Drive Commander through the tmux
shell pattern in the **keeper-admin** skill.

## Record model

Modern records are **typed**: each type has a defined field set. Common types:

- `login` - login + password + URL + TOTP; the everyday credential.
- `serverCredentials`, `databaseCredentials` - host/port plus credentials.
- `pamUser` - the credential KeeperPAM rotates and injects; references a target resource.
- `pamMachine`, `pamDatabase`, `pamRemoteBrowser` - PAM targets (see the keeper-pam skill).
- `sshKeys`, `bankCard`, `bankAccount`, plus custom types.

Records carry standard fields and **custom fields** (free-label key/values).
Address either with Keeper notation; custom fields use `custom_field`
(see the keeper-secrets plugin's keeper-notation skill).

## Searching

```bash
My Vault> search "<term>"        # titles, logins, URLs, notes - regex supported
My Vault> ls -l                  # current folder with UIDs
My Vault> tree                   # folder structure
My Vault> get <RECORD_UID>       # record structure; secret fields stay masked
My Vault> record-history <UID>   # change history
```

Read field *labels* and metadata from `get`; never unmask secret-typed field
*values* (`--unmask` is off-limits in this skill).

Rank matches by exactness of title, then folder relevance, and review the full
result set before concluding. Disambiguate when several records match - never
guess which one the user meant, especially before a mutating action.

## Folders and sharing

Records live in folders. **Shared folders** can be shared to individual users
or to **teams**, each with a permission level (Read-Only, Can Edit, Can Share).
A record inside a shared folder is considered shared even if the folder itself
is shared to no one yet. This is the access surface the compliance reports
decrypt - see the enterprise-admin skill.

```bash
My Vault> share-report -v                 # who can reach what
My Vault> share-record -e user@co.com -a grant -u <RECORD_UID>
My Vault> share-folder -e user@co.com -a grant -u <FOLDER_UID>
```

`find-password` is the Commander primitive that reveals a value; in this
plugin you do not surface that value - reference the record instead and, if a
value is genuinely needed, route through `/keeper-secrets:get-secret`, which
retrieves only the one field and never prints it.

## Safe handling

Identify records by title and UID, return only the field that is needed, never
display secret values, and confirm before any update or share change. Treat
every record read as an audited event.
