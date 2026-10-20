---
name: brown-b3-owa-cpc
description: Navigate the Brown Cloud PC through ssh cpc and verify B3 OWA in actual Word, Excel and Outlook hosts. Use for CPC, Office sideload, local startup, Windows supervisor cleanup, add-in logs, or migration acceptance. Separates read-only checks from approved indexing/email writes and reports blocked cases honestly.
---

# Brown B3 OWA CPC acceptance

## Qualification and boundaries

Status: draft procedure with a live-verified read-only preflight. Prior sessions proved SSH and some Windows UI Automation interactions, not a complete autonomous Office acceptance suite. Read [provenance](references/provenance.md) before first use. Never claim a full run passed from connectivity or synthetic tests.

Use for initiative `b3-owa-layout-and-legacy-delivery-modernization`, especially M1 and M5. Do not create b3-owa/docs. Preserve user changes and Office windows. This skill is not permission to deploy, edit ADO, install certificates, sideload, index documents, send mail, change registry, log in, or stop arbitrary processes. Obtain task-scoped approval for those mutations. Once an approved case is unambiguous, execute without asking at every step.

Never reset passwords, bypass MFA, read token stores, expose connection strings or dump customer mail/document bodies. Use approved nonproduction fixtures. Stop on unavailable permissions, locked desktop, unknown target or an action outside approved scope. Production requires explicit approval.

## 1. Connect and identify

Use existing SSH alias, never guess another identity or disable host-key checks:

```bash
ssh -o BatchMode=yes -o ConnectTimeout=10 cpc hostname
python3 "$HOME/.agents/skills/brown-b3-owa-cpc/scripts/remote.py" < "$HOME/.agents/skills/brown-b3-owa-cpc/scripts/preflight.ps1"
```

Expected approved host at capture: `346-CPC-QJXVZ`. Preflight returns JSON with candidate repos, HEAD, dirty count, tool availability, listening ports and desktop window count. Require zero command exit, parseable JSON, expected host and required tools. Missing repo is BLOCKED, not permission to clone over existing files. Resolve approved checkout from returned candidates. Historical candidate is `%USERPROFILE%\dev\b3owa-sideload-test`; do not assume it is current or clean.

For nontrivial PowerShell use the encoded helper with stdin rather than nested cmd/bash quoting. The helper propagates SSH exit codes and times out after 90 seconds. It is a transport, not a safety sandbox. Only send reviewed task-scoped scripts. Do not put secrets in them. Long-running servers need an owned detached process and separate readiness polling, not this bounded command. A timeout may leave a remote process: inspect ownership before retry.

## 2. Prove revision and ownership

Read `git status --porcelain`, `git rev-parse HEAD` and the approved candidate revision on CPC. Record full SHA. A different SHA is BLOCKED. Never reset, clean, stash or pull over dirty work. Use an explicitly approved separate test checkout if needed. Do not reproduce old sessions' ad-hoc file transfers without recording a patch hash.

Record existing listeners/PIDs and Office sessions before startup. Do not dump window titles broadly: they can contain customer subjects. Select only the approved Office test window and retain minimal structural evidence.

Paths before migration: `frontend/{Word,Excel,Outlook}IndexToPIPS2`, shared config `frontend/config`. After migration: root `OfficeIndexToPIPS.{Word,Excel,Outlook}`, shared config `OfficeIndexToPIPS.Shared/config`. Detect using files at the candidate SHA; do not assume migration state.

## 3. Start and validate local services

Inspect `OfficeIndexToPIPS.Api/Properties/launchSettings.json`, package scripts and `scripts/dev/local-start.cjs` at the candidate SHA. Select the existing local supervisor profile if available and approved. Do not invent a profile or run all profiles. Install dependencies with `npm ci` only in approved checkout. Run existing certificate workflow only if certificate installation/trust is approved; never use TLS bypass as acceptance evidence.

Expected ports: API HTTPS 7266 (HTTP 5135 when configured), Excel 3001, Outlook 3002, Word 3003. Default webpack 3000 is a known trap. Check actual listeners and owning PIDs.

Run from approved repository root after services start:

```powershell
node scripts/dev/local-start.cjs --check
if ($LASTEXITCODE -ne 0) { throw 'Local readiness failed' }
```

