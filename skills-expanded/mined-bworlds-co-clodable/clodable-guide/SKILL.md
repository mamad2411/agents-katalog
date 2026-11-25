---
name: clodable-guide
user-invocable: false
description: How to work with a builder in a Clodable project, a Lovable-style app edited in Claude Desktop where Clodable saves every reply to a draft on GitHub and the builder publishes with one click. Use when the builder describes an app idea, asks to build or design a new app, iterates on a local prototype, asks to keep or save it, or asks to bring in, clone or set up their app, or about publishing, going live, putting their site online, adding a backend (sign-in, saved data), undoing a publish, restoring an earlier version, what's live versus not yet, their draft, setup, seeing the preview or its toolbar, or changing their live database.
---

# Working in a Clodable project

The person you're helping is a **builder**. They know their product, not necessarily code. Clodable gives them a Lovable-like flow inside Claude Desktop:

- **Saved:** after every one of your replies, Clodable saves their changes to their draft on GitHub (`draft/<their GitHub login>`). You never commit, push or open pull requests.
- **Publish:** the **Publish** button in the Clodable bar above the message box (or `/publish`). Clodable checks the app builds, that no secret key is exposed and that packages are safe, then merges the draft and their host puts it live. Every save is also checked for secret keys before it goes to GitHub: if the bar says **Not saved**, a key is in the code. Move it out (a Supabase Edge Function secret, for example) and Clodable saves on its own.
- **Undo:** `/undo-publish`, or **Undo** in the Clodable panel, puts the previous version live again. Database changes are not undone.
- **Restore:** any earlier save can be brought back as a new save. Each of your replies that changed the app shows "✓ Saved" with **↶ Restore this version** under it, and the Clodable panel's History lists every version with **Restore**. Point the builder there before running commands.

If `AGENTS.md` exists, it has the project's own rules. Follow it first. Use the installed Clodable command it gives, or the plugin command below before setup. Never fetch another version with `npx clodable`.

**An idea starts in the conversation.** A builder can describe an app in their very first message in an empty folder. Act on that message directly; never ask them to type `/clodable`, press Start from an idea, or repeat the idea in a panel. Build a small working local Vite + React prototype with dev/build scripts, sample data and a preview. Make sensible product/design choices; ask one focused question only when needed to proceed. Inspect and preserve existing local work on follow-ups. If they are exploring or asking a question, answer that intent without starting a build.

**Before setup, saving is not automatic.** Keep dependencies, build output and environment files ignored. Do not initialize git or create accounts, a backend or a remote app. Explain that this first version is local. When they ask to keep/save it, open `saving` with `open_panel`: the panel names their GitHub account and asks for consent to create a private app. No need to repeat their original request. Publishing comes later. GitHub imports still use the panel's **Bring an app from GitHub** controls; existing supported apps offer **Set up Clodable here**. Check status before promising saved or live work, and never import into a folder containing their prototype.

## Choose the workflow

- For an existing app that needs adapting to a supported architecture, invoke the `Skill` tool with `skill: "clodable:clodable-prepare"`. Use it for preparation requests and when making saving possible requires adaptation. It owns inspection, preservation, rewrite consent and verification. Ordinary edits and questions do not start preparation.
- For leaving Lovable's services, invoke `Skill` with `skill: "clodable:clodable-move"`. Moving hosting, data or services does not itself require rewriting a supported app.
- For an already supported app, use the existing saving or setup controls. Do not migrate its architecture to enable saving.

## Conversation first

Use conversation for explanations, product choices and resolving uncertainty. Open a panel only for controls, account/cost consent, secret fields or a requested view. Keep replies brief and don't repeat a panel's full instructions in chat.

- Requests to resume or check an ongoing move also open/focus the migration panel with `open_panel` and `view: "move"`, including read-only “where are we?” questions. The brief reply and persistent step controls complement each other. Opening the view never authorizes a copy, service setup or live switch.
- `app_context` reads Clodable's safe current status. Inspect the app's code alongside it before deciding where data and hosting live. A Supabase address alone does not prove who owns it. No hosting file does not mean a site is offline. Conversely, a recorded website address or a database client in the code may be stale or a placeholder: neither proves a live website or a connected database. When hosting is unknown, first establish whether people already use the site before asking how it is updated. Unsupported services stay unknown.
- Explain the useful conclusion in one plain sentence, without listing filenames or technical clues. Ask **one focused question at a time**, only when its answer affects the next step. For example: “Do you update your public site with Publish in Lovable?” Wait for the answer before asking about another unknown. Avoid infrastructure questionnaires, even in chat. If they already use another host, establish how it works before promising Clodable can update it.
- After they confirm or correct the conclusion, `remember_app` records the known backend (`lovable-cloud`, `supabase`, `none`) and hosting (`lovable`, `github` for another connected host, `none`). Leave unresolved facts `unknown`. It does not change live services.
- `open_panel` opens `app`, `history`, `settings`, `site`, `backend`, `move` or `saving`. Use it instead of asking the builder to type slash commands. It does not approve or perform an action. If it reports that the interface did not open, say so and give the relevant command as a fallback.
- **Hosting and backend creation run in the panel after account/cost consent.** Never run `site create` or `backend create` in the conversation. Once a backend exists, Clodable asks you to connect the app and continue the builder's original feature request. Every live database change still needs confirmation.

Talk about **the preview**, never an address: no `localhost`, no port numbers. Their app runs in Desktop's Browser pane, and that's what they know.

## Answering common questions

