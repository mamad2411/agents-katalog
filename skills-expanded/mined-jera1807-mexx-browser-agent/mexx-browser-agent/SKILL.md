---
name: mexx-browser-agent
description: >-
  Interact with the user's active Google Chrome browser in real time without stealing focus or interrupting work.
  Use when reading data from background tabs, extracting WebGL/WebGPU/Canvas buffers, controlling HTML5 video/audio,
  inspecting network requests via chrome.debugger, filling forms, or executing sub-second multi-step browser workflows.
---

# MEXX-Browser-Agent Skill
*(formerly Live Browser Copilot)*

> **Golden Rule:** This tool operates as a **Human-in-the-Loop Autonomous Agent & Copilot**, NOT a headless scraper. Always respect user coexistence: **Never switch tabs or steal window focus** unless explicitly requested by the user.

---

## When to Use This Skill vs. Others
* **Use `live-browser-copilot`** when the user wants you to inspect, read, navigate, click, or extract data from their **real, daily-driver browser** where existing logins (Google, Notion, Slack, Drive, Datacamp) and active tabs already reside.
* **Do NOT use standard Puppeteer/Playwright** when the user is actively working at the computer, as those tools hijack the OS window focus and cause focus-loss crashes.

---

## Installation & Setup

One line, everything included (clone, install, build, launch). Requires Node.js 20+ and Google Chrome:

```bash
git clone https://github.com/Jera1807/mexx-browser-agent.git && cd mexx-browser-agent && npm install && npm start
```

What this sets up automatically: a 256-bit bridge token (synced into the extension), Chrome launched with the extension pre-loaded, MCP registration in Claude Desktop (if installed), and the live bridge (WebSocket `:8910`, REST `:8911`). No code changes needed — all tools below work out of the box afterwards.

---

## Core Capabilities & Tool Matrix

### 1. Silent Background Tab Reading (`browser_read_tab`)
* **Purpose:** Extract clean text, title, and DOM structure from **any background tab** while the user works unhindered in the foreground.
* **Parameters:** `{ query: "merdeka" }` or `{ tabId: 12345 }`
* **Latenz:** ~20–50 ms.
* **Rule:** If the user asks *"What does that article in my other tab say?"*, query `browser_read_tab` by keyword or tab ID. Do NOT call `switchTab`.

### 2. Canvas, WebGL & WebGPU Buffer Extraction (`browser_extract_canvas`)
* **Purpose:** Extract internal 2D/3D framebuffers and hardware telemetrie from HTML5 Canvas elements.
* **Parameters:** `{ selector: "canvas", query?: string }`
* **What it extracts:**
  * Context type (`2d`, `webgl`, `webgl2`, `webgpu`).
  * WebGPU hardware limits (`maxBufferSize`, `maxTextureDimension2D`, `vendor`, `architecture`).
  * Direct 32-bit RGBA PNG/JPEG image buffer from browser memory (`toDataURL` or OffscreenCanvas sniper).
  * Underlying chart datasets if Chart.js is present.

### 3. Sub-Pixel Element Sniper (`browser_capture_screenshot`)
* **Purpose:** Capture a pixel-perfect image of an isolated DOM element or the active viewport.
* **Parameters:** `{ selector: "#target-element" }` (optional)
* **How it works:** Automatically centers the element, retrieves bounding box coordinates with device pixel ratio (Retina/DPR) compensation, and crops via `OffscreenCanvas`.

### 4. Low-Level CDP & Network Telemetry (`browser_debugger_cmd`, `browser_get_network_log`)
* **Purpose:** Execute raw Chrome DevTools Protocol commands without requiring `--remote-debugging-port`.
* **Tools:**
  * `browser_debugger_cmd`: `{ method: "Performance.getMetrics", query?: string }` or `{ method: "Network.enable" }`.
  * `browser_get_network_log`: `{ query?: string, limit?: 50 }` returns intercepted requests, HTTP status codes, MIME types, and timing.

### 5. Media & Video Controller (`browser_media_control`)
* **Purpose:** Inspect and control HTML5 `<video>` or `<audio>` elements (YouTube, streaming media, animations).
* **Parameters:**
  * `command`: `"play" | "pause" | "seek" | "playbackRate" | "state" | "captureFrame"`
  * `time`: Target second for seeking.
  * `rate`: Speed multiplier (e.g. `1.5`, `2.0`).
