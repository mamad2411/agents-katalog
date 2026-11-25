---
name: native-verification
description: Verify Mac app behavior on a synthetic profile, beginning with the U11a cockpit observation and budget scenario. Use for launch, preflight, evidence collection or review of a native verification attempt.
---

# Native verification (draft)

Run from the checkout root. This skill is draft until a verification run at its exact head. [Feature map](feature-map.md) is owned by integration; unknown routes remain unbound. Public inputs are neutral placeholders only; approved proprietary art is supplied locally.

## 1. Launch

Use `bin/check_inputs.py <root> <entry>` to catch missing relative modules before an attempt; this is a local link check, not a release-asset manifest gate. Use `bin/launch.py --config <run.json>` to validate an existing run contract. `--execute` starts only the explicit test executable with a fresh synthetic HOME/TMPDIR after a matching release and fresh lease. The script creates no scheduling authority. The coordinator grants the epoch and GO; M1 posts window start/end and runs `bin/guardian.py` as the independent watchdog. Owner takeover stops it. The absolute run deadline includes waiting, launch, preflight and cleanup, at most 1200 seconds. Remaining time must cover declared phases plus cleanup, with no arbitrary start cutoff. Non-GUI build/tests need no GUI lease; avoid heavy jobs during announced measurement windows.

M1 uses this exact sequence (details and coordinator withdrawal are in
[`bin/BOOKINGS.md`](bin/BOOKINGS.md)). Configure `MODELPLAN_BOOKING_LEDGER` with
the shared ledger path supplied by the coordinator; there is no default. Use the
agreed synthetic file paths and run/epoch values below. `APPROVAL_URL` must be the
https URL of the coordinator's OK comment. `release.py` checks only that it is an https URL;
before issuing the receipt, M1 itself must open the comment and confirm it is the coordinator's OK
for this run. Copy the returned booking ID into `BOOKING_ID` and the run config.

```sh
set -e  # any failed step before launch stops the sequence (no release, no launch)
python3 desktop/native/verification/bin/book.py request \
  --lane M1 --unit U11a --scenario cold --minutes 20
python3 desktop/native/verification/bin/book.py start \
  --id "$BOOKING_ID" --lane M1 --run-id "$RUN_ID" --epoch "$EPOCH" > "$LEASE_PATH"
# Guardian: heartbeat, stop/deadline, and it stops the subject on any exit path (background).
python3 desktop/native/verification/bin/guardian.py --lease "$LEASE_PATH" \
  --stop "$STOP_PATH" --subject-pid-file "$SUBJECT_PID_PATH" > "$GUARDIAN_OUT" &
GUARDIAN_PID=$!
python3 desktop/native/verification/bin/release.py \
  --lane M1 --id "$BOOKING_ID" --lease "$LEASE_PATH" \
  --approval "$APPROVAL_URL" --output "$RELEASE_PATH"
# Exactly ONE controller per booking starts subjects; the guardian's registration lock refuses a
# second one. Set CONTROLLER_MODE explicitly:
#  launch: launch.py starts the app and the scenario drives an app it did not start (e.g. drive-u6.py)
#  drive:  drive-scenario.py starts its own subjects (do NOT run launch.py); its cleanup result is read
#          from the batch named in $RUN_CONFIG itself
# Both stay attached and use subjectPidPath=$SUBJECT_PID_PATH from the run config.
case "$CONTROLLER_MODE" in
  launch) python3 desktop/native/verification/bin/launch.py --config "$RUN_CONFIG" --execute & ;;
  drive)  python3 desktop/native/verification/bin/drive-scenario.py --config "$RUN_CONFIG" & ;;
  *) echo "CONTROLLER_MODE must be launch or drive" >&2; exit 2 ;;
esac
CONTROLLER_PID=$!
# ... in launch mode, drive the scenario against the launched subject here ...
# Close: request stop, then wait for both supervisors. Record --cleaned ONLY when the guardian
# confirmed closure (exit 0) and either launch ended normally (0) or by supervision (3), or the
# guardian reported subject "never-started" (its project-scoped scan found nothing); otherwise do
# not finish at all and report the run as unconfirmed for coordinator follow-up.
touch "$STOP_PATH"
set +e
wait "$CONTROLLER_PID"; CONTROLLER_STATUS=$?
wait "$GUARDIAN_PID"; GUARDIAN_STATUS=$?
DRIVE_CLEAN=0
if [ "$CONTROLLER_MODE" = drive ]; then
  python3 desktop/native/verification/bin/check_drive_cleanup.py "$RUN_CONFIG" || DRIVE_CLEAN=1
fi
SUBJECT=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("subject", ""))' "$GUARDIAN_OUT" 2>/dev/null)
if [ "$GUARDIAN_STATUS" -eq 0 ] && [ "$DRIVE_CLEAN" -eq 0 ] && { [ "$CONTROLLER_STATUS" -eq 0 ] || [ "$CONTROLLER_STATUS" -eq 3 ] || [ "$SUBJECT" = never-started ]; }; then
  python3 desktop/native/verification/bin/book.py finish \
    --id "$BOOKING_ID" --lane M1 --run-id "$RUN_ID" --epoch "$EPOCH" --cleaned
else
  # Do not finish: the booking stays started (the Mac stays held) until the coordinator verifies
  # closure or the documented expiry recovery applies.
  echo "closure unconfirmed: controller=$CONTROLLER_STATUS guardian=$GUARDIAN_STATUS subject=$SUBJECT drive-cleanup=$DRIVE_CLEAN; report to the coordinator" >&2
fi
```

