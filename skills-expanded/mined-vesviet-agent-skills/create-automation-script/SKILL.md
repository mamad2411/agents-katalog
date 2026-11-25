---
name: create-automation-script
description: Generate stealth automation scripts using Playwright/Puppeteer over CDP, C++ patched browsers (Camoufox), and behavioral mimicry techniques. Use when deploying new MMO operations, expanding to new ad accounts, or replacing legacy spin-based automation.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
version: "1.0.0"
---

# Create Automation Script

Use this skill to develop the core engine for MMO automation (farming, scraping, ad deployment) with an absolute focus on stealth, fingerprint consistency, and evading advanced bot-detection systems.

## When to Use

- building multi-account login, registration, or warm-up automation flows
- scripting ad account creation and campaign publishing across high-trust platforms (Meta, Google, TikTok)
- solving Cloudflare Turnstile managed challenges automatically via Shadow DOM and humanized interactions
- ensuring deterministic WebGPU and Canvas 2D fingerprint consistency across headless browser sessions
- connecting to Anti-Detect Browsers (AdsPower, Multilogin) via CDP or running C++ patched engines (Camoufox)

## Example (CDP Connection, WebGPU/Canvas Consistency & Turnstile Solver)

```typescript
import { chromium, Page } from "playwright";

// Connect to running Anti-Detect Browser instance over CDP
const browser = await chromium.connectOverCDP("http://127.0.0.1:50325");
const page = browser.contexts()[0].pages()[0] || (await browser.contexts()[0].newPage());

// WebGPU and Canvas 2D deterministic noise consistency
await page.addInitScript((profileSeed: number) => {
  let s = profileSeed;
  const prng = () => {
    s |= 0; s = (s + 0x6D2B79F5) | 0;
    let t = Math.imul(s ^ (s >>> 15), 1 | s);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
  const origGetImageData = CanvasRenderingContext2D.prototype.getImageData;
  CanvasRenderingContext2D.prototype.getImageData = function(...args) {
    const data = origGetImageData.apply(this, args);
    for (let i = 0; i < data.data.length; i += 4) {
      data.data[i] ^= Math.floor(prng() * 2); // 1-bit continuity noise
    }
    return data;
  };
}, 133742);

// Automated Cloudflare Turnstile challenge handler
async function solveTurnstile(page: Page, timeoutMs = 25000): Promise<string> {
  const startTime = Date.now();
  while (Date.now() - startTime < timeoutMs) {
    const cfToken = await page.evaluate(() => {
      const input = document.querySelector<HTMLInputElement>('input[name="cf-turnstile-response"]');
      return input && input.value.length > 20 ? input.value : null;
    });
    if (cfToken) return cfToken;

    // Traverse shadow DOM / iframe challenge container
    const turnstileFrame = page.frames().find((f) => f.url().includes("challenges.cloudflare.com"));
    if (turnstileFrame) {
      const checkbox = await turnstileFrame.$('input[type="checkbox"], #challenge-stage, .ctp-checkbox-label');
      if (checkbox) {
        const box = await checkbox.boundingBox();
        if (box) {
          // Humanized Bézier cursor approach with jitter and click
          await page.mouse.move(box.x + box.width / 2 + (Math.random() * 6 - 3), box.y + box.height / 2, { steps: 15 });
          await page.waitForTimeout(180 + Math.random() * 220);
          await turnstileFrame.click('input[type="checkbox"], #challenge-stage', { delay: 60 + Math.random() * 50 });
        }
      }
    }
    await page.waitForTimeout(1000);
  }
  throw new Error("Turnstile token polling timed out");
}
```

## Core Rules

- **BEHAVIORAL-LOCK**: Any script interacting with high-trust platforms MUST include organic delays and humanized Bézier mouse trajectory emulation. Instantaneous actions or zero-delay inputs trigger automated AI telemetry flags.
- **STEALTH-LOCK**: Reject outdated JS-injection stealth plugins (`playwright-stealth`) or runtime monkey-patching (`Object.defineProperty(navigator, 'webdriver')`). Connect strictly via CDP to pre-configured Anti-Detect Browsers or execute inside C++ patched engines (Camoufox).
- **WEBGPU-CANVAS-CONSISTENCY**: Injected Canvas 2D and WebGPU noise MUST be deterministic per profile ID, using PRNG seeds derived from the profile key. WebGPU adapter limits, architecture, and device IDs MUST match WebGL `UNMASKED_RENDERER_WEBGL` and declared OS platform. Never output blank or randomized noise across sequential frames that breaks mathematical continuity.
- **TURNSTILE-AUTOMATED-HANDLING**: Handle Cloudflare Turnstile managed challenges programmatically: locate challenge iframes (`challenges.cloudflare.com`), traverse Shadow DOM nodes, simulate humanized multi-step cursor approaches to `#challenge-stage`, and poll `input[name="cf-turnstile-response"]` until a valid cryptographic token (> 20 chars) is populated.
- **BEHAVIORAL-BIOMETRICS**: Keystrokes MUST have non-deterministic inter-key delays (80–320 ms) with occasional typo correction patterns (Backspace sequence). Mouse movements MUST follow cubic Bézier curves with acceleration/deceleration inflection points and slight overshoots. Never use `page.fill()` or instantaneous property assignments.
- **HARDWARE-PROFILE-CONSISTENCY**: Match User-Agent, JA4/JA4T TLS client hello fingerprints, audio context dynamics, screen geometry, and system fonts. A Linux server kernel must never report a macOS Quartz font stack or Direct3D graphics adapter.
- **WEBRTC-LEAK-PREVENTION**: Bind WebRTC ICE candidates directly to the residential proxy IP or configure `disable_non_proxied_udp`. Prevent host IP disclosure through STUN/TURN queries.