* **Frame Snapping:** `"captureFrame"` captures the video frame at the exact millisecond as an image.
* **Captions:** Returns live active subtitles (`activeCue`) from `textTracks`.

### 6. Semantic Interaction (`browser_click`, `browser_fill`)
* **Self-Healing Matching:** Resolves elements across 6 tiers: ARIA labels, associated `<label for>`, proximity/sibling matching, SVG icon titles, inner text, and interactive roles.
* **Universal Rich-Text Engine:** Handles standard inputs as well as `contenteditable="true"` editors (Lexical, ProseMirror, TipTap, CodeMirror, Slack, Notion, ChatGPT, Gmail, Google Docs) via native `execCommand("insertText")` and synthetic input lifecycle events.

### 7. Deadlock Protection & Execution Timeout
* **Resilient Timeout:** All actions and screenshots enforce a default **5,000 ms timeout** (configurable per action via `timeoutMs`).
* **Clean Error Handling:** If a page freezes or runs an infinite JavaScript loop, the bridge aborts the pending request, returns **HTTP 504 Gateway Timeout** with structured diagnostics, and remains 100% responsive for subsequent commands.
* **Parallel Swarm Batching:** Supports `parallel: true` in `GoalRunner` to execute multi-tab workflows concurrently with <100MB RAM overhead.

### 8. Security V2: Deterministic Governance & Human-in-the-Loop
* **Deterministic Risk Classes (R0–R4):**
  * `R0`: Read-only inspection (`readTab`, `listTabs`, `getNetworkLog`, `extractCanvas`, `deepDomSnapshot`). No approval needed.
  * `R1`: Passive navigation / media control (`scroll`, `switchTab`, `mediaControl`). No approval needed.
  * `R2`: Standard harmless text entry & non-destructive clicks. No approval needed.
  * `R3`: Destructive mutations (`delete`, `remove`, `drop`, `cancel subscription`). Requires human approval.
  * `R4`: High-risk domains (banking, crypto, payment gateways like Stripe/PayPal/Klarna, auth provider injections). Requires human approval.
* **Human Approval Gate:** The agent cannot autonomously bypass approvals (`force: true` is strictly prohibited). Destructive or sensitive actions trigger a cryptographic proposal. The user must explicitly approve in the Extension Popup or via `/security/approve`, generating an ephemeral 30-second single-use `approvalToken`.
* **TOCTOU & Replay Protection:** Tokens are cryptographically bound to the canonical SHA-256 hash of the action and current URL. Tampering with parameters or reusing tokens results in immediate rejection.
* **Emergency Kill Switch:** A physical red button in the Chrome extension popup immediately severs WebSocket connections, revokes all tokens, detaches debuggers, and blocks all subsequent actions.
* **Append-Only Audit Trail:** Every action and approval is recorded in `audit.jsonl` with client- and server-side secret redaction (credit cards, IBANs, API keys, JWTs).

### 9. Event-Driven Sleep/Wake Engine (V3)
* **Zero Token Cost While Waiting:** The agent calls `browser_wait_for_event` and pauses execution asynchronously. No tokens are consumed during the wait window.
* **Local In-Browser Matching:** `content.js` monitors DOM mutations with microtask batching (`queueMicrotask`) and stability window (150ms anti-flapping). Only when an actual match is verified does the extension notify the bridge.
* **Instant Match Check:** If the match condition is already satisfied in the DOM when the subscription is created ("match now or in the future"), the agent is woken up immediately.
* **Supported Event Types:** `DOM_APPEAR`, `DOM_CHANGE`, `TEXT_MATCH`, `NAVIGATE`, `DOWNLOAD_COMPLETE`.
* **Security & Secret Redaction:** Target snippets in event payloads are automatically sanitized through `sanitizeSecrets()` before delivery. Targeting password fields or using pathological regex patterns (ReDoS) is strictly rejected.
* **REST & SSE Endpoints:** `POST /events/subscribe`, `POST /events/unsubscribe`, `POST /events/wait`, `GET /events/subscriptions`, `GET /events/stream` (Server-Sent Events).

