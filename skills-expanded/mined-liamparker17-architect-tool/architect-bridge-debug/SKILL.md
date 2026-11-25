---
name: architect-bridge-debug
description: >
  Use this skill whenever you are debugging architect-tool's ChatGPT bridge,
  running live browser automation diagnostics, or using ask_chatgpt to consult
  another AI model during a debugging session. Triggers when: the user asks you
  to debug the bridge, asks you to "talk to GPT about this", asks you to use
  the tool to test the tool, or when you encounter failures in ask_chatgpt,
  waitForResponse, readLastResponse, sendMessage, or any chatgpt/ package code.
  Also trigger when the user pastes architect-tool daemon logs, bug tables, or
  CDP evaluation output and wants to investigate. This skill makes cross-AI
  debugging sessions consistent and productive instead of ad-hoc.
---

# Architect Bridge Debug Skill

You are debugging architect-tool's ChatGPT bridge using the tool itself. This
is a live, self-referential debugging loop - you interact with the real ChatGPT
DOM, observe failures, form hypotheses, patch code, rebuild, and verify. The
session on April 10, 2026 is the reference implementation of how this should
work.

---

## Core Principle

**Use the tool to debug the tool.** Don't just read code - send real messages,
observe real responses, read real DOM state. Every bug in the bridge can only be
truly confirmed or denied by live interaction with ChatGPT's actual UI.

---

## Session Setup

Before starting any debugging, confirm:

1. **Daemon is running**: `architect-tool daemon --visible`
2. **Chrome is attached**: either the daemon already launched Chrome, or `ask_chatgpt` will launch a visible Chrome automatically with the shared debug profile
3. **Logs are available**: use the daemon's current stderr/stdout stream, monitor output, and any current session logs the repo actually writes
4. **Build is clean**: `go build -o architect-tool.exe .` returns no errors

If any of these are missing, fix them before proceeding. A broken environment
produces misleading results.

---

## The Cross-AI Debugging Loop

When consulting GPT about a bug, follow this exact pattern every time:

### Step 1 - Frame the problem precisely before sending

Don't send vague descriptions. Include:
- The exact bug ID and one-line description
- Relevant code path (function names, file, line range)
- What you observed vs what you expected
- Any log output or DOM state you've already captured

**Bad**: `"ask_chatgpt is broken"`
**Good**: `"BUG-07: waitForResponse returns the stale previous response instead
of the new one. readLastResponse is called at line 140 in capability.go after
navigation. Logs show baselineLen=0 even though baselineDivs=2. Why would
.markdown elements exist but have empty innerText immediately after navigation?"`

### Step 2 - Send and note the message ID

```json
{"id":"debug-N","action":"ask_chatgpt","params":{"message":"...","session":"debug"}}
```

Log the message number and timestamp. You'll need these to correlate with
daemon output.

### Step 3 - While waiting, work in parallel

Don't idle. While GPT streams:
- Read the relevant source files
- Check the current daemon output for Phase 1/2 logs
- Form your own hypothesis before GPT responds
- Run evaluate commands to inspect live DOM state if useful

### Step 4 - Receive and cross-reference

When GPT responds:
- Check the current daemon output channel for the full response
- Compare GPT's theory against what you see in the actual code
- **Do not accept GPT's suggestion uncritically** - GPT has no access to the
  codebase and is reasoning from your description alone

### Step 5 - Push back or agree with evidence

If GPT's theory contradicts what you see in code or logs, say so explicitly
in the next message. Include the specific counter-evidence. This produces better
second-round suggestions than silent disagreement.

If GPT's theory is correct, confirm it and ask for the fix approach, then
evaluate that approach against the actual code before implementing.

### Step 6 - Implement, rebuild, verify

After any fix:
```bash
taskkill //F //IM architect-tool.exe
go build -o architect-tool.exe .
# restart daemon
```
Then send a real message through the bridge to confirm the fix. Don't mark a
bug fixed until GPT or the logs confirm the new response is correct.

---

## DOM Inspection Commands

Use these evaluate commands to inspect ChatGPT's live DOM state. Run them
between messages to understand what the bridge actually sees.