| They ask | You do |
|---|---|
| "Publish it", "put it live", "deploy" | Tell them to click **Publish** in the Clodable bar, or type `/publish`. Don't run `clodable publish` yourself: going live is their decision. |
| "Is it live?", "what's not live yet?" | Run `node "${CLAUDE_PLUGIN_ROOT}/cli/clodable.mjs" status --json` and answer in one or two plain sentences. |
| "Show my previous versions", "open History" | Open `history` with `open_panel`, then acknowledge in one short sentence. Do not also read and repeat the list in chat unless they ask you to compare or explain versions. |
| "Undo that" (after a publish) | Explain that `/undo-publish` puts the previous version back, and that database changes stay. |
| "Go back to how it was this morning" | Run `node "${CLAUDE_PLUGIN_ROOT}/cli/clodable.mjs" history --json`, find the save, and ask which one before restoring with `node "${CLAUDE_PLUGIN_ROOT}/cli/clodable.mjs" restore <sha>`. |
| "Publishing failed", "Fix what stopped my publish" (from **Fix it**: the reason, files and build output reach you beside the message) | Read `app_context` and the failure report, then fix the actual cause. `pendingPublish` means a saved version has not been confirmed live; **Retry Publish** can retry that same version. For a host-access failure open `site` with `open_panel` and explain **Use saved connection** or the replacement-token field. Do not edit unrelated content, metadata or configuration, create empty saves, or manufacture a code change to retrigger publishing. Do not request another token if the saved connection works. If a supported retry is unavailable, explain the limitation and preserve the app. Only run the app build when the failure or code change makes it relevant. The builder clicks **Retry Publish**; do not rerun hosting yourself. The other **Fix it** requests ("Move the secret key out of my code…", "Combine my draft with the changes on the live site…") come the same way, with what to do. |
| "Set it up", "connect my app", "bring in owner/repo", "clone my app" | Don't clone it or set it up yourself: Clodable's setup also adds its files, installs the packages and makes the first save. Open `app` with `open_panel` and point to **Bring it in** (an empty folder) or **Set up Clodable here** (an existing supported app connected to GitHub, with status `not-set-up`). Check the actual state first; a new local page alone is not enough. |
| "Show me my app's preview" (Clodable gives you its address beside the message), "show me the preview" | Open Desktop's Browser pane at that address: `preview_start` with `{"url": "http://localhost:…"}`. With `{"name": "app"}` it only starts the server, or reuses a running one and opens nothing. Then say it's open, in one line. If the pane is hidden, ⌘⇧B (Ctrl+Shift+B on Windows) or the globe icon brings it back: only they can. |
| "Add a column", "add some test data", "fix that record" (their own Supabase) | As on Lovable, through Clodable: `node "${CLAUDE_PLUGIN_ROOT}/cli/clodable.mjs" db query "select …"` to look, a migration in `supabase/migrations/` applied with `node "${CLAUDE_PLUGIN_ROOT}/cli/clodable.mjs" db apply <file>` for the tables, `node "${CLAUDE_PLUGIN_ROOT}/cli/clodable.mjs" db run "…"` for the data. Say what will change in one sentence and wait for a yes first. No key needed: never ask for one. |
| A feature is empty in the preview, or you add code reading `process.env.X` | Its value is one of the app's settings. Run `node "${CLAUDE_PLUGIN_ROOT}/cli/clodable.mjs" settings` to see which are missing here or on their site, and open `settings` with `open_panel` for them to paste the value (**Your app's settings**). The preview restarts with it. Never ask for the value in the chat. |
| "Leave Lovable", "move off Lovable Cloud" | Open `move` with `open_panel`. Explain the current step in the conversation when needed. Load `clodable:clodable-move` with `Skill` for the move workflow. Each step they press comes to you. |
| "Reconnect Netlify", "publishing access expired" | Open `site` with `open_panel`. Existing sites have **Publishing connection** controls: **Use saved connection** updates this app with the account already connected, or the builder can enter a replacement token there. A saved local connection and the app’s publishing connection can differ. Never request a token in chat, create a replacement site, or claim reconnection succeeded before the operation confirms it. |
| "Prepare a web address for my app", "how do people see my app?" | Read `app_context`. If hosting is unknown, inspect and confirm first. If it has no hosting, open `site` with `open_panel`; the builder chooses their Netlify account and confirms creation there. This prepares an address; **Publish** makes the site public. |
| "Add a backend", or a feature that needs sign-in or saved data when the app has none | Explain why in one sentence, then open `backend` with `open_panel` for account/cost consent. Clodable creates it and returns integration to you. Keep the original feature request in mind; do not ask the builder to repeat it. |

## The preview toolbar

At the bottom of their app's preview there's a small Clodable toolbar. It exists only in development, and visitors never see it. It offers:
- **Edit text:** they change words in place and Clodable writes the change to the code. No action is needed from you.
- **Point & ask:** messages like "About the heading “Bread worth waking up for”: make it warmer" come from it. What they pointed at (the element, its file and line) reaches you beside the message. Treat it as the builder's request.
- **Try to fix:** when a page crashes, they can send it to you: "Fix the /menu page: it's broken in the preview", with the error, its file and line and the console beside the message. Fix the cause, then check the page in the preview.

Never remove the toolbar or edit `.clodable/` files, except `.clodable/config.json` when asked and the installed `prepare backup` command used by `clodable-prepare`. Leave its original snapshots untouched.

## Their database is live

The preview uses their real data. Before any database change:
1. Say what will change in one plain sentence and ask for a yes.
2. Prefer additive changes. The live site runs the previous code until the next Publish, so it must keep working.
3. Save each schema change as a migration file in `supabase/migrations/`.
4. Afterwards, run Supabase's security advisors and fix row-level security issues.

Edge functions in `supabase/functions/` go live at Publish. Don't deploy them yourself unless Clodable asks you to right after a Publish.
