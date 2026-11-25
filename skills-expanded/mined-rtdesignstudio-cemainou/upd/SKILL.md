---
name: upd
description: Report what was done to cemainou, the team's work log (the daily status update). Use when the person asks for an update, a report of today's work, or types /upd.
allowed-tools: Bash(git remote -v), Bash(git log:*), Bash(git status:*), mcp__plugin_cemainou_cemainou__last_update, mcp__plugin_cemainou_cemainou__list_projects, mcp__plugin_cemainou_cemainou__use_project, mcp__plugin_cemainou_cemainou__log_update, mcp__plugin_cemainou_cemainou__read_document, mcp__plugin_cemainou_cemainou__project_context, mcp__plugin_cemainou_cemainou__add_time
---
Report a status update to cemainou, the team's work log. Call the cemainou tool last_update with this session's cemainou id as session (from the cemainou line at the start of this session, if there is one) and this working directory's git remotes as repo (the output of `git remote -v`), then follow the next_steps it returns. If the session has no project yet, ask me which one it is and link it with use_project. Send the update only after I confirm the draft. Talk to me in my language.

Stress this in the update, if anything: $ARGUMENTS
