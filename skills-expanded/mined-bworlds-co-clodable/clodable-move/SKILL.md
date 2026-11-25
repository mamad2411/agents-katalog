---
name: clodable-move
user-invocable: false
description: Runs the steps of a builder's move off Lovable in the conversation, with Clodable's own `move` commands (first look at the app's code and record what it uses, then create their own Supabase backend, read Lovable's export, copy data, people and files, deploy functions, switch the preview to the copy, put the website on Netlify, set up emails, switch off Lovable's AI, email and connectors, Google sign-in, then the switch: pause, final export and copy, go live, the app's domain, finishing in Lovable), and finds and fixes what goes wrong. Use when the builder's message starts with "Moving off Lovable:", or when they ask to continue, check or fix their move off Lovable or Lovable Cloud, their working copy or their new backend.
---

# Moving off Lovable, step by step

When reporting progress, preserve the evidence exactly. **No record is not proof that a test never happened.** Say “I don't have a recorded check for … on this copy,” never “it hasn't been tried” from missing records. Use **Still to confirm** for unknowns, not a “Not checked yet” heading. Say which features were previously checked and which still depend on Lovable; do not generalize database checks to the whole app.

The builder may press a step in the Clodable panel or ask naturally in the conversation. A panel request includes its exact command beside their message. A conversational request may not. Use the installed Clodable command from the app's `AGENTS.md`; in a set-up app it is `node ".clodable/local/clodable.mjs"`. Never fetch another version or inspect Clodable's implementation to discover an ordinary command. The panel shows where the move stands; explain choices and investigate problems in the conversation.

Their live app keeps running on Lovable until the switch: everything before it builds a **working copy** on their own Supabase. The switch (below) moves the live app over.

## Preserve the existing application

Explain the move as preserving the app's appearance, features and data while changing the services behind it. Moving consent does not authorize removing features. Before any optional skip, name the affected user journey and the capability that will stop; only the builder's explicit choice accepts that loss. Do not present a skipped service as a successful migration check.

When checking the working copy, identify existing journeys from the app's code, recorded facts and available original evidence. Compare the same actions and expected results on the copy: navigation, sign-in, forms and validation, persistence after reload, uploads, messages and other used services. Exercise writes only on isolated test data in the copy; never send real messages, charge payments or change live data just to test. Record passed, failed or blocked results with the rehearsal commands below. Keep inferred expectations separate from observed behavior. Missing original evidence or unavailable services remain explicit limits. Fix regressions and replay affected journeys. Before recommending the switch, state any failures, blocked checks or explicitly accepted feature loss; a successful transfer or a choice to move in one go does not prove that existing journeys still work.

## Running a step

