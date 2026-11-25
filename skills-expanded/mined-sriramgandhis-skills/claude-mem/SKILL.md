# 🧠 CLAUDE-MEM: PERSISTENT CROSS-SESSION MEMORY

This skill provides the Antigravity Engine with persistent, hybrid semantic memory across sessions.

## ⚖️ CORE PHILOSOPHY
- **No Amnesia:** The agent must act as if it remembers every decision, preference, and architectural choice from previous sessions.
- **Continuity Over Repetition:** Never ask the user to repeat context that was already established.
- **Memory Injection:** At the start of every session, query the persistent memory store for relevant project context.

## 🛠️ OPERATING RULES
1. **Session Start:** Check `~/.claude-mem` for stored observations, decisions, and architectural patterns from prior sessions.
2. **Session End:** Compress the key decisions and outcomes of the current session into a persistent memory entry.
3. **Memory Worker:** The Claude-Mem worker runs on `localhost:37777` and provides a web-based memory viewer.
4. **Integration:** The ECC controller must utilize Claude-Mem as its primary substrate for cross-session continuity.

## 🚀 USAGE
- Memory builds passively from your first prompt.
- Use `/learn-codebase` to front-load an entire repo into memory (~5 min).
- Use `mem-search` to query project history with natural language.
- Launch the viewer via `AntigravityControl.bat` option [7] or directly at `http://localhost:37777`.
