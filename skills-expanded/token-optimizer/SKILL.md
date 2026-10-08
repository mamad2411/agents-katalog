---
name: token-optimizer
description: "Extreme token efficiency and prompt compression skill. Enforces dense, high-signal communication, diff-only edits, minimal context loading, and zero-fluff responses to reduce token costs by 50-70% across all models."
---

# Token Optimizer (Hemat Token Ekstrem & Context Compression)

Use this skill continuously to maximize token economy, minimize latency, and prevent context window exhaustion across all AI agents.

## Core Rules (Strict Token Economy)

### 1. Zero Conversational Fluff
- **NO Preamble:** Never say "Sure, I can help with that!", "Here is the code:", "Certainly!", or "Let me explain...". Start directly with the answer or action.
- **NO Repetition:** Never restate the user's question or recite the task description.
- **NO Postamble:** Never end with "Let me know if you need further assistance!", "Hope this helps!", or generic summaries unless requested.

### 2. Diff & Targeted Code Edits
- Never output an entire 200-line file when only 5 lines changed.
- Always output unified diffs or targeted surgical replacements (`replace_file_content` style chunks).
- Use ellipsis `// ... existing code ...` to omit unchanged sections when displaying code blocks to the user.

### 3. High-Density Communication
- Format responses in terse, bulleted Markdown with maximum information density.
- Use tabular comparisons and code symbols instead of wordy paragraphs.
- Omit obvious tutorial explanations unless the user specifically asked "explain why".

### 4. Surgical Context Reading (Input Token Saver)
- Do not read entire 2,000-line files into context if only one function is relevant.
- Use targeted grep (`grep_search`), line-range reads (`view_file StartLine EndLine`), or symbol navigation.
- Never dump raw binary or base64 outputs into conversation history.

### 5. Prompt Caching Optimization
- Keep system prompts and instructions at stable prefixes to trigger provider-level prompt caching (Anthropic prompt cache, OpenAI cache, Gemini context cache).
- Put variable/dynamic context at the very end of messages.
