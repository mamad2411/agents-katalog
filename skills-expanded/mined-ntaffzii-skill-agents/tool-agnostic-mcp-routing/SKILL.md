---
name: tool-agnostic-mcp-routing
description: Route tasks to available MCP or agent tools by capability rather than exact local tool names. Use when an agent has tools from Gemini, ChatGPT, Claude, Codex, or another MCP server and must decide which available tool capability to use.
---

# Tool-Agnostic MCP Routing

Use this skill when the current environment may have different tool names than this repository.

## Capability Map

Translate task needs into capabilities:

| Need | Capability |
|---|---|
| Inspect code | file search, file read |
| Choose tool scope | toolset recommender, toolset inspector, registry |
| Edit code | patch, file write, code edit |
| Verify code | command runner, test runner |
| Hand off blocked commands | user-run script generator, command handoff planner, script risk validator |
| Plan validation | validation planner, command policy checker |
| Inspect repository state | version control status, diff, log |
| Control repository state | branch creator, checkout, stage, unstage, commit |
| Understand project shape | project stack, scripts, manifest inspection |
| Understand project docs | documentation index, README/docs reader, context bundle |
| Build repo map | repository index builder, symbol/file search, related-file finder |
| Compare external MCP ideas | MCP catalog search, repo pattern comparison, local adaptation planner |
| Inspect dependencies | package manager detection, dependency manifest reader, lockfile status |
| Inspect containers | Docker CLI checker, Dockerfile inspector, Compose service inspector, Docker validation planner |
| Inspect API surface | route finder, endpoint extractor, OpenAPI spec reader, API config hints |
| Inspect data layer | schema finder, migration finder, ORM model extractor, database config hints |
| Query configured database | read-only SQL planner, SQL risk explainer, read-only Postgres runner |
| Inspect configuration | config finder, env key lister, secret hygiene checker |
| Inspect tests | test file finder, framework detector, source-to-test mapper |
| Inspect CI | CI file finder, GitHub Actions job inspector, validation command extractor |
| Inspect local tasks | TODO/FIXME scanner, roadmap file finder |
| Inspect dependency risk | unpinned dependency finder, high-risk dependency name checker |
| Scan repository security | secret scanner, dangerous command scanner, env exposure scanner, security report |
| Inspect release readiness | changelog finder, version detector, release checklist |
| Snapshot before broad edits | backup planner, zip snapshot creator |
| Edit structured registries | JSON/YAML/TOML reader, path getter, structured path patcher |
| Preserve project memory | memory saver, memory search, project memory summary |
| Build personal context | typed memory saver, context pack builder, memory handoff generator |
| Search long-running context | vector or semantic memory search, related-memory finder, memory cluster summarizer |
| Build RAG context | text chunker, RAG provider planner, embedding request planner, source metadata preserver |
| Inspect GitHub metadata | workflow finder, Actions inspector, PR description drafter |
| Inspect GitHub API data | repo reader, issue reader, PR reader, PR file lister, check status reader |
| Inspect browser/UI readiness | browser capability checker, static HTML inspector, smoke-check planner |
| Map a web page | HTML page mapper, heading/link/form/button extractor, element finder by label |
| Inspect live UI | Playwright runtime checker, page inspector, screenshot capture |
| Automate live UI | Playwright click, fill, text assertion, console/network failure inspector, accessibility snapshot, persistent session runner |
| Inspect design files | Figma auth checker, design file summary, token/component extractor, frontend implementation planner |
| Try safe experiments | sandbox workspace creator, snippet compiler, sandbox run planner |
| Understand tool failures | audit log, policy denial inspection |
| Audit MCP safety | risk classifier, mutating tool finder, policy coverage checker |
| Research current facts | web search, URL fetch |
| Capture public web pages | provider-neutral static fetch, browser capture, optional cloud scraper adapter, social public-only reader |
| Research finance markets | market quote reader, crypto price reader, finance-news planner, watchlist summarizer, position-risk calculator |
| Work with Notion | Notion auth checker, page search, page reader, note/update payload planner |
| Bridge Obsidian and Notion | Obsidian note inspector, Notion payload planner, Markdown conversion planner, sync checklist |
| Work with chat apps | Slack/Discord config checker, message search, channel summarizer, reply drafter, action-item extractor |
| Triage inbox | email config checker, email search planner, email summarizer, action extractor, reply drafter |
| Plan calendar | calendar config checker, event summarizer, daily plan builder, meeting prep drafter, follow-up extractor |
| Plan issue work | issue reference parser, issue draft builder, task breakdown, issue update planner |
| Inspect UI | browser automation, screenshot |
| Work with images/video | media inspection, frame extraction |
| Improve prompts | prompt analysis, rewrite, scoring |
| Save progress | handoff, document write |

## Workflow

1. Identify the next job
   - What must be learned, changed, verified, or created?

2. Choose capability
   - Pick the needed capability before choosing a tool.
   - If several tools can do it, prefer the least risky one.

3. Map to current tools
   - Read available tool names and descriptions.
   - If registry/introspection tools exist, call them before guessing.
   - Select the closest matching tool.
   - If no tool exists, explain the missing capability and use a text-only fallback.

4. Execute safely
   - Inspect before editing.
   - Preview before broad writes when possible.
   - Run narrow validation before broad validation.

5. Record mapping
   - In the final answer, say what capability was used.
   - Mention exact tool names only when useful to the user.

## Rules

- Do not assume this repo's `mcp-tools/` exists.
- Do not call tools by guessed names.
- Do not use a high-risk tool when a read-only tool is enough.
- If tool descriptions are ambiguous, choose the safer read-only action first.

## Output Format

End with:

- Needed capability
- Tool used or fallback
- Result
- Verification
