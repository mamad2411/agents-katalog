---
name: codex-harness-agent
description: Comprehensive production guide and runner for OpenAI's Agents API, the managed Codex Cloud Harness, and Computer Use (CUA). Covers session state persistence, context compaction, execution environments (OpenAI cloud sandboxes, E2B, local PyAutoGUI/Playwright), multi-agent dispatch, and human-in-the-loop safety boundaries. Use when delegating autonomous tasks to OpenAI's managed harness, controlling GUI interfaces via Computer Use, or orchestrating hybrid multi-agent workflows.
aliases:
  - codex-harness-agent
  - openai-agents-api
  - codex-agent
  - computer-use-agent
  - cua-harness
category: "07 - Codebase Exploration & Tooling"
tags:
  - agent-skill
  - openai-agents
  - codex-harness
  - computer-use
  - stage-7
  - autonomous-agents
---

# Codex Harness Agent: OpenAI Agents API, Managed Cloud Runtime & Computer Use

This skill provides an enterprise engineering blueprint and production execution runner for OpenAI's **Agents API**, leveraging the **Codex Harness**—the battle-tested agentic execution runtime powering OpenAI Codex and Operator. It incorporates a **5-Pillar Enterprise Architecture** combining autonomous multimodal reasoning intelligence with zero-latency local physical hands on macOS.

---

## 5-Pillar Production Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│               CODEX HARNESS COMPUTER USE ENTERPRISE HUD                │
├────────────────────────────────────────────────────────────────────────┤
│ [Red/Yellow/Green]    Computer Use Mini Display   [Take Over] [⌘K]     │
├────────────────────────────────────────────────────────────────────────┤
│ ┌────────────────────────────────────────────────────────────────────┐ │
│ │                                                                    │ │
│ │                     Live Desktop Mini Preview                      │ │
│ │              (Apple Neural Vision OCR Bounding Box)                │ │
│ │                                                                    │ │
│ └────────────────────────────────────────────────────────────────────┘ │
│ ┌─ Filmstrip History (Last 6 Action Snapshots) ──────────────────────┐ │
│ │ [ Frame 1 ] [ Frame 2 ] [ Frame 3 ] [ Frame 4 ] [ Active Frame ]   │ │
│ └────────────────────────────────────────────────────────────────────┘ │
│ Status Pill: [Spinner] Working... Clicking 'Table Editor' [Approve/Deny]│
│ Command Input: [ ⌘K Type command or press ⌥Space to focus...         ] │
└────────────────────────────────────────────────────────────────────────┘
```

1. **Pillar 1: Autonomous Closed-Loop VLM ReAct Engine (`codex_vision_loop.py`)**:
   - Executes multi-turn "Perceive–Think–Act–Observe" cycles.
   - Structured 9-primitive `computer_use` tool schema: `click`, `double_click`, `right_click`, `move`, `drag`, `type`, `press_key`, `scroll`, `wait`, `takeover`, `done`.
   - Native CoreGraphics event synthesis for mouse glide curves and typing cadences.
2. **Pillar 2: Universal Coordinate Normalization Engine (`coordinate_transformer.py`)**:
   - Deterministic bidirectional coordinate mapping across Model Space `[0..1000, 0..1000]`, macOS Logical Points `(pt_x, pt_y)`, and Physical Retina Pixels `(px_x, px_y)`.
   - Dynamic AppKit `backingScaleFactor` detection (2.0x Retina scaling) and multi-display coordinate virtualization.
3. **Pillar 3: Triple Hybrid Grounding (AXTree v2 + Apple OCR + VLM Coordinates)**:
   - *Layer 1 (Fast Path)*: Swift Native Accessibility Scanner v2 (`ax-scanner`) with in-memory element tree caching (< 5ms UI queries).
   - *Layer 2 (Text Path)*: Apple Silicon Neural Vision OCR (`VNRecognizeTextRequest`) running on local Neural Engine (< 15ms).
   - *Layer 3 (Visual Path)*: Multimodal VLM bounding box coordinates for iconographic and unlabelled visual targets.
4. **Pillar 4: Human Takeover Mode & Sensitive Field Privacy Shield**:
   - Dedicated `[ Take Over ]` and `[ Resume AI ]` buttons on the Mini Display HUD.
   - Automated detection of sensitive credential fields (`AXSecureTextField`, password/token queries).
   - Hardware-level screenshot capture suspension during human credential entry.
5. **Pillar 5: Sliding-Window Visual Context Compaction & Session Ledger**:
   - Retains only baseline Frame 0 + Frame N-1 + Frame N with active image payloads.
   - Compresses frames (< 150 KB JPEG/WebP) and rolls older turns into structured Markdown summaries.
   - Guarantees token consumption stays strictly under 40,000 tokens across 20+ turn tasks.
   - Persists complete audit trail to `~/.codex/sessions/<session_id>.md`.

---

## Quick Invocation & Shortcuts

### 1. In AI Chat (Antigravity & Cursor)
- **`/codex <task>`**: Dispatches task to the Codex Harness.
- **`/cua <task>`** or **`/cua <url>`**: Triggers visual Computer Use with persistent Mini Display HUD.
- **Natural Language Triggers**:
  - "สั่ง codex ทำ..."
  - "รันบน codex harness..."
  - "ใช้ computer use ตรวจสอบหน้าเว็บ..."
  - "รันงานระยะยาวบนคลาวด์..."

### 2. From Terminal (Global CLI Shortcut)
```bash
# Run autonomous visual Computer Use on macOS Desktop or Web (with persistent HUD)
codex-agent --gui "เปิด Safari ไปดู YouTube แล้วค้นหา อนันเป็ด"

