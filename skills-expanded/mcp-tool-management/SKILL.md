---
name: mcp-tool-management
description: Design, organize, document, validate, or refactor MCP tools so they fit a skills/workflows/tools architecture. Use when the user asks to create tools, convert skills into tools, expose Python functions through MCP, map tools to skills, or maintain an mcp-tools folder.
---

# MCP Tool Management

Use this skill to keep tools separate from skills while making them work together.

## Repository Model

- `skills/` tells the agent how to think and behave.
- `workflows/` tells the agent what order to do work in.
- `mcp-tools/` contains executable actions.
- `data/tools.json` indexes tool groups, modules, and the skills/workflows that use them.

## Decision Rule

Make something a tool when it performs an action that benefits from code:

- Reading or searching files
- Editing files
- Running tests or commands
- Calling APIs
- Processing media
- Fetching web pages
- Scoring or transforming prompts

Keep something as a skill when it is judgment, policy, order of operations, or domain guidance.

Make something a workflow when it combines multiple skills and tools into a repeatable job.

## Tool Design Rules

- One tool should do one narrow job.
- Inputs should be typed and explicit.
- Outputs should be structured and easy for an agent to inspect.
- Errors should explain what failed and what input caused it.
- Tools should not hide broad multi-step workflows.
- Tools should not duplicate long `SKILL.md` instructions.
- Dangerous operations should require explicit confirmation or be split into inspect/apply phases.

## Recommended Tool Groups

- `filesystem.py` - list, read, search, and inspect files.
- `registry.py` - inspect available tools, workflows, runtime capabilities, and policy.
- `toolsets.py` - route agents to curated tool groups by job type.
- `audit.py` - inspect audit logs, policy denials, and recent tool activity.
- `mcp_security_audit.py` - inspect local MCP tool risk and policy coverage.
- `security_scanner.py` - scan repository secrets, dangerous commands, env exposure, and dependency risks.
- `project.py` - inspect project stack, package scripts, important files, and health.
- `docs.py` - find documentation, read README/docs files, and build context bundles.
- `package.py` - inspect package managers, manifests, lockfiles, and dependencies.
- `api.py` - inspect API route files, endpoints, OpenAPI specs, and API config hints.
- `database.py` - inspect schema files, migrations, ORM models, and database config hints.
- `config.py` - inspect config files, env keys, examples, and secret hygiene signals.
- `test_inspection.py` - inspect test files, frameworks, and source-to-test hints.
- `task.py` - scan task markers and roadmap files.
- `dependency_risk.py` - inspect offline dependency risk signals.
- `release.py` - inspect release files, versions, and readiness.
- `backup.py` - create allowed-root zip snapshots before broad edits.
- `structured_data.py` - read, validate, inspect, and patch JSON/YAML/TOML safely.
- `memory.py` - store, search, and summarize local project memories.
- `memory_context.py` - save typed decisions, preferences, bug lessons, and context packs.
- `github.py` - inspect GitHub workflow metadata and draft PR text.
- `browser.py` - inspect browser readiness and plan local UI smoke checks.
- `sandbox.py` - create temporary workspaces and compile snippets safely.
- `git.py` - inspect status, diffs, branches, and commits without mutation.
- `git_control.py` - create/switch branches, stage/unstage, and commit through allowlisted commands.
- `playwright_tools.py` - inspect live pages and capture screenshots when Playwright is available.
- `playwright_actions.py` - click, fill, assert text, inspect console/network failures, and run UI checks.
- `code_editing.py` - patch, format, diff, and test code.
- `validation.py` - plan and run allowlisted test, lint, typecheck, and build commands.
- `prompt_improver.py` - analyze, improve, score, and template prompts.
- `web.py` - search, fetch, extract, and summarize sources.
- `media.py` - inspect and process image, audio, and video files.
- `system.py` - inspect environment and run validation commands.

## Workflow

1. Classify the capability.
   - Skill: guidance or behavior.
   - Workflow: ordered playbook.
   - Tool: executable action.
   - Registry entry: discoverability and routing metadata.

2. Choose the tool group.
   - Put the function in the smallest matching module.
   - Create a new module only when no existing group fits.

3. Define the contract.
   - Name
   - Purpose
   - Inputs
   - Output shape
   - Error behavior
   - Safety constraints

4. Update the registry.
   - Add or update `data/tools.json`.
   - Map the tool group to relevant skills and workflows.
   - Add runtime introspection when agents need to discover the capability themselves.

5. Update skill or workflow text only when behavior changes.
   - Skills should say what capability to use.
   - Workflows should say which phase uses it.

6. Validate.
   - Confirm the module path exists.
   - Confirm registry JSON is valid.
   - Confirm no workflow depends on a missing skill or tool group.

## Output Format

End with:

- Tool group changed
- Tool contracts added or updated
- Skills/workflows connected
- Validation result