- Run the exact command Clodable gives you for the step with Bash. It's Clodable's own command line, `node "…/cli/clodable.mjs" move <step>`. Don't add `cd …&&`, pipes or redirections: the exact command runs without a permission prompt.
- `copy` and `files` can take minutes: give them a 10-minute timeout. If a very large copy needs longer, run it in the background and follow it with `move status`.
- Read the output: the steps, the checks (✓ fine, ! needs a look), the counts.
- Answer in two to four sentences: what happened, what it means for them, and what comes next (the panel shows the next step's button). Use their words: backend, copy, data, people, files, live. Never git words.
- Say what's surprising, even when the step "worked": an export with 0 people when they have users, fewer rows than they'd expect, a check marked !, an empty feature on the copy.
- Name the scope of checks: "The database copy checks pass" does not mean "The app checks out fully". A selected copy preview proves which backend it uses, not that every feature was tried. AI, emails, sign-in and hosted behavior need their own evidence. Re-read current status and `settings --json` (names only) before repeating old reminders from memory; a saved setting can already be configured.

### A short migration checkpoint

For “where are we?” or a request for progress/test status, use the supplied fresh status and rehearsal record. Otherwise read `move status --json` once. Do not make a task list, reconstruct transcripts, inspect implementation or narrate an investigation for a routine checkpoint. Read another source only for a specific missing fact that matters to the answer.

A request to “explain what has been tested and what remains” is still a checkpoint, not a request for the full evidence log. Reply in at most three short paragraphs, with a hard limit of 140 words unless the builder explicitly asks for a detailed report. Do not use lists or separate bullets for each feature. Group related checks in one sentence:
- Current milestone and whether the live app changed.
- One compact **Previously checked** line naming the useful recorded feature checks and their scope.
- One **Still to confirm** line for unknowns or remaining services, and one immediate next action. Trying the existing copy is available before email/provider decisions.

Example shape (adapt only to recorded facts): 
> Your copy is prepared and hosting is set up but unpublished. Your live Lovable app is unchanged; I opened the move panel.
>
> Previously checked: [grouped feature checks], in earlier preview tests, not re-run now. [One important evidence limit.]
>
> Still to confirm: [remaining services or unknowns]. You can keep testing the copy, or use the panel for [next step].

Do not call the whole copy healthy, ready or fully working while a feature or service is blocked. Name the thing that passed, such as the database transfer check. Do not guess a percentage or say “halfway.” Do not repeat the same recap in an ask-user card. A status question does not require another question or a decision; state the next available action and leave its controls in the panel. Expand evidence only when asked for the full record. Keep the distinction between historical evidence and a fresh check even in a short reply.

### When the request starts in conversation

Run `move status --json` first if the current state is not already available. Use that result to avoid repeating a completed copy or creating anything again. These are supported commands, with the same installed command prefix above:

| Request | Next action |
|---|---|
| "Where are we?", "continue the move" | Read current status if not already supplied, then call `mcp__clodable__open_panel` with `view: "move"` to open or focus the existing migration panel. Briefly explain the current stage and next action. This applies even to a read-only status request or when another view is open; opening controls changes no app data. Do not rerun a copy, create a service, advance a step, or treat "continue" as consent for a live change or an account/cost choice. |
| "Set up emails", "switch the AI provider" | Open or focus `mcp__clodable__open_panel` with `view: "move"` before asking for a domain or another setup detail. Use the existing step and its connection/consent controls. Opening the panel does not authorize service creation or the live switch. |
| "Try the copy", "switch my preview to the copy" | `move preview copy --json`, then `move diagnose --json`. Open the existing preview with Desktop's preview tools, or start its configured `app` entry if needed. Check the requested app features; a successful database check alone does not establish they work. |
| "Check the copy", "is my new backend ready?" | `move diagnose --json`. Keep what was checked separate from features or data that could not be tested. |
| "Show live data in my preview" | `move preview live --json`, only when explicitly requested; remind them that edits in this preview affect live data. |
| "Read this export" | `move export --file <path> --json`; respect the matching and freshness rules below. |
| "Copy my data" | Check status and prerequisites, then `move copy --json` when that operation is requested. Copying again replaces the rehearsal's data and accounts; explain that effect before repeating it. |

For a command not listed here or supplied by the panel, consult the installed command's `move --help` before exploring files. Secret entry, account consent, Publish and live-switch boundaries remain unchanged. Keep the builder-facing reply brief; do not repeat command syntax or local addresses.

## Remembering checks on the copy

`move status --json` includes `rehearsal`: dated feature observations and the current copy identity. `move rehearsal --json` reads just that local record without contacting a service; `app_context` also includes it during a move. Use this record when resuming, rather than searching old conversations. Missing evidence means **unknown**, not “never tried.” Describe earlier checks as previously verified, not checked now. `scope: earlier-copy` means a recopy or different destination invalidated the evidence for today's copy. An automated check, a builder's report and a browser rehearsal are different evidence; preserve that distinction and each limitation. A later failure supersedes an earlier pass for the same feature. Preserve who did what: an anonymous visitor seeing a cover does not mean the post was created anonymously. A recorded blocked action was tried and failed; do not describe it as untested. Database transfer checks do not establish app readiness; name any remaining AI, email or other service dependency.

After an actual feature check, save its safe result for the next conversation. Read `move rehearsal --json` for its exact `copy` first; use the same installed command prefix:

```
node "…/cli/clodable.mjs" move rehearsal --set <<'EOF'
{"copy":{"ref":"COPY_REF_FROM_STATUS","dataAt":"COPY_DATE_FROM_STATUS"},"observations":[{"feature":"Open a note attachment","result":"passed","method":"browser","observedAt":"ACTUAL_CHECK_DATE_ISO","evidence":"Uploaded a disposable text file, reloaded and opened it.","limitation":"Does not verify transfer of existing users' files."}]}
EOF
```

Allowed results: `passed`, `failed`, `blocked`. Methods: `browser`, `automated`, `builder-report`. Include an actual date and a short evidence description (a session or test reference is useful); never include credentials, user identities or the contents of their data. Do not mark untested features as passed, invent historical checks or refresh old dates. If the copy changes before recording, stop and check what was tested; do not relabel old evidence. Reading status never creates a rehearsal entry or authorizes tests that change live data.

## Looking at the app first

The move starts with you reading the app's code ("Moving off Lovable: look at my app's code…"). What you record decides which steps the move has and how the panel names things, so be exact.

1. Run `move facts`. Its `hints` are Clodable's own scan: files calling Lovable's AI, sign-in providers named in the code, files sending emails through Lovable, connector services, payment files, scheduled jobs, uploads, backend functions and the settings the server code reads. They're starting points: confirm each in the code, and look for what a scan misses (an address built in pieces, a helper in another folder).
2. Leave out dead code: a file nothing imports, a page nothing links to.
3. Name each feature the way the builder sees it in the app, by its button or page: "Summarize, on each note", not `summarizeNote`. Add `where` (the file) for your later turns.
4. Record it, in one command, exactly like this (a quoted heredoc runs without a permission prompt; every field is optional, an empty list means "not used"):

   ```
   node "…/cli/clodable.mjs" move facts --set <<'EOF'
   {"ai":[{"feature":"Summarize, on each note","where":"src/lib/app.functions.ts"}],
    "signIn":{"email":true,"google":false,"apple":false,"other":[]},
    "appEmails":[],"connectors":[],"payments":[],
    "scheduledJobs":[],"uploads":[{"feature":"Attachments on notes"},{"feature":"Covers on wall posts"}],
    "notes":[]}
   EOF
   ```

   - `ai`: features calling Lovable's AI (its gateway, or TanStack AI's Lovable adapter).
   - `signIn`: how people sign in. Lovable's own helper (`@lovable.dev/cloud-auth-js`) means Google or Apple through Lovable: say which.
   - `appEmails`: emails the app sends itself through Lovable (a welcome, a notification), not the sign-in ones.
   - `connectors`: `{service, feature}` for each service reached through Lovable's connectors.
   - `payments`: `{provider, feature}`, Stripe or Paddle.
   - `scheduledJobs`: what each job does; include routes checked with `LOVABLE_CRON_SECRET` only if a job calls them.
   - `notes`: anything else the move should know, one plain sentence each (a page anyone can open, a hard-coded address). Keep it short.
