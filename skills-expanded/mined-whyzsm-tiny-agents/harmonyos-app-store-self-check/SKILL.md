---
name: harmonyos-app-store-self-check
description: "Audit HarmonyOS applications for AppGallery/AGC release readiness, including Huawei UX/HMI controls, system-feature integrations, and performance gates for multi-input interaction, latency, frame rate, content display, memory, and CPU. Use when users ask for 鸿蒙上架自检、应用市场审核、AGC发布前检查、控件/系统特性/人机交互/签名/隐私/权限/截图/性能核对或 release 包门禁, especially for Stage-model projects with module.json5, build-profile.json5, hvigorw, and local-first data constraints."
---

# 鸿蒙项目自检 / HarmonyOS Project Self-Check

## Overview

Audit a HarmonyOS/OpenHarmony project before an AppGallery/AGC submission. The
Skill has two deliberately separate modes:

- **Local preflight**: inspect the project and release artifact without sending
  anything to Huawei. This finds likely blockers before upload.
- **AGC live validation**: use the logged-in AGC console and its real-device
  "上架自检" flow. Only AGC's own result is allowed to become an AGC pass.
- **Report-driven simulation**: use a supplied AGC report as a reference
  profile and re-check the current project/package locally. This reproduces
  the report shape and conservative status handling, but never copies a
  historical device result into the current package's AGC result.

The output is an evidence-backed release gate, not a promise that Huawei will
approve the application. Keep evidence provenance and result state separate:

- `confirmed`: observed in the repository, a successful command, a device run,
  or an AGC result supplied by the user;
- `official`: a rule or standard copied from the current official Huawei
  document snapshot in `references/huawei-ux-guidelines-v30.md` or
  `references/huawei-performance-guidelines-v7.md` or
  `references/huawei-controls-overview-v6.md` or
  `references/huawei-hmi-guidelines-v6.md` or
  `references/huawei-system-features-v6.md` or
  `references/huawei-atomic-service-ux-v4.md` or
  `references/huawei-design-concepts-v6.md`;
- `baseline`: a useful check derived from the visible
  `harmonyos-code-workshop` material;
- `unverified`: a current AGC policy, account setting, device behavior, or
  artifact property that was not checked.

This Skill is for release readiness and submission preparation. Local preflight
does not upload packages, create certificates, modify signing material, or
silently fix project files. AGC live validation may upload the explicitly
selected release package only after the user confirms that external action at
the moment of upload; it still does not create certificates or change signing
material.

## Triggers And Inputs

Use it for requests such as:

- “帮我做鸿蒙应用上架自检，找出 AGC 审核阻断项。”
- “检查这个 HarmonyOS Stage 项目的 release 包、隐私、权限、签名和应用市场截图。”
- “我的鸿蒙 AppGallery 发布前还缺什么证据？”
- “按华为性能体验建议检查时延、帧率、内存和 CPU。”
- “按华为控件规范检查这个页面的导航、输入、选择和容器控件。”
- “按华为人机交互规范检查触屏、鼠标、键盘、触控板和焦点导航。”
- “按华为系统特性规范检查通知、实况窗、多窗口、服务卡片和播控中心。”
- “按华为元服务设计规范检查服务卡片、免安装入口、静默登录和分享体验。”
- “按华为设计理念评估这个 HarmonyOS 应用的 UI 和多设备体验。”

Accept a project root, an optional target module/product, target API/OS version,
AGC listing metadata, privacy/legal material, screenshots, performance evidence,
and an already-built HAP/APP. Performance evidence must identify the exact
package, device, OS/API, scenario, statistic, unit, sample count, and source
trace. For AGC live validation, also require a logged-in AGC console, the target
app, and the exact release package to test. If a path or artifact is not supplied,
inspect the repository first; ask only for information that blocks the next
useful check.

## Outputs And Completion

Return a Chinese report unless the user asks for another language. Include:

