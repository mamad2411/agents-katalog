---
name: call-gpt-pro
description: "Use after the user has authorized GPT Pro help; manage a prompt-plus-sources workspace, route through ChatGPT Projects when available, and audit returned reasoning."
---

# Call GPT Pro

Use this skill to delegate expensive proof or reasoning work to a GPT
Pro-capable model while keeping Codex as controller. The default workflow is a
managed prompt-plus-sources workspace: maintain source files locally under
`.agents/pro-manage`, keep them synchronized with a ChatGPT Project when the web
route is available, paste a focused prompt for each turn, audit the answer, and
integrate only verified parts.

This skill is a route map. Detailed source-management and dispatch mechanics
live in sibling reference files and should be loaded only for the route being
used.

## Route Selection

Default to the ChatGPT web project route when the user has GPT Pro web access.
Use the scripted OpenRouter route only when the web route is blocked, the user
asks for API dispatch, or a project-backed source set is unavailable.

- **ChatGPT web**: read `references/chatgpt-web.md`.
- **Script/OpenRouter fallback**: read `references/openrouter-script.md`.

The ChatGPT web route depends on the user's existing logged-in browser state.
When this route is selected, explicitly load and use the Chrome plugin/skill
surface. Do not substitute Playwright, the in-app browser, or another fresh
browser context for Chrome unless the user explicitly changes the route.

Do not silently switch routes after the route is selected. If the selected route
fails, report the blocker. Use OpenRouter fallback only when the user request or
project settings already authorize API credit spending.

## Shared Project Record

Write prompts, source manifests, and route metadata to workspace files under
`.agents/pro-manage/`. The record should make the concrete project state and
prompt turn reproducible:

1. `DEFAULT_ROUTE`: `chatgpt-web` unless the user or project overrides it.
2. `SELECTED_ROUTE`: `chatgpt-web` or `openrouter-script` for this handoff.
3. `PROJECT_NAME`: visible ChatGPT Project name when the web route is used.
4. `REMOTE_PROJECT_STATE`: `synced`, `synced-via-bundle`, `needs-sync`,
   `blocked`, or `unknown`.
5. `MODEL`: web model label or OpenRouter model slug.
6. `PROMPT_FILE`: path to the exact model-facing prompt for the next turn.
7. `SOURCE_MANIFEST`: local source inventory and sync status.
8. `OUTPUT_FILE`: path where the answer should be saved.
9. `TRANSCRIPT_FILE`: path for web/API metadata.
10. `AUTHORIZATION_SOURCE`: the user request or project setting that authorized
    this route and any API spending.
11. `TASK`: the exact theorem, lemma, gap, or derivation target.
12. `PROHIBITIONS`: no invented citations, hidden assumptions, or workspace edits.
13. `MEMORY_ISOLATION`: `isolated-project`, `shared-project`, `not-applicable`,
    or `unknown`, with a short note when the ChatGPT web route is used.
14. `REQUIRED_DIRECT_SOURCES`: files the user or run manifest requires as
    separate visible Project sources, especially named PDFs.
15. `CONVERSATION_MODE`: `new-project-chat`, `same-project-followup`,
    `new-project`, or `unknown`.

Use `scripts/manage_pro_sources.ps1` to initialize the local record, generate a
text source bundle, or generate a prompt skeleton when a workspace does not
already have one.

Keep route metadata in `project-record.md`, source manifests, and transcript
files, not in `PROMPT_FILE`. The prompt pasted into ChatGPT should contain only
the model-facing instruction: task, constraints, expected output, and references
to visible synchronized project sources when needed. Do not paste local paths,
output paths, transcript paths, model labels, or project bookkeeping as prompt
content.

## Dispatch Rule

Invoking this skill means the user has authorized GPT Pro assistance for the
current task. Ask when execution would require an unselected paid route, a
different model family, uploading sources not covered by the current
authorization, or a second independent web/API dispatch.

For the ChatGPT web route, do not start Chrome on the user's behalf. If the
Chrome plugin reports that Chrome is not running, send the user a short message
asking them to start Chrome, then stop and wait. Continue with Chrome browser
work only after the user reports that Chrome has been started.

For every ChatGPT web GPT Pro dispatch, follow the response waiting protocol in
`references/chatgpt-web.md`: poll at 15-minute intervals, keep the run in
progress while the page still shows active Pro thinking or generation controls,
and only classify output quality after the final assistant message is visibly
complete.

## Output Handling

After any route returns:

1. Save the answer into the active workspace and treat that file as authoritative.
2. Confirm the answer follows the project record, prompt contract, and required
   end marker when one was requested.

Do not store API keys, account identifiers, private paths, unpublished source
excerpts, or live transcripts inside the skill directory.
