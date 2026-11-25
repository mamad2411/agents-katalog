---
name: stelz-browser
description: Do browser tasks in persistent Stelz profiles through the Stelz MCP tools (`profile_*` and `tab_*`), with exclusive control, verified readiness, and human authentication. Also use it to install Stelz when a user sends a link to this skill.
---

# Stelz browser

Stelz runs persistent browser profiles. You control them through the tools of one `stelz mcp` connection.
[Shared MCP tools](https://github.com/souljorje/stelz/blob/main/docs/mcp.md) is the tool contract, including the control-handle rules.
Requires Stelz 0.6.0 or later. Check with `stelz --version`.

## Install

When a user sends a link to this file and asks you to install it:

1. Save this file as `stelz-browser/SKILL.md` in your client's skill folder. See [Connect your agent](https://github.com/souljorje/stelz/blob/main/docs/clients.md).
2. If `stelz` is missing or older than 0.6.0, or the Stelz MCP tools are missing, follow [Agent setup](https://github.com/souljorje/stelz/blob/main/docs/bootstrap.md).

Run `stelz setup` only in a terminal. MCP tools do not download prerequisites.

## Do a browser task

1. Call `profile_list({})`. Select the profile ID that the task needs.
2. If that profile is missing, call `profile_create({profileId})`.
3. If its browser is stopped, call `profile_start({profileId})`.
4. Check readiness in the start result or in `profile_status({profileId})`:
   - `phase` is `"ready"`.
   - If `verificationRequired` is true, `verificationStatus` is `"verified"` and `exitIp` agrees with the intended route.

   If a check fails, do not acquire. Report `location` to the user and go to [Recover](#recover).
5. Call `profile_acquire({profileId})`. Keep the returned `controlHandle` with its profile ID. Never write it in reports, configuration, or handoff notes.
   Send both fields in each later call for that profile.
6. Call `tab_list` to find the startup page. Navigate that tab.
7. Work on the page with these rules:
   1. Read a full `tab_snapshot` on a new tab, after a navigation, or after resume.
   2. Click, type, select, and press return a diff, or the full page with `baseline: true`. Read it to check the result. Do not call `tab_snapshot` after an action. If the result says `The action completed`, the read of the page failed. Read `tab_snapshot`. Do not repeat the action.
   3. Target elements by role and name (`target`). Use a ref only if the last result showed it.
   4. If an expected change is not in the diff yet, use `tab_wait`. Do not poll with snapshots.
   5. Use `scope` or `contains` on long pages.
   6. Ask for a screenshot only when the layout matters.

   See [Targets](https://github.com/souljorje/stelz/blob/main/docs/mcp.md#targets), [Refs](https://github.com/souljorje/stelz/blob/main/docs/mcp.md#refs), [Observe](https://github.com/souljorje/stelz/blob/main/docs/mcp.md#observe), [Wait](https://github.com/souljorje/stelz/blob/main/docs/mcp.md#wait), and [Snapshots](https://github.com/souljorje/stelz/blob/main/docs/mcp.md#snapshots).
8. When you finish, or before another agent takes over, call `profile_release({profileId, controlHandle})`. Leave the browser open.

## Rules

- Never repeat an action that may have reached the page or that stopped before it finished. Read a fresh snapshot first.
- If another controller holds the profile, do not start another browser or create another profile. Ask the operator to release it.
- For changes that the tools cannot make, ask the operator to use the CLI or UI.
- `tab_evaluate` and `tab_init_script` work only on a profile that the operator allowed, and only when the connection lists them. If a call says that scripts are off, ask the operator to allow scripts in the CLI or UI. Never try to change this setting. After a `tab_evaluate` timeout, read a snapshot. Do not run the script again.
- Before you type long text, read [Typing](https://github.com/souljorje/stelz/blob/main/docs/configuration/typing.md) to select a `tab_type` mode.
- Tell the operator about location warnings in `location.evidence`. Never claim a physical location from status, and never bypass a location blocker. See [Managed location data](https://github.com/souljorje/stelz/blob/main/docs/configuration/network.md#managed-location-data).
- If status shows `restartToUpdate: true`, tell the user. Restart only when the user asks. Release before the restart, and acquire again after it. See [Restart to update](https://github.com/souljorje/stelz/blob/main/docs/troubleshooting/setup.md#restart-to-update).

## Human authentication

1. When a page needs a person, for example to sign in, call `profile_pause({profileId, controlHandle})`.
2. Tell the operator what to do in that browser window. [Find a profile's windows](https://github.com/souljorje/stelz/blob/main/docs/ui.md#find-a-profiles-windows) tells them how to find it.
3. Wait for the operator. Then call `profile_resume({profileId, controlHandle})`.
4. After the resume, read a full `tab_snapshot` before the next action.

Do not try to bypass an authentication challenge.

## Recover

After an error, call `profile_status({profileId})` before another browser action. Then use the procedure for the problem:

- [IP verification failed](https://github.com/souljorje/stelz/blob/main/docs/troubleshooting/network.md#ip-verification-failed). After the operator repairs the route, call `profile_recheck({profileId, controlHandle})`.
- [Missing or stale control handle](https://github.com/souljorje/stelz/blob/main/docs/troubleshooting/control.md#missing-or-stale-control-handle).
- [Browser action or IP check timed out](https://github.com/souljorje/stelz/blob/main/docs/troubleshooting/lifetime-and-state.md#browser-action-or-ip-check-timed-out).
- Other problems: [Troubleshooting](https://github.com/souljorje/stelz/blob/main/docs/troubleshooting/index.md).

Diagnostics, stop, and recovery are operator actions. Never send signals to processes or work around uncertain process ownership.