1. `READY`, `BLOCKED`, or `UNVERIFIED` local gate status. When AGC was run,
   include a separate `AGC_READY`, `AGC_NOT_READY`, `AGC_PENDING`, or
   `AGC_EXECUTION_FAILED` result copied from the AGC console.
2. A flat table with check ID, status (`PASS`/`FAIL`/`BLOCKED`/`UNVERIFIED`/
   `NOT_APPLICABLE`),
   severity (`P0`/`P1`/`P2`), evidence path or command, and remediation.
3. A short release artifact checklist and the exact commands that were run.
4. Assumptions, unavailable AGC/device evidence, and the next smallest action.
5. A separate Huawei performance result: `READY`, `BLOCKED`, or `UNVERIFIED`,
   with each applicable rule ID, measured value, unit, device, and evidence.
6. When the product is an atomic service, a separate `ATOMIC_READY`,
   `ATOMIC_BLOCKED`, or `ATOMIC_UNVERIFIED` result with the applicable local
   `ATOMIC-*` checks and current-version evidence.
7. For a broad UI or design review, a separate design-principle section with
   `DESIGN-ONE`, `DESIGN-HARMONIOUS`, and `DESIGN-UNIVERSE`, concrete evidence,
   and any unverified device or accessibility scope.

Never merge a local `READY` result into `AGC_READY`. A local pass means that
the inspected evidence has no known blocker; it does not mean that Huawei's
cloud devices accepted the package.

The gate is `READY` only when no P0/P1 release blocker remains and all checks
that are required for the chosen product are confirmed. Otherwise use
`BLOCKED`; use `UNVERIFIED` when the project may be ready but evidence is
missing. Never turn an unrun check into a pass.

## Workflow

1. **Route the request.** This Skill handles release-readiness audits directly.
   For policy/API/version questions that require authoritative Huawei sources,
   search the official documentation or AGC console and cite the source. For
   project code fixes, fix only after presenting the audit findings and getting
   user approval. For broad functional/UI/interaction review, treat it as a
   separate quality-review request. Do not expand the audit scope into unrelated
   changes.
2. **Inspect project shape.** Read repository instructions first. Locate
   `AppScope/app.json5`, each `module.json5`, `build-profile.json5`,
   `entry/build-profile.json5`, `hvigorfile.ts`, `oh-package.json5`,
   `main_pages.json`, source modules, tests, privacy/legal pages, listing
   screenshots, and project QA/release notes. Record the target product,
   module, API level, and build mode.
3. **Run the local preflight.** From this package, run:

   ```bash
   python3 scripts/check_harmony_release.py --project-root <project-root> --format text
   ```

   Add `--forbid-network` for a local-first app, `--artifact <path>` for the
   exact `.app`/`.hap` under review, and `--strict` when the report should exit
   non-zero on failures. The helper is advisory; inspect every finding before
   making a release decision.
4. **Check identity and packaging.** Verify bundle name, label, version code,
   version name, module/ability entry, route registry, device types, target and
   compatible SDKs, and release-mode configuration. Confirm that the artifact
   being reviewed is the same product/version represented in the listing.
5. **Check privacy, permissions, and data handling.** Map every declared or
   runtime-sensitive permission to a real feature and user-visible disclosure.
   Check minimum permission scope, denial/error behavior, privacy policy,
   deletion/retention language, third-party SDK disclosure, and any children,
   advertising, payment, health, location, or account flows that are actually
   present. For photos, verify that binaries remain app-local and only local
   references reach SQLite. Treat unexplained network access or remote-sync
   claims as a blocker for local-first projects.
6. **Check release security.** Require a release build, a valid AGC signing
   chain and profile for the target bundle, and a reproducible artifact path.
   Scan tracked and staged files for certificates, profiles, keystores,
   passwords, tokens, home-directory paths, and debug-only configuration. Do
   not print secret values; report only the path and kind of leak.
