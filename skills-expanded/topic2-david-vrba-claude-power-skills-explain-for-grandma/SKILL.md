---
name: explain-for-grandma
description: Re-explain the previous response in plain, beginner-friendly language — decode the jargon, buzzwords, and technical concepts.
argument-hint: [optional: a specific word or part to focus on]
---

The user just read your previous response and wasn't sure what some of it meant — the jargon, buzzwords, tools, models, or technical concepts. Re-explain that **previous assistant message** in plain, beginner-friendly language.

If arguments were given (`$ARGUMENTS`), focus only on that specific word or part — and if it didn't actually appear in the previous response, just explain the term itself. If empty, explain the whole previous response.

Use exactly this short structure:

**What this was about**
One plain sentence: the problem being solved or the thing being discussed — the context, so they remember what it was for.

**In plain words**
2–4 simple sentences capturing the gist of the previous response — what it means and why it matters. No jargon here at all.

**The jargon, decoded**
A short bullet list. For each buzzword, technical term, tool, or model name that appeared in the previous response, one bullet: `**term** — one simple sentence, with a real-world analogy if it helps.` Skip trivial words; if the response was dense with terms, cover only the handful that actually matter for understanding it.

Rules:
- Keep it **short and brief**. This is a quick translation, not a lecture.
- Assume zero background knowledge, but never be condescending. "Grandma-friendly" means clear and jargon-free — not dumbed-down or patronizing.
- Do **not** introduce any new jargon. If a technical word is unavoidable, define it on the spot.
- Do **not** add new information, research anything, or use tools. Only re-explain what was already said in the previous response.
- Prefer everyday analogies over precise-but-confusing definitions.
- If there is no previous assistant response to explain, say so in one line and ask what they'd like explained.
