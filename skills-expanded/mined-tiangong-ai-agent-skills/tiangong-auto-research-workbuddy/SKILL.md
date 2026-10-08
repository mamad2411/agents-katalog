---
name: tiangong-auto-research-workbuddy
description: Adapt a managed Tiangong Auto Research workflow to a native WorkBuddy or CodeBuddy producer running in Default Permission mode, especially when independent review needs the explicit sandbox-bridge transport. Use only as a thin router to the project-installed tiangong-auto-research Skill; do not use for unrelated WorkBuddy tasks or standalone searches.
---

# Tiangong Auto Research for WorkBuddy

For feedback or Issue requests, load the sibling `tiangong-auto-research/SKILL.md`
and follow its reporting route before workspace inspection. Its installed
`references/issue-reporting.md` supplies the common templates and reporting rules.

Use the research workflow below only inside a user-selected managed Auto Research workspace.
Inspect the exact workspace context first. If setup is absent, use the canonical
Skill's setup reference; do not copy control files or invent a workspace.

Load the sibling project-installed `tiangong-auto-research/SKILL.md`, then read
its `references/sandboxed-ide.md` and the other reference selected by the
current stage. That canonical Skill owns the research workflow, schemas,
budgets, evidence rules, and recovery behavior; this adapter does not duplicate
them.

Run canonical CLI operations through this adapter's
`scripts/workbuddy_research_cli.sh`. It selects only an explicit Node.js 24
runtime and then delegates to the sibling canonical resolver. Do not call
WorkBuddy's ambient Node 22/npx after an `EBADENGINE` warning and do not suppress
the engine requirement.

Keep WorkBuddy in Default Permission mode. Never choose Full Access, an
unsandboxed-command escape hatch, `dangerouslyDisableSandbox`,
`dangerously-skip-permissions`, `excludedCommands`, or silent transport
fallback.

The workspace must identify the actual native producer as `workbuddy` or
`codebuddy`. Use that same value for the packet's `--host-agent`; never
impersonate Codex or Claude. The CLI must not launch the producer as a child.

For `sandbox-bridge`, require the owner to start the exact-version reviewer
sidecar from a separate native terminal and a private state directory outside
the workspace. From the IDE, verify `research reviewer status`, then run the
explicitly cost-confirmed reviewer doctor. Stop on any structured bridge,
signature, nonce, model, version, result-binding, or sandbox-policy failure.

After readiness passes, perform native producer stages in this current task and
return every result through the canonical CLI packet. Independent review and
mechanical closure remain CLI-controlled.
