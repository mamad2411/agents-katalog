---
name: phone-call
description: Real Telegram voice calls and voice messages using Pyrogram userbot with TTS.
tools: [shell, telegram_call, tts]
trigger: call, phone, voice call, ring, urgent, emergency, call me, ring me, phone me
---
# Phone Call Skill

## Making Calls
To call the owner, include this tag in your response:
```
[MAKE_CALL: Your message to speak aloud]
```

The bot will:
1. Generate TTS audio from your message
2. Ring the owner's Telegram phone
3. Play the audio when they answer
4. Fall back to a voice message if not answered

## When to Use
- Owner says "call me", "ring me", "phone me"
- Owner asks you to deliver something by voice call
- Urgent alerts that need immediate attention
- Reminders with delivery type "call" or "both"

## Examples
- "Call me with the weather" -> Fetch weather, then `[MAKE_CALL: Good morning, the weather in Al Ain is 35 degrees and sunny]`
- "Ring me and tell me a joke" -> `[MAKE_CALL: Why did the programmer quit his job? Because he didn't get arrays!]`
- "Call me now" -> `[MAKE_CALL: Hello, you asked me to call you. How can I help?]`

## /call Command
The `/call <text>` command is also available for direct calls without going through the agent.
