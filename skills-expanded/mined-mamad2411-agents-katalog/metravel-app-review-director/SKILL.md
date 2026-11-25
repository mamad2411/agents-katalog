---
name: metravel-app-review-director
description: Prepare scene scripts and record the Apple App Review demo video on the physical iPhone and iPad for an exact TestFlight candidate. Use when Apple asks for a device video (Guideline 2.1) or when registration, report/block, account-deletion or sign-in scenes must be captured with disposable QA accounts.
---

# Metravel App Review Director

Turn the scene catalog into executable device scripts, record each scene on
the physical devices, and hand the raw files to `$metravel-evidence-editor`
and `$metravel-app-review-evidence`. This role does not edit video, write
Reply/Notes, build, upload, submit or touch App Store Connect.

`AGENTS.md` is inherited. Operational contracts:
`.claude/skills/ios-device-qa/SKILL.md` (driver, private input, TCC),
`docs/WORKFLOW_OPERATIONS.md` → «3.1 E2E окружение» (accounts, activation)
and «3.2.1 iOS testing and release operations» (operation gate),
`docs/CODEX.md` → `Media-agent dispatch` (checkpoint, retry, output limits).

## 1. Candidate and devices

1. Fix the candidate from App Store Connect/TestFlight: `version (build)`,
   source SHA, IPA SHA-256 if archived. Video of any other build is invalid.
2. `source scripts/ios-device-qa.sh` (bash), list devices, confirm both are
   unlocked and that the installed `by.metravel.app` shows the same
   `version (build)`; record model and OS, never UDID. Latest stable OS is
   required on the primary video device; the other device is a compatibility
   pass.
3. Primary video: the device on the latest OS (12.09.2026: iPad mini 6,
   iPadOS 26.6.2). Compatibility: the other device, same scene ids, shorter.
4. Take a crash-report baseline before the first scene and diff it after the
   last one.

## 2. Accounts

- Permanent reviewer demo: `APP_REVIEW_DEMO_EMAIL`/`APP_REVIEW_DEMO_PASSWORD`
  in `.env.e2e`. It is the account Apple has; use it only for the `login`
  scene, never delete it, never print it, never put it in a scene name,
  `QA_SCRIPT`, screenshot, tree, board or doc.
- Disposable account for `register` → `account-delete`: Gmail plus-addressing
  on the demo mailbox, `<demo-local-part>+appleqa-<YYYYMMDD>-<n>@gmail.com`,
  with a fresh password generated into a private `0600` file. The activation
  mail lands in the demo mailbox; activation is either the owner/main session
  tapping the link in the open Gmail tab, or the documented database-token
  recipe (`POST /api/user/confirm-registration/`) executed during a labelled
  cut. Neither path types the password through the model.
- Author for `ugc-report`/`ugc-block`: the existing `E2E_EMAIL2` user (public
  profile and trip exist). Report and block are reversible: unblock afterwards
  and tell the owner the moderation report id to dismiss.
- Cleanup: the delete scene destroys the disposable account; verify with a
  failed login. Nothing else on production is mutated.

## 3. Scene scripts

For every `required` id in
`.codex/skills/metravel-app-review-evidence/scenes.json` write
`<out>/scenes/<id>.json`: helper steps (`tapText`, `tapId`, `wait`,
`longPressPlaceholder` + explicit Paste tap, `terminate`/`activate`), the
expected end state, and which frames show the build (TestFlight card or
Settings version/build at scene start). Rules:

- one scene = one file = one recording; no unrelated waiting on an unlocked
  device (prepare the next command before asking for unlock);
- secret screens: `QA_PRIVATE_INPUT=1`, `secretClipboard` → paste →
  `clearSecretClipboard`; no `tree`/`shot`/`type` there; run the dummy canary
  once per runner build before real credentials;
- Do Not Disturb on, notifications and Messages never in frame, EN locale
  unless the scene tests locales;
- `purchases`: not recorded; the manifest carries `notApplicable` with
  evidence (no IAP dependency, ASC Free).

## 4. Recording

Capture is QuickTime Player → File → New Movie Recording with the device as
camera source and no microphone, driven through desktop automation; the
device's own Screen Recording is the fallback. Start capture before the
first step, run `tools/ios-device-uitests/run.sh` with the scene JSON, stop
after the expected state is visible, save as
`.codex-temp/app-review-<date>/device/<device>/<id>.mov`, then run
`node .codex/skills/metravel-evidence-editor/scripts/media-report.mjs` and
store the report beside the file. The private-input protocol pauses capture
for the paste segment: split the scene into `<id>-a.mov`/`<id>-b.mov` and
record the cut in the checkpoint; the editor labels it.

One take, no dead time. Everything that can be prepared happens before
capture starts: helper build and dummy canary, the secret file already in
the runner container, the whole scene in one `QA_SCRIPT` (including
`secretClipboard` → `longPressPlaceholder` → Paste → `clearSecretClipboard`
→ submit), the activation command dry-run, and a rehearsal of the scene
without capture. A recorded scene is a continuous 30–90 s run; never wait
for a person, debug, or read trees while capture is running. If a pause is
unavoidable, stop capture and continue in a new file. A take with idle
waiting is a draft, not evidence: re-record it.

Budget: about three minutes of wall clock per scene. The dummy canary runs
once per runner build, not per scene; at most one rehearsal per scene; the
first take whose expected end state is visible in the last frames is final
(no second take "for quality", no post-take XCTest verification — the video
is the verification); short steps are merged into one `QA_SCRIPT` so
`xcodebuild` is not launched per tap; checkpoint and board notes are written
once per batch, plus once after any failure.

Rerun only a failed scene, once, after fixing the observed cause. Two
identical operational failures (lock, trust, signing, capture source) → stop
and name the exact owner action.

## 5. Handoff

Write `<out>/checkpoint.json` (candidate, devices, scene → file, SHA-256,
result, cut notes, next scene) after every scene and a per-device draft
manifest in the `$metravel-app-review-evidence` schema with real timecodes
from the raw files. Hand raw files to `$metravel-evidence-editor`; the final
manifest and privacy playback belong to `$metravel-app-review-evidence`.
Board: anonymised progress only (scene ids, file names, SHA, blocker).

Return at most 12 lines: candidate, devices/OS, scenes recorded/failed with
files, accounts used (masked), cleanup state, crash diff, checkpoint path,
next step.
