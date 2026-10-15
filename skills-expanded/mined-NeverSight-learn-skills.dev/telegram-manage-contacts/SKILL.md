---
name: telegram-manage-contacts
description: Manage Telegram contacts for the telegram-notify and telegram-ask skills. Use when the user asks to add, remove, or list Telegram contacts/recipients.
metadata:
  author: roziscoding
  version: "1.0.0"
---

# Telegram Manage Contacts

Add, remove, and list named contacts stored in `~/.config/telegram-skills/credentials.json`. These contacts can be used with `--to` in the telegram-notify and telegram-ask skills.

## Usage

The binary is at `<skill-dir>/../telegram-skills-bin/bin/telegram`.

> **Requires the `telegram-skills-bin` skill.** The binary lives in that sibling skill. If `<skill-dir>/../telegram-skills-bin/bin/telegram` does not exist, tell the user to install it (`bunx skills add roziscoding/telegram-skills`) instead of failing with a raw error.

### Add or update a contact

```bash
<skill-dir>/../telegram-skills-bin/bin/telegram --contact-add alice 123456789
```

This is an upsert — if the contact already exists, its chat ID is updated.

### List contacts

```bash
<skill-dir>/../telegram-skills-bin/bin/telegram --list-contacts
```

Outputs tab-separated `name\tchat_id` lines, one per contact.

### Delete a contact

```bash
<skill-dir>/../telegram-skills-bin/bin/telegram --delete-contact alice
```

## Notes

- Contact names are case-insensitive (stored lowercase)
- Changes are written directly to `~/.config/telegram-skills/credentials.json`
- The credentials file is created automatically if it doesn't exist yet
