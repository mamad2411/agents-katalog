---
name: add-desktop-engine
description: Connect a desktop AI (Claude, Codex, Antigravity, or any coding agent with a local desktop app) to Agent Frontdesk so it can do what Claude and Codex do there - projects and chats in the sidebar, file preview, the agent rail's character, speech bubble and quota, new chats, rendering of replies and cards, model / effort / permission menus, send / stop / steer / queue. The interface and these capabilities already exist as shared parts; you connect your data, pick the channel for each action, and declare what you can do. Use it when asked to add or onboard an agent, or to fill in what an existing agent's plugin is missing.
---

# Connecting a desktop AI to Agent Frontdesk

Frontdesk is a remote window onto each desktop AI: it shows the desktop app's conversations one to one, and only carries messages into the desktop app and reads back what the desktop app wrote. Execution, history and settings stay in the desktop app.

**You do not build pages.** The agent rail, the left sidebar, the right panel, the composer, every kind of card in a conversation, and the whole send / stop / steer / queue machinery were turned into shared parts when Claude and Codex were connected. You do three things:

1. **Read**: parse your session records on this machine, read-only, and hand them to the shared layer in the shape the contract asks for.
2. **Pick channels**: for each action Frontdesk takes (send, steer, stop, change settings, start a chat, answer a card), decide which route carries it into your desktop app. This is the decision that matters most; see [Choosing channels](references/channels.md).
3. **Declare**: say in your plugin what you can do (`capabilities`) and what your desktop app looks like (`look`, `accent`, `character`, `spaces`, `permissionModes`). The page reads only these. It never checks which engine you are.

## Read these first, in this order

1. [Design philosophy](references/philosophy.md): the reason behind every decision. When something is not covered, reason from the "why".
2. [Choosing channels](references/channels.md): the three questions that decide whether a channel may be used; the three routes (the desktop process's own interface / the desktop's window-to-window channel / the shared accessibility driver), how to find and build each; which route each existing AI uses for each action.
3. [Capability paths](references/capabilities.md): for every capability on the page, how it travels from the page to your desktop app, what is already done, what you provide, and how Claude and Codex provide it.
4. [Plugin contract](references/plugin-contract.md): the exact shape of every field and method.
5. [Acceptance checklist](references/acceptance.md): check every item before you hand over.
6. [Matching the look](references/ui-fidelity.md): only when the person explicitly asks for "exactly like my desktop app".

In the project root, `docs/architecture.md` (the overall structure, how each existing agent is reached, and the known limits) is the first place to look when unsure.

