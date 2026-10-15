---
name: macos-contacts
description: Manage macOS Contacts.app — search, view, create, edit, and delete contacts. Use when the user asks to find a contact, look up a phone number or email, add a new contact, update contact details, or list contact groups.
---

# macOS Contacts

Use this skill when the task is about Apple Contacts.app on macOS.

## Overview

- Public interface: `scripts/commands`
- Internal backend: `scripts/applescripts/contact`
- Output: JSON with a stable `{"success": ...}` envelope
- Installed global skill directory: `~/.agents/skills/macos-contacts`
- `skills check` and `skills update` may refer to the upstream package name `apple-contacts` from `vinitu/apple-contacts-skill`

## Main Rule

Use only `scripts/commands`.
Do not call `scripts/applescripts/contact` directly.
Do not use `scripts/contacts.sh` in skill instructions; it is kept only as a compatibility wrapper.

## Requirements

- macOS with Contacts.app
- `bash`
- `osascript`
- Terminal automation permission for Contacts.app

## Public Interface

- `scripts/commands/contact/search.sh`
- `scripts/commands/contact/get.sh`
- `scripts/commands/contact/list.sh`
- `scripts/commands/contact/add.sh`
- `scripts/commands/contact/edit.sh`
- `scripts/commands/contact/delete.sh`
- `scripts/commands/group/list.sh`
- `scripts/commands/system/doctor.sh`

`add.sh` keeps the old verb `add` to preserve compatibility with older callers.

## Output Rules

- Commands return JSON by default.
- Logical failures return `{"success": false, "error": "..."}` and exit with status `1`.
- Success payloads return `{"success": true, ...}`.
- `--json`, `--plain`, and `--format=plain|json` are not supported.

## Commands

### Contacts

```bash
bash ~/.agents/skills/macos-contacts/scripts/commands/contact/search.sh --field name --limit 10 "John"
bash ~/.agents/skills/macos-contacts/scripts/commands/contact/search.sh --field email --exact "john@example.com"
bash ~/.agents/skills/macos-contacts/scripts/commands/contact/get.sh "John Doe"
bash ~/.agents/skills/macos-contacts/scripts/commands/contact/get.sh --id "23B708DC-4556-41E3-8738-89867826B760:ABPerson"
bash ~/.agents/skills/macos-contacts/scripts/commands/contact/list.sh --limit 20
bash ~/.agents/skills/macos-contacts/scripts/commands/contact/list.sh --group "Work"
bash ~/.agents/skills/macos-contacts/scripts/commands/contact/add.sh --first "John" --last "Doe" --phone "+48123456789" --email "john@example.com" --org "Acme" --birthday "04-20"
bash ~/.agents/skills/macos-contacts/scripts/commands/contact/add.sh --first "John" --last "Doe" --birthday "1988-04-20"
bash ~/.agents/skills/macos-contacts/scripts/commands/contact/edit.sh "John Doe" --phone "+48111222333"
bash ~/.agents/skills/macos-contacts/scripts/commands/contact/edit.sh --id "23B708DC-4556-41E3-8738-89867826B760:ABPerson" --email "new@example.com"
bash ~/.agents/skills/macos-contacts/scripts/commands/contact/edit.sh "John Doe" --birthday "04-20"
bash ~/.agents/skills/macos-contacts/scripts/commands/contact/edit.sh --id "23B708DC-4556-41E3-8738-89867826B760:ABPerson" --birthday "1988-04-20"
bash ~/.agents/skills/macos-contacts/scripts/commands/contact/edit.sh --id "23B708DC-4556-41E3-8738-89867826B760:ABPerson" --clear-birthday
bash ~/.agents/skills/macos-contacts/scripts/commands/contact/delete.sh --id "23B708DC-4556-41E3-8738-89867826B760:ABPerson"
```

### Groups

```bash
bash ~/.agents/skills/macos-contacts/scripts/commands/group/list.sh
```

### System

```bash
bash ~/.agents/skills/macos-contacts/scripts/commands/system/doctor.sh
```

## JSON Contract

Success envelope:

- `success`: `true`
- command-specific fields such as `count`, `data`, `id`, `name`, or `message`

Failure envelope:

- `success`: `false`
- `error`: string

Contact object:

- `id`
- `name`
- `phones`
- `emails`
- `addresses`
- `organization`
- `job_title`
- `birthday`
- `note`

Search and list rules:

- `search.sh` supports `--field name|phone|email|org|all`, `--limit N`, and `--exact`
- `add.sh` and `edit.sh` support `--birthday` in `MM-DD` or `YYYY-MM-DD` format
- `edit.sh` supports `--clear-birthday` to remove an existing birthday
- use `--field phone` or `--field email` for exact lookups by number or email
- phone, email, and address labels are normalised to values such as `mobile`, `home`, `work`, and `other`
- Contacts can return birthday year `1604` when the year is not set

## Safety Boundaries

- Read commands are safe by default.
- Write commands are explicit: `add.sh`, `edit.sh`, and `delete.sh`.
- Treat contact records as real user data.
- Do not call internal AppleScript files directly when public wrappers exist.
- If Contacts automation is blocked by macOS permissions, report that clearly instead of retrying destructive actions.
