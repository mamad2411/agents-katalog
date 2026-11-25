---
name: agent-browser-scrape
description: "[INTERNAL TEMPLATE] Data extraction execution protocol. Called by agent-browser orchestrator."
---

# Data Extraction — Execution Protocol

> **Internal template.** Entry point: `agent-browser` skill.

---

## NEVER

```
NEVER `eval` before `wait --load networkidle` — JS-rendered content won't exist yet
NEVER assume lightpanda handles JS-heavy pages — always have a --engine chrome fallback ready
NEVER scrape without checking `get count` first — validates that your selector found items
```

---

## Execution Sequence

```bash
# 1. Try lightpanda first (fastest, no JS overhead)
AGENT_BROWSER_ENGINE=lightpanda agent-browser open <url>
AGENT_BROWSER_ENGINE=lightpanda agent-browser wait --load networkidle

# 2. Understand structure
AGENT_BROWSER_ENGINE=lightpanda agent-browser snapshot -c

# 3. Verify selector finds items before extracting
AGENT_BROWSER_ENGINE=lightpanda agent-browser get count ".item"

# 4. Extract
AGENT_BROWSER_ENGINE=lightpanda agent-browser eval "[...document.querySelectorAll('.item')].map(el => ({
  name: el.querySelector('h2')?.textContent?.trim(),
  price: el.querySelector('.price')?.textContent?.trim()
}))"

# 5. If empty/wrong → fallback to chrome engine
agent-browser open <url>
agent-browser wait --load networkidle
agent-browser get count ".item"    # verify selector still works
agent-browser eval "<same query>"
```

> **Note on `AGENT_BROWSER_NATIVE=1`:** This env var was used in older workflows as a shorthand for the Rust daemon. In 0.22+, the daemon is always active — use `AGENT_BROWSER_ENGINE=chrome` (or just default) instead. `AGENT_BROWSER_NATIVE=1` is still accepted but no longer documented.

---

## Pagination Handling

```bash
# Scroll-based infinite scroll
agent-browser scroll down
agent-browser wait --load networkidle
agent-browser get count ".item"    # check if count increased
agent-browser eval "<extract again>"
# Repeat until count stops increasing

# Click-based pagination
agent-browser find role button click --name "Next"
agent-browser wait --load networkidle

# Wait for specific text to confirm page loaded
agent-browser wait --text "Page 2 of"
```

---

## Output Parsing Tips

```bash
# Add --content-boundaries to help parse output when using --max-output
AGENT_BROWSER_CONTENT_BOUNDARIES=1 agent-browser eval "<query>" --max-output 50000

# JSON output for structured parsing
agent-browser get text @e1 --json
agent-browser snapshot -i --json
```

---

## Anti-Bot Bypass

```bash
# Level 1: custom user-agent
agent-browser --user-agent "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" open <url>

# Level 2: disable automation detection (combine with level 1)
agent-browser \
  --user-agent "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
  --args "--disable-blink-features=AutomationControlled" \
  open <url>
```

---

## Recovery Patterns

| Failure | Recovery |
|:---|:---|
| lightpanda returns empty | Switch to `--engine chrome` (or default) |
| Detected as bot | Add `--user-agent`, then combine with `--args` |
| `eval` before content loads | `wait --load networkidle` before every `eval` |
| Infinite scroll not handled | `scroll down` + re-`eval` loop, check `get count` for progress |
| Output truncated | Add `--max-output 100000` or `AGENT_BROWSER_MAX_OUTPUT` env |

---

## Judgment Gates

Pause when:
- Anti-bot measures block all approaches (CAPTCHA requires human)
- `get count` returns 0 after fallback — show `snapshot -c` to user, ask how to identify items

---

## Pitfalls

| Mistake | Fix |
|:---|:---|
| lightpanda returns empty | Switch to `--engine chrome` |
| `eval` before load | `wait --load networkidle` first |
| Bot detected despite `--user-agent` | Add `--args "--disable-blink-features=AutomationControlled"` |
| Extracted 0 items silently | Always `get count "<selector>"` before `eval` |
| Output cut off mid-JSON | Increase `--max-output` or use `--content-boundaries` |
