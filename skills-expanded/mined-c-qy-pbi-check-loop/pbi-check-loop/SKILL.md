---
name: pbi-check-loop
description: >-
  Closes the verify loop for Power BI Desktop development: reloads a .pbip so Desktop re-reads
  TMDL/PBIR changed on disk, and captures the window so a model can see what rendered. Power BI
  has no reload command of its own.
  Use whenever working on a .pbip project - editing measures, TMDL, relationships, M,
  visual.json, PBIR or themes. Such edits stay invisible to the running Desktop until reloaded,
  so the edit is not finished until this runs.
  Trigger - after ANY edit to a project file: run Check unasked, then reload if it changed. A
  reload discards unsaved work in Desktop - confirm once per session, not each time.
  Trigger - reload: "reload pbi", "restart power bi desktop", "重开一下 Desktop", "重载一下".
  Trigger - check: "is desktop up to date", "Desktop 是最新的吗", "需要重载吗".
  Trigger - shot: "screenshot the report", "看看现在报表", "截个图".
  Trigger - iterate: "match the mockup", "照着原型图做", "改到跟原型一致".
  Trigger - diagnose (AUTO): a broken visual, blank page, or an error dialog.
  Not for Power BI Service or DAX. Windows only.

version: 1.0.0
license: MIT
allowed-tools: [PowerShell, Read]
---

## Workflow

**Step 1 — Pick the mode**

| Situation | Mode | Section |
|---|---|---|
| Is Desktop stale? Which instance is running? | Check | Step 2 |
| Disk changed and the result must be seen | Reload | Step 3 |
| The reload produced an error | Diagnose | Step 4 |
| Need to see what rendered | Shot | Step 5 |

Always run Check before Reload. If Check reports no disk change, say so and stop — a reload
costs a full model load for nothing.

**Step 2 — Check**

```powershell
& "$env:USERPROFILE\.claude\tools\pbi-reload.ps1" -ListOnly
```

Changes nothing. Reports PID, edition (regular vs. Report Server), window title, start time,
the associated `msmdsrv` PID, and whether any `*.tmdl / *.json / *.pbir / *.pbism` under the
project is newer than the running instance. That last line is the decision.

Pass `-Path` to get that verdict. Without it the report says `Disk state UNKNOWN` —
**that is not the same as "no changes"**. Treat it as a question you have not answered yet:
supply the path and run again rather than concluding the disk is clean.

**Step 3 — Reload**

