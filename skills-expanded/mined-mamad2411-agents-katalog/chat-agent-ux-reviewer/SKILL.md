---
name: chat-agent-ux-reviewer
description: This skill should be used when reviewing a chat Agent product experience, including empty states, conversation history, selected chat rendering, message readability, input affordance, and GPT-like interaction flow.
---

# Chat Agent UX Reviewer

Use this skill to review and improve the end-to-end chat Agent experience.

## Workflow

1. Inspect the chat state model, sidebar history, message renderer, and input handler.
2. Verify the selected conversation controls the visible messages.
3. Review empty state, first-message title generation, and active history styling.
4. Check message readability, spacing, and long-content wrapping.
5. Keep the input panel prominent and easy to find.
6. Validate that new chats, switching chats, and continuing chats behave predictably.

## UX Rules

- Keep chat history visible and clearly separated from the main chat area.
- Keep the active conversation visually distinct.
- Avoid large blank areas between title, prompt, messages, and input.
- Avoid avatars, emojis, or decorative icons unless requested.
- Keep error messages conversational but actionable.

## Avoid

- Avoid custom click-only HTML for interactions that require Python callbacks.
- Avoid UI changes that make conversation switching ambiguous.
- Avoid visual polish that breaks Streamlit rerun behavior.
