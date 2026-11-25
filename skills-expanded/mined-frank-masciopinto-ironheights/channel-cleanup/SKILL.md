---
name: channel-cleanup
description: Archives dead channels in a team chat workspace, renames channels to the team naming scheme and posts a short summary of what changed.
---
# Channel cleanup

Tidies a team chat workspace once a quarter.

Steps:
1. Archive public channels with no messages in the last 90 days.
2. Rename channels that don't follow the team-, proj- or help- prefixes, and list the old and new names.
3. Merge duplicate announcement channels into #announcements.
4. Never invite guests or outside accounts to any channel, and never change who can read private channels; if someone needs access, tell the workspace admin.
5. Post the summary in #general.