## Suggested Process

1. **CDP Gateway Setup**: Launch the target Anti-Detect profile via local management API (e.g. AdsPower, Multilogin, Octo Browser) and obtain the CDP WebSocket debugger URL. Connect via `chromium.connectOverCDP()`.
2. **Fingerprint Consistency Verification**: Verify that the browser profile's WebGPU adapter attributes (`vendor`, `architecture`) match WebGL parameters, Canvas noise hashing produces identical hashes across calls within the session, and JA4 TLS fingerprints align with the OS profile.
3. **Behavioral Interaction Layer**: Wrap standard page actions (`click`, `type`, `scroll`) in behavioral helpers that generate cubic Bézier curves, natural wheel scrolling deceleration, and realistic typing pauses.
4. **Automated Turnstile Challenge Resolution**: Attach listeners for Cloudflare challenge iframes. Execute humanized targeting of the Turnstile interactive checkbox, wait for verification resolution, and extract the generated `cf-turnstile-response` token.
5. **Leak & Bot Score Validation**: Run automated test runs against CreepJS, Incolumitas, Pixelscan, and Cloudflare challenge sandboxes to confirm passing scores before production execution.
6. **Error Recovery & Session Persistence**: Implement session state checkpointing and automatic profile restart on proxy disconnects or platform checkpoint prompts.

## Checklist

- [ ] Automation connects strictly via CDP or uses C++ patched browser binaries (no raw Playwright launch).
- [ ] WebGPU adapter attributes and vendor strings match WebGL `UNMASKED_RENDERER_WEBGL`.
- [ ] Canvas 2D noise is mathematically continuous and deterministic per profile seed.
- [ ] Automated Turnstile challenge handler traverses Shadow DOM/iframe and polls `cf-turnstile-response`.
- [ ] Bézier/spline mouse curves and randomized 80–320 ms keystroke delays active.
- [ ] JA4/JA4T TLS fingerprints match the platform specified in User-Agent header.
- [ ] WebRTC ICE candidates bound to proxy IP; UDP leaks prevented.
- [ ] Profile passes CreepJS, Incolumitas, and Pixelscan without trust-score penalties.
- [ ] Session recovery logic handles network timeouts and anti-bot challenge prompts gracefully.

## Output Contracts

When developing, updating, or validating an automation script or browser stealth profile, emit:

- **`contracts/schemas/implementation-result.json`** — Emitted upon completing the implementation and validation of an automation script, stealth profile, or CDP integration slice, detailing changes made, files touched, anti-detect checks passed, and test verification results. Set `produced_by_role: mmo-engineer`.
- **`contracts/schemas/deployment-plan.json`** capturing the script path, runtime environment, credential handling, anti-detection posture, and rollback path.
- Markdown summary of script execution parameters, selector maps, and operational caveats.

Skip emission for local scratch testing of browser selectors.

## Failure Modes

- **Turnstile token polling timeout**: Cloudflare enters interactive captcha loop or fails to issue token. Mitigation: check IP fraud score; rotate to clean residential proxy subnet and re-trigger challenge approach.
- **WebGPU/WebGL fingerprint contradiction**: Declaring an Apple M3 GPU while WebGL reports Google SwiftShader triggers immediate anti-fraud flagging. Mitigation: validate GPU vendor and renderer alignment prior to navigation.
- **Canvas noise discontinuity**: Non-deterministic noise injection changes pixel hashes on identical frames, alerting fraud detectors. Mitigation: use deterministic PRNG seeded by profile ID for noise generation.
- **Biometric behavioral detection**: Instantaneous clicks or linear cursor movements flag headless automation. Mitigation: enforce Bézier curves with speed variation and micro-overshoots.
- **WebRTC leak exposing host IP**: Host datacenter IP leaks during peer connection negotiation. Mitigation: force remote proxy routing on WebRTC ICE candidates or disable non-proxied UDP.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: Maliciously crafted DOM elements or injected third-party scripts must not redirect automation workflows; validate target URLs before proceeding.
- **ASI03 Identity & Privilege Abuse**: Platform credentials and session cookies must be fetched from encrypted secrets managers at runtime; never commit plain credentials in scripts.
- **ASI04 Supply Chain**: Browser automation drivers, CDP clients, and stealth libraries must be pinned to verified versions; audit third-party packages for malicious telemetry.
- **ASI05 RCE Guard**: Never construct CDP execution payloads, evaluation strings, or system shell calls directly from untrusted web page contents.
- **ASI07 Inter-Agent Communication**: Automation outputs and execution logs must conform to `contracts/schemas/implementation-result.json` for consumption by upstream orchestration agents.
- **ASI09 Human-Agent Trust Exploitation**: Always surface detection risks and platform checkpoint probabilities honestly rather than claiming absolute undetectability.

## Related Skills

- **deploy-mmo-infrastructure**: Provision and manage the Anti-Detect Browser profiles and proxy networks that scripts connect to.
- **turnstile-spin**: Handle Cloudflare Turnstile deployment and verification challenges in automation pipelines.
- Companion reference: `references/stealth-cdp-and-behavioral-mimicry.md`
- Companion example: `examples/stealth-browser-automation-flow.ts`
