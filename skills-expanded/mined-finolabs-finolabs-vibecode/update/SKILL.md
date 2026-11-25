---
name: update
description: Update finolabs-vibecode with the user's permission and walk them through what the new version asks of them, show what is new without changing anything, target the latest or a chosen released version, pin or unpin a version, skip a release, or stop update notices. Use when the user requests a plugin update, asks whether a newer release is available or what a new version changed, wants a specific or older version, chooses skip this version, or says never ask again.
argument-hint: "[status | whats-new | <version> | pin <version> | unpin | skip <version> | never]"
disable-model-invocation: true
---

# Update the plugin

Run only at the user's request. A session-start notice tells the agent to let the user know a newer version is available, or that the installed version has upgrade notes, and that they can type `/update` (on Codex `$update`). Only the user can invoke this skill; a notice is not permission to update. An earlier yes to checking or opening this skill is not a yes to installing an update or to any setup step.

The helper and its shared core are in this skill's own `scripts/` folder. Resolve `<update_check.py>` there. It uses `fnl_metrics.state_dir()` for all state, independently of metrics consent. It reads the plugin's own manifest when installed with the plugin; a standalone skill has no manifest, so its installed version is unknown. Use the host's installed-plugin listing to establish that version rather than guessing it. Command output and states are in `references/onboarding.md`; host commands and privacy are in `references/hosts.md`.

**Arguments:** $ARGUMENTS

## Show the facts, then ask

Questions below ask through the host's native question tool when the session has one. Ask in text when the session has no such tool, the tool is refused or fails, nobody can answer (a delegated or headless run records the open decision and never assumes or invents an answer), or the decision is free text. The enforcer is agent judgment, so this is advisory.

**Advisory (agent judgment):** Talk to the user in the language they are using, including questions and option labels; keep command names, flags, file paths, skill names and other technical names unchanged. Script output stays English; report it to the user in their language (advisory, agent judgment).

1. Run `python3 -I <update_check.py> status`. This reads local state only. Show `installed`, `available` (the cached latest stable release), whether it is `newer`, whether the cache is `stale`, any `pinned` version, and any skipped versions or never-ask choice. A null value is unknown, not evidence that the plugin is current. Empty output means the check is off or a read failed: report that limitation. Do not fetch a release manually or claim a stale cache is current. The startup hook schedules a background refresh after 24 hours; the result is read on a later startup.
   For an update, first find the target: `target` alone for the latest stable release (the default), or for `/update <version>` the evidence form in `references/onboarding.md`. A refusal ends the update; report its reason. For a rollback, show the `lost:` lines first.
2. If the user only asked for status, finish with those facts. For an update, report the host's native command for the installed identifier, its status from `references/hosts.md` and any restart or trust step. Ask for a clear **yes to running that command now**, through the host's native question tool when the session has one. Offer neutral Yes and No choices with none preselected or marked recommended; a default, a timeout or an auto-selected option never counts as the yes. Wait for the answer. A skip, silence or ambiguous answer grants no permission.
3. After that yes, run only a verified native update command for the matching host and installed identifier. Report the actual result. An error is an error, not a successful update. Verify the resulting installed version with the host's listing; a still-running session's manifest can describe the old loaded copy.
4. Go straight on to the checklist (step 5); the user is never sent to a second command. First re-resolve `<update_check.py>` inside the newly installed copy that the host listing reports, and run its `status`: its `installed` must equal the verified version. If it does not (the host keeps the old copy loaded until a restart), stop here, say a restart is needed and that `/update whats-new` or `/update` continues afterwards, and do not run `onboard seen`.

## The checklist

5. Run `python3 -I <update_check.py> whats-new` and show it. For each `[open]` or `[unknown]` item in the order given, offer its setup step: invoke `setup` with that `/setup add <feature>`, which asks its own consent, preview and neutral yes exactly as it always does. Nothing is set up without the user's own answer there. When the user chooses to skip an item, run `onboard skip <id>`. Items without a setup step are told, not offered.
6. When the user has gone through that installation's list, run `onboard seen <installed version>` with the same re-resolved helper and run `whats-new` again to verify. This clears the session-start line.

`/update whats-new` runs step 5's command only: it shows the checklist and changes nothing, installs nothing, offers no setup step and never calls `onboard`.

## Pin, skip a version or stop asking

When the user explicitly chooses to **hold a version**, run `python3 -I <update_check.py> pin <version>`; `unpin` removes it. While a pin is set the newer-release notice is silenced and `status` shows `pinned`; the pin does not change the installed plugin.

When the user explicitly chooses **skip this version**, use the validated available version from status and run `skip <version>`. When the user explicitly chooses **never ask**, run `never`. These commands are local and silent; read `status` again to verify the choice before reporting success. Skip affects that release only; never-ask suppresses the release notices, but the background check remains on.

Never put response text into a shell command: versions must match `v?X.Y.Z` with decimal digits and dots only, and item ids must be ones `whats-new` printed.

## Privacy and off switch

The automatic check makes one fixed HTTPS GET to the GitHub `/releases/latest` endpoint at most once a day and sends nothing about the user; nothing in this skill adds a network call. `FNL_UPDATE_CHECK=off` stops the check, the notices and these helper commands. Details are in `references/hosts.md` and PRIVACY.md.
