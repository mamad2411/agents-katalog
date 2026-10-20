---
name: rl-protect-run-report
description: "Opens the interactive HTML security report and wires it to this Claude Code session. Regenerates the report from the remediation plan, starts the local bridge so the report's ⋮ action menus (Accept / Triage / Fix) and Ask-an-AI chat reach Claude, launches the report in the browser, and arms an event-driven watcher so clicked actions and questions are handled automatically. TRIGGER when: the user wants to open, view, launch, or interact with the security report, or asks to connect the report to Claude. SKIP when: there is no remediation plan yet — run rl-protect-audit first. SKIP when: the user only wants a static Markdown export — use rl-protect-report."
---

This skill makes the HTML security report **interactive**: the user uses a finding's ⋮ menu (Accept / Triage / Fix) or asks a question in its chat panel, and Claude does the work. It (1) regenerates the report, (2) starts the bridge the report talks to, (3) opens the report, and (4) arms an event-driven watcher so clicks and questions are handled without the user asking each time.

The user has approved both auto-opening the report in the browser and arming the watcher for this skill.

## Step 1 — Locate the scripts and the plan

```
Glob: **/rl-appsec-agent/scripts/bridge.py
Glob: **/rl-appsec-agent/scripts/make-report.py
```

`{bridge.py}` and `{make-report.py}` are placeholders — substitute the absolute paths Glob returns. They live side by side, so `{make-report.py}` is `make-report.py` in the same directory as `{bridge.py}`.

Determine `{project_dir}`: the project directory the user named, else the current working directory. All pipeline artifacts live under `{project_dir}/.rl-protect/`. The plan is always `{project_dir}/.rl-protect/plan/remediation-plan.db` (`{plan_path}`) and the report is `{project_dir}/.rl-protect/reports/security-report.html` (`{report_path}`).

If `{plan_path}` does not exist, stop and tell the user to run `rl-protect-audit` first — there is nothing to report on. Do not traverse to parent directories looking for one.

## Step 2 — Pick the bridge port, then regenerate the report

Each project gets its **own bridge on its own port**, so several reports can be open at once without sharing one action queue. Pick the port by scanning from 7357 upward for the first that is **free** or **already serving this project's queue** (`{queue}` = `{project_dir}/.rl-protect/plan/actions.jsonl`):

```bash
RL_BRIDGE_QUEUE={queue} python - <<'PY'
import os, urllib.request, json, pathlib, hashlib
# /ping no longer leaks the absolute path (security); it exposes a non-reversible project id
# (sha256(project_dir)[:16]). Recognise our own bridge by matching that id. The queue now lives
# under <project>/.rl-protect/plan/, so walk up out of .rl-protect to the project root.
q = pathlib.Path(os.environ["RL_BRIDGE_QUEUE"]).resolve()
proj = next((a.parent for a in [q, *q.parents] if a.name == ".rl-protect"), q.parent)
mine = hashlib.sha256(str(proj).encode("utf-8")).hexdigest()[:16]
for p in range(7357, 7377):
    try:
        pid = json.load(urllib.request.urlopen(f"http://127.0.0.1:{p}/ping", timeout=1)).get("project", "")
    except Exception:
        print(p, "start"); break               # free port -> start our bridge here
    if pid == mine:
        print(p, "reuse"); break                # our bridge is already up on this port
else:
    print(0, "none")
PY
```

Use the printed `{port}` and mode (`start` / `reuse`) in every later step. (`0 none` means all 20 ports are busy with *other* projects — tell the user and stop.) Then regenerate the report, **baking that port** so its offline/`file://` fallback also targets the right bridge:

```bash
mkdir -p {project_dir}/.rl-protect/reports
python {make-report.py} --plan {plan_path} --output {report_path} --no-error-code --bridge-port {port}
```

`{report_path}` = `{project_dir}/.rl-protect/reports/security-report.html`. Regenerating ensures the report carries the current bridge buttons, port, and the latest plan state.

## Step 3 — Start the bridge (if not already running)

If Step 2 printed **`reuse`**, this project's bridge is already up on `{port}` — skip to Step 4. If it printed **`start`**, launch the bridge **in the background**, pinned to this project's queue **and** port, serving the report same-origin:

```bash
RL_BRIDGE_QUEUE={queue} RL_BRIDGE_PLAN={plan} RL_BRIDGE_PORT={port} python {bridge.py} serve --report {report_path}
```