### MacCI (lane V1)

MacCI is a second test Mac with its own ledger; M1 does not run there. Per the coordinator
ruling, the coordinator's GO comment on the handoff issue stands in for the M1 release, for
synthetic-profile runs only. The dev-Mac rule (only M1 releases) is unchanged. Differences from the
sequence above, everything else identical:

- Set `MODELPLAN_VERIFICATION_HOST=macci` for V1's commands on MacCI only (prefix the commands or
  export it in V1's run shell; not in a runner service environment). `release.py` and admission
  refuse when the declared host and this variable disagree; unset means `dev-mac`.
- Book, start and finish with `--lane V1`. Release with
  `release.py --lane V1 --host macci --id "$BOOKING_ID" --lease "$LEASE_PATH" --coordinator-go "$GO_URL" --output "$RELEASE_PATH"`,
  where `GO_URL` is `https://github.com/OWNER/REPO/issues/N#issuecomment-ID` of the coordinator's
  GO. `release.py` checks only that reference's syntax; before releasing, V1 itself must open the
  comment (for example `gh api repos/OWNER/REPO/issues/comments/ID`) and confirm it is the
  coordinator's GO for this run. The receipt records
  `host: macci`, `releasedBy: V1` and `coordinatorGo`, never the M1 release flag, so it cannot
  admit a dev-Mac run, and an M1 receipt cannot admit a MacCI run.
- The run config sets `"host": "macci"` and `"launchMode": "direct"`: on MacCI direct children
  activate (key window, `NSApp.isActive`), while LaunchServices returned -10810 for the ad-hoc
  ModelPlan.app. Use `"subjectKind": "app-zip"` for the full app. Do not substitute a custom controller: only launch.py/Drive register the subject the guardian
  can close.

Launch modes (`launchMode`, recorded in launch.py's JSON lines, the subject registration and the
evidence manifest): `direct` (default) keeps the exec-gated child. `launchservices` copies the
pinned binary into a minimal `.app` under `syntheticTmp/.launchservices/` (hash re-checked; optional
`bundleIdentifier`, `bundleUIElement` default true, `bundleResources`, `bundleSign: adhoc`), opens
it with `open -n -W --env HOME=… --env CFFIXED_USER_HOME=… --env TMPDIR=…`, finds the subject by its
exact bundle executable path, registers its identity, then supervises it by identity. The app's
stdout/stderr go next to the bundle as `subject.{stdout,stderr}`. A LaunchServices app also inherits
the user's launchd environment apart from the overridden variables. Both modes set
`CFFIXED_USER_HOME` to the synthetic home: `HOME` alone does not move Foundation's Application
Support or preferences paths.

