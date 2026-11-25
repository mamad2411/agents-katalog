---
name: "webapp-testing"
description: "AISP-backed bridge for Local-only AISP V1.0.0 Playwright skill that tests a LOCAL web app: verify frontend, debug UI, audit accessibility (axe-core WCAG 2.2 AA, data-only), capture screenshots/console logs, visual-regression diffs, trace.zip, network HAR, and debug video; isolates external deps via local egress-preserving route-stubbing. Reconnaissance-Then-Action, web-first readiness-wait before inspect (domcontentloaded + expect(getByRole).toBeVisible; networkidle demoted to optional auxiliary), expect auto-wait. Red lines: headless-only, always-close-browser, local-only host, no egress. Use when The user asks to test or verify the frontend of a LOCAL web app (a dev server on localhost or a static .html file) — does the page render, do the buttons/forms work.; The user wants to debug UI behavior of a local web app and needs to inspect the rendered DOM, discover selectors, or click/fill/submit elements. Do not use when The user wants to test a REMOTE or PRODUCTION website (any non-localhost / non-file://..."
license: "Apache-2.0"
metadata:
  generated_from_aisp: "true"
  aisp_program: "aisp.aisop.json"
  protocol: "AISP V1.0.0"
  bridge_mode: "native_sidecar"
---

# Webapp Testing (AISP-backed Agent Skill)

<!-- generated_from_aisp: true -->
<!-- source: aisp.aisop.json -->
<!-- generator: tools/aisp_skill_md.py -->

This `SKILL.md` is a thin Agent Skills discovery bridge, not the source of truth. The executable source of truth is the same-folder `aisp.aisop.json` AISP program.

Deleting this file does not change the native AISP skill. A conforming AISP/AISOP runtime should load `aisp.aisop.json`, read `user.content.aisp_contract`, and run `user.content.aisop.main` exactly as declared.

## How to use

1. Load `aisp.aisop.json` from this folder.
2. Read `user.content.aisp_contract` before following any workflow.
3. Follow `user.content.instruction`: `STRICTLY OBEY aisp_contract; its non_negotiable rules are inviolable and bound to real enforcement mechanisms; then RUN aisop.main.`.
4. Load declared resources only when the AISP graph reaches the node that needs them.
5. Enforce every non-negotiable rule through the mechanism named by `enforced_by`.

## Declared resources

- `scripts/with_server.py` (script, execute_only)
- `examples/element_discovery.py` (example, read_only)
- `examples/static_html_automation.py` (example, read_only)
- `examples/console_logging.py` (example, read_only)

## Non-negotiable boundaries

- Headless launch: the browser MUST be launched in headless mode (chromium.launch(headless=True)); no visible/headed browser window is ever opened. (`LaunchBrowser.step2:sys.assert`)
- Wait-before-inspect (Reconnaissance-Then-Action): for a dynamic webapp the skill MUST wait until a role-based readiness signal is visible BEFORE inspecting the DOM, deriving selectors, or taking a screenshot (the source's documented Common Pitfall: inspecting too early) — the web-first readiness contract is page.wait_for_load_state('domcontentloaded') followed by a web-first assertion on a user-facing locator, expect(page.getByRole(<role>, name=<name>)).toBeVisible() (or .toBeEnabled()), which auto-waits for the actual element the test depends on. networkidle is DISCOURAGED (an anti-pattern per playwright.dev — background-polling/websocket/SSE pages may never reach it) and is at most demoted to an OPTIONAL auxiliary technique, no longer a mandatory red line. Inspect -> identify -> act ordering is mandatory. (`Reconnaissance.step3:sys.assert`)
- Browser close on completion: the browser MUST be closed on every completion path; no leaked browser process or resource remains. (`Teardown.step2:sys.assert`)
- Local-only target: every navigation host MUST be localhost / 127.0.0.1 / file://; remote or production sites are never targeted. (`ClassifyTarget.step2:sys.assert`)
- No exfiltration: data is processed purely locally; nothing is uploaded or sent over any network. The skill declares no open-world/network capability — its tools allow-list (browser, code, filesystem) carries open_world=false on every tool. (`tools`)

## Runtime boundary

Agent Skills platforms can use this bridge to discover and inspect the package. Hard guarantees such as `sys.assert`, `sys.io.confirm`, tool gating, dispatch behavior, and path confinement require a conforming AISP/AISOP runtime. A generic non-AISOP agent can only follow the contract on a best-effort basis.

Passing `SKILL.md` generation or bridge validation proves only projection consistency and bridge shape. It does not prove external trust, safety, registry approval, or hard execution on a non-AISOP platform.

Align Axiom 0: Human Sovereignty and Wellbeing. AISP - AI Skill Protocol V1.0.0. www.aisp.dev
