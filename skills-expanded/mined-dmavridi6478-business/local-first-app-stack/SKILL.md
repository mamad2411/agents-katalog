---
name: local-first-app-stack
description: Decision guide for moving an app builder's own files onto local, open-source tools - demo videos to LocalSend (one-off transfer) or Syncthing (continuous sync), notes and launch checklists to Joplin, credentials to KeePassXC, original artwork to Krita - with the backup rule the source carousel adds ("sync can carry deletions too"). Records the licences read from the repos. Use when someone asks which tool to use for local files, notes, passwords, device sync or illustration, or wants an audit of what lives only in a cloud account.
---

# Local-first app stack

Source: a @dotdevs carousel, "Open-source tools for your app business", 5 picks. Its opening question is the method: **"Which file would you move local? Demo videos, notes, credentials or artwork? Start there."** A sixth slide advertises the author's own paid task app (Slothy, "paid app with a trial, not an open-source recommendation"); it is excluded from this stack.

| File type | Tool | What the slide says it is for | Licence (read 4 Oct 2026) |
|---|---|---|---|
| Demo videos, moved once between nearby devices | LocalSend | Local-network transfer, no cloud account | Apache-2.0 |
| Demo files kept in step across your devices | Syncthing | Continuous peer-to-peer sync | MPL-2.0 |
| User-interview notes, launch checklists | Joplin | Notes available offline | AGPL-3.0-or-later |
| Credentials | KeePassXC | Encrypted local database | Multiple files (GPL-2/GPL-3 family plus others in the repo); read `COPYING` before redistributing |
| Original illustrations and app visuals | Krita | Painting program that runs on your machine | Not checked here; the carousel says free and open source |

## Rules (the carousel's own caveats first)

1. **Sync is not backup.** The Syncthing slide warns it "can carry deletions too": deleting a file on one device deletes it on the others. Keep a separate, versioned backup. **[Certain]** (carousel text; this is how any two-way sync works).
2. **KeePassXC: back up the database file and protect the master password.** Losing either loses every credential. Keep the backup somewhere other than the synced folder, and do not store the master password in the database. **[Certain]**
3. **Move one file type first**, the one whose loss or leak would hurt most. For most app builders that is credentials.
4. **LocalSend needs both devices on the same network**; use Syncthing when devices are not on at the same time. **[Likely]** (from each tool's stated purpose).
5. **Joplin is AGPL**: using it for your own notes has no obligation; modifying and hosting it for others does.

## Install pointers

Use each project's own download page: syncthing.net, keepassxc.org, joplinapp.org, krita.org, localsend.org. LocalSend's README links a Homebrew cask (`brew install --cask localsend`). No installer was run in the build environment; these are desktop apps for your own machine.

## Audit procedure (what `/local-first-audit` runs)

1. List where each of the four file types lives today (cloud drive, email, a SaaS vault, phone).
2. For each, mark: only in a cloud account / local and backed up / local and not backed up.
3. Recommend the single first move and the backup that must exist before it.
4. Never ask the user to paste passwords, keys or private files.