7. **Apply the official UX gate.** Read
   `references/huawei-ux-guidelines-v30.md` and determine the product's declared
   device types and feature scope before checking the standards. Record the
   exact official ID, grade (`必须`/`推荐`/`强烈推荐`), applicability, evidence
   kind, and result for each applicable item:

   - For the linked `视觉风格` section, check contrast, minimum text size,
     layered 1024 px application icons, interface icon size, icon clarity, and
     cursor clarity where applicable.
   - For `基础体验` and `人机交互`, check system back, punch-hole avoidance,
     system-gesture conflicts, long-press/double-tap timing, hit areas, and
     scroll-control height.
   - For `动效` and `系统特性`, check transitions, motion duration, startup,
     scrolling feedback, navigation-bar avoidance, notifications, live windows,
     multi-window/PiP, dark mode, status bar, and immersive scenarios when the
     feature or device scope applies.

   Separate evidence into `static` (source/config/resource), `screenshot`
   (current-version UI capture), `runtime` (emulator/device operation record),
   and `agc` (current AGC report). A static scan is only a lead for interaction
   and visual standards. Missing evidence is `UNVERIFIED`; explicitly
   inapplicable standards require a written reason and `NOT_APPLICABLE`.
   Optionally validate a project evidence manifest with:

   ```bash
   python3 scripts/check_harmony_release.py \
     --project-root <project-root> --ux-audit \
     --ux-evidence <project-root>/docs/qa/huawei-ux-evidence.json \
     --format text
   ```

   Before evaluating individual pages, read
   `references/huawei-controls-overview-v6.md` and classify the actual controls
   into navigation, display, operation, input, selection, or container. Record
   each control's name, route/page, applicable device, evidence type, and state.
   Use the taxonomy to choose the relevant UX checks; a component name in source
   code alone is not behavioral evidence.

   Read `references/huawei-system-features-v6.md` when the app uses or declares
   navigation bars, notifications, live view, multi-window, service cards,
   picture-in-picture, dark mode, status bars, or media control center. For each
   applicable capability, record the official child-document URL, capability
   entry/configuration, device scope, current package version, and runtime or
   AGC evidence. Use `NOT_APPLICABLE` with a reason for capabilities the app does
   not use. The local `SYS-FEATURE-*` IDs are routing labels, not Huawei or AGC
   test IDs.

   For input behavior, also read `references/huawei-hmi-guidelines-v6.md`. Check
   touch gestures and system-gesture conflicts, cursor semantics and hover,
   focus initialization/traversal/visibility, mouse primary/secondary actions,
   keyboard shortcuts, touchpad gestures, drag and selection, and equivalent
   event behavior across at least two applicable input methods. HMI evidence must
   name the input device and operation path; missing evidence is `UNVERIFIED`.

   If the product is a HarmonyOS atomic service or exposes atomic-service
   metadata, read `references/huawei-atomic-service-ux-v4.md`. Check whether the
   release is actually a service, then audit service discovery, no-install
   opening, no-splash/one-load behavior, service-card identity, Menubar/capsule
   avoidance, 2-5 bottom tabs, Huawei-account silent login, privacy/permission
   control, service status/messages, add/favorite/remove management, sharing,
   waiting/cancel/retry feedback, and the open-to-exit lifecycle. Ordinary apps
   must record these checks as `NOT_APPLICABLE`; do not apply atomic-service
   requirements by assumption.

   For a broad UI or product-experience review, also read
   `references/huawei-design-concepts-v6.md` and report the three principle-level
   findings separately: `DESIGN-ONE` (human-centered clarity and intuition),
   `DESIGN-HARMONIOUS` (balanced visual and interaction language), and
   `DESIGN-UNIVERSE` (multi-device consistency with necessary differentiation).
   These are official direction-level references, not AGC result codes or new
   hard thresholds. Tie each principle to concrete controls, routes, devices,
   screenshots, or runtime records; without current evidence use `UNVERIFIED`.

