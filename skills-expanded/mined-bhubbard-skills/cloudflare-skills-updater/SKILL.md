---
name: cloudflare-skills-updater
description: "Use this skill to check the official Cloudflare Skills GitHub repository for any new or updated AI skills and sync them to your local environment."
---

# Cloudflare Skills Updater

The official Cloudflare AI Skills are continuously updated by the Cloudflare team at `https://github.com/cloudflare/skills`. Use this skill when requested to check for updates or sync the latest Cloudflare skills to the local repository.

## Update Workflow

Follow these steps to check for and apply updates:

### 1. Clone the Upstream Repository
First, securely clone the latest version of the official repository into a temporary directory so you can compare it against the local copy.

```bash
git clone https://github.com/cloudflare/skills /tmp/cloudflare-skills-update
```

### 2. Compare and Sync
The local Cloudflare skills are stored in `skills/cloudflare/` (relative to the root of the user's skills repository). The upstream skills are located in `/tmp/cloudflare-skills-update/skills/`.

Compare the directories. You can either use `rsync`, or simply copy the directories over, overwriting existing files to ensure they are up to date.

```bash
# Sync upstream skills into the local directory
cp -r /tmp/cloudflare-skills-update/skills/* /absolute/path/to/local/skills/cloudflare/
```

### 3. Clean Up
Remove the temporary clone once the synchronization is complete.

```bash
rm -rf /tmp/cloudflare-skills-update
```

### 4. Report Changes
If possible, run a `git status` or `git diff` in the user's local repository to identify exactly which skills were updated or added, and provide a summary of the new capabilities to the user.
