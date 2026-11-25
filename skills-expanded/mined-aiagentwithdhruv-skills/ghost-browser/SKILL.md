---
name: ghost-browser
description: Manus-level AI browser agent that drives Dhruv's REAL logged-in Chrome (any profile — AIV, Onsite, etc.) via natural-language commands. Persistent, human-paced, un-blockable (real session), LLM-driven so it survives obfuscated selectors. Use when Dhruv says "control my AIV / control my <profile>", or asks to browse, search, apply, engage, or automate anything in his real browser.
---

# Ghost Browser — Agentic control of Dhruv's real Chrome

> You give it a goal in plain English. It drives his actual logged-in Chrome like a human —
> scrolling, clicking, typing, reading — and stops before any irreversible public action.

**Runtime lives at:** `Social-Media-Agent-1.0/browser-automation/`
**Engine:** `browser-use` (0.13.x) + Playwright CDP attach + real Google Chrome
**Brain:** OpenAI `gpt-5.4-mini` (actions) + `gpt-5.4` (accurate page reading), keys in that folder's `.env`

---

## Why this beats normal automation
- **Un-blockable:** drives your REAL Chrome with your REAL logged-in sessions + residential IP — same trick Manus uses. Not a headless bot, so bot-detection has nothing to catch.
- **Persistent:** Chrome opens ONCE and stays open. No reopening tabs per action.
- **Human-paced:** small scrolls, brief pauses, deliberate steps — fast where safe, slow where blocking is a risk.
- **LLM-driven:** you state the goal; it decides the clicks. Survives LinkedIn/any site renaming its buttons (no brittle selectors).
- **Safe on the brand account:** never clicks a final Submit / Post / Send / Apply-confirm, or reacts to >3 posts per run. It fills everything and STOPS for Dhruv's click. Override with `--allow-submit`.

## How to run it (two steps)

**Step 1 — attach to a profile** (once per session). Quits Chrome, clean-copies the login, relaunches on the debug port. His everyday Chrome is untouched (works on a copy).
```bash
cd "Social-Media-Agent-1.0/browser-automation"
./.venv/bin/python ghost_launch.py aiv     # or: onsite | msbc | dhruv | agi | default
# waits for "✅ READY"
```

**Step 2 — command it in plain English** (repeat as many times as you want; Chrome stays open).
```bash
./.venv/bin/python ghost_agent.py "open Jobs, search Solution Consultant remote India, list the top 5 with company + location"
./.venv/bin/python ghost_agent.py "scroll my feed and draft a thoughtful comment on the top AI post — do NOT post it"
./.venv/bin/python ghost_agent.py "open this job <url>, fill the application with my details, stop before Submit"
```

## Profile map (name → Chrome profile)
| say | profile | account |
|---|---|---|
| `aiv` | Profile 6 | Ai with Dhruv (aiwithdhruv@gmail.com) — **default** |
| `dhruv` | Profile 2 | Dhruv Tomar |
| `onsite` | Profile 4 | dhruv.tomar@onsiteteams.com |
| `msbc` | Profile 12 | MSBC |
| `agi` | Profile 8 | agiwithdhruv@gmail.com |

## Safety model (do not weaken without Dhruv's explicit OK)
- Reading, scrolling, navigating, searching, opening posts, and **typing** into comment/message/application fields = automated.
- Final public/irreversible actions (Post, Send, Submit, Publish, Connect, >3 reactions/run) = **Dhruv clicks**, unless the command includes `--allow-submit`.
- This protects the brand account from a ToS flag mid-job-hunt.

## Files
| file | role |
|---|---|
| `ghost_launch.py` | quit + clean-copy profile + relaunch Chrome on CDP port 9222 |
| `ghost_agent.py` | the LLM-driven agent (natural-language task → human-paced actions) |
| `ghost_chrome.py` | low-level Playwright CDP driver (for scripted, non-LLM control) |
| `.env` | OpenAI + Euri keys (gitignored) |

## Notes / gotchas
- Chrome 136+ blocks the debug port on the *normal* profile dir — that's why `ghost_launch.py` uses a clean copy under `.chrome-cdp-<name>/` (gitignored).
- Set a different brain with `GHOST_MODEL` / `GHOST_READ_MODEL` env vars. Euri keys are present for cost-sensitive product runs.
- The engine has a built-in LLM-judge that grades each run — watch for its verdict to catch misreads.
- Requires the runtime built: `python3 -m venv .venv && .venv/bin/pip install browser-use playwright && .venv/bin/playwright install chromium`.

## Alternative: Claude for Chrome (official, complementary)
For interactive "Claude, do this in my browser" moments, the official Anthropic **Claude for Chrome** extension (Max plan) is the safest zero-code option — records/repeats workflows, schedules tasks, uses live sessions. Ghost Browser is the *scriptable, ownable* version for automation Dhruv controls.