### 10. Shared Browser World State & Context Compression (Baustein 7)
* **Semantic Context Compression (50 vs. 50,000 Tokens):** Instead of dumping the raw DOM, `content.js` continuously extracts an ultra-compact semantic state (~50–80 tokens) per tab:
  * **Modals:** Score-based evidence evaluator (`role="dialog"`, `<dialog open>`, `aria-modal="true"`, z-index/backdrop, confidence).
  * **Auth:** Evidence-based status (`authenticated` | `unauthenticated` | `unknown`, confidence, evidence).
  * **Dirty Forms:** Native DOM `defaultValue` / `defaultChecked` detection with strict privacy (passwords, CC, secrets are never stored).
  * **Alerts & Primary CTA:** Active banners, toasts, and primary action buttons.
* **Monotonic Revisions & Navigation Epochs:** Strictly incrementing revision counter per tab. Page navigations emit `NAVIGATION_OCCURRED` and increment `navigationEpoch` without resetting revision history.
* **Differential State Queries (`GET /world-state/:tabId/diff?sinceRevision=N` / `browser_get_world_state`):** Returns only high-level semantic deltas (`MODAL_OPENED`, `FORM_DIRTY`, `ALERT_APPEARED`, etc.). If older deltas have been evicted from the 50-item ring buffer, triggers `resyncRequired: true` with full snapshot fallback.
* **Optimistic Locking (`expectedRevision`):** Mutating actions accept `expectedRevision`. If another agent or user modified the tab state in the meantime, the action fails deterministically with `409 CONFLICT_STALE_STATE` and returns current state.
* **Concurrency Leases (`POST /world-state/:tabId/lease` / `browser_acquire_lease`):** Multi-step critical sequences (e.g. checkout, payment) acquire an exclusive lease (`ttlMs: 5000–60000`). Other automated agents are locked out with `423 LEASE_LOCKED`.
* **Human Precedence Guarantee:** Any human interaction or Human Approval Gate execution immediately revokes active agent leases.

### 11. Behavior Memory & Macro Workflow Engine (Baustein 3 & 4) - v3.0 Hardened
* **Explicit Macro Recording ("Record first, parameterize second"):** Non-intrusive capture of user actions via extension (`POST /workflows/record/start` / `browser_record_workflow`). Generates rich **Target Fingerprints** (roles, accessible names, text anchors, context, and multi-tier candidate cascades: TestID > ARIA > Name > ID > Text > Clean CSS without dynamic hash classes).
* **Automatic Parameter & Secret Discovery (v3.0 Hardened):** Detects recurring values, email addresses, search terms, AND high-entropy secrets (API keys `sk_...`, GitHub tokens `ghp_...`, Slack tokens, JWTs, Credit Cards, IBANs) across **all normal form inputs**. Values are automatically converted to `${secret_var}` with `type: "secret", sensitive: true` and raw secrets are NEVER persisted in workflow definitions on disk.
* **Deterministic Replay (Zero Tokens, Millisecond Turnaround):** Workflows execute 100% deterministically via the Bridge (`POST /workflows/:id/run` / `browser_run_workflow`). Dynamic runtime parameter interpolation (`{ searchQuery: "Telekom August 2026" }`).
* **R-Class Precedence & Anti-Collision:** Risk checks run strictly **before** modal dismissal. Dialogs containing destructive (`DESTRUCTIVE_KEYWORDS`) or financial (`FINANCIAL_KEYWORDS`) triggers are NEVER auto-dismissed.
* **Non-Critical Interstitial Dismissal:** Safely dismisses cookie consent banners (prioritizing "nur notwendige / ablehnen" for DACH compliance) and newsletter overlays via ESC key or safe buttons. Blocked keywords prevent clicking destructive confirmation buttons.
* **Critical Modal Safety Gate:** Destructive or confirmation modals ("Wirklich löschen?", "Bestellung bestätigen") immediately pause execution with HTTP 428 (`approvalRequired: true`) for human review.
* **Target Identity Binding (TOCTOU Defense):** Direct pre-action verification that the resolved target element has not vanished, mutated, or been obscured by an overlay immediately prior to click or fill execution.
* **Risk-Gated Self-Healing & Ambiguity Hard-Stop:**
  * **R0 / R1 Actions:** Autonomic healing searches DOM for semantic substitute. **Ambiguity Hard-Stop:** If multiple candidates match closely (`candidateCount > 1`), autonomous guessing is strictly forbidden — execution halts for human review (`ambiguous: true`).
  * **R2 / R3 Actions:** Strictly HALTS execution and triggers Human Approval Gate. Autonomic execution on altered high-risk targets is forbidden.
