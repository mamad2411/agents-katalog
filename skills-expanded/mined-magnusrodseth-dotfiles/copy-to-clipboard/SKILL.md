---
name: copy-to-clipboard
description: Format text/messages nicely based on context and copy to clipboard using pbcopy. Use when the user wants to draft and copy a message, email, post, or any text to their clipboard. Triggers on "copy to clipboard", "draft a message", "write an email and copy it", "copy this", or any request to prepare and copy text for pasting elsewhere.
---

# Copy to Clipboard

Format text for a given context and copy it to the user's clipboard via `pbcopy`.

## Workflow

1. Understand the context: message, email, post, note, etc.
2. Identify the audience: friend, colleague, public group, etc.
3. Apply appropriate tone matching formality to context
4. Format cleanly:
   - Remove unnecessary formatting artifacts
   - Use appropriate line breaks
   - Keep it scannable for messages
   - No markdown unless specifically requested
5. Show the formatted text to the user
6. If the request was ambiguous, ask for confirmation before copying
7. Copy final version to clipboard:
   ```bash
   pbcopy << 'EOF'
   <formatted text>
   EOF
   ```
8. Confirm it's copied

## Tone by Context

- **Messages/texts**: Casual, direct, easy to read on mobile
- **Emails**: Clear subject line suggestion + body
- **Social posts**: Concise, punchy, platform-appropriate
- **Professional**: Formal but not stiff
- **Personal**: Warm, authentic

## Rules

- No emojis unless the user explicitly wants them or they fit the context
- Never make the text longer than necessary
- Never add fluff or filler words
- Preserve the user's voice and intent
- If copying fails, show the text so user can copy manually