Full app (`"subjectKind": "app-zip"`, either launch mode): `argv[0]` is the zip and
`binarySHA256` its hash. launch.py copies the zip into `syntheticTmp/.launchservices/`, re-hashes
the copy, extracts it with `ditto -x -k --noqtn`, requires exactly one top-level `.app` with no
symlink leaving it, a valid `CFBundleExecutable`, and `codesign --verify --deep --strict` passing
(ad-hoc accepted; the kind is recorded as `codeSignature`: `adhoc`, `identity` from an `Authority=`
line, or `unknown` when `codesign -dv` fails or reports neither). With `launchservices` it opens the
`.app`; if `open` fails, its LaunchServices error code is recorded as `launchServicesError` (MacCI
returns -10810 for the ad-hoc ModelPlan.app). With `direct` (use this on MacCI; direct children do
activate there) the extracted `Contents/MacOS/<CFBundleExecutable>` is exec'd as the gated child
with the same synthetic HOME, `CFFIXED_USER_HOME` and TMPDIR. Either way the scan scope is the exact
main executable plus the `.app` prefix under run scratch, so its bundled helpers are covered. For a
plain binary in direct mode the scope is run scratch only and the subject matches by its recorded
PID plus start time, so the same binary running outside the run is never matched.
Keychain is not redirected by a synthetic HOME: do not grant consent to tools during a synthetic
run, so no reader touches the host user's Keychain.

### Prepared packaged candidate (V1, direct mode)

Use the same booking, guardian and V1 coordinator-GO release sequence above. A
local JSON manifest supplies `sourceSHA` (40 lowercase hex) and `sha256` (64
lowercase hex); `--archive` points at the already downloaded zip. The launch
template supplies `profile: synthetic`, `host: macci`, the complete
`expectedLease` from the started booking, `booking`, `requiredSeconds`, and
absolute local `leasePath`, `releasePath`, `stopPath`, `subjectPidPath` and
`candidateCleanupReceipt`. The last five paths are outside the removable run
scratch. `prepare` verifies the archive before creating a fresh scratch root.
Set the guardian arguments to the same paths used in the template:

```sh
python3 desktop/native/verification/bin/packaged_candidate.py prepare \
  --archive "$ARCHIVE" --manifest "$MANIFEST" --template "$RUN_TEMPLATE" \
  --scratch-parent "$SCRATCH_PARENT" --registry "$REGISTRY"
python3 desktop/native/verification/bin/guardian.py --lease "$LEASE_PATH" \
  --stop "$STOP_PATH" --subject-pid-file "$SUBJECT_PID_PATH" \
  --candidate-registry "$REGISTRY" --candidate-parent "$SCRATCH_PARENT" \
  --candidate-cleanup-receipt "$CLEANUP_RECEIPT" > "$GUARDIAN_OUT" &
GUARDIAN_PID=$!
python3 desktop/native/verification/bin/release.py --lane V1 --host macci \
  --id "$BOOKING_ID" --lease "$LEASE_PATH" --coordinator-go "$GO_URL" --output "$RELEASE_PATH"
python3 desktop/native/verification/bin/packaged_candidate.py run \
  --registry "$REGISTRY" --receipt "$RECEIPT"
wait "$GUARDIAN_PID"
```

The caller must finish the booking only after the guardian and candidate
cleanup receipt confirm closure. An unconfirmed cleanup keeps it held. A fresh
HOME is not a Keychain or network sandbox; do not grant real-tool consent.

Synthetic Dock data: the shipped (release, ad-hoc) app has **no** canned-rows or scenario input. Its
normal entry takes rows only from its bundled CLI `app-server`, which reads real provider sources
under HOME (after consent) and verified publication data; the child gets only `HOME`, `PATH`,
`TMPDIR`, locale and provider API-key variables. The existing synthetic paths are test-only builds:
`MODELPLAN_E2E_JOURNEY` (app, `DEBUG` plus macro, `package-neutral.sh --e2e-journey`; a fake
Codex provider), the `tools/u14` CLI constructor overlays (recording providers) and the
Swift-test `WireRowsSnapshot` captures. A fresh synthetic HOME therefore shows only the empty
state. Covering several subscriptions, overflow, warning/critical and reset notices needs a
separate verification build (proposal in the PR); launch.py has no `--scenario` until that exists.

