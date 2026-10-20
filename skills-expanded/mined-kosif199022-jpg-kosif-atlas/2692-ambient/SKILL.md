---
description: Use for all ambient-library operations. Triggers on setting up ambient-library in a project ("set up ambient-library", "install skills", "initialize the skill system"), configuring project skills ("configure my skills", "which skills do I need"), updating or managing skills ("update skills", "refresh skills", "add/remove a skill"), code review ("review this code", "code review", "check for security issues"), making a folder ambiently intelligent ("make this folder ambient", "stamp .aai here", "set up an ambient/agentic folder for X", "interview me about this folder"), and any project-specific task a domain skill covers ("write a project brief", "summarize this project", "create a project overview").
---

# ambient

You are the ambient router. Your bundled instructions and subskills live in
`${CLAUDE_PLUGIN_ROOT}/.aai/`. Read the router instructions and follow them:

**Read `${CLAUDE_PLUGIN_ROOT}/.aai/instructions.md` and execute it for this request.**

That file routes the request to the correct subskill in
`${CLAUDE_PLUGIN_ROOT}/.aai/skills/` and tells you how to handle domain skills in
`${CLAUDE_PLUGIN_ROOT}/library/`. Do not guess — read it first.
