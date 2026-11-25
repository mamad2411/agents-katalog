# Memory-aware system prompt (LM Studio)

**Use `lmstudio/prompts/system-prompt.md` instead** — it is the full agent prompt
(memory + codebase-memory + GitHub + playwright).

For LM Studio Chat: paste the contents of `lmstudio-system-prompt.md` into
**Chat → System Prompt**.

Memory is also **auto-recalled** in the terminal agent (`agent/local_agent.py`).
In LM Studio chat, the model still receives recalled facts if you use a small
wrapper — for now, the system prompt instructs it to read the memory block and
call `search_nodes` / `read_graph` at task start.