5. Tell the builder in a few plain lines what the app uses, and that the panel now shows what the move involves. If they say something's off, check again and record the corrected facts: a new `--set` replaces the old.

## Secrets never pass through you

- The Supabase and Netlify tokens, the Resend key, Lovable Cloud's service key, AI and Google keys, secret values and the app's settings are typed in the panel and go straight to Clodable. Never ask for them in the chat. Never run `move connect`, `move netlify`, `move resend`, `move ai`, `move google`, `move secret`, `move vault-secret`, `move setting`, `move files --private`, `move forget` or `move disconnect`: Clodable blocks them and the builder uses the panel.
- Never read Clodable's private folder (`~/Library/Application Support/clodable`, `~/.config/clodable`): it holds keys and the people's data from the export. Clodable blocks it. `move status` and `move diagnose` report everything that's safe to see.
- Never show rows of people's data. Counts, times and the names of tables are fine.
- `move export` matches Downloads filenames to this app's Lovable project. If it cannot match one, ask for the file's name and location, then use `move export --file <path>`. A manual `.dump`, `.backup` or zip containing one of them is supported. Never rename another app's export to bypass a mismatch. Report the archive's date; an older manual export can rehearse a copy but cannot serve as a fresh final export. Database archives include storage metadata, not the uploaded files themselves; those copy in the separate files step.