8. **Check product and listing evidence.** Confirm that the name, icon,
   description, screenshots, claims, privacy URL, and supported devices match
   implemented behavior. Screenshots must show real, reachable product states;
   remove placeholders, fake social data, and claims of synchronization or
   capabilities not implemented. Check Chinese user-facing loading, empty,
   error, permission-denied, and deletion feedback where the project requires
   it.
9. **Check Huawei performance evidence.** Read
   `references/huawei-performance-guidelines-v7.md` and determine which rules
   apply from the product capabilities and declared device types. The matrix
   covers `DELAY-1..12`, `FPS-1..9`, `CONTENT-1..3`, `MEMORY-1..3`, and `CPU-1`.
   Run the evidence validator when a normalized measurement file is available:

   ```bash
   python3 scripts/validate_performance_evidence.py \
     --evidence <performance-evidence.json> \
     --format text
   ```

   Use `--strict` for the release gate. Do not fill absent measurements with
   `0`, an old package's result, a source-code estimate, or a screenshot-only
   guess. Rules for unsupported features must be marked `not_applicable` with a
   reason; missing evidence remains `UNVERIFIED`. A performance `READY` is a
   local evidence result, never `AGC_READY`.
10. **Run verification in increasing cost.** Run repository validation scripts
   and `git diff --check`; run the project release/HAP build with its own
   `hvigorw`; then run the manual QA script on emulator/device for cold start,
   offline behavior, core CRUD, permission denial, restart persistence, data
   deletion, migration, crash/error recovery, and the applicable Huawei
   performance scenarios. Use a performance tracing tool for frame, CPU, memory,
   and audio/video metrics. Label static-only checks and unavailable device/AGC
   checks explicitly.
11. **Run AGC live validation when requested.** Use the browser capability on
   the logged-in AGC console, open the target app's `应用上架 > 软件包管理`,
   and verify the uploaded row before starting a test:

   - `合法性 = 已达标` confirms the package was accepted as an upload. It is
     not the same as passing the full self-check.
   - `上架自检 = 检测中` means the official test is still running. Do not
     report a result yet.
   - Click `启动自检` only for the exact release package and device scope that
     matches the listing. Wait for the report rather than inferring a result
     from the upload status.
   - Read the AGC report's overview and each available category: `兼容性`,
     `稳定性`, `功耗`, `性能`, and `UX`. Record report ID, package identity,
     API level, tested devices, total/failed/warning/passed counts, test result,
     and any failed or warning test name.
   - Map the final `上架自检` state exactly: `已达标` -> `AGC_READY`, `待优化`
     -> `AGC_NOT_READY`, `检测中` -> `AGC_PENDING`, and `执行失败` ->
     `AGC_EXECUTION_FAILED`. Any missing category or incomplete device coverage
     remains `UNVERIFIED`.

   Follow `references/agc-live-validation.md`. Uploading a package and starting
   a cloud test are external actions; obtain confirmation immediately before
   the first upload or test start.
12. **Synthesize the gate.** Deduplicate findings, classify P0 (submission or
   core workflow blocked, data/privacy/security can be false or lost), P1
   (must fix before release), and P2 (lower-risk polish or evidence gap), then
   report the smallest remediation order. Ask before edits, signing, upload,
   commit, push, or other external side effects.

## Report-Driven Simulation

When the user supplies an AGC report URL, screenshot, PDF, HTML, or structured
content, read the report with the browser/document capability and normalize the
visible fields using `references/agc-report-driven-simulation.md`. Then:

1. Preserve the report's `通过`/`警告`/`不通过` values as historical AGC
   evidence, including report ID, test time, device scope, and issue names.
2. Check the new `.app`/`.hap` and project identity locally. Compare bundle name,
   version, API level, and declared device types when the report exposes them.