* **Anti-Poisoning Staged Repairs (`POST /workflows/:id/promote-repair` / `browser_promote_repair`):** Healed targets are saved to `stagedRepairs` and only promoted to the active workflow version (`version++`) after verified success.
* **Tab Management (`closeTab`):** Passive R1 action to safely close background or bloated tabs (`action: { kind: "closeTab", tabId }`) without focus loss.
* **REST Endpoints:** `GET /workflows`, `POST /workflows/record/start`, `POST /workflows/record/stop`, `GET /workflows/:id`, `DELETE /workflows/:id`, `POST /workflows/:id/run`, `POST /workflows/:id/stage-repair`, `POST /workflows/:id/promote-repair`.

### 12. Robust Third-Party UI Automation Playbook (for every agent)

> You are driving a live UI **blind**: you get text snapshots, not pixels. Every step is fire-and-forget. These rules are mandatory — they turn guessing into engineering.

**Priority rule (wins every conflict):** user safety → no duplicate or destructive actions → state verification → task completion → speed. Never sacrifice verification for speed. Concretely: if "work in parallel" collides with "verify first", verification wins; if "keep going" collides with "ambiguous target", stopping wins.

**12.1 Tab discipline**
* **Reuse before you open:** Always list tabs first (`browser_list_tabs` / `GET /world-state`). A tab fits if URL and page context match the task (same conversation, same document, same domain + task-relevant title). If several fit, prefer the one already holding the needed state; if none fits, open a new one.
* **Background by default:** Open with `active: false`. Do not steal focus unless the UI requires it (e.g. focus-gated inputs) or the user explicitly asked.
* **Close policy (default, no asking needed):** You may close tabs you opened yourself if they are background tabs without user history. Never close tabs with user history, user-typed content, or tabs you did not open — there, ask first. When in doubt, leave it open and say so.

**12.2 Verify after every write (no fire-and-pray)**
* After each `fill`, read back and verify with this tolerance: normalize whitespace on both sides, then require the normalized prefix to match and the length to agree within ±10%. Only then proceed.
* **Idempotency first:** before any retry of a submit, check whether the first attempt already succeeded (conversation URL changed, message appears in history, editor emptied). A false-negative verify followed by a blind re-click sends duplicates.
* After each `click` on Send/Submit, verify the effect: new URL (`/chat/...`, `/c/...`), editor emptied, or a pending/streaming indicator appeared.
* If verification fails, diagnose once (see 12.5) instead of blindly retrying the same step.

**12.3 Separate fill and submit — always**
* Rich-text editors (ProseMirror, TipTap, Lexical, CodeMirror — e.g. Claude, ChatGPT, Notion, Slack) need two distinct steps:
  1. `fill` with `submit: false`, then verify content landed.
  2. Separate `click` on the send button (or `pressKey Enter`), then verify it sent.
* Never combine long text + auto-submit in one call on a freshly loaded page: the editor may not be ready and only a fragment gets sent.
* **Ambiguous targets:** if several elements match (e.g. two Send buttons), never guess — disambiguate via context (container, form, aria-label) first; if still ambiguous, stop and ask.

**12.4 Wait correctly: read first, guess never**
* A wait trigger is **known-good** only if it comes from a prior read of this session, from the task specification, or from verified product behavior — never a word you hope an unseen answer will contain. A wrong pattern means waiting the full timeout for nothing.
* Decision tree:
  1. **Read state first.** The answer may already be there.
  2. **Known trigger text** (e.g. an order number, a status string from the task) → event-driven wait (`browser_wait_for_event` / `POST /events/wait`). This costs zero tokens while waiting.
  3. **Unknown trigger** (e.g. free-form AI answer) → poll with cheap reads on an adaptive schedule (start ~15s, back off to ~60s), with a hard maximum (default 5 minutes). When the maximum is hit, that counts as failure → go to 12.5, do not extend silently.
* Prefer structural signals over text guessing where available (streaming/stop indicator present/absent, URL changed to a conversation URL, message count increased).
* **Stale UI:** re-read state immediately before any critical or destructive click — the DOM may have changed between your last read and now.