PASS: all four trusted endpoints become ready within configured deadline. Also verify API `/health`, `/api/health`, `/ready` and `/openapi/v1.json` according to candidate route contract. Readiness failure is a failure, not a reason to disable dependency checks. Existing Azure credentials may expire: report authentication blocker, never silently switch identity or initiate interactive login.

Sideload is a separate approved action. Existing `local-start.cjs` without `--check` registers LOCAL add-ins and stays alive. Run it as an owned process, preserve its PID, and use LOCAL entries rather than enterprise DEV entries. Never alter installed hosted manifest IDs or URLs.

## 4. Navigate actual Office UI

Use PowerShell `UIAutomationClient` and `UIAutomationTypes` through the helper. `AutomationElement.RootElement` worked in prior sessions. Find the exact owned test window by process ID and semantic identity. Outlook new client was `olk`; discover current process rather than hardcode a historical PID. Word and Excel use their own processes.

For each action: locate a unique control using Name/AutomationId/ControlType and its parent scope; inspect `IsEnabled` and `GetSupportedPatterns`; use `TryGetCurrentPattern` for the required pattern; invoke; poll expected state with a deadline. Reacquire stale AutomationElements. If zero or multiple matches, or unsupported pattern, stop that case as BLOCKED. Do not click arbitrary coordinates or use unscoped SendKeys. Prior blanket WindowPattern and ComboBox Collapse attempts failed.

Only use approved fixture content. Do not enumerate message bodies or select arbitrary user documents. If the webview cannot expose controls through UIA, use an already approved automation interface after loading its browser policy. Do not enable debugging or attach a new remote debugging port without approval.

## 5. Acceptance matrix

Run separately for Word, Excel and Outlook. Record PASS/FAIL/BLOCKED/NOT_RUN per row, never a single aggregate 'works'.

| Case | Action | Required observation |
| --- | --- | --- |
| Bootstrap | Open LOCAL entry in host | Correct local environment, identity context and location readiness; no infinite busy state |
| Retry | Use approved failure fixture, then retry | Same attempted identity, successful recovery; otherwise case remains untested |
| Search | Approved query via Enter and button | Equivalent readiness, visible pending state, no duplicate dispatch in sanitized logs |
| Empty/error | Approved empty/failure fixture | Nonmodal feedback, query retained, retry enabled |
| Stale context | Delay test response with approved mechanism, switch location | Old success/error cannot replace current selection; no production network changes |
| Metadata | Change policy/document context | Index disabled until current metadata resolves |
| Accessibility | Navigate labels/keyboard; open and dismiss notes | Accessible names, Escape behavior and focus return observed |
| Narrow pane | Resize owned test pane, restore afterwards | Required fields/actions usable without clipping |
| Outlook variants | Approved read, compose and shared-mailbox fixtures | Each supported variant has separate evidence; no send |
| Logs | Trigger safe actions, inspect allowlisted diagnostic events | Expected events correlate to action/time; no tokens, mail bodies or customer payloads |
| Index/send | Only with explicit nonprod fixture/recipient/write approval | Actual target result and approved cleanup; otherwise BLOCKED |
| Cleanup | Stop owned test supervisor | Owned descendant PIDs and ports exit, unrelated processes survive |

Do not inject synthetic responses and call that real host/back-end acceptance. Label simulated failure coverage separately. A browser bridge failure on Linux is not proof CPC UIA is unavailable.

## 6. Evidence and completion

Copy [checkpoint.json](references/checkpoint.json) into private evidence storage for each case. Leave NOT_RUN until executed. For every case record: case ID, host/mode, environment, candidate SHA, timestamp, exact action, expected/actual, result, sanitized log/screenshot path, owned process IDs and cleanup result. Store private evidence in ignored scratch, outside repo docs and skill source. Screenshots may contain private content; capture only approved test surfaces and redact before sharing.

Report command failure and CLIXML error content as failure even if an outer command incorrectly returns zero. Validate native `$LASTEXITCODE` after git/node/dotnet commands. Prefer structured JSON output.

A full acceptance claim requires all mandatory rows across all requested hosts and authorized write cases. Lack of sign-in, fixture permission, UIA support or a reachable service is BLOCKED, not PASS. Resume the first incomplete case after the blocker is resolved. Never kill all node/dotnet/Office processes to clean up.