3. Recreate the five AGC sections (`兼容性`, `稳定性`, `功耗`, `性能`, `UX`),
   but mark device-only measurements as `UNVERIFIED` unless a fresh device
   trace is supplied. A report from an older upload is not a fresh trace.
4. Apply the official UX reference as a local evidence cross-check. A historical
   AGC UX warning such as gesture timing should be mapped to the matching Huawei
   standard ID when possible, but it must remain historical evidence rather than
   a current-package pass.
5. Apply `references/huawei-performance-guidelines-v7.md` to the AGC `性能`
   tab. Map visible latency, frame-rate, content, memory, and CPU items to the
   matching `DELAY-*`, `FPS-*`, `CONTENT-*`, `MEMORY-*`, or `CPU-*` rule when
   possible. Historical values remain reference evidence; re-run the current
   package on an identified device before declaring a local performance pass.
6. Apply `references/huawei-hmi-guidelines-v6.md` to AGC UX issues involving
   gestures, focus, cursor, mouse, keyboard, touchpad, drag, selection, or input
   event normalization. Map the issue to the local `HMI-*` ID when possible;
   historical AGC evidence still cannot become a current-package pass.
7. Flag inconsistent report totals or missing category data as evidence issues;
   do not silently repair or average them.
8. Use `SIMULATED_BLOCKED` when local P0 blockers exist and
   `SIMULATED_UNVERIFIED` when the package is locally clean but dynamic AGC
   evidence is missing. The simulation must never emit `AGC_READY`.

## Harmony Wardrobe Adapter

When the inspected repository is Harmony Wardrobe / `衣不缺`, enforce its
project facts in addition to the generic checks:

- `io.wardrobe.tiny` is the bundle name and the product is a Stage app for
  phone/tablet. Read the resource label instead of assuming a display string.
- The app is local-first: SQLite business tables are the source of truth,
  photos are copied to app-local storage, and SQLite stores only local
  URI/path references. No `INTERNET` permission, backend, remote sync, fake
  social feed, or “待同步” claim may be introduced without an explicit scope
  change.
- Read `docs/legal/privacy-policy.html`, `docs/legal/user-agreement.html`,
  `docs/architecture.md`, `docs/qa/manual-test-script.md`, and
  `docs/delivery/first-release-verification.md` when present. Use
  `docs/appgallery/screenshots/` as listing evidence only after checking that
  the screens are reachable and current.
- A delete flow is not complete until the business row, derived search index,
  and orphaned local media are handled consistently. Permission denial and
  local media-copy failure must remain visible to the user.
- Treat a `build-profile.json5` containing `signingConfigs`, passwords,
  `.p12`/`.cer`/`.p7b`, or `/Users/` paths as local signing material, not as a
  publishable repository artifact. Preserve the user's uncommitted changes and
  redact values in reports.
- If UI changes are proposed, read `docs/background/yibuque-design.md` first;
  do not turn this release audit into an unrelated redesign.

## Evidence Rules

The visible workshop source provides a release-flow baseline: developer/AGC
registration, certificate/profile preparation, signed HAP/APP packaging, listing
metadata, privacy/permission checks, and submission. Its “上架合规必查” bullets
are guidance, not the current official policy. For policy-sensitive questions,
consult current official Huawei documentation or AGC UI and cite the exact
source/date in the report. The workshop version metadata is inconsistent
(`SKILL.md` says 6.1.0 while `_meta.json` says 5.0.0); do not infer API or policy
support from that inconsistency.

## Guardrails

- Do not log, copy, upload, install, generate, or expose signing secrets; never
  upload a certificate, Profile, keystore, password, token, or other secret.
- Do not perform AGC login, package upload, self-check start, certificate
  creation, publication, commit, push, deletion, dependency installation, or
  deployment without explicit user authorization. Confirm at action-time for
  the selected package and destination account.
- Do not claim “审核通过” from static code inspection, a successful debug
  build, or an unverified screenshot. Distinguish build success from signed
  release readiness and from AGC approval.