# Run with custom model and maximum step constraints
codex-agent --gui --model google/gemini-2.5-flash --steps 20 "Inspect schema in Supabase"

# Directly trigger Apple Silicon Neural Vision OCR Grounding for text on screen
codex-agent --ocr "Safari"

# Run a task via native Codex CLI in an isolated worktree
codex-agent --worktree "Refactor auth middleware and verify tests"

# Cloud mode via OpenAI Agents API
export OPENAI_API_KEY="sk-..."
codex-agent --cloud "Run full overnight stress testing"
```

---

## 1. Architecture Overview: Managed Codex Harness vs. Client SDK

```
┌────────────────────────────────────────────────────────────────────────┐
│                   AGENT EXECUTION RUNTIME COMPARISON                   │
├────────────────────────────────┬───────────────────────────────────────┤
│ Client-Side Loop (Agents SDK)  │ Managed Cloud Loop (Codex Harness)    │
├────────────────────────────────┼───────────────────────────────────────┤
│ • Local Python/Node process    │ • OpenAI-managed serverless container │
│ • Local machine memory/state   │ • Durable session state persistence   │
│ • Manual context truncation    │ • Autonomous context compaction       │
│ • Client handles tool recovery │ • Built-in self-healing and recovery  │
│ • Stops if laptop closes       │ • Continues executing asynchronously  │
│ • Local OS / Docker runtime    │ • Native Cloud Sandbox & Computer Use │
└────────────────────────────────┴───────────────────────────────────────┘
```

### The Three Operational Layers:
1. **The Codex Harness**: The internal execution engine developed by OpenAI for Codex and Operator. It manages the agentic loop (Reasoning -> Tool Call -> Observation -> Reflection), state checkpointing, error recovery, and automatic context compaction so sessions never hit context window hard limits.
2. **The Agents API (Cloud Control Plane)**: A managed API service exposing the Codex Harness as a first-class developer primitive. Developers create an agent, define tools (including Computer Use and Bash), start a session, and dispatch long-lived tasks.
3. **Execution Sandboxes (The "Hands")**: Where tool actions actually run:
   - **OpenAI-Hosted Sandboxes**: Ephemeral or persistent Linux micro-VMs managed by OpenAI.
   - **Local Workstation Desktop (HUD)**: Native Swift 6 Mini Display (`computer-use-hud`) and Ghost Cursor overlay with Apple Vision OCR.

---

## 2. Safety Boundaries & Guardrails

> [!CAUTION] Mandatory Safety Boundaries
> Agents executing OS-level actions or browsing the open web must be strictly constrained:

1. **Non-Privileged Execution**: Never run computer-using agents as root or with administrative OS privileges.
2. **Interactive Human Approval Gate**: Destructive actions (database drops, git force-pushes, financial payments, account deletions) require clicking `[ Approve ]` on the Mini Display HUD.
3. **Sensitive Data Privacy Shield**: Screen captures are paused and masked when touching credentials, password inputs, or payment cards.
4. **Domain Whitelisting**: When browsing, enforce network proxy rules allowing only required application domains (e.g. `localhost`, `staging.internal`, `github.com`).

---

## 3. Verification Checklist Before Marking Work Complete

- [ ] Has the target mode (`native`, `cua`, `hybrid`, `cloud`) been explicitly declared?
- [ ] Is `computer-use-hud` persistent and responsive to `/tmp/cua_hud.pipe`?
- [ ] Did Apple Silicon Vision OCR and AXTree detect the target GUI elements reliably?
- [ ] Are safety guardrail approval gates active for critical/destructive actions?
- [ ] Did the agent capture evidence (screenshots or logs) proving task completion?

---

## 🔗 Connected Skills

- [[Skills/subagent-driven-development/SKILL|subagent-driven-development]] — Task decomposition and subagent coordination
- [[Skills/sdk/SKILL|sdk]] — Cursor Agent SDK and programmatic agent runtime patterns
- [[Skills/playwright-cli/SKILL|playwright-cli]] — Browser automation and UI test execution
- [[Skills/determine_threat_model/SKILL|determine_threat_model]] — Threat modeling and attack surface isolation
- [[Skills/review-security/SKILL|review-security]] — Security review and safety boundary enforcement
- [[Skills/verification-before-completion/SKILL|verification-before-completion]] — Evidence-based verification without assumptions

<!-- v2.0.0 synchronized: 2026-10-01 -->
