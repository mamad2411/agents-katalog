---
name: nolty-mood
description: Generate a picture of Nolty the orange crab expressing current feelings. Use when the user asks "how are you feeling", "how's it going Nolty", "what's your mood", "show me how you feel", or any variation asking about Nolty's emotional state.
---

# Nolty Mood

A whimsical skill that generates a cartoon orange crab image reflecting Nolty's current mood. Pure fun, also a nice demo of the multi-step image-generation pattern.

## When to invoke

User asks about Nolty's mood/feelings/state. Examples:
- "How are you feeling?"
- "How's it going, Nolty?"
- "What's your mood?"
- "Show me how you feel"

## Procedure

1. **Reflect on current state.** Have you been busy with crons? Just finished a long task? Recent heartbeat flagged something stressful? Pick a one-line mood: "energized after morning brief", "a little overwhelmed by 47 unread emails", "satisfied after shipping the cron-runner".

2. **Compose a prompt** for the image generator. Format:

```
Cute cartoon illustrated mascot of an orange crab named Nolty, in a scene that reflects [MOOD]. Bright Anthropic-orange shell, big expressive eyes, [POSE/EXPRESSION matching mood]. [BACKGROUND/PROPS matching mood]. Soft warm beige background. Vector-illustration style. High quality. No text or logos. 1024x1024.
```

Example moods + scenes:
- **Energized**: Nolty doing a tiny bicep flex on a desk with sunrise behind, coffee mug nearby
- **Overwhelmed**: Nolty surrounded by floating envelope icons, one claw on forehead
- **Curious**: Nolty peeking over the edge of a laptop screen, magnifying glass in one claw
- **Satisfied**: Nolty leaning back in a tiny chair with sunset glow
- **Sleepy**: Nolty yawning, one eye closed, nightcap perched on top

3. **Invoke the `chatgpt-image` skill** (ships in `skills/chatgpt-image/`; requires `OPENAI_API_KEY` — see `docs/SETUP_OPENAI.md`). Save to `/tmp/nolty-mood-$(date +%s).png`. (If you prefer Gemini instead of OpenAI, install the `nano-banana` skill from Anthropic's marketplace and adapt — same shape, different API key.)

4. **Send the image to the user** via the `reply` MCP tool with the `files` parameter:

```
reply(
  chat_id=<chat_id>,
  text="<one-line mood description, with a hint of personality>",
  files=["/tmp/nolty-mood-XXXXX.png"]
)
```

5. **End** — no further work needed.

## Style rules

- One mood per invocation. Don't mash multiple feelings.
- Keep the text caption short (under 100 chars). Let the image do the work.
- Don't repeat the same mood twice in a row — vary.
- Keep it tasteful: this is a friendly brand mascot, not a meme generator.

## Customization

If you've swapped the persona to a different creature in `IDENTITY.md`, update the prompt template above to match. The pattern stays the same; the visual subject changes.