- Do not claim latency, frame-rate, memory, or CPU thresholds from source code,
  a debug build, a screenshot, or a measurement from another package. Huawei
  performance rules require current-package evidence on an identified device.
- Do not claim HMI compatibility because an event handler exists. Verify the
  actual input device, focus path, visual feedback, and equivalent operation on
  every applicable device class.
- Do not invent official thresholds, required permissions, API behavior, or
  hidden workshop material. Mark uncertain rules `UNVERIFIED` and suggest
  checking the current official Huawei AppGallery documentation or AGC console.
- Preserve unrelated working-tree changes. Never rewrite a user's signing
  configuration just to make a scanner pass.
- Ask before destructive, external, installation, publication, commit, or push actions.
- Do not use secrets, local absolute paths, or undocumented private interfaces.

## Validation

For this Skill package, validate the helper script and check for obvious issues:

```bash
# Run local preflight against the exact release artifact
python3 scripts/check_harmony_release.py \
  --project-root <project-root> \
  --artifact <project-root>/path/to/release.app \
  --format text

# Run unit tests
python3 -m unittest discover -s tests -p 'test_*.py'

# Quick smoke test with --strict and --forbid-network
python3 scripts/check_harmony_release.py --project-root <project-root> --forbid-network --strict --format json

# Validate Huawei V7 performance evidence for the current release package
python3 scripts/validate_performance_evidence.py \
  --evidence <performance-evidence.json> --strict --format json

# Validate a normalized AGC report and simulate its result locally
python3 scripts/simulate_agc_self_check.py \
  --report <normalized-agc-report.json> \
  --project-root <project-root> \
  --artifact <project-root>/path/to/release.app \
  --format text
```

When validating against the actual Harmony Wardrobe project, also run the
repository-level checks listed in the project's AGENTS.md.

## References

- Read `references/harmonyos-appgallery-self-check.md` before producing a full
  report; it contains the check IDs, workshop baseline mapping, and the
  Harmony Wardrobe evidence map.
- Read `references/huawei-ux-guidelines-v30.md` for every UX-focused audit or
  when the user supplies the Huawei UX guideline URL. Cite the canonical URL,
  document version, access date, official ID, and evidence boundary.
- Read `references/huawei-controls-overview-v6.md` when reviewing UI controls,
  screenshots, routes, interaction flows, or a Huawei control-design URL. Use
  its six categories to structure the report before assigning UX findings.
- Read `references/huawei-design-concepts-v6.md` for broad UI/product-experience
  reviews or when the user supplies the Huawei design-concepts URL. Keep its
  `DESIGN-*` findings separate from AGC and threshold-based `UX-*` checks.
- Read `references/huawei-hmi-guidelines-v6.md` for the official HMI page tree,
  input mappings, focus navigation, cursor, keyboard, touchpad, drag, selection,
  and event-normalization evidence rules.
- Read `references/huawei-system-features-v6.md` when reviewing system-feature
  integrations or the Huawei system-features overview URL. Follow the linked
  child documents for current feature-specific rules and keep unused features
  explicitly out of scope.
- Read `references/huawei-atomic-service-ux-v4.md` when reviewing a meta-service,
  service card, no-install flow, Huawei atomic-service URL, or atomic-service
  listing. Keep `ATOMIC-*` checks separate from ordinary-app UX and AGC status.
- Read `references/agc-live-validation.md` when the user asks for the same
  result as AGC's `上架自检` or provides an AGC console/report URL.
- Read `references/agc-report-driven-simulation.md` when a historical AGC
  report is supplied as the simulation baseline.
- Read `references/huawei-performance-guidelines-v7.md` for the official V7
  performance thresholds and evidence schema. Run
  `scripts/validate_performance_evidence.py` for normalized measurements.
- Read only the relevant reference sections for focused checks. Keep current
  official AGC/Huawei documentation above the workshop-derived baseline.