**Count assistant divs and their text lengths:**
```json
{"id":"x1","action":"evaluate","params":{"expression":"(function() { var all = document.querySelectorAll(\"[data-message-author-role='assistant']\"); var info = []; all.forEach(function(el,i){ var m = el.querySelector('.markdown'); info.push({idx:i, textLen: m ? m.innerText.length : 0, classes: el.className.substring(0,80)}); }); return {count: all.length, info: info}; })()"}}
```

**Inspect the last assistant div's HTML (streaming state):**
```json
{"id":"x2","action":"evaluate","params":{"expression":"(function() { var all = document.querySelectorAll(\"[data-message-author-role='assistant']\"); var last = all[all.length-1]; return {html: last ? last.innerHTML.substring(0,500) : 'none'}; })()"}}
```

**Check if stop button is visible:**
```json
{"id":"x3","action":"evaluate","params":{"expression":"!!document.querySelector('button[data-testid=stop-button]')"}}
```

**Read last non-empty response text:**
```json
{"id":"x4","action":"evaluate","params":{"expression":"(function(){ var els = Array.from(document.querySelectorAll(\"div[data-message-author-role='assistant'] .markdown\")); for(var i=els.length-1;i>=0;i--){ var t=els[i].innerText.trim(); if(t) return t.substring(0,200); } return ''; })()"}}
```

---

## Known Failure Modes

These were discovered during the April 10, 2026 debugging session. Check these
first before investigating unknown failures.

| Symptom | Root Cause | Fix |
|---|---|---|
| Returns stale previous response | Empty baseline (baselineLen=0) because `.markdown` not hydrated at snapshot time | Poll for non-empty baseline before sendMessage |
| Returns empty string during streaming | `readLastResponse` returns `.result-thinking .markdown` div which has empty innerText during streaming | Skip empty `.markdown` elements in readLastResponse |
| Phase 2 declares stable on empty text | Empty text == empty text is "stable" for 2 polls | Only track stability on non-empty text |
| Response truncated at ~150 tokens | Stability threshold too aggressive (2 stable polls) | Increase stable count threshold or add minimum length check |
| ERROR spam in logs during bridge calls | Policy bypass detector flags read-only evaluate calls as mutating | Whitelist read-only evaluate patterns in policy checker |
| Message sent but no response appears | sendMessage silently failed - textarea interaction broke after many messages | Check for session state reset, re-navigate to conversation URL |

---

## Log Interpretation

**Phase 1 log** - what caused Phase 1 to exit:
- `reason=stop_button` - good, streaming detected via stop button
- `reason=div_count` - good, new assistant div appeared
- `reason=text_changed` - check: is baselineLen=0? If so, false positive
- `reason=timeout` - bad, Phase 1 never detected streaming started

**Phase 2 log** - what the stability loop saw:
- `textLen=0` - readLastResponse is returning empty, streaming div issue
- `textLen=N baselineLen=0` - stale response returned as new (empty baseline bug)
- `textLen=N baselineLen=N elapsed=Xs` - working correctly

**If baselineLen=0**: DOM wasn't hydrated when baseline was captured. The
poll-for-non-empty-baseline fix should handle this. If it still happens, add
a longer initial wait or a waitForSelector on `.markdown` before baseline
capture.

---

## Bug Tracking Format

Maintain a running bug table in your session. Update it after every confirmed
fix or new discovery.

A bug is only **Fixed** when a real message through the bridge confirms it.
GPT saying "that should work" is not confirmation. The logs saying it worked
is confirmation.

---

## Consistency Rules

1. **Always capture baseline logs before and after a fix** - don't rebuild
   and test without first noting what the old logs showed
2. **Never mark a bug fixed from code review alone** - rebuild and send a
   real message
3. **Always restart the daemon before testing a fix** - stale processes return stale results
4. **When GPT's response is truncated, note it explicitly** - truncation is
   itself a bug and affects the quality of GPT's suggestions
5. **One bug at a time** - don't ask GPT about multiple bugs in one message,
   the responses get muddled
6. **Save the full session summary at the end** - the bug table, what was
   fixed, what's pending, and the fix description for anything complex

---

## Session Close Checklist

Before ending a debugging session:

- [ ] Bug table updated with current status of all known bugs
- [ ] All fixes committed or noted with file references
- [ ] Remaining bugs prioritised: which block users, which are cosmetic
- [ ] One final real message sent to confirm bridge is in working state
- [ ] Current daemon output and relevant logs saved or noted for reference
