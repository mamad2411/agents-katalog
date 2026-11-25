---
name: agent-browser-visual
description: "[INTERNAL TEMPLATE] Visual evidence capture and regression testing protocol. Called by agent-browser orchestrator."
---

# Visual Evidence & Regression — Execution Protocol

> **Internal template.** Entry point: `agent-browser` skill.

---

## NEVER

```
NEVER compare screenshots before `wait --load networkidle` — animation frames cause false diffs
NEVER use default diff threshold for pixel-perfect checks — set --threshold 0.05 or lower
NEVER skip baseline update after intentional UI changes — stale baseline = false positives forever
NEVER start `network har start` after navigation — HAR must begin before the requests you want to capture
NEVER start `record start` before opening the page — start after `open` + `wait` to preserve auth state
```

---

## Use Case Decision Tree

| Goal | Command |
|:---|:---|
| Catch visual regression (before/after deploy) | `diff screenshot --baseline` |
| Compare staging vs production side by side | `diff url` |
| Detect DOM structure changes | `diff snapshot` |
| Create shareable demo / bug report video | `record start` → actions → `record stop` |
| Annotated screenshot for docs / ticket | `screenshot --annotate` |
| Capture full network trace for perf/debug | `network har start` → actions → `network har stop` |

---

## Visual Regression Workflow

```bash
# Step 1: Capture baseline (run once before changes)
agent-browser open <url>
agent-browser wait --load networkidle
agent-browser screenshot --full baseline.png

# Step 2: After changes, compare
agent-browser open <url>
agent-browser wait --load networkidle
agent-browser diff screenshot --baseline baseline.png --output diff.png --threshold 0.1

# Step 3: Scope to specific element (reduces noise from unrelated areas)
agent-browser diff screenshot --baseline baseline.png -s "#main-content"

# Step 4: Compare two environments (snapshot + optionally screenshots)
agent-browser diff url https://staging.example.com https://prod.example.com
agent-browser diff url https://staging.example.com https://prod.example.com --screenshot --full
```

**Threshold guide:**
- `0.1` (default) — tolerates antialiasing, minor rendering differences
- `0.05` — catches subtle color/font changes
- `0.01` — pixel-perfect (sensitive to any rendering difference)
- `0.2` — forgiving mode for dynamic content areas

---

## Video Recording Workflow

```bash
# Best practice: open page first, then start recording (preserves auth state)
agent-browser open <url>
agent-browser wait --load networkidle
agent-browser snapshot -i            # explore first, plan your actions
agent-browser record start ./demo.webm
# ... perform actions ...
agent-browser record stop

# Record from a fresh URL
agent-browser record start ./onboarding.webm https://app.example.com/signup

# Restart (stop current recording, start new — useful for retakes)
agent-browser record restart ./take2.webm
```

> To convert WebM → GIF: `ffmpeg -i demo.webm -vf "fps=10,scale=800:-1:flags=lanczos" demo.gif`

---

## Annotated Screenshot

```bash
agent-browser screenshot --annotate step1.png
```

Output: screenshot with numbered labels overlaid + a legend mapping each number to its element name.

Ideal for: bug reports, documentation, sharing context with non-technical reviewers. The annotation labels survive screenshot compression better than cursor overlays.

---

## HAR Recording (full network trace)

```bash
# Must start BEFORE navigation to capture all requests
agent-browser network har start ./trace.har
agent-browser open <url>
agent-browser wait --load networkidle
# ... perform actions you want to trace ...
agent-browser network har stop

# View: open in browser DevTools → Network tab → Import HAR
# Or: https://har.tech (online analyzer)
```

Use when: diagnosing slow pages, verifying API calls, auditing third-party requests.

---

## DOM Snapshot Diff

```bash
# Compare current DOM vs last snapshot in this session
agent-browser diff snapshot

# Compare against a saved snapshot file
agent-browser diff snapshot --baseline before.txt

# Scope to a specific section
agent-browser diff snapshot -s ".sidebar" -c

# Combined: compact + depth-limited scope
agent-browser diff snapshot -s "#app" -c -d 4
```

Use when: verifying a code change didn't silently alter DOM structure, or checking that a UI component renders identically across environments.

---

## Recovery Patterns

| Failure | Recovery |
|:---|:---|
| Diff always shows changes (animation/loading) | `wait --load networkidle` + add `wait 500` for CSS transitions |
| Diff too sensitive (antialiasing noise) | Increase `--threshold 0.2` |
| Diff misses real regression | Decrease `--threshold 0.05` |
| Video file too large | Scope recording to shorter flow; use `screenshot --full` for static evidence |
| HAR missing early requests | Restart: `network har start` must be called before `open` |
| `record` loses auth state | Always `open` + `wait` first, then `record start` (no URL arg) |

---

## Pitfalls

| Mistake | Fix |
|:---|:---|
| Screenshot before page is stable | `wait --load networkidle` before any capture |
| Baseline not updated after intentional design change | Delete old baseline, re-capture: `screenshot --full baseline.png` |
| `diff screenshot` without `--baseline` | `--baseline <file>` is required |
| HAR started after XHR calls already fired | `network har start` must come before `open` or `reload` |
| `record start` before page open loses auth | Open page + wait first, then start recording |
