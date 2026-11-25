---
name: evaluate
description: Measure whether Nexus-MCP helps on the user's own project before they adopt it. Runs the free offline `nexus-mcp-ci eval` check, explains the verdict, and offers the agent tier (which spends the user's own LLM API tokens) and the optional share step. Use when the user asks to try, test, evaluate, benchmark or compare Nexus-MCP, or asks whether it is worth installing.
model: sonnet
---

# Evaluate Nexus-MCP on this project

Follow these steps in order. Do not skip the consent steps.

1. **Say what will happen.** Tell the user in two sentences: the quick check indexes this
   folder in a temporary place, makes no LLM call and sends nothing off the machine. The first
   run downloads the embedding model once (about 32 MB).

2. **Find a runner.** Use the first that works: `nexus-mcp-ci`, then `uvx --python 3.12 nexus-mcp-ci`, then
   `pipx run nexus-mcp-ci`. `uvx` needs Python 3.10 to 3.12; add `--python 3.12` if the
   default Python is newer.

3. **Run it through the `nexus-evaluator` agent**, so the raw output stays out of this
   conversation. Pass the folder (default: the current folder) and ask for the report summary.
   If no agent is available, run `<runner> eval --json` and read only `verdict`, `summary` and
   `by_kind`.

4. **Explain the verdict** in plain words:
   - the token numbers, Grep and Read against Nexus-MCP;
   - how often each found the right file first and in the top 3;
   - where Grep and Read did as well or better. Say it plainly. A "Weak fit" is a valid result.
   - The numbers are a token proxy, not a bill.

5. **Offer the agent tier only if the user wants real cost numbers.** Before you run it, state:
   it uses their own `claude` (or `codex`) login, it sends prompts and the code the agent reads
   to Anthropic (or OpenAI), and it costs about the estimate that the CLI prints (the default
   cap is $5). Run `<runner> eval --agent claude` only after a clear yes in this conversation.

6. **Recommend a setup** when the fit is good:
   `claude mcp add nexus-mcp -- nexus-mcp-ci`, or the plugin. Mention about 270 MB of memory
   with the model loaded, and that call edges exist for Python, JavaScript, TypeScript, Go,
   Java and Rust only. Offer to add `.nexus/` to `.gitignore`: the index holds code.

7. **Offer to share, never post on your own.** `<runner> eval share <run-id>` prints the exact
   payload (numbers only, no paths or code) and asks y/N. Run it only after the user says yes
   in this conversation, and let the user answer the CLI question.

To remove everything the eval stored: `<runner> data clear --evals --yes`. Details:
https://github.com/jaggernaut007/Nexus-MCP/blob/main/docs/EVALUATE.md