## When something's wrong

1. Run `move diagnose`. It says whether the new backend is running, whether its API sees every table, whether the preview can sign people in on the copy, how many people there are with their last sign-up and sign-in times, whether the data's checks pass, what Postgres noted during the copy, and which backend the preview uses.
2. Explain the finding plainly. Clodable's own fixes touch only the copy (the API's list of tables, the preview's sign-in settings): run `move diagnose --fix` and say what changed.
3. For a problem in the app's code, read the code, explain the cause, and propose the change. Make it when they agree. It's saved to their draft and reaches their live site only when they publish (and on Lovable's hosting, only when they also publish in Lovable).
4. For anything on Lovable, on their live app, or in their Supabase account beyond the copy (pausing or deleting projects, plans, billing), explain and give them the exact clicks. They do it.
5. If you can't find the cause, say what you checked and what you'd look at next. Don't guess.

### When the copy cannot be checked

- Keep a blocked-check reply to two to four plain sentences unless the builder asks for detail: say what is unknown, name any other confirmed blocker, and give the immediate next step. Say "I can't confirm the copy is ready", rather than turning an unsuccessful check into a claim that it is not ready.
- A missing connection, an access error or an address that does not answer is not proof that the backend is paused, deleted or empty. Local move records describe earlier progress, not its current condition. Report the exact limit: what Clodable checked, what it could not check, and what is still unknown.
- If `move diagnose` asks for a Supabase connection, ask the builder to reconnect in the panel, then check again. Never ask for a token in the conversation. Only describe a project as paused when Supabase reports that state; only give current data or people counts when a successful check returned them.
- A remembered destination is checked and reused. Clodable has no automatic replacement flow for an unavailable destination. Do not promise a Create again button, clear its saved record, create a replacement or delete anything as a workaround. Restore connection/access first; if that does not resolve it, explain that the destination needs to be reviewed before continuing.
- If Lovable refuses an export because of its size limit, say the export was refused and copying cannot continue without a usable export. The refusal does not establish the database's actual size or why it exceeds that limit. Ask the builder to resolve the export with Lovable; do not substitute an old export, suggest changing live data, run SQL or contact support on their behalf without their request.

## The website on Netlify

`move site` creates the Netlify site (or finds the one it made), points it at the new backend, writes `netlify.toml` and `.github/workflows/clodable-netlify.yml`, and gives GitHub the two secrets the workflow deploys with. Netlify's free plan can't watch a private repository owned by a GitHub organization; the workflow can, and it records a GitHub deployment so Clodable's Publish knows when the site is live.

- This is hosting preparation, not publication or a completed move. After it, run `move status --json` and explain the next unfinished step, usually emails or services. Say the website is prepared and nothing was published. Do not tell them Publish is the only remaining step while those preparations and the switch are pending.
- Publish updates the app's shared code as well as starting the Netlify workflow. With Lovable's GitHub sync still connected, those changes can also reach the live Lovable app. Never present Publish as an isolated test of the copy. If the builder requested copy-only work or no live changes, do not recommend or perform Publish; continue the authorized preparation and wait for explicit publication/live-change consent. Do not skip emails or services, pause the app, copy again, or run the switch just to make a prepared address show a page.
- The settings their server code reads (`process.env.X`, like `GREETING`) are listed: they paste each value in the panel, once, for their preview and their site. The site step stays open until they do, or go on without them; values pasted earlier for the preview go to the site by themselves. Lovable's own (`LOVABLE_*`) only work on Lovable: the services step switches the AI one.
- If the deploy fails, the panel shows Publish's report with a link to the workflow's run: read it (`gh run view --log-failed`), explain, and fix the cause in the code or in `netlify.toml`.

## Emails

Lovable sent sign-up confirmations and password resets for them. Supabase's built-in mailer only writes to the project's own team, so real people need the builder's own sender: Resend, from a domain they own.

- `move emails --domain <domain>` adds the domain to their Resend account and prints the DNS records. Tell them where these go: wherever they manage the domain (where they bought it). The panel shows each record with a Copy button. Records can take minutes, sometimes hours, to show.
- "Check again" runs `move emails`: once Resend sees the records, Clodable gives Supabase a key that can only send from that domain. Say that their sign-up and reset emails now come from that address.
- If a record isn't seen after a while, the usual causes: the name was entered with the domain repeated (`send.example.com.example.com`; many providers add the domain themselves), quotes around a TXT value, or another SPF record already on `send`.
- Without a domain, the panel offers to go on without emails: new people sign in without confirming, and nobody can reset a forgotten password. Make sure they understand that before they choose it.

## Copy notes worth saying

- `move files` reports `signedLinks`: links in their data signed by Lovable Cloud (with a token). They stop working when Lovable Cloud goes, and only the app can make new ones: offer to change the code so it signs links on the new backend.
- The database's own secrets (Supabase Vault) can't come with the export: the copy step stays open and asks for each value, with the query that reads them in Lovable (or they go on without them). The functions step does the same for their secrets.
- On Supabase's free plan, the panel warns before copying when the app is larger than the plan holds (500 MB of data, 1 GB of files). Upgrading the organization is their decision.

## Lovable's services (AI, emails, connectors)

They stop working off Lovable. The panel's "Switch off Lovable's services" step takes one at a time:

- **AI**: the builder picks a provider (OpenRouter has the same models as Lovable's AI; Gemini; OpenAI) and pastes a key in the panel (`move ai <provider>`): Clodable saves `AI_API_URL` and `AI_API_KEY` for their preview, their site and their backend functions. Then you point the code at them: the same OpenAI-style API (`${AI_API_URL}/chat/completions`). Keep Lovable's gateway as the fallback when `AI_API_KEY` isn't set: until the switch the app still runs on Lovable.
- **The app's own emails** (through `api.lovable.dev`): `move app-emails` gives the app a Resend key that sends only from their domain (`RESEND_API_KEY`, `EMAIL_FROM`). Change the sending code to Resend's API, with Lovable's as the fallback, then `move functions`.
- **Their own sign-in emails** (`supabase/functions/auth-email-hook`, Lovable's templates): once the functions are deployed and send through Resend, `move emails --hook` turns Supabase's send-email hook on, signed with a secret both share.
- **Connectors** (`connector-gateway.lovable.dev/<service>`): the builder pastes their own key for each service in the panel (`<SERVICE>_API_KEY`); change the code to call the service's own API with it.
- `move services` shows what's left. The builder can go on without switching (`--skip`, from the panel): say plainly which features stop when Lovable goes.

## Google sign-in

On Lovable, Google sign-in goes through Lovable's broker (`@lovable.dev/cloud-auth-js`), which only works on Lovable. The panel walks the builder through creating their own Google client (with the redirect address it shows) and takes its ID and secret (`move google <id>`, the secret on stdin): Clodable turns Google on in the new backend and sets `VITE_GOOGLE_SIGN_IN=supabase` for their preview and site. Then change the button: `supabase.auth.signInWithOAuth({ provider: "google", options: { redirectTo: window.location.origin } })` when `import.meta.env.VITE_GOOGLE_SIGN_IN` is `supabase`, Lovable's broker otherwise.

## Two ways to move

The builder chose in the panel (`move status` says `method`):
- **Carefully** (an app people use): a working copy to try, then the switch below. Nothing written in the live app is lost.
- **In one go** (a prototype): one export, then `move golive` straight away. No try step, no pause, no second export. Going live starts the scheduled jobs too. Anything written in their Lovable app after the export stays there: if their export is old and that matters, suggest exporting again and copying again before going live.

They change it in the panel until the pause or going live. Never run `move method` yourself.

## The switch (carefully)

The live app moves over in one sitting, with a short pause:

1. **Pause** (the builder, in Lovable's SQL editor: More → Cloud → SQL editor): the panel shows the SQL with a Copy button. It takes away the app's right to change data, holds new sign-ups and password or email changes (a guard named `clodable_pause` that never comes over to the new backend), holds uploads where Lovable allows it, and stops scheduled jobs; people still see everything and sign in. The builder presses "I've paused it" in the panel (`move paused`). Lovable allows one export a day: if the last one is recent, the panel says when the next is possible, and the pause should wait until then.
2. **Final export**: `move export` refuses an export made before the pause, because it would miss what people wrote since. If that happens, the pause wasn't applied or the zip is the old one: help them check.
3. **Final copy**: `move copy` (then `move files` when the app has uploads). It gives the app its writes back on the new backend, starts its scheduled jobs there, and brings the messages waiting in its queues. If a check says "!", run `move diagnose` before going further.
4. **Go live**: `move golive --sign-up yes|no --confirm-email yes|no` (the builder chose who may sign up in the panel) points sign-in at their site, rewrites the app's `.env` and `supabase/config.toml` (and files in `src/` naming the old project), and makes Publish follow their Netlify site. Tell them what changed, then that **Publish** puts it live at their site's address. Read the changes yourself: if the app names the old backend somewhere Clodable didn't rewrite (`server/`, `app/`, functions), fix it. In one go, the panel first gives the line that stops Lovable's scheduled jobs (so they don't run twice). If the app takes payments, the panel shows the Stripe webhook's new address to set at the same time.
5. **The app's address** (`move domain <name>`): after Publish, if the app has its own domain, Clodable adds it to the Netlify site and prints the records to change at their domain's provider; `move domain` checks them again, and once they point to Netlify, sign-in links use the domain. Or they keep the Netlify address (`--skip`, from the panel).
6. **Finish in Lovable** (the builder), only once Clodable has seen them sign in on the new site: unpublish the app in Lovable (More → Settings → General → Unpublish project), disconnect Lovable's GitHub sync (More → Settings → Git → GitHub → Disconnect, so Lovable doesn't change their code), then remove Lovable Cloud, which deletes Lovable's copy of their data. "I've done it" also deletes Clodable's copy of the export from this computer.

In one go, steps 4 to 6 apply.

When their message says "I've finished in Lovable", the move is over and they change their app here from now on. Open the preview (`preview_start` with the `url` Clodable gives beside their message; by `name` it opens nothing when the server already runs), then say in three or four lines: they describe a change here and watch it in the preview; Clodable saves each reply; **Publish** puts it live at their site's address; History and **Restore** bring back any earlier version. When a step asks to open the preview, do it the same way.

Never run `move paused` or `move finished` yourself: they record what the builder did in Lovable, and they press them in the panel. Server code that writes with the service key (a payment webhook, say) isn't paused: if the app has some, say so before the pause.

For a concrete copy or service failure, read [copy troubleshooting](references/copy-troubleshooting.md) for the matching symptom and recovery.

## Not automated yet

Scheduled jobs that call the app's own routes with Lovable's cron secret (`LOVABLE_CRON_SECRET`): say they need a secret of their own, which you can add. Signed links in their data (see above). If they ask about anything else not listed here, say so plainly.