Ask in conversation first: **"Any unsaved changes in Desktop?"** Pass `-Yes` only after the
answer is no. See [Rules](#rules) — this cannot be skipped.

```powershell
& "$env:USERPROFILE\.claude\tools\pbi-reload.ps1" -Path "...\project.pbip" -Yes
```

| Parameter | Meaning |
|---|---|
| `-Path` | `.pbip` path. Remembered in `pbi-reload.last.json`. Always pass it explicitly |
| `-Yes` | Asserts the user confirmed no unsaved changes. Without it the script only warns |
| `-Id` | Which instance, when the title match is ambiguous |
| `-ListOnly` | Check mode. Also prints the Analysis Services endpoint |
| `-Wait` | Block until the model engine is up, then return — and print its endpoint |
| `-WaitTimeout` | How long `-Wait` waits, default 180 s |
| `-NoDismiss` | Leave the sign-in dialog alone |
| `-DismissTimeout` | Watcher lifetime, default 120 s |

Returns in ~2 s; a detached watcher keeps working in the background. A large model then takes
tens of seconds to load, and **nothing downstream is valid until it finishes** — a DAX query
against a half-loaded model fails or lies.

**Pass `-Wait` and let the script handle it:**

```powershell
& "$env:USERPROFILE\.claude\tools\pbi-reload.ps1" -Path "...\project.pbip" -Yes -Wait
```
```
Waiting for the model to finish loading (timeout 180s)...
Ready after 23s - title settled and the model engine is up.
  Analysis Services: localhost:58894   [msmdsrv 29412]
```

It returns `Ready`, `Desktop exited`, or a timeout that tells you to go read the dialog. Without
`-Wait` you have to poll the title yourself — **do not**. The obvious way to poll is broken:
"wait until the title is no longer `Untitled - Power BI Desktop`" fails outright on a localized
Desktop (zh-CN shows a different word), so the check passes the instant any window appears and
you query a model that is still loading. `-Wait` matches the *project name* instead, which only
a finished load can produce, in any language.

🔴 **`Ready` means two things, and the second one is why you can trust it.** The title settling
is necessary but not sufficient — it flips to the project name while the model engine is still
coming up, and a DAX query issued at that moment comes back *"table not found"*, which reads
exactly like a broken edit. `-Wait` therefore also waits for the instance's `msmdsrv` child, and
prints the endpoint it is listening on.

**That endpoint is the other half of the loop.** A capture proves a visual *rendered*; only a
DAX query proves a number is *right*. Take the `localhost:<port>` from the output and query it
(ADOMD, Tabular Editor, DAX Studio — outside this skill's scope, but this is where you point it).

⚠️ **Do not read `msmdsrv.port.txt` to find the port.** With two projects open, the newest port
file belongs to whichever loaded last, so you can silently connect to the *wrong model* — and
then a missing table looks like your edit broke something, when you are simply querying another
project. The endpoint printed here is resolved by parent PID → child `msmdsrv` → listening port,
which has no such ambiguity. `-ListOnly` prints it too.

🔴 **Reload is not a data refresh, and you almost never need to trigger one.** Reopening re-reads
the model definition and recomputes every DAX expression against the cached data — which is
exactly what a measure, relationship, format or visual change requires. It does **not** go back
to the source:

| Changed | Needs |
|---|---|
| Measures, relationships, formatting, PBIR | Reload — this skill. Done |
| Rows in the underlying source | A manual Refresh in Desktop — **the user's call, not yours** |
| **A partition's M expression** (added a column, changed a query, new table) | **Reload *and* a manual Refresh.** Reloading invalidates that table's cached data — it comes back **empty**, and every table whose M references it goes empty too. Pages bound to them render blank. That is expected, not a broken edit. Say so, then ask the user to refresh |

Never click or automate Refresh yourself. It re-queries the data source, takes minutes on a large
model instead of seconds, and may hit a production database — a decision that belongs to the user.
Your job is to *tell them it is now required*, and why.

**Step 4 — Diagnose a failed reload**

Reopening a project you just edited is exactly when it breaks. **First classify the failure —
the two classes need opposite handling.**

**4a. Wait for the load to settle before judging anything.** A missing window or an empty canvas
usually means *still loading*, not *failed*. Reload with `-Wait` and let it tell you which one
this is — `Ready` means the load finished and anything still wrong is a real failure; a timeout
means something is blocking it, most often a dialog.

⚠️ An empty canvas after a **partition M change** is not a failure at all — see the table in
Step 3. That table's cache was invalidated and the data is waiting on a user Refresh.

```powershell
& "$env:USERPROFILE\.claude\tools\pbi-reload.ps1" -ListOnly
```

**4b. Classify.**

| | **Class A — the project will not open** | **Class B — it opened, a visual is broken** |
|---|---|---|
| Symptom | Modal error dialog; no project loaded; title never settles | Title settles, report renders, but a visual shows an error or is blank |
| Layer | Model / project file | Report layer, or one table in the model |
| Loop state | **Broken** — nothing downstream can run | Intact — Reload and Shot both still work |
| Detect with | `-Text` (the dialog is the whole story) | `-Text` for a message, image for a blank tile |

**4c. Class A — read, close, fix, reopen.** In that order, and do not skip the close.

```powershell
# 1. read the dialog verbatim — note the PID it reports
& "$env:USERPROFILE\.claude\tools\pbi-shot.ps1" -Text

# 2. close ONLY that instance, by the PID from step 1
Stop-Process -Id <pid> -Force

# 3. fix the file on disk, then reopen
& "$env:USERPROFILE\.claude\tools\pbi-reload.ps1" -Path "...\project.pbip" -Yes
```

🔴 **Never `Stop-Process -Name PBIDesktop`** — that kills *every* Desktop on the machine,
including another agent's or the user's own unsaved work. Always target the single PID.

**Never leave a broken instance running while editing.** It holds the project, its `msmdsrv`
child lingers, and the next reload has to fight both. Read the error, close it, then fix.

| Class A error mentions | Fix |
|---|---|
| TMDL syntax, unexpected token, a line/column number | Re-read the file you wrote — usually indentation or a stray quote |
| A column, table or measure "not found" / cannot be resolved | The reference does not exist, or you renamed one end of it |
| A relationship invalid, circular or ambiguous | Your new relationship conflicts with an existing one |
| A property not defined / schema does not allow it | Wrong schema version for this edition — remove the offending property |
| Credentials, sign-in, gateway, cannot connect, timeout | **Environment, not your edit. Stop and tell the user** |
| File locked, in use, access denied | Another instance holds it — find it, ask which to close |

**4d. Class B — the loop still works, so use it.** The project is open; keep it open. A broken
visual is diagnosed in place, one round of the normal loop per attempt.

- `-Text` first: a visual error message is real text and reads exactly
- If the tile is simply blank with no message, capture the image — blankness is visual, not textual
- Then read back the `visual.json` you wrote. Common causes: a `queryRef` pointing at a renamed
  measure, a stale `stylePreset`, a field that no longer exists, a tile positioned off-canvas
- A table that failed to load shows up here too — one visual empty while its neighbours render
  usually means that table, not that visual

⚠️ **Not every bad edit produces a dialog.** A broken calculated table lets the project open
normally and fails silently — verified. Absence of a dialog is not proof the edit was good;
check that what you edited actually renders.

**4e. Look before guessing.** If the project is in git, `git diff` on the files you touched
beats re-deriving intent from an error message. After two failed attempts, revert to a working
state and reapply the change in smaller pieces.

🔴 **Never "fix" an error by having the user save from Desktop.** Desktop holds the pre-edit
model; saving would overwrite the very edit you are trying to repair.

**Step 5 — Shot**

```powershell
& "$env:USERPROFILE\.claude\tools\pbi-shot.ps1" -Out "<scratch>\pbi.png"   # image
& "$env:USERPROFILE\.claude\tools\pbi-shot.ps1" -Text                      # plain text
```

| Parameter | Meaning |
|---|---|
| `-Out` | Output path. Default `%TEMP%\pbi-shot.png` |
| `-Text` | Read the window via UI Automation instead of capturing pixels |
| `-Id` | Which instance, when several run |
| `-FullScreen` | All monitors instead of the window — privacy-sensitive, avoid by default |

Image mode uses `PrintWindow`: it captures non-foreground and occluded windows without stealing
focus. Read the PNG with the Read tool. When a dialog is open its text is printed automatically
alongside the image.

Pick the channel by the question:

| Question | Use |
|---|---|
| What does this error say? | `-Text` |
| Which visuals are on the page? What value is in this cell? | `-Text` |
| Which tables and relationships exist? | `-Text` |
| Layout, colours, spacing — does it match the mockup? | image + vision |
| Do the numbers tie out? | ADOMD DAX against the live model (not this skill) |
| Are fields bound / visuals off-canvas? | read back the PBIR JSON you just wrote |

Text gives what the report *says*; only an image gives how it *looks*. Text is sometimes more
precise — a name truncated to `SALES_DETAIL_BY_RE…` in the capture comes back whole in text.

## Running the loop unattended

The steps above are single moves. This is how they compose into an iteration loop that does not
stop for a human every round — the reason this skill exists.

**First, know which loop you are in. They use different oracles, and confusing them produces
false conclusions:**

| | Model layer | Report layer |
|---|---|---|
| The work | Measures, relationships, M | Layout, visuals, formatting |
| The question | Is the number *correct*? | Does it *look* like the prototype? |
| The oracle | **ADOMD/DAX against the live model** | The prototype image |
| This skill's part | Reload so the model reflects the disk; Shot to read errors | The whole loop below |

🔴 **Never judge numeric correctness from a capture.** Seeing a card render `1,234` proves the
measure *evaluated*, not that `1,234` is right. A capture cannot validate a number — only a DAX
query against the live model can, and that is outside this skill.

**Use the loop below when** a prototype, mockup or explicit spec exists and the task is to make
the report match it. **Do not use it** without one: see the stop condition.

```
Task Progress:
- [ ] 0. Establish the oracle — the prototype, or a written spec of what "correct" means
- [ ] 1. Confirm no unsaved changes in Desktop (ask once, up front — covers the whole run)
- [ ] 2. Edit the PBIR/TMDL on disk
- [ ] 3. Reload
- [ ] 4. Wait for the title to settle, then Shot
- [ ] 5. Compare against the oracle; list concrete differences
- [ ] 6. Differences remain and rounds < 2 → back to step 2. Otherwise stop and report.
```

**Step 0 is what makes the rest legal.** Without an oracle there is nothing to compare against,
and an agent that invents its own standard will declare success on anything. If no prototype
exists, do not run this loop — do one round, show the user, and let them judge.

**Ask about unsaved changes once, at step 1, not every round.** Once the loop owns the file the
user is not editing in Desktop; re-asking every iteration destroys the point of running
unattended. If the user does touch Desktop mid-run, stop the loop and re-confirm.

**Step 5 is the part that cannot be faked.** Every difference must be specific enough to
translate directly into one edit:

```
Bad   "The layout is close to the mockup."
      → not a comparison; nothing can be done with it

Good  "KPI row sits at y=120, mockup has it at y=80."
      "Card 3 title wraps to two lines, mockup keeps it on one."
      "Legend is bottom-right, mockup puts it top-left."
      → three differences, three edits
```

If you cannot see images, you cannot run this loop: use `-Text` for what the report *says*, and
hand the layout question to the user.

**Stop after two full rounds** that have not converged. Report what you changed, what you see
now, and what still differs. A third round burns another model load and rarely finds what the
first two missed.

**Step 6 — Report back**

Use the matching template. Do not narrate the mechanics.

### Check — English
```
Desktop   PID {pid} · {edition} · {title}
Disk      {changed, N files / no changes}
Verdict   {reload recommended / no reload needed}
AS        localhost:{port}        ← only when you are about to check numbers
```

### Check — Chinese
```
Desktop   PID {pid} · {edition} · {title}
磁盘      {已变更，{N} 个文件 / 无变更}
结论      {建议重载 / 不用重载}
AS        localhost:{port}        ← 只在接下来要核对数值时才报
```

**Reload:** one line for the outcome, then what was observed — where the window landed, whether
a dialog was dismissed. Quote the watcher log only when something went wrong.

**Diagnose:** quote the error text verbatim, name which of your edits caused it, and state the
fix. If it is environmental (credentials, gateway, lock), say so plainly and stop — do not
attempt a fix you cannot make.

**Shot:** describe what the image actually shows and answer the question from it. Do not
transcribe the whole screen.

## Rules

- **A reload needs human consent, because two opposite situations are indistinguishable:**

  | Situation | Correct action |
  |---|---|
  | Disk TMDL edited, Desktop memory stale | Never save — saving overwrites the disk edits |
  | User edited in Desktop without saving | Must save first — otherwise the kill discards it |

  Desktop's title bar carries no modified marker and window enumeration exposes no dirty state.
  Only the user knows. Never assume "the user does not edit in Desktop" — polishing the report
  layer is their job by design. This is information asymmetry, not a capability gap, which is
  why consent is required — see the session-scope rule below for how often to ask.
- **Always pass `-Path`.** The target instance is then identified by matching the project name
  against window titles, so another agent's Desktop is never killed. `pbi-reload.last.json` is
  shared machine-wide; without `-Path` you may inherit someone else's project.
- **Never run two agents against one report.** The conflict is at the file layer — two writers
  on the same TMDL/PBIR — which this tool cannot serialize.
- **Compare against something.** A capture alone is not a verdict. Compare to the prototype or
  mockup and name the differences; with no oracle, report what you observe and let the user judge.
- **Stop after two failed rounds.** If two edit → reload → shot cycles have not converged, stop
  and report what you tried. Each further round burns a full model load.
- **Execute the scripts, do not read them into context.** This document states everything needed
  to call them. Read the source only to modify it.
- **Treat captures and `-Text` output as confidential** — they contain live business data:
  revenue, supplier names, part numbers, customers.
  - Write captures to a scratch path, never into the user's project or a git repo
  - Never publish one to an artifact, a web page, or any external service
  - Quote only the values the question requires
  - Error dialogs may expose connection strings, server names or credentials — never echo those
- **Never expose secrets, tokens or passwords** found in config files, logs or captures.
- **If you cannot read images, never call image mode and then describe the report** — that is
  inventing content. Use `-Text`, or hand the PNG path to the user.
- **Act on your own, scaled to the risk.** Waiting to be told to reload puts a human back inside
  the loop, which is the problem this skill exists to remove. Autonomy is graded by what the
  action can destroy:

  | Action | Risk | Behaviour |
  |---|---|---|
  | **Check** | none — read-only | Run it **immediately** after writing any project file. Never ask |
  | **Shot** | none — read-only | Run it whenever you need to see the result. Never ask |
  | **Reload** | high — terminates Desktop without saving | Session-scoped consent, below |

  So: **every time you finish editing TMDL/PBIR, run Check without being asked.** If it reports
  no change, say so and stop. If it reports a change, proceed to the reload rule.

  🔴 **Do not save reloads up to "do them together later."** The tempting version is: *I'll
  investigate this data question first, then reload everything in one go.* It sounds efficient
  and it loses work — while you are off doing something else, the user may hit Ctrl+S in
  Desktop, and Desktop writes its **in-memory** model over your edits on disk. Observed: an
  agent edited TMDL, went to run queries instead of reloading, and the next user save silently
  reverted the edit. Reload after each edit, even when the next step is only a lookup.

- **Get consent for reloads once per session, not once per reload.** The first time a reload is
  warranted, say what you intend and what it requires:

  > I'll reload Desktop to verify this, and do the same after each further edit. That discards
  > anything unsaved in Desktop — please don't edit there while I work. OK?

  After that, **announce and proceed without waiting** — state one line, then run it in the same
  turn. Do not block for a reply on every round; that is the cost this skill exists to remove.
  Announcing keeps it visible — a reload blanks Desktop for tens of seconds, and silence reads
  as a hang.

  **The line is a statement, not a question.** Say it and keep going:

  > Disk changed, reloading now. *(after a partition M change, add:)* You'll need to hit Refresh
  > once it's up.

  Ending on "…OK?" or "shall I?" re-opens the consent you already have. It feels safer and is
  not — the user granted this for the session, and re-asking every round is exactly the failure
  mode this skill was built to remove. If you notice yourself hedging because *this* reload costs
  the user something (a long refresh, a big model), that cost is real but it is still not a new
  decision: state the cost in the same line and proceed.

  **Re-ask when the premise breaks**, not on a timer: the user says they edited in Desktop, they
  take over the window themselves, or they tell you to stop.

- **Match the user's language.** Chinese in, Chinese out.

## Failure handling

| Message | Meaning | Do this |
|---|---|---|
| `Power BI Desktop is not running` | Nothing to reload | Ask whether to open the project, or open it with `-Path` |
| `Several Desktop instances found` | Title match was ambiguous | Show the listed PIDs and editions, ask which, pass `-Id` |
| `No path available` | No `-Path`, nothing remembered | Ask for the `.pbip` path |
| `Disk state UNKNOWN` | Check ran without a path — the verdict is missing, not negative | Re-run with `-Path`; never read this as "no changes" |
| `Stopped. Nothing was changed.` | `-Yes` was omitted | Correct behaviour — confirm with the user, then retry |
| `WARNING: the running instance is '…' which does not match -Path` | Another project's Desktop | Stop and confirm before proceeding |
| `Recorded window rect looks wrong` | Window was minimized or off-screen | Expected; it reopens at the default position |
| `PrintWindow failed; fell back to CopyFromScreen` | Raw screen pixels captured | Another window may occlude it — say so rather than trusting the image |
| `No capturable window for PID …` | Wrong instance, or a reload whose window is not rebuilt yet. The message lists every running Desktop and its title — read that first | Match the PID against the list; if a reload just ran, use `-Wait` |
| `Still loading after Ns` (from `-Wait`) | A dialog is most likely blocking the load | Read it: `pbi-shot.ps1 -Text`, then Step 4c |
| `Desktop exited … without finishing the load` (from `-Wait`) | The process died mid-load | Class A. Check the project files you just wrote |
| A DAX query returns `table not found` right after a reload | You queried before the engine was up, **or** you are connected to another project's instance | Use the endpoint printed by `-Wait`/`-ListOnly`; never read `msmdsrv.port.txt` |
| Watcher log shows `restore done … MISMATCH` | Window restore did not settle | Report it; the reload itself still succeeded |
| Desktop reopens but shows an error dialog | Class A — usually your own edit | Step 4c: read with `-Text`, close, fix, reopen |
| Opens fine but one visual errors or is blank | Class B — report layer or one table | Step 4d: diagnose in place, keep it open |
| Desktop reopens with an empty canvas | Almost always still loading | Wait, re-check the title; only then treat as failure |

Watcher log: `~\.claude\tools\pbi-reload.dialogs.log`. Read it only when diagnosing.

## Maintaining these scripts

Empirically discovered pitfalls — dialog timing, the detached watcher, `IsZoomed` lying about
maximized state, verifying too early, BOM requirements — live in
[`docs/FINDINGS.md`](docs/FINDINGS.md). Read it only when modifying the scripts.
