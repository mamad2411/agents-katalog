---
name: wordpress-skills-updater
description: "Use this skill to check the official WordPress Agent Skills GitHub repository for any new or updated AI skills and sync them to your local environment."
---

# WordPress Agent Skills Updater

The official WordPress Agent Skills are continuously updated by the WordPress team at `https://github.com/WordPress/agent-skills`. Use this skill when requested to check for updates or sync the latest WordPress skills to the local repository.

## Update Workflow

Follow these steps to check for and apply updates:

### 1. Clone the Upstream Repository
First, securely clone the latest version of the official repository into a temporary directory so you can compare it against the local copy.

```bash
git clone https://github.com/WordPress/agent-skills /tmp/wordpress-agent-skills-update
```

### 2. Compare and Sync
The local WordPress skills are stored in `skills/wordpress/` (relative to the root of the user's skills repository). The upstream skills are located in `/tmp/wordpress-agent-skills-update/skills/`.

Compare the directories. You can either use `rsync`, or simply copy the directories over, overwriting existing files to ensure they are up to date.

```bash
# Sync upstream skills into the local directory
cp -r /tmp/wordpress-agent-skills-update/skills/* /absolute/path/to/local/skills/wordpress/
```

### 3. Clean Up
Remove the temporary clone once the synchronization is complete.

```bash
rm -rf /tmp/wordpress-agent-skills-update
```

### 4. Report Changes
If possible, run a `git status` or `git diff` in the user's local repository to identify exactly which skills were updated or added, and provide a summary of the new capabilities to the user.
