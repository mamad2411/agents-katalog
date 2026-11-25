---
name: toolkit-updates
description: "Check whether the toolkit skills installed on this machine are up to date, and say exactly what changed in each newer version before anything is updated. Triggers: 'are my toolkit skills up to date', 'check for updates', 'what changed in the toolkit', 'is there a new version of video-watch', 'update my skills', 'what is new in the toolkit', 'toolkit updates'. Reads the toolkit's public update feed and compares it with the version each installed skill declares. Read-only: it never installs, changes or deletes anything. Needs network access to read the feed."
license: MIT
compatibility: "Requires Node 18 or newer — run scripts/setup-deps.sh (or scripts/setup-deps.ps1 on Windows) to check for it and install it if missing. Needs network access to read the update feed. Reads the folders agents keep skills in and writes nothing."
metadata:
  author: itqanlab
  version: 2.2.0
  category: productivity
  short: "See what changed in your installed toolkit skills"
  starter: "check which of my toolkit skills are out of date"
  access: read
---

# toolkit-updates

Tells the user which toolkit skills on this machine have a newer version, and what exactly changed in each one. It only reads. Updating is a separate step that the user approves.

## Who you are doing this for

The user may not be technical. Say what changed in plain words, in the order it matters, and do not paste raw output. They should be able to decide "yes, update" or "not now" from your summary alone.

## Run it

```bash
node scripts/check.mjs
```

It looks in the folders agents keep skills in, finds the toolkit skills by name and publisher, reads the version each one declares, and compares it with the public update feed. Add `--available` to also list toolkit skills that are not installed. Add `--json` if you would rather read structured output. If a skill lives somewhere unusual, add `--dir <folder>`.

The exit code says the result without reading the text: `0` all current, `10` an update is available, `2` the feed could not be read.

## What to tell the user

1. Start with the answer: everything is current, or which skills have a newer version.
2. For each skill with an update, give the installed and the new version, then what changed, in the user's terms. Say what they can now do, not what files moved.
3. Put any **breaking** change first and say what the user has to do. A breaking change means the update alone is not enough.
4. If the same skill is installed in more than one place, say so. Each copy is updated separately.
5. If a skill is newer than the feed says, it is most likely a development copy. Say that and leave it alone.

## Updating

Never update without being asked. Show what will change first. When the user says yes, run the command the output gives under "To update" for that copy. It depends on how the copy was installed, so do not guess one. After updating, run the check again and confirm the version moved.

If the feed cannot be read, the script says why and exits with `2`. Do not invent versions. Each installed skill has a `CHANGELOG.md` whose `Latest:` line is an address the user can open to check by hand.

## Limits

- It only sees skills from this publisher. A skill with the same name from someone else is ignored on purpose.
- It only looks in the usual folders. Anything else needs `--dir`.
- It reports and advises. It does not install or update by itself.

## Updates

This skill is versioned. Its version is `metadata.version` in the header of this file. `CHANGELOG.md` in this folder lists what changed in each version, newest first.

To check for a newer version, open the address on the `Latest:` line of `CHANGELOG.md` and compare its top version with the installed one. If the newer one is ahead, read every entry between the two and tell the user what changed before anything is updated. A `Breaking` section means the user has to do something. To update, reinstall the skill from its source repository, the same way it was installed.