Never registered: both modes record the run's scan scope in the reservation: the exact subject
executable path, the `.launchservices` bundle prefix (LaunchServices mode) and the PID plus start
time of each helper launch.py spawned (exec gate, `open` helper), so a reused PID never matches.
The scan reads only resolved executable paths and owned start identities; it never matches by
process name and never reads any process's environment or arguments. If the launcher exits before
registering, the guardian stops any owned process inside that scope, rescans after a settle delay and reports
`subject: never-started` when nothing was ever found, which permits `finish --cleaned`. A stray it
had to stop (`unregistered-stopped`) or anything unconfirmed keeps the booking started.
A launcher that exits non-zero before reserving (for example an admission refusal) leaves a
run-bound `<subjectPidPath>.no-subject.json`; the guardian then also reports `never-started`.

Reader scope, allow-listed candidate environment and the real-profile product backup
(`--readers off|passive|codex,zcode`, `--backup product`, the run manifest) are specified in
[VERIFY-RUN.md](VERIFY-RUN.md#candidate-environment-reader-scope-and-product-backup-launchpy-packaged_candidatepy).

If the booking is abandoned **before start**, use this instead of start/release/launch:

```sh
python3 desktop/native/verification/bin/book.py withdraw \
  --id "$BOOKING_ID" --lane M1 --reason "unit no longer ready"
```

Keep `LEASE_PATH`, `STOP_PATH`, `SUBJECT_PID_PATH` and `GUARDIAN_OUT` on the test Mac's local disk (run scratch), never on DevShared: lease writers coordinate with `flock` on `<lease>.lock`, which is only reliable locally. Every lease writer (the guardian, Drive's own guardian, any revocation) goes through `guardian.update_lease`.

Start issues one lease snapshot with the booked interval and initial heartbeat;
`bin/guardian.py` keeps that heartbeat within admission's 2-second tolerance, writes the stop file at the deadline minus a 30-second cleanup reserve (at least 25), and stops on SIGTERM; a dead guardian makes admission fail closed. The release writer refuses a lease that differs
from the started head or has expired. Only M1 writes a release (V1 on MacCI, see above), and an existing
receipt is never overwritten. Run configs supply `leasePath`, `releasePath` and
`stopPath`, plus the matching booking. Both Launch and Drive use `admission.py` to
reread these files, validate M1's approval reference (V1's coordinator GO on MacCI), heartbeat and timing, then
check live booking ownership. Inline approval does not grant execution. A started
booking cannot be withdrawn; it requires finish or the documented expiry recovery.

Compile test observation code with `MODELPLAN_TEST_ONLY_SPI`; omit this flag in release. `Observation.swift` excludes the WebKit selector/KVC and test RAF message handler from release. Runtime opt-in alone is insufficient. The scoped SPI is limited to the measured synthetic WKWebView, never process-name discovery.

## 2. Doctor

Emit `WindowObservation.fields` with native timestamp, actual activation call, viewID and generation before applying any combined gate. `bin/doctor.py` reports running, active, key, visible, WebKit, disk and lease individually as timestamped pass/fail. A failed conjunction must retain which condition failed; it is not evidence of owner input. Record the activation call actually made, including explicit `not-invoked` when none was used. Never repeatedly steal focus.

U11a preflight is a **separate** two-second test-only WKScriptMessageHandler RAF proof. Use `VerificationFrameHandler` and `installVerificationRAFTicks`; native elapsed time and advancing frame counts must span two seconds. The preflight also closes and reopens its owned window once to catch lifetime faults before long sampling. Dispose that preflight view/process before starting the cold measurement App/baseline, so preflight cannot prewarm the baseline. A windowless cold baseline records App state without requiring key/visible window conditions; the stop hook arms only on activity actually observed in that current App process. No completed GUI receipt is required merely to schedule a future run. The admitted run collects it.

Keep per-region animation timeline controls from `animation-observer.js` as stronger complementary evidence. DOM presence and one RAF are insufficient. [Neutral controls](fixtures/animation-controls.html) qualify the mechanism; they do not substitute for the actual cockpit.

## 3. Drive

M2 owns `bin/drive-scenario.py` and its independent tests. The command orchestrates one announced epoch with an independent watchdog, separate preflight process, and three measured cycles. M1 independently checks the final closure.