**Living examples**: `src/server/plugins/claude.plugin.ts` + `src/server/claude-bridge.ts` + `src/server/native/claude-desktop.swift` / `claude-desktop.cs` (every action through the accessibility helper, on macOS / Windows); `src/server/plugins/codex.plugin.ts` + `src/server/codex-bridge.ts` + `src/server/codex-desktop.ts` (an official interface, the window-to-window channel and the helper, mixed); `src/server/plugins/antigravity.plugin.ts` (everything through a local service's interface, no helper). Start from the one most like your desktop app.

## How to work

- **List your steps first**: use your own task list or plan feature to list the stages below and tick them off as you go. Without one, keep a numbered list in your replies and update it.
- **Run it and look at it yourself**: start Frontdesk, call the endpoints, run the tests, open the page and look (take screenshots if you can). Never declare something done from reading code alone.
- **Make it resumable**: keep `docs/skins/<engine-id>/progress.md` with what each step finished, what comes next, how to start any temporary server, and the channel table from step 2. If your quota runs out midway, you or another session can pick up from there.
- **Be frugal**: shrink screenshots before looking and look only at the region you need; keep temporary files in your temporary directory and clean them up.
- **Write TypeScript**: all source is strict TypeScript. Your plugin is `export const setup: PluginSetup = …`, and its shapes come from `src/shared/contract.ts` ([Plugin contract](references/plugin-contract.md) explains it); a wrong field or a missing required method fails `npm run build` / `npm run typecheck`. No `any`; treat native records as `unknown` first and narrow them with `src/shared/guards.ts` and your tolerant parsing, skipping records you cannot read, never pretending to know a shape with `as`.
- **Servers**: while you work, run `npm run dev` (`bridge-dev` in `.claude/launch.json`; the page is on 4110, page changes show at once and `tsx watch` restarts the server when it changes; it has no Accessibility permission). To test the helper, build and start a temporary port from a terminal (Bash), for example `npm run build && PORT=4131 node dist/server/server.js` (Windows PowerShell: `npm run build; $env:PORT=4131; node dist/server/server.js`); on macOS only a terminal-started server has Accessibility permission, on Windows any server with the same rights as the desktop app can act on it; after a code change you build and start it again. Do not casually restart the instance the person is using (port 4100 by default; go by the one they actually use); before you must, check that its `/api/activity` shows nothing `running`, then build and start it again from a terminal on the same port.

## Steps

### 1. Find out how things are (read-only, no code yet)

- Read the existing plugins in `src/server/plugins/`. If you already have one, this task is to fill in what the acceptance checklist says is missing.
- **Data**: where the session records are and in what format; where titles, working folders and update times are kept; which project a session belongs to (a field in an official interface, or the desktop app's own state file) and the project order; sub-sessions; the native evidence for "running" and for "this turn ended"; where each session's model / reasoning effort / permission mode is kept; whether the desktop app's own message queue is recorded; a quota interface; character art.
- **What appears in a conversation**: step lists, commands and their output, screenshots and generated images, images the person pasted, changed files, permission prompts, questions with options, the end-of-turn summary card, subtasks. What each looks like in the native record.
- **Sidebar**: the projects in your desktop app's sidebar, how many sessions each has (write it down to compare later), and whether there is a mode switch at the top of the sidebar.
- **Channels**: look for the interfaces your desktop app exposes (a local service, the socket or pipe its windows talk over, deep links, your official CLI's protocol), as described in section 2 of [Choosing channels](references/channels.md). Look for these before settling on the accessibility helper: they keep the desktop app and Frontdesk in step just as well, and they are faster and do not touch the window. Write down the evidence (`--help` output, protocol definitions, interface names found in the asar, the result of one test session). Do not guess.
- **Shared capabilities**: if your desktop app has speech-to-text, wire up `dictate` and `dictationReady` (contract section 6) and it becomes one of the microphone's sources; without it nothing breaks for anyone, since the microphone uses another engine's or the browser's.

### 2. Pick the channels (write them down before you build)

Fill in a table in `progress.md`, one row per action: route A, B or C, the evidence, and why it cannot be done if it cannot.

| Action | Channel | Evidence | When it cannot be done |
| --- | --- | --- | --- |
| Send | | | Do not send; say why |
| Steer | | | Fall back to the queue (`fallback: 'queue'`) |
| Stop | | | Do not declare `interrupt`; say to stop it in the desktop app |
| Change model / effort / permissions | | | Do not send; say why |
| New chat / new chat in a project | | | Say why |
| Answer a question / permission card | | | Say to answer it in the desktop app |
| Open this chat in the desktop app (the chat header's button) | | | Say why; every engine so far does it (the shared driver's `show-session`) |
| Open a file in the desktop app | | | Do not declare `openFile` |

Every row must pass the three questions in section 1 of [Choosing channels](references/channels.md). Any row that plans to "start another process to run this turn" gets crossed out and rethought. A row on route C says why routes A and B cannot do it; a row on route A or B names its fallback (route C, the queue, or not doing it and saying why). If you need the helper, get `probe` working first (Choosing channels, section 4) before going further.

### 3. Build it in stages

After each stage, open the page and look, add tests, and update `progress.md`. For every item, "what to copy" is in the matching section of [Capability paths](references/capabilities.md).

1. **Read-only, visible**: the plugin skeleton (`about` with `detect`, then `setup` registering an engine with `accent` and `character`), `status`, `models`, `list` (with `metadata.group`, `recentMessages`, `turnStartedAt`, the `desktop` settings), `projects`, `read` (turns, messages, tools, step lists, images via `media`), `usage`. By now the sidebar, conversations, your avatar on the agent rail, the speech bubble (for turns started in the desktop app) and the quota bar should all show.
2. **Sending, live**: `send` through the channel you picked, counted as sent once the native record shows the message; turn what the desktop app writes into events; end only on native evidence; `blocked()`; `observe`.
3. **Stop, steer, queue**: `interrupt`, `steer` (throw `fallback: 'queue'` when it cannot join). The queue is shared; you only make sure `read()` shows "running". If your desktop app has its own message queue, add `metadata.desktopQueue` and `sendNow`.
4. **Settings follow the message**: `metadata.desktop` sets where the menus start; what the person changed is changed in the desktop app first, then sent (map names in `desktopSettings`, read back to confirm); `permissionModes`.
5. **New chats**: pick an approach from the table in section 5 of [Capability paths](references/capabilities.md) (`cwd` / `createRequiresPrompt` / `newOptions` / `newSettings`); the "+" on projects; the desktop's modes (`spaces`).
6. **Cards, files, and the way back to the desktop**: question / permission cards (`approval` events, `questionCard`, `decide`, `approval_resolved`), the summary card (`registerTool` mapped to `summary`), `openFile`, `fileRoots`, and `showInDesktop` + `show(id)` (the chat header's "Open in <you>"; also what a card that can only be answered in the desktop app sends the person to).
7. **Looking like yourself**: fill in `look` from your desktop app; if needed, change `--kit-*` variables in `src/client/public/skins/<id>/skin.css`; register renderers for things only you have. Do a one-to-one match only when the person explicitly asks.

### 4. Hand over

- Run `npm run build`, `npm test` and `npm run check` (type check + build); all must pass. Add tests for new parsing and protocol logic (with test doubles, never paid tasks to a real agent). Add English for interface text and error messages to `src/client/js/i18n.ts`.
- **Try it for real (cheaply, with the person's consent first)**: test doubles cannot prove a channel really works. Tell the person this costs about a few short messages of quota. Once they agree:
  1. Start a new chat in Frontdesk (an empty temporary folder, the cheapest model) and send "Reply with ok only, do not use any tools". Check that Frontdesk shows the reply as completed, that the desktop app shows the turn right away, and that no second, forked session appeared.
  2. Pick a different model or reasoning effort on the page and send again; check that the desktop app's menu changed too.
  3. Send something that takes a while (for example "Count to 30, one number per line, pausing between lines"), steer it with one more line while it runs and check it joined that turn; then try stop.
  4. If you have permission prompts or question cards: trigger one, answer it on the page, and check the desktop's record holds that answer.
  If the person declines to spend quota, list what is "not verified with a real send" in your report.
- Go through the [acceptance checklist](references/acceptance.md) item by item.
- Before committing, make sure `git status` has no screenshots containing real chats.
- Give the person a short report: which files changed; the channel table; which capabilities work, which do not and why; extension points the shared layer lacks; what the person still has to do (sign in, grant Accessibility permission on macOS or run Frontdesk with the desktop app's rights on Windows, restart the Frontdesk server, delete test chats in the desktop app); which platforms you tried it on.

## Files you will create

| File | Required | What it is |
| --- | --- | --- |
| `src/server/plugins/<id>.plugin.ts` | Yes | Who you are (`export const about: PluginAbout`), then capability declarations and method mapping (`export const setup: PluginSetup`); a few dozen lines |
| `src/server/<id>-bridge.ts` | Yes | Reads native records, uses the channels |
| `test/<id>.test.ts` | Yes | Test doubles covering parsing and protocol |
| `docs/skins/<id>/progress.md` | Yes | Progress, channel table, how to resume |
| `src/server/<id>-desktop.ts` | With the helper | Extends `DesktopAutomation`, one method per command |
| `src/server/native/<id>-desktop.swift` | With the helper | Steps only; actions come from the shared driver |
| `src/server/native/<id>-desktop.cs` | With the helper, on Windows | The same steps for the Windows driver (`uia-driver.cs`); without it every command on Windows answers `not_ported` |
| `src/server/native/profiles/<id>.json` | With the helper | How controls are recognised (without their names where possible) and other data; on Windows also its `windows` section (`exe`, and locators the Windows app draws differently) |
| `src/client/public/skins/<id>/skin.css` | Optional | Only `--kit-*` variables |
| `src/client/public/assets/characters/<id>.svg` | Without official art | An original stand-in, marked as such |

Change the shared layer (`src/server/core/`, `src/server/services/`, `src/client/kit/`, `src/client/js/`, `ax-driver.swift`, `uia-driver.cs`) only when a shared part really lacks something, and make it an extension point every engine can use (defaults unchanged). List it separately in your report.

## Do not

- Do not start a CLI / SDK process, or resume the session on a service of Frontdesk's own, to run a turn: that is a second writer the desktop app cannot see. When the channel cannot do it, do not send, and say why.
- Do not read or extract other programs' private tokens or keys; your own official CLI's sign-in credentials may be read on the server at the moment of use (philosophy 2a and 15). Ask the person first for anything that needs their authorization.
- Do not add a read-only mode, and do not block sending because the session is running in the desktop app.
- Do not change or delete the desktop app's local data.
- Do not copy another app's images or fonts into the project; read them from the installed app at run time.
- Do not write `engine === '<id>'` in the page or the kit; do not copy the kit's styles to change them; do not change other engines' plugins.
- Do not make up model lists, quotas or completion states; when you cannot get them, show honestly that you cannot.