Run this with the Bash tool's `run_in_background: true`. Use the **same `RL_BRIDGE_QUEUE` and `RL_BRIDGE_PORT` in every later command** so reads and writes hit the same queue/port. The `serve` daemon **self-stops ~120s after the report tab is closed** (it idles out when the report stops pinging `/ping`; `RL_BRIDGE_IDLE_TIMEOUT` tunes it, `0` disables) — so closing the report winds the bridge down on its own. The Monitor (Step 5) then just sees no more actions; tear it down with `TaskStop` when you're done. `--report {report_path}` makes the bridge serve that HTML at `http://127.0.0.1:{port}/` — open it that way (Step 4) so the report and the bridge share one origin and the browser raises no Private Network Access prompt. `RL_BRIDGE_PLAN={plan}` lets the bridge handle **bridge-direct** actions itself (currently `remove-version`): it drops the candidate and regenerates `{report_path}` with no Claude session. (The bridge derives the plan from the queue's project root as `.rl-protect/plan/remediation-plan.db`, so it finds it without this, but pass it to be explicit.)

## Step 4 — Open the report

Open it **same-origin via the bridge** so there is no Private Network Access prompt:

```bash
python -c "import webbrowser; webbrowser.open('http://127.0.0.1:{port}/')"
```

Because the page is served from `127.0.0.1:{port}` and its bridge calls use that same origin, **multiple project reports can be open at once** — each talks only to its own bridge and queue. (If you ever open the `file://` path directly instead, the report falls back to the baked `{port}` over loopback and the browser shows a one-time "access other apps" prompt the user must Allow.)

Tell the user the report is open and that the **Claude chip** (top-right, next to the light/dark toggle) should show a green dot ("connected" on hover). If its dot is grey ("offline") on a `file://` fallback, the browser blocked the localhost call — point them to opening it in Firefox, or use the `http://127.0.0.1:{port}/` URL.

## Step 5 — Arm the watcher (event-driven)

Drain clicked actions automatically by arming a **Monitor** on the queue file — it wakes you the instant a new action is posted (near-instant pickup, no idle polling). Do **not** use `/loop` here: cron's 1-minute floor makes pickup slow and polling an empty queue wastes turns.

Arm this with the **Monitor** tool (`persistent: true`). It polls the local queue every 0.5s, emits one line per genuinely-new pending action, and skips ones already handled:

```bash
cd {project_dir}
export RL_BRIDGE_QUEUE={queue}
declare -A seen
while true; do
  while IFS='|' read -r id action target; do
    [ -z "$id" ] && continue
    if [ -z "${seen[$id]}" ]; then seen[$id]=1; echo "new bridge action: $action on ${target:-?} ($id)"; fi
  done < <(python {bridge.py} pending 2>/dev/null | python -c "import sys,json; [print(a['id']+'|'+a['action']+'|'+a.get('target','')) for a in json.load(sys.stdin)]" 2>/dev/null || true)
  sleep 0.5
done
```

If you must skip a known-stale action, pre-seed it (e.g. `seen[<id>]=1`) before the loop. When the Monitor notifies you (a `<task-notification>`), run Step 6. Tell the user it's live — they can just click or ask in the report (no "I asked" needed) — and that it stops when the session ends or they ask you to `TaskStop` it.

## Step 6 — Process queued actions (on each notification)

Read the pending actions:

```bash
RL_BRIDGE_QUEUE={queue} python {bridge.py} pending
```

Each action has `id`, `action`, `kind`, `target`, `purl`, an optional `batch`, a `to` (the **Suppress** target gate tier — `warning` or `pass`), and (for `ask`) a `note`. `kind` is the report surface — `cve`, `policy`, `package`, `governance`, `malware`, `safe` (assessment category), `general` (a project-wide chat opened from the **+** on the Claude pill; no `purl` — answer using the whole plan), or `profile` (the scan-profile editor's **Ask an AI** assistant — see below) — and `target` identifies the thing within it (CVE id, policy code, category, threat name, `#N` for a generic chat, or empty for a whole package). The kebab menu is **kind-specific** (`triage`/`fix` only appear where they map to a real operation; `policy`/`safe` offer **Downgrade** — action id `suppress` — instead of triage; `governance` offers only accept/ask). A finding that already carries a change **we** made (its ⓘ explains it — an Accept, a Downgrade, or a Governance acceptance) also offers **Revert Changes** (action id `revert`, with a `reverted` hint of `accept`/`suppress`/`governance`); **Fix is not revertible this way**. Resolve the right plan finding from `kind` + `target` + `purl`. Do the work, then resolve it:

### Keep the conversation alive — post progress often

A queued action's chat bubble shows only a spinner and your **most recent** `progress` line, so if you work silently the user assumes it's stuck. **Narrate as you go** — this applies to *every* action below (`ask`, `run-stage`, `add-version`, `find-versions`, batched plans, re-scans):

```bash
RL_BRIDGE_QUEUE={queue} python {bridge.py} progress {id} "<present-tense, 5–9 words>"
```

- Post a line **before every step / tool call**, not just once — e.g. *"Reading the plan…"*, *"Checking reachability in your source…"*, *"Querying OSV for the CVE…"*, *"Diffing vs current…"*, *"Writing the result…"*. Aim for a fresh line every few seconds of real work; **never let a step run more than ~15s with no new update.**
- For anything that takes **minutes** (a re-scan, `explore-versions`, a remediator/triager run, scanning a single version), **set expectations up front** (*"Scanning 0.15.18 — about 1–2 min…"*) and prefer tools that **stream their own progress** so the bubble keeps moving: pass **`--bridge-progress {id}`** to `explore-versions.py`, and post a `progress` line per phase when you spawn an agent.
- `progress` only updates the bubble — it does **not** resolve. Always finish with `answer` (for `ask`) or `resolve` (everything else). One last line like *"Done — see below."* right before the final answer reads well.
- **Plan-bar execution rows (batched plans).** During an Execute-plan batch, the same `progress` line also drives each task row's live status. The report **prefixes `Working:` itself**, so post only the bare **activity phrase — super short, verb + identity** (e.g. `Triaging CVE-2024-39689`, `Researching CVE-2024-39689`, `Re-scanning release,transitive`); it renders as *"Working: Triaging CVE-2024-39689"*. Do **not** write the `Working:` prefix yourself. Crucially, **post the `progress` line and let it sit — do not collapse `progress` then `resolve` into the same instant**, or the ~1.5s tracker poll never catches the `working` state and the row jumps straight to done with no visible activity. For a genuinely instant deterministic task (e.g. an `accept`), still post one short `Working:` activity line before resolving.

### The resolve note is the task's execution summary — ANSWER the per-action questions

The plan bar builds the summary **for** you: the collapsed status line (e.g. `Accepted ruff@0.15.20`) and the detail table's **question labels** are generated programmatically from the action. So the `NOTE` you pass to `resolve` is **just your answers** — **one answer per line**, in the exact order of that action's questions below. No labels, no summary line, no bullets: line 1 answers question 1, line 2 answers question 2, line 3 answers question 3.

The report renders them as a two-column **Question → Answer** table (one row per question), expandable from the row and maximizable to a full overlay for auditing.

**Per-action questions (answer in this order, one line each):**

| Action | Q1 | Q2 | Q3 |
|---|---|---|---|
| `accept` | What was accepted? | Why is it acceptable? | Recorded where? |
| `triage` | Reachable? | Verdict & severity? | Evidence? |
| `upgrade` | New version? | CVEs cleared? | Tests & behavior diff? |
| `fix` | What was fixed? | CVEs resolved? | Tests & behavior diff? |
| `suppress` (Downgrade) | What was downgraded? | Why downgrade? | Effect after re-scan? |
| `revert` | What was reverted? | Why? | Effect? |
| `reapply` | What synced? | Acceptances applied? | Re-scan needed? |

Rules:
- **Exactly one answer per line, in order.** Each answer is a single line (it becomes one table row) — keep it to a sentence or two; you may use inline Markdown (`` `code` ``, **bold**, `[label](https://…)`). Do **not** add your own labels or a summary line; the report supplies them.
- **Cite specifics, not vibes** — exact versions/deltas (`2.25.0 → 2.32.4`, `−4 CVEs`), CVE/policy ids, which module/symbol is (un)reachable in *their* source, re-scan recipe + verdict, test counts, profile categories + audit author.
- **Be honest about limits** — if something was already done, skipped, partial, or failed, say so in the answer (and use `resolve … failed "<reason>"` for failures). Never imply more was verified than actually was.

Example — an `upgrade` of `requests` (3 lines = answers to *New version? / CVEs cleared? / Tests & behavior diff?*):

```
`2.25.0 → 2.32.4`, pinned in `requirements.txt`.
All 4 release CVEs (incl. CVE-2024-39689) cleared; re-scan at `release,transitive` introduced no new findings.
38-test suite passes; behavior diff shows no new risks. Package now **APPROVE**.
```

These per-action questions mirror `SUMMARY_QS` in `make-report.py` — keep the two in sync if you change them.

**Batched plans (the report's "Execute plan" bar).** When actions share a non-empty `batch` id, the user staged them and committed them as one plan. Do the work in **two phases** so a mixed batch re-scans exactly **once**, at the very end — never one scan per action, and never the remediator's gate *plus* a separate suppress re-audit. The bar polls `GET /actions?batch=<id>`: per-action rows show `queued → working → done`, and the **batch's single re-scan is tracked separately** (a synthetic `rescan` record → the "Re-scanning…" indicator beside Stop).

  1. **Group** the pending actions by `batch` (un-batched actions are handled individually). Note whether the batch contains any `suppress`, `fix`, a **`revert` of a Downgrade** (`reverted == "suppress"`), or a **`reapply` whose save changed `overrides` or disabled/enabled an assessment category** (`configuration.policy.assessments.<cat>.ignored`) — those are the only actions that touch **scan inputs** (the profile's overrides/assessments, or a manifest). If so, **open the re-scan tracker up front** so the bar shows it's coming, then drive it through Phase 2. **This is mandatory, not optional:** the bar predicts the re-scan **client-side the instant Execute is clicked** (from the staged task types) and `pollTrack` **won't mark the plan complete until a `rescan:<batch>` record settles** — so once a scan-input action is in the batch you **must** settle that tracker, *including the case where the action later fails and no scan actually runs* (Phase 2). Open it with:

     > **How to tell a `reapply` changed scan inputs — do NOT eyeball the action.** The queued `reapply` carries a **`rescan`** flag (a `true` value on the action means the save changed `overrides` or an `assessments.<cat>.ignored` toggle → the batch must re-scan) and a **`retriage`** flag (the save changed the threat model → re-triage, no scanner). **Trust these flags** — if `rescan` is set, open the tracker even when acceptance is empty and the threat model looks unchanged (an assessment-toggle reapply *stamps no findings*, yet is still a scan-input change — the trap is assuming "nothing to apply" means "no re-scan"). **Fallback if the flags are absent** (older report, or you can't see them): detect the scan-input change deterministically — read the saved profile and the plan, and treat it as a re-scan when **any `configuration.policy.assessments.<cat>.ignored` is `true` while the plan still holds findings of that category** (`plan.py findings` → a `secrets`/`hardening`/… finding whose category is now ignored ⇒ the ignore hasn't been applied yet ⇒ re-scan), or when the profile's `overrides` differ from what the plan was scanned under. When in doubt that a reapply is scan-affecting, **open the tracker** — settling an unneeded tracker `done` is cheap; leaving an expected one unopened hangs the bar forever.

     ```bash
     RL_BRIDGE_QUEUE={queue} python {bridge.py} rescan {batch} scanning "Applying changes…"
     ```

     The tracker's **message is shown verbatim as the plan-bar re-scan indicator's label**, so keep it **phase-accurate**: use *"Applying changes…"* (or a per-action mutation phrase) while Phase 1 writes mutations, and only switch it to *"Re-scanning (release,develop,transitive)…"* when the actual scan starts in Phase 2. Do **not** leave it saying "Re-scanning" during Phase 1 — a mixed batch (e.g. an upgrade the remediator later finds it can't apply) would otherwise show "Re-scanning" for minutes while nothing is being scanned, then settle with no scan having run.

  2. **Phase 1 — apply every action's *mutation* and resolve its row, with NO scanning.** Post a `progress` line as you start each, `resolve` it the instant it's settled:
     - `accept` → `apply-action.py accept …` (stamps the plan + writes the profile in one call; `--governance` for a governance block). No re-scan.
     - `suppress` → `apply-action.py downgrade …` (writes the profile `overrides`). **Do not scan here** — it rides the single Phase 2 re-scan.
     - `fix` → spawn **one** `rl-appsec-remediator` for *all* fixes (the Execute click is the consent — **never re-confirm** mid-execution). Have it **edit the manifests**; it does **not** run its own re-scan gate when the batch will re-scan in Phase 2. **For a lock-sourced plan** the remediator edits the *source* manifest and **regenerates the lock in Phase 1** (see its "When the scanned file is a lock file") so the Phase 2 re-scan of the recorded lock file picks up the change; if the lock tool is offline it edits the source, and Phase 2 re-scans the source with a stale-lock warning.
     - `revert` → undo the change (see the **revert** verb below). An Accept/Governance revert is a plan/profile clear, **no scan**; a Downgrade revert removes the profile `overrides` entry here and is applied by the Phase 2 re-scan.
     - `reapply` (`kind: profile`) → the gear editor already saved the profile; sync the **plan** to it (see the **reapply** verb below) — match the profile's acceptance rules to findings and stamp them (no scan). If the action's **`rescan`** flag is set (the save changed `overrides` **or turned an assessment category off/on**, `assessments.<cat>.ignored`), the batch re-scans in Phase 2 — you already opened the tracker in step 1, and you **must settle it** there (both only take effect on a scan — a disabled category makes the scanner emit no findings for it, and the report renders that category's SAFE card as "Assessment disabled by the profile"). If the action's **`retriage`** flag is set (the save changed the **threat model**, `configuration.policy.modeling` differs from `plan.py modeling`), that changes triage *judgment*, which is stored — so it needs a **re-triage** in Phase 2 (no scanner). Note an assessment-toggle reapply stamps **no** findings in Phase 1 (acceptance may be empty), yet still requires the Phase-2 re-scan — do not treat "nothing to stamp" as "nothing to do".
     - `triage` → record the verdict (one `rl-appsec-triager` scoped to the batch's CVEs); `ask` → answer.

     ```bash
     RL_BRIDGE_QUEUE={queue} python {bridge.py} progress {id} "Writing override…"
     RL_BRIDGE_QUEUE={queue} python {bridge.py} resolve {id} done "<summary — what you did + result, 1-3 sentences>"
     ```

  3. **Phase 2 — exactly one re-scan (only if Phase 1 opened the tracker).** After **every row is resolved**, run a single scan that picks up *all* the mutations at once — the new manifests from fixes **and** the new profile from suppresses — then rebuild + re-triage + re-derive acceptances:
     - **Any `suppress` in the batch** → run the full **re-scan workflow** (re-audit at the stored `recipe`). It applies the suppresses *and* re-verifies the fixes' upgraded manifests in the same pass.
     - **Fixes only, no suppress** → the remediator's combined re-scan gate (+ tests) is that single scan.
     - **A `reapply` whose only scan-input change is the threat model (no suppress/fix/upgrade)** → **re-triage, no rl-protect scan.** The manifests are unchanged, so rebuild the plan from the **existing cached scan report(s)** (`.rl-protect/reports/<eco>.report.json`) with `plan.py create --profile {saved profile}` — this re-imports the new threat model — then re-run **`rl-appsec-triager`** (it reads the new model via `plan.py modeling`, re-derives verdicts, and re-applies the profile's acceptance rules in its Step 6). A rebuild owns all findings, exactly like the suppress re-scan, but skips the scanner. Drive it through the same tracker (`rescan {batch} scanning "Re-triaging…"` → `done`).
     - **The scan-input action(s) all *failed* → no scan runs, but you still MUST settle the tracker.** If every scan-affecting action failed in Phase 1 (e.g. a `fix` with no resolving version, so nothing changed on disk), there is nothing to re-scan — but the tracker the bar opened on Execute is still waiting. Leaving it open hangs the bar on "Re-scanning…" forever. Settle it `failed` with the reason (`rescan {batch} failed "<why no scan ran>"`), or `done` if the failure means no change was needed. Then the bar completes with the per-action rows showing their `failed`/`done` states.

     Drive the tracker as you go and settle it at the end:

     ```bash
     RL_BRIDGE_QUEUE={queue} python {bridge.py} rescan {batch} scanning "Re-scanning (release,develop,transitive)…"
     RL_BRIDGE_QUEUE={queue} python {bridge.py} rescan {batch} done "re-scan complete"   # or: failed "<reason>"
     ```

  4. **Regenerate the report once** at the very end (after the re-scan, if any) → the refresh nudge pulses.

For a single (un-batched) action, do the work for its `action` below and resolve it on its own:

> **Accept and Suppress both write the scan profile — that's the durable source of truth.** The profile (`rl-profile.json`) is the project's standing policy: it survives re-scans, re-applies to every future assessment, and is the git-committable record of what's been decided. So Accept and Suppress each (1) write the profile through the bridge's `save_profile` (validator-gated — the same path `kind:profile` uses; do **not** claim success if it returns `(False, …)`), **and** (2) stamp the **current** plan so the report updates immediately with no re-scan. The profile is the law; the plan applies it now.

- **accept** — Record a risk acceptance, audit-trailed (author = the user, timestamp, reason). **Use `apply-action.py accept`** — it does **both** halves deterministically so you don't hand-build them: stamps the live plan (`accepted_risk` + the acceptance overlay, recomputed at render — no re-scan) **and** writes the validator-gated profile `acceptance` rule(s), **mapping each finding to its SAFE category for you** (the part that's easy to get wrong by hand). You supply only the identity + wording; it prints a JSON `summary` you can fold into the resolve note.
  ```bash
  # whole package (default), one finding (--cve), or a SAFE card (--category vulnerabilities|hardening|tampering|secrets|licenses)
  python {apply_action} accept --plan {plan} --purl {purl} --manifest {manifest} [--cve {id} | --category {cat} | --all] \
    --statement "<what risk is accepted>" --reason "<why>" --author {user}
  ```
  A **whole-package** accept (`--all`, the default — `kind:package`) **also accepts the package's governance (freshness) block if it has one**, so one Accept makes the package APPROVE; pass `--manifest {manifest}` so it can (it's in the action). `--cve`/`--category` accept findings only (governance is out of their scope). `--all` and `--category` touch **only the findings the report displays** — i.e. effective severity warning/fail, or a CVE; passing policy checks the scanner collected but the UI hides are left alone (we never accept on the user's behalf what they can't see). Likewise `downgrade --category` only disables **displayed** SQ/TH codes. For a **governance-only** action (`kind:governance` — the freshness callout's own Accept) use `--governance --manifest {manifest}`: it accepts just the block and writes a `governance` profile rule. The report renders an accepted block **ACCEPTED** (purple) and stops forcing REJECT. `{apply_action}` is from `plan.py locate`. (It drives `plan.py` + the shared validator — never the DB directly. By-hand fallback: `plan.py remediate … --status accepted_risk --acceptance {…}` per finding + `plan.py accept-governance` for the block + profile `acceptance` entries; the remediate-batch payload nests fields under a **`remediation`** object.)
- **suppress** (UI label **Downgrade**) — **Disable a policy** so the scanner stops flagging it. *Not* a risk acceptance and **not** a plan edit — disabling a policy changes what the **scanner** produces (including the inherent risk tier, baked at scan time), so it only takes effect on a **re-scan**. **Use `apply-action.py downgrade`** to write the scanner-native `overrides` into the profile (validator-gated):
  ```bash
  # SQ and TH codes (the scanner honors TH overrides); only CVE ids can't be overridden (accept those instead). --category resolves the package's SQ/TH codes in that bucket.
  python {apply_action} downgrade --plan {plan} (--code SQ… | --category {cat} --purl {purl}) \
    --blocker fail --reason "<why>" --author {user}
  ```
  It writes `overrides` keyed by rule-id (`{ "enabled": false, "blocker": "fail", "apply_to": ["any"], "audit": {…} }`) but **does not scan** — **you still run the re-scan to apply it (the re-scan workflow below)**. Don't "poke" the plan to fake the result — the scanner is the source of truth (there is no `plan.py override` verb).
- **triage** — Cross-reference the finding (OSV.dev, NVD, GitHub — fetched live) and run reachability, then record the verdict with `plan.py triage`. For anything non-trivial, spawn `rl-appsec-triager` scoped to this finding. (Only `cve`/`malware` findings offer triage.)
- **fix** — A fix clicked **from the report is pre-authorized** by that click — proceed straight to `rl-appsec-remediator` without a second confirmation; the re-scan gate + tests are the safety net, and re-prompting an already-committed plan is exactly what the user does not want. (Only when *you* initiate a fix outside a report click — e.g. from a plain CLI conversation — confirm first, since there was no click to authorize it.)
- **upgrade** (`kind: version`) — The version switcher's **Replace version** in the upgrade-review dialog: apply the user-picked `target` version through `rl-appsec-remediator` exactly like `fix`, but the target is explicit and the choice **is** the human acknowledgement — so the behavior diff is **recorded, not blocking** (per the remediator's "When the user picked the version" path; list every added indicator in the summary). If the action carries a **`note`**, it is the owner's acknowledgement statement typed in the dialog — record it as the acceptance (`plan.py remediate … --acceptance {note}`) so the diff-recorded upgrade keeps the same audit trail (author + timestamp + statement) as the app's dialog.
- **add-version** (`kind: version`) — The version switcher's "Add another version": scan one user-supplied version and append it to that package's dropdown. `purl` = the package; `target` = the version (e.g. `3.2.1`), or a **full purl** the user pasted — when it carries `?artifact=`, `--add` scans that exact wheel verbatim (for a version needing a different wheel than the installed one, e.g. an abi3 wheel); a bare version mirrors the current wheel's platform tag. Run `python {explore_versions} --add --plan {plan} --purl {purl} --version {target} --bridge-progress {id}` (the `--bridge-progress {id}` streams scan progress into the chat bubble — the scan takes ~1–2 min). It scans the **current,target purl pair directly** (no manifest), diffs against current, and appends a candidate — applying the installed version's decisions to it (same transfer as the explorer). If rl-protect **can't resolve** the version/artifact (or a full purl for a *different* package was pasted), the script exits non-zero with a clear message — `resolve` the action as **failed** with that message (do not regenerate). On success, **check the new candidate's `needs_triage`** (`python {plan.py} version-options --plan {plan} --purl {purl}` → the just-added candidate's `card.needs_triage`): if it's **non-empty** (an imported package's added version introduced genuinely-new CVEs — e.g. a downgrade), spawn `rl-appsec-triager` in **candidate-delta mode** (its Step 8) to evaluate just those and record via `plan.py triage-version`, so the added version is judged by the same rules as every other — **the same auto-triage the `--actionable` explore does** (don't leave it stuck at a raw scanner verdict). Empty (the common case — a newer version resolves findings, or a not-imported package) → skip. Then **regenerate the report** and `resolve` with a one-line summary (e.g. "added requests@2.32.0: -1 CVE"). The cap is 5 added versions. `{explore_versions}` is from `plan.py locate`.
- **remove-version** (`kind: version`) — **Bridge-direct; you normally will not see this in the queue.** The bridge runs `explore-versions.py --remove` + regenerates by itself (no scan), so the trash button works without a session. It only appears here as a fallback if some client enqueued it; if so, run `python {explore_versions} --remove --plan {plan} --purl {purl} --version {target}` (drops only user-`added` candidates), regenerate, and `resolve`.
- **run-stage** (`kind: general`) — The report header's kebab launches one pipeline step through its AI agent. `target` is the step id; map it and run against this project's plan at its recorded recipe (`analysis.recipe`), then **regenerate the report** and `resolve` (e.g. "triager complete"):
  - `assess` → re-run `rl-appsec-assessor` (re-scan + import).
  - `explore` → `python {explore_versions} --plan {plan} --bridge-progress {id}` (the whole project — deterministic, cached; no agent; `--bridge-progress` streams per-package scan progress to the chat). For when someone ran only the assessor + report and wants **every** package's version switcher populated (also fills `op_risk`/staleness for all).
  - `triage` → `rl-appsec-triager` over the **important** (priority 0/1) findings — its normal scope. **Then auto-explore the survivors** (see below).
  - `triage-all` → `rl-appsec-triager` over **every** untriaged finding, regardless of priority. **Then auto-explore the survivors** (see below).
  - `investigate` → `rl-appsec-investigator` over the malware (`threats`/`malware`) findings — behavioral analysis, hash matching, call-site tracing — which records `CONFIRMED_MALWARE` verdicts so a malware package can advance past **Triaged** (the triager never verdicts malware; without this the chip stalls forever). No auto-explore. Runs before `remediate`.
  - `remediate` → `rl-appsec-remediator` (only if the user wants fixes — a report-clicked run is pre-authorized).
  Post a `progress` line per phase (re-scan / triage / remediate run for minutes) so the user sees activity.

  **Cooperative stop (triage / triage-all / investigate / remediate only).** These steps run a **package-iterative** agent that honours a **Stop** button in the report's progress ribbon. The Stop click posts `/control {op:'stop-run'}`, which the bridge turns into a **stop-signal file beside the plan** (`$(dirname {plan_path})/stop-signal`); the agent checks it at each **package boundary** and halts cleanly after finishing the current package (never mid-package — so the plan is never left inconsistent). Your part of the lifecycle:
  1. **Clear any stale flag BEFORE spawning** the agent: `rm -f "$(dirname {plan_path})/stop-signal"` — so a leftover flag from an earlier run can't insta-stop this one.
  2. Spawn the agent. If the user clicks Stop, the agent finishes its current package, then returns early reporting how many packages it completed.
  3. **After the agent returns, delete the flag again** (`rm -f "$(dirname {plan_path})/stop-signal"`, whether it stopped early or completed), then continue to auto-explore + regenerate. When it stopped early, `resolve` with an honest note (e.g. *"stopped after 21/38 packages; 17 still untriaged — click Triage again to continue"*). The plan is consistent (each package is fully triaged or untouched), so a later run just picks up the remaining untriaged findings.

  **Auto-explore survivors after triage (prepare the remediator).** As soon as a `triage` / `triage-all` run finishes, run `python {explore_versions} --plan {plan} --actionable --bridge-progress {id}` **before** regenerating. `--actionable` scopes the (expensive) version_options exploration to the packages the triager left with an OPEN/exploitable CVE — usually a small handful, since triage clears most as not-reachable/accepted — so the remediator (and the report's version switchers) have scan-validated upgrade targets ready without you clicking "Find upgrade versions" per package, and without wasting scans on cleared packages. It's deterministic + cached; `op_risk` still covers every package. (If there are no survivors it does nothing and exits fast.) Then regenerate once and `resolve` (e.g. "triaged N; explored M survivor package(s)").

  **Auto-triage candidate-version deltas (only if any).** The explorer applies the installed version's decisions to every candidate so all versions are judged equally, but it can't transfer a verdict for a **genuinely-new CVE** a candidate introduces — those stay in each candidate card's `needs_triage`. After the `--actionable` explore, check `python {plan.py} version-options --plan {plan}`: if any `card.needs_triage` is non-empty, spawn `rl-appsec-triager` in **candidate-delta mode** (its Step 8) to evaluate them and record each with `plan.py triage-version` (reachability-only — no re-scan), so a candidate isn't stuck at a raw scanner verdict the user can't compare. Empty everywhere (the common case — not-imported packages clear package-wide) → skip. Do this before the final regenerate.
- **find-versions** (`kind: version`) — A package's per-version kebab "Find upgrade versions" (shown only when the explorer hasn't run for that package). `purl` = the package. Run `python {explore_versions} --package {purl} --plan {plan} --bridge-progress {id}` (explores just that one package — patch/minor/latest + op_risk, leaving other packages untouched; `--bridge-progress` streams scan progress to the chat), then **regenerate the report** and `resolve`. Lets the user populate one switcher at a time without scanning the whole project.
- **refetch** (`kind: package`) — The **"Fetch again"** item on the Repository SAFE card of a package whose scan came back **"unavailable, check later"** (e.g. a version published so recently the backend hasn't ingested it yet). `purl` = the package; `manifest` = its manifest id. Re-scan **just this one purl** (cache-bypassed) and merge it back — no project re-scan, no plan rebuild:
  1. Post a `progress` line (`Re-scanning {purl}…`). Scan the single purl to a fresh report: `rl-protect scan {purl} --save-report {tmp_dir}/refetch.report.json` (add the plan's connection/`--profile` as usual; a lone purl needs no manifest). rl-protect resolves the exact artifact from the purl.
  2. Merge it: `python {plan.py} refresh-package --plan {plan_path} --manifest {manifest} --purl {purl} --report {tmp_dir}/refetch.report.json`. It rebuilds just that package's row + findings from the fresh scan, **preserving any triage/accept we already recorded (keyed by finding id)**, and prints `{ok, available, recommendation, findings, decisions_carried}`.
  3. **Regenerate the report only when something changed** (`available: true`) — then `resolve done` with the fresh recommendation (e.g. *"re-fetched setuptools@83.0.0 — now APPROVE, 0 findings"*). If `available` is **false** (still not ingested) or the merge errored (`ok:false`, non-zero exit), **do not regenerate** — nothing changed, so a reload would just disappoint. `resolve done` with a message that includes the word **"unavailable"** (e.g. *"setuptools@83.0.0 is still unavailable — try again in a bit"*). The report polls the action and surfaces that note **inline as an amber toast**, and it only shows a reload nudge when the report file actually changed — so the user sees the truth without being sent to refresh for nothing.
- **reapply** (`kind: profile`) — The user saved the scan profile in the gear editor; the profile file is already written, but the **plan** doesn't reflect the new acceptance/overrides yet. A save does **not** scan or auto-queue — it **stages a "Reapply profile" task into the plan bar** (joining any other staged work), so it arrives as part of an Execute-plan `batch`; the saved profile path is in `note` (**if `note` is empty, fall back to `{project_dir}/.rl-protect/rl-profile.json`, then `{project_dir}/rl-profile.json`** — the same lookup order the assessor uses). The action also carries **`rescan`**/**`retriage`** flags — see the detection callout under *Batched plans → Group* above; **read them and honor them** (an assessment-toggle reapply sets `rescan` even though it stamps no findings). Sync the plan to the saved profile:
  1. For each enabled `configuration.policy.acceptance` rule → match it against the plan's findings (same conservative category/reachability rules the triager's Step 6 uses) and accept the matches via `plan.py remediate … --status accepted_risk --acceptance {…}` (or `remediate-batch`). Acceptance is *our* concept, so it applies **without** a re-scan. (Also drop plan acceptances whose profile rule was removed — see **revert** for the per-finding clears.)
  2. If the save changed `configuration.policy.overrides` (a disabled policy / blocker) **or `configuration.policy.assessments.<cat>.ignored` (a disabled assessment category)** — i.e. the action's **`rescan`** flag is set — that changes **scanner** output and needs a re-scan. In a batch this is the **single Phase-2 re-scan**, not a separate one, tracked by the `rescan:<batch>` record you opened in step 1 above — **you must settle it** (`done` after the re-scan, or `failed`/`done` if it turns out no scan is needed), never resolve the reapply row and leave the tracker open. If only acceptance changed (`rescan` unset), no re-scan. **Reality check before skipping:** a category set `ignored:true` whose findings are still in the plan (`plan.py findings`) *has not been applied yet* and needs the re-scan regardless of what acceptance/modeling look like — do not conclude "no scan-input change" just because acceptance is empty and the threat model matches.
  3. If the save changed the **threat model** (compare the profile's `configuration.policy.modeling` against `plan.py modeling`), re-run triage so the new judgment context takes effect — the threat model shapes stored verdicts, not a render overlay. **No scanner:** rebuild from the cached scan report(s) with `plan.py create --profile {saved profile}` (re-imports the new model) then `rl-appsec-triager`, as described in the Phase-2 "reapply whose only scan-input change is the threat model" bullet. When the same batch already re-scans (an overrides change or a suppress/fix/upgrade), that re-scan re-triages with the new model anyway — do **not** re-triage twice.
  4. Regenerate the report **once per batch** and `resolve` the action with a one-line summary of what synced.
- **revert** — Undo a change **we** previously applied to this finding. The action carries a `reverted` hint (`accept` / `governance` / `suppress`); confirm it against the finding's current state and apply the **inverse** — the exact mirror of the original action:
  - **`accept`** (a `cve`/`policy`/`safe` finding with `remediation.status == accepted_risk`) → clear the plan stamp: `plan.py revert --plan {plan} --manifest {manifest} --purl {purl} --cve {target}`. Acceptance is *our* render overlay, so **no re-scan**. Also drop the matching `acceptance` statement from the profile via `save_profile` **only** when no other finding still relies on it (statements can be shared — when in doubt, leave the profile rule and just clear the plan stamp).
  - **`governance`** (a package-level block with an `acceptance`) → `plan.py accept-governance --plan {plan} --manifest {manifest} --purl {purl} --clear`. Render overlay, **no re-scan**; the block returns to REJECT.
  - **`suppress`** (a `policy`/`safe` card whose ⓘ is a disabled-policy override) → remove that code's entry from the profile's `overrides` via `save_profile` (for a `safe` card, every code in the category), then **re-scan** (the re-scan workflow) — restoring a policy is a scanner change, the exact inverse of Downgrade. In a batch it rides the single Phase 2 re-scan.
- **ask** — A question (in `note`) about the target, asked from the report's conversation panel. **Post a `progress` line before each lookup/step** (see *Keep the conversation alive* above) so the user sees steady activity, not a lone spinner — start one with your first lookup command:

  ```bash
  RL_BRIDGE_QUEUE={queue} python {bridge.py} progress {id} "Checking the plan and your project source…"
  ```

  Then answer it **back into the browser** so the reply renders in that panel:

  ```bash
  RL_BRIDGE_QUEUE={queue} python {bridge.py} answer {id} "<your markdown answer>"
  ```

  **If `kind: codefix`, this is a fix-iteration turn, not a generic question** — regenerate the hardened snippet incorporating the feedback (in `note`) and prior context; see the **codefix** section's *Iterating on the fix*.

  `answer` also resolves the action — do **not** also `resolve` it. If the action has a `thread`, it may be a follow-up; read the prior turns first so your reply stays in context:

  ```bash
  RL_BRIDGE_QUEUE={queue} python {bridge.py} thread {thread}
  ```

  **Q&A vs. action requests — two typed verbs, so the wire format is never guessed.** The report renders each reply by its server-set `answer_format` tag (`prose` | `actions` | `profile`); pick the verb that matches your intent and the bridge tags + validates it for you — do **not** hand-write a JSON envelope onto `answer`.
  - **A question** → `bridge.py answer {id} "<markdown>"` (tagged `prose`; rendered as Markdown, never parsed for actions).
  - **A request to act** on a finding/package — **accept, triage, fix, or upgrade** — do **not** mutate the plan directly; reply with **`answer-actions`**, which stages the actions into the plan bar for the user to review and **Execute** (one batch → one re-scan), exactly like the buttons. Resolve the package to its canonical `purl` + `manifest_id` from `plan.py export`; for an upgrade use the version the user named, else the smallest resolving candidate from `version_options`. Pass a markdown `summary` and the actions as a JSON array (a file, or inline):

  ```bash
  cat > {tmp_dir}/stage.json << 'EOF'
  [{"action":"upgrade","kind":"version","purl":"pkg:pypi/requests@2.34.2","manifest":"<manifest_id>","target":"2.32.4"}]
  EOF
  RL_BRIDGE_QUEUE={queue} python {bridge.py} answer-actions {id} "Staged: upgrade requests -> 2.32.4 - review & Execute." {tmp_dir}/stage.json
  ```

  `action` ∈ `accept` | `triage` | `fix` (use `"kind":"package"`, no `target`) or `upgrade` (`"kind":"version"`, `"target":"<version>"`); each entry needs a `purl` or `target`. The bridge **validates the array** and refuses (non-zero, nothing written) if an action isn't stageable or lacks a purl/target — so a malformed payload can't reach the UI; fix it and retry. The report stages each into the plan bar, opens it, and renders your `summary`; **nothing runs until the user clicks Execute**. If the request is ambiguous, spans many packages, or you can't validate it (unknown package, no resolving version), fall back to **`answer` (prose)** asking to clarify and stage nothing. (Profile edits use `edit-profile.py --answer`, which tags `profile` — see the `kind: profile` section.)

  For a plain question, do not modify the plan. When your answer names a package (especially for a general question that spans several), **link it so the user can jump to its card**: write `[<short name>](rl-pkg:<purl>)` — use the canonical purl without the `?artifact=…` qualifier (e.g. `[mysqlclient](rl-pkg:pkg:pypi/mysqlclient@2.2.8)`). The report turns these into in-page links that scroll to and highlight the package card.

  **`kind: profile` is special — apply it, don't prose.** The question comes from the scan-profile editor's **Ask an AI** assistant; the user wants you to *configure the scan profile* — they expect the change to land and the editor to reload. **Use `edit-profile.py`** (from `plan.py locate`, key `edit_profile`) — it does the whole thing deterministically: pulls the editor's live draft from the action, applies the edit, re-validates with the shared validator, writes the canonical file, **and** answers the action so the editor reloads. Do **not** hand-roll a `bridge`-importing Python snippet.
  1. **Map the natural-language request to an op.** That mapping is the only judgement call — everything after is mechanical. `edit-profile.py` verbs (all take `--from-action {id}` to build on the draft and `--answer {id}` to reply):
     - `set --set PATH=VALUE` (repeatable, also `--unset PATH` / `--append PATH=VALUE` / `--remove-item PATH=VALUE`) — any scalar/object/list. Paths may start at a policy key (`governance.community.min_version_age`, `assessments.malware.ignored`) or be fully qualified; values are parsed as JSON (`true`/`30`/`"x"`) else a string.
     - `accept --category CAT --statement S --reason R [--disabled]` / `drop-acceptance --category CAT [--match SUBSTR]` — acceptance rules (audit block built for you).
     - `override --code SQ#####/TH##### [--blocker fail|pass] --reason R [--enabled]` / `drop-override --code SQ#####/TH#####` — scanner policy overrides (SQ or TH; not CVE).
     - `govern-add --list allow|block --pattern PURL [--comment C]` / `govern-remove --list allow|block --pattern PURL` — governance rules.
     - Pass `--author {user}` for the audited verbs (accept/override/govern).
  2. **Run it** — one call applies, validates, writes, and answers:

     ```bash
     RL_BRIDGE_QUEUE={queue} python {edit_profile} set --from-action {id} --answer {id} \
       --set governance.community.min_version_age=30
     ```

     It prints `{"summary", "applied", ...}` and (with `--answer`) sends the same `{summary, applied}` to the editor. On a validation failure it exits non-zero and answers `applied:false` with the reason — **do not claim success**; nothing is written when it refuses. When `applied` is true the editor **re-fetches and reloads** — the user does **not** Save. For a plain *question* about the profile (no change requested), skip the script and answer with prose (or `applied:false`).

- **codefix** (`kind: codefix`) — From the reachability evidence modal's **"Fix with AI"** action on a call site. Rewrite/**harden the user's own vulnerable code** at that site. `target` = the CVE/finding id, `note` = the call site `file:line`, `label` = the finding description, `purl` = the affected package. The action carries a **`thread`** — the report persists your answer and seeds it as the first turn of an iterate chat, so the user can refine it (see *Iterating* below). Steps:
  1. Read the source around `file:line` (a dozen lines of context) with the Read tool, so you rewrite the *actual* code, not a guess.
  2. Understand the weakness from the CVE id + description + package, and produce a hardened rewrite. **Stay tightly scoped to the code being asked about** — the specific call and the few lines it depends on (e.g. `yaml.load(x, Loader=yaml.Loader)` → `yaml.safe_load(x)`; add input validation / an allowlist for an SSRF sink; parameterise a query). Do **not** refactor unrelated code, rename things, or restructure the file. Minimal, idiomatic, aligned to the shown lines.
  3. **Be honest about the limits of a snippet.** The Fixed panel shows *only* your snippet — it is not applied and cannot express file-wide edits. If the correct fix needs anything beyond the shown lines — **adding an import** (e.g. `import ipaddress`), an **import that is now unused** and should be removed elsewhere, a new helper/config, or edits at other call sites — **say so in the explanation**; do not pretend the snippet is complete, and never imply you removed/added imports you can't show.
  4. Answer with `bridge.py answer {id} "<markdown>"`. **Two shapes, and the shape signals whether there's a fix:**
     - **A real code fix** → a short explanation (Markdown), then **exactly one fenced code block containing ONLY the fixed snippet**. The report renders the prose as the note and the block into the Fixed panel, with the **Original/Fixed** pill + **Copy fixed code**.
     - **No source-level fix** (e.g. a CA-bundle/dependency-trust CVE, or the code is already correct) → **prose only, NO fenced code block.** Say plainly there's no snippet fix and point to the real remediation (e.g. a dependency upgrade). With no code block the report shows it as an **advisory note** — it does **not** show a Fixed pill or "Copy fixed code" (there's nothing to switch to or copy). Do **not** wrap upgrade commands in a code fence just to have one; that would fake a "fix". The explanation is Markdown (bold/inline code/lists render).
  5. **Link the dependencies you name to their card in THIS report** so the user can click and land on it. Use an `rl-pkg:` Markdown link with the package's **canonical purl (no `?artifact=…` qualifier)** from `plan.py export`: `[certifi](rl-pkg:pkg:pypi/certifi@2024.7.4)`. The report scrolls to and flashes that package's card (and closes the evidence modal first). Link the *first, most relevant* mention (the fix target), not every occurrence. If the package genuinely isn't a card in this report, fall back to its registry page (`[name](https://pypi.org/project/<name>/)`, opens in a new tab).

  ```bash
  RL_BRIDGE_QUEUE={queue} python {bridge.py} progress {id} "Reading config.py and hardening the yaml.load call…"
  RL_BRIDGE_QUEUE={queue} python {bridge.py} answer {id} "Use safe_load so untrusted YAML can't construct arbitrary objects.\n\n\`\`\`python\nraw = open(config_file, encoding=\"utf-8\").read()\ncfg = yaml.safe_load(raw)\n\`\`\`"
  ```

  **Copy-only — this is a suggestion, not a change.** Do **not** edit any file, run a scan, touch the plan, or regenerate the report. `answer` resolves the action (don't also `resolve`). The user reviews it via the Original/Fixed toggle and copies it themselves. (This is distinct from `fix`, which upgrades a dependency version behind a re-scan gate — `codefix` never touches dependencies or files.)

  **Iterating on the fix (feedback).** If the user isn't happy with a fix, the evidence card's kebab offers **Regenerate with AI**, which closes the evidence modal and opens a chat thread seeded with your fix. Their feedback arrives as an **`ask` with `kind: codefix`** on the **same `thread`** (`target` = the CVE, `purl` = the package) — but here **`note` is the user's feedback text, not the call site**. Recover the call site (and your prior fix) from the thread's first turn: `bridge.py thread {thread}` — its first message's `note` is the `file:line`, and its `answer` is the fix you last gave. Read the source there again, apply the feedback, and answer with `bridge.py answer {id}` using the **same two shapes** (prose + optional single fenced snippet; still copy-only). Your reply renders in the chat **and** repaints the evidence card's Original/Fixed view in place. Keep the same tight scope and honesty rules as the first pass.

After handling, resolve and (for state-changing actions — not `ask`/`codefix`) regenerate the report so the user sees the update — **once per batch** if the actions were batched:

```bash
RL_BRIDGE_QUEUE={queue} python {bridge.py} resolve {id} done "<summary — what you did + result, 1-3 sentences>"
python {make-report.py} --plan {plan_path} --output {report_path} --no-error-code
```

If an action fails, resolve it `failed` with the reason rather than leaving it stuck pending. When the queue is empty, do nothing — the Monitor will notify you again on the next new action.

### The re-scan workflow (Suppress, reverting a Suppress, and override-changing profile saves)

Disabling a policy can only be applied by the **scanner**, so don't patch the plan — **re-derive it from the manifest + profile by re-running the whole audit**. This is consistent by construction (the disabled policy simply stops appearing; everything else is recomputed):

1. **Read the recipe** the original scan used — `plan.py export --plan {plan}` → `analysis.recipe` = `{check_deps, transitive_depth, target?}` (and `analysis.report.manifests` for the manifest files). When `target` is present, get its scan flags with `plan.py target-flags --plan {plan}` and pass them to **every** scan in the rebuild, so the re-import resolves the same PyPI artifacts the plan was built from. Don't re-derive a target — a mismatched one silently swaps which wheel each finding describes.
2. **Re-run the audit at that recipe** with the **scan-safe** profile (strip **both** `acceptance` and `modeling` for the scan — the rl-protect scanner rejects either policy key, even when empty; keep `overrides` and pass the full profile to `create` — the usual split): `rl-appsec-assessor` (scan + `create --check-deps {check_deps} [--transitive-depth N]`) → `rl-appsec-triager` (re-derives triage **and** re-applies the profile's acceptance rules) → `rl-appsec-investigator` if malware. Start the plan fresh (the rebuild owns all findings). A `--reset` create **carries the recipe's target across** when the assessor doesn't re-supply one, so a rebuild can never silently drop it.
3. **Track it — this is long.** Post a `progress` line at each phase so the plan-bar row shows live activity rather than a silent spinner, e.g. `… progress {id} "Re-scanning (release,develop,transitive)…"`, then `"Rebuilding plan…"`, `"Triaging N CVEs…"`. Post one before each multi-minute agent so the row never looks dead. **Batch:** fold all of one Execute's suppresses into a **single** re-audit.
4. **Finish:** regenerate the report (bumps the version → the **refresh nudge** pulses for the user to click) and `resolve` the suppress action(s) `done`.
