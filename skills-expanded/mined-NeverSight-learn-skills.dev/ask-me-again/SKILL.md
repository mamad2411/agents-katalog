---
name: ask-me-again
description: Re-ask the assistant's pending questions as native interactive choices.
disable-model-invocation: true
---

# Ask Me Again

Re-ask every unanswered question from the assistant's preceding message through native
structured input (`AskUserQuestion` in Claude Code, `request_user_input` in Codex).

- Preserve the question order and any existing options or recommendation.
- For a question without options, offer two or three mutually exclusive choices. Put the
  recommended choice first and explain each choice's tradeoff in one sentence.
- Batch independent questions up to the tool's limit. Ask dependent questions after the
  earlier answers.
- When structured input is unavailable, ask one plain-text question at a time.
- When no unanswered question exists, say so and stop.
