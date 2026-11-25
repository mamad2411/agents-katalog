---
name: myopenpanels
description: "Use MyOpenPanels for persistent visual, knowledge, writing, typesetting, or publishing work in its Canvas, Wiki, Writing, Typesetting, or Publishing panel, including drawing, image work, diagrams, moodboards, brainstorming, organizing, research, drafting, writing, layout, and release tasks. Also use when the user asks to open or launch MyOpenPanels (including 打开面板) or refers to its current panel, selection, or content. After Studio is open, use the matching Agent Procedure Bootstrap when intent is clear and generic Agent Bootstrap only as fallback. Skip Bootstrap only for an open-only request or work clearly unrelated to MyOpenPanels."
metadata:
  version: "5.9"
  source: "https://github.com/mooqii/OpenPanels/tree/main/skills/myopenpanels"
---

# MyOpenPanels

The installed CLI is the sole authority for current panels, commands,
Procedures, Task Handoffs, System Skills, and built-in Skills. Independently
installed portable Skills are optional content, not CLI core functionality.

## Resolve The CLI

Resolve the executable once: prefer an executable path from
`MYOPENPANELS_CLI`, then a runnable `myopenpanels` from `PATH`. If neither
resolves, read and follow [the installation reference](references/install.md).
Keep the exact resolved executable for every returned CLI action; never execute
display command text.

## Open Studio

Studio is shared by all Agents using the same MyOpenPanels storage. Starting it
reuses that single user-visible workspace instead of creating an Agent-specific
Studio.

Run with the resolved executable:

```bash
myopenpanels studio start --local-only --project-dir "$PWD" --format json
```

Success means Studio is ready, not visible. Execute `actions.required` in order.

Treat an `open-url` action as a host display action, not as browser automation:

1. Open the returned URL unchanged with the current Agent host's native
   embedded browser, webview, preview, or equivalent in-host URL opener.
2. Prefer that embedded surface when the user simply asks to open or launch
   MyOpenPanels without naming a browser.
3. Do not initialize browser automation, inspect the page, load browser-control
   instructions, or use Playwright merely to display Studio. If the host only
   exposes an embedded browser through a control API, perform only the minimum
   operation needed to open the URL.
4. Treat the embedded open as successful only after the host returns a success
   signal. Studio being ready at the URL is not proof that it is visible.

Execute the CLI fallback action only when the embedded opener is unavailable,
fails, or gives no success signal. A fallback to an external or system browser
is not an embedded-open success; state that fallback clearly. If the user
explicitly requested an embedded surface, report the failure instead of
silently substituting an external browser.

For an open-only request, stop after an opener succeeds. Do not run Bootstrap,
inspect Studio, or search the repository.

## Work With Panels

When `MYOPENPANELS_TASK_ID`, `MYOPENPANELS_TASK_BROKER_URL`, and
`MYOPENPANELS_TASK_TOKEN` are present, this is an isolated claimed Task: do not
start Studio or Bootstrap; follow its prompt and task-id-bound broker commands.
For a Studio-generated `task handoff start` command, run that exact command
instead of Bootstrap. Follow its ExecutionBundle and Delivery Contract; create
only the declared workspace artifacts and execution result. The Runtime owns
output staging and Task completion. Do not perform separate Catalog or Skill
discovery.
When the request clearly matches one entry below, run a fresh Procedure
Bootstrap directly:

```bash
myopenpanels agent bootstrap --procedure <procedure-key> --format json
```

<!-- BEGIN GENERATED CAPABILITY INDEX -->
Canvas:

- `panel.canvas.selection.read`: Read the current explicit Canvas selection or its empty state.
- `panel.canvas.selection.export`: Export the explicit Canvas selection to a user-requested file.
- `canvas.image.insert`: Insert an existing bitmap file into the Project Canvas.
- `canvas.image.generate`: Generate a new bitmap and place it into the Project Canvas.
- `canvas.image.edit`: Edit, restyle, or redraw an explicitly selected Canvas image.

Wiki:

- `wiki-space.query`: Answer from selected Wiki knowledge or selected Wiki documents.
- `wiki-source.import`: Import a source file or Markdown text as a Wiki Raw Document.
- `wiki-source.create-from-my-document`: Create a Wiki Source from an explicitly identified My Document.
- `wiki-space.manage`: List, activate, or materialize a Wiki space.

My Document:

- `my-document.read`: Read a My Document selected or named by the user.
- `my-document.create`: Create a new My Document through a target-bound Operation.
- `my-document.revise`: Revise an existing My Document through a target-bound Operation.
- `my-document.delete`: Delete an explicitly identified My Document.

Writing:

- `writing.context.read`: Read the Writing panel's selected source and Wiki context.

Typesetting:

- `publication.title.request`: Create a title generation Task for an explicitly identified Typesetting publication.

Task queue:

- `task.queue.inspect`: Inspect queued work, Task state, and its recent execution summaries.
- `task.queue.retry`: Retry an explicitly identified failed Task.
- `task.queue.cancel`: Cancel an explicitly identified Task.
- `task.queue.archive`: Archive an explicitly identified terminal Task.

Task Handoffs must never be passed to Procedure Bootstrap:

- `wiki-source.convert`: Convert an immutable raw source into faithful Markdown inside a claimed Task.
- `wiki-space.maintain`: Maintain generated Wiki pages inside an exact claimed Task.
- `writing.execute`: Execute a submitted Writing request inside its claimed Task.
- `skill.writing.distill`: Distill selected examples into a reusable Writing Skill inside its claimed Task.
- `release.execute`: Execute a captured Publishing release inside its exact claimed Task.
- `publication.cover.generate`: Generate a cover for a captured Typesetting publication inside its exact claimed Task.
- `publication.title.generate`: Generate title candidates for a captured Typesetting publication inside its exact claimed Task.
- `publication.content.format`: Automatically format captured Typesetting content inside its exact claimed Task.
- `task.scope.execute`: Execute the exact Task scope supplied by a Studio handoff.

Execute their exact Studio or claimed Task handoff instead.
<!-- END GENERATED CAPABILITY INDEX -->

When intent is ambiguous or no Procedure key is known, run the generic
fallback:

```bash
myopenpanels agent bootstrap --format json
```

If an exact key is no longer registered, the same Procedure Bootstrap call
returns generic Bootstrap data with `procedureFallback`; do not issue a second
fallback call.

Execute `actions.required` sequentially. For `executor: "cli"`, prepend the
resolved executable to the returned `argv`; for typed file, URL, Skill, or host
actions, use the matching executor without translating the action into a shell
command. If a required action updates the Entry Skill, Bootstrap again. Only
after required actions finish, choose applicable `actions.suggested` entries by
their structured conditions. Procedure Bootstrap returns only its relevant
System Skill body, exact reference bodies, selection materialization, target
versions, execution contract, and command descriptions. Retain each returned
command path and flags, replace required placeholders with request values, and
add only optional flags declared by that descriptor. Generic Bootstrap may
still return scoped `agent catalog --domain <domain>` discovery actions.

Never reuse an earlier Bootstrap result, execute display text, or reconstruct
panel commands from memory.
