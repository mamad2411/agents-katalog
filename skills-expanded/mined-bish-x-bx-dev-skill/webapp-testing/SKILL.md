---
name: webapp-testing
description: Toolkit for interacting with and testing web applications using cmux browser. Supports verifying frontend functionality, debugging UI behavior, and inspecting page state.
license: Complete terms in LICENSE.txt
---

# Web Application Testing

## cmux browser reference

**Read `../../references/cmux-browser.md` for the full cmux browser reference** (commands, type vs fill, viewport, React forms, troubleshooting, best practices).

## Decision Tree

```
User task → Is the server already running?
    ├─ No → Start the server first (npm run dev, python server.py, etc.)
    │        Then open cmux browser to the local URL
    │
    └─ Yes → Open cmux browser and test:
        1. Open browser → get surface ID
        2. Wait for page load
        3. snapshot -i → read DOM, note element refs (e1, e2, etc.)
        4. Interact: click, type, fill
        5. snapshot -i again → verify results
        6. CLOSE browser when done
```

## Full Workflow Example

```bash
# 1. Open browser (uses $CMUX_WORKSPACE_ID automatically)
RAW=$(cmux browser open http://localhost:5173)
SURFACE=$(echo "$RAW" | grep -o 'surface:[0-9]*' | head -1)

# 2. Wait for full page load
cmux browser --surface $SURFACE wait --load-state complete

# 3. Get interactive snapshot — DOM with element refs
cmux browser --surface $SURFACE snapshot -i

# 4. Type into input using ref
cmux browser --surface $SURFACE type e3 'test query'

# 5. Click submit button using ref
cmux browser --surface $SURFACE click e7

# 6. Wait for navigation/update, then re-snapshot to verify
cmux browser --surface $SURFACE wait --load-state complete
cmux browser --surface $SURFACE snapshot -i

# 7. CLOSE browser when done (MANDATORY)
cmux close-surface --surface $SURFACE
```
