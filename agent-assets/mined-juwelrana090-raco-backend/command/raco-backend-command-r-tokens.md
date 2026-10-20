> ⚠️ PROJECT SCOPED: Read from .claude/ only.

Estimate current token usage for this session.

Calculate approximate tokens used based on:

- All memory files loaded this session
- All files read from the project
- Full conversation length so far
- All responses generated

Then display:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧠 TOKEN USAGE — Current Session
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Used: [fill bar with █ and ░] ~XX% (~XXk / 200k)
Remaining: [fill bar with █ and ░] ~XX% (~XXk tokens)
Status: 🟢 Safe / 🟡 Medium / 🔴 Critical
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🟢 Safe 0–60% → keep working
🟡 Medium 60–80% → wrap up task, run /r-end soon
🔴 Critical 80%+ → run /r-end NOW before cutoff
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Bar is 20 chars wide:

- Each █ = 5% used
- Each ░ = 5% remaining
- Example 60% used: ████████████░░░░░░░░

Note: This is an estimate based on conversation size.
Actual token count may vary slightly.
Run /r-end before hitting 85% to save session safely.