First scenario: U11a, three cycles of **60s pre-open baseline → 60s open → close → 60s post-close**. Preflight two seconds is separate; all waits and cleanup stay within the absolute lease. Gate/frame/post-close evidence missing means **not-run**, never a performance-budget failure. A requested open is not confirmed active appearance. Indicator/session/HUD activity and static porthole inputs must be pinned in the subject.

For each view capture WebContent PID plus start identity; retire on replacement, teardown and `webViewWebContentProcessDidTerminate`. Bind window/frame/attribution receipts to the same viewID/generation. PID changes invalidate previous ownership. GPU/other WebKit attribution uses pre/post snapshots of the already isolated synthetic session only; `bin/attribute_webkit.py` rejects ambiguous or unattributed hosts. No unrelated process inventory or guessed PID. `top` samples only verified role PIDs; missing capability is unsupported, never zero.

## 4. Evidence

`bin/evidence.py` writes a new `manifest.json` and file hashes in the approved independent evidence batch. Bind source head, profile, scenario IDs, outcomes, attribution method, source units and actual cleanup. Reports/CSVs go only to the approved exchange batch, with README/file list; stop and report any refused write to M0, without retry. Project updates are consolidated by M0. Screenshots are synthetic and task-scoped only; no owner account data.

`bin/verify_u11a.py` checks correlated observation evidence. Reuse `scripts/u11a-aggregate.py` and `docs/u11a-aggregation.md`: App uses `native-self-counters`; attributed WebContent/GPU use genuine `top` exports. Never relabel a source or write another reducer.

The approved open budget is average App + WebContent + GPU <=10% of one core. Missing role/activation/frame/post-close coverage cannot establish a total pass. Report canonical after-close RSS differences and cycle endpoints/trend without inventing numeric memory tolerance. Energy may be unsupported. An interrupted actual attempt stays distinguishable from an unlaunched run. A merge or non-GUI check is not GUI/L2 completion.

## 5. Cleanup

M2 owns `bin/cleanup-run.py` and its tests. It quits owned processes, verifies closure, releases only this run's lease/resources and deletes only approved scratch. Retain evidence until its cleanup policy permits deletion. M2 posts start and end+cleaned receipts for the granted run; M1 checks closure independently. No automatic renewal or retry after interruption. A granted test run may request foreground activation once when needed; record the actual call, then stop on subsequent loss of activation rather than continuously reclaiming focus.

## 6. Helpers

M0 owns the verification skill; changes are reviewed by the coordinator (Claude). M1 independently checks post-run closure. Stable commands live in `bin/`; do not rewrite them in each lane.

For named status-menu actions and native arrival correlation, follow [StatusMenu/README.md](StatusMenu/README.md) before driving the item.

Batch GUI runs (verification plan v2): `bin/preflight.py` (PF-01..PF-12, fail closed) and `bin/verify-run.py`, which chains the section 1 sequence per segment from a batch manifest and per-ID step files in `scenarios/`. Contract, step-file format and outputs: [VERIFY-RUN.md](VERIFY-RUN.md).

For a cheap early look at a packaged owner test app on a hosted Mac, without booking, see [walkthrough/WALKTHROUGH.md](walkthrough/WALKTHROUGH.md).

Non-GUI qualification:

```
python3 -m unittest discover -s desktop/native/verification -p 'test_*.py'
python3 -m unittest discover -s desktop/native/verification/tests -p 'test_*.py'
node desktop/native/verification/test-animation-observer.mjs
node desktop/native/verification/test-stable-layer.mjs
node scripts/check-source-policy.mjs
```

Drive/Evidence portions that need no GUI also belong on the standard free hosted macOS checks. Actual test-build compilation, scoped PID capability, two-second preflight, full cycles and cleanup at the submitted head remain required run evidence; their missing outcomes stay explicit.

Role-counter follow-up: `role_counters.py` filters only effective-user `com.apple.WebKit.*` helper PIDs, records pre/post start identities and refuses foreign/ambiguous candidates. It never inspects WindowServer. CPU remains genuine directed top; resident bytes come from identity-checked `ps -o rss` KiB with explicit `ps-rss` provenance in a separate raw file, never relabelled top MEM or native-self-counters. Canonical statistics for that additional RSS source require a separately approved reducer contract.