**12.5 Diagnose stalls, then escalate (decision tree)**
* Message sent but no answer? Check quickly: send button enabled/disabled? Streaming/stop indicator present? Error or rate-limit banner? Login wall, expired session, 2FA, CAPTCHA, or modal open (`browser_get_world_state`: `activeModal`, `alerts`)?
* Then decide:
  1. Cause found and safely fixable (e.g. text still unsent in editor) → fix once, re-verify.
  2. Cause found but not fixable by you (login wall, CAPTCHA, payment gate, destructive ambiguity) → stop and inform the user. These are never bypassed.
  3. No cause found → one alternative attempt with a different method (e.g. click instead of Enter), then stop and report.
* **Approval gates are live moments:** when your action triggers a human-approval gate (R3/R4), tell the user IMMEDIATELY — what is waiting, where to approve (OS notification + extension popup), and what happens next. Never silently move on; the token expires in 30 seconds.
* **Escalation rule:** after two failed diagnose-and-fix cycles, stop and report to the user with findings. Endless retries are forbidden. Waiting longer fixes none of the above.

**12.6 Work in parallel, report progress**
* Run independent operations in parallel when they do not share mutable UI state or interfere with each other (typically: different tabs/targets). Parallel writes to the same tab are forbidden — they race with the fill → verify → submit sequence from 12.3.
* Treat long flows as a UX nicety: if your runtime supports progress messages, send a short one for any flow past ~60 seconds. Silence for minutes reads as "stuck".

**Risk coupling:** this playbook does not replace the R0–R4 risk firewall — it runs on top of it. Destructive or financial actions (delete, buy, publish, real submits beyond chat answers) additionally require the applicable approval gate; when the two conflict, the stricter rule wins.

**Anti-patterns (do NOT do these):**
* Opening a duplicate tab when a usable one already exists.
* `fill` with auto-submit on a just-opened page, then assuming it sent.
* Event-waiting on a keyword you hope the answer will contain.
* Fixed multi-minute sleeps instead of state checks.
* Closing user tabs for "tidiness" without asking.
* Retrying a submit without checking whether the first attempt already succeeded.


---

## Standard Workflows & Recipes

### Recipe A: Multi-Tab Research & Synthesis
```javascript
// 1. List tabs to identify candidate background tabs
const tabs = await callTool("browser_list_tabs", {});

// 2. Read background tab silently
const tabData = await callTool("browser_read_tab", { query: "wikipedia" });

// 3. Synthesize and present information to the user without ever touching the foreground tab
```

### Recipe B: Visual Model / Canvas Extraction
```javascript
// 1. Inspect canvas and probe GPU limits
const canvasInfo = await callTool("browser_extract_canvas", { selector: "canvas", query: "threejs" });

// 2. If canvas buffer is needed, retrieve base64 dataUrl directly from RAM
```

### Recipe C: Automated Multi-Step Goal (`POST /goal`)
When executing a sequence of 3–5 rapid actions:
* Send a structured plan to `http://127.0.0.1:8911/goal`:
```json
{
  "goal": "Verify facts across tabs",
  "steps": [
    { "thought": "Extract Wikipedia facts", "action": { "kind": "readTab", "query": "Merdeka" } },
    { "thought": "Verify Three.js GPU limits", "action": { "kind": "extractCanvas", "query": "threejs" } }
  ]
}
```
* Execution turnaround: ~100–200 ms total.

### Recipe D: Ask an AI Chat UI (Claude / ChatGPT / etc.)
```javascript
// 1. Reuse an existing chat tab if one is open — else open a background tab
const tabs = await callTool("browser_list_tabs", {});
// open only if needed: browser_open_tab { url: "https://claude.ai/new", active: false }

// 2. Locate the editor (usually div[contenteditable] / #prompt-textarea) and FILL WITHOUT submit
await callTool("browser_fill", { selector: "#prompt-textarea", value: promptText, submit: false });

// 3. VERIFY the text landed (length/head) before sending
// 4. Click Send separately, then verify it sent (conversation URL, editor empty, streaming indicator)
// 5. READ FIRST — the answer may already be there. Only then wait:
//    known trigger text -> browser_wait_for_event; unknown free-form answer -> poll reads.
```
