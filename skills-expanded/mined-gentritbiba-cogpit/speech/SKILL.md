---
name: speech
description: Present text the user can turn into speech using Cogpit's Text to speech plugin.
---

When the user asks for a spoken explanation, narration, reading passage, or text they can listen to, put the exact words to speak in this fenced Markdown block:

```cogpit:cogpit.tts:speech
The words to speak go here.
```

Use natural spoken prose. Keep code, tables, URLs, and commentary outside the block unless the user wants them spoken. A block can contain multiple paragraphs and up to 16 KiB of UTF-8 text; split longer passages into separate blocks. Do not nest fences inside a speech block.

Cogpit renders a card with a play button. The user presses it to generate audio and start playback. Rendering or reopening a conversation does not generate speech. The plugin's settings supply speed and audio format; its connection supplies the voice. Do not include an API key, endpoint, or executable code in the block, and do not call the service yourself just to render a card.

This service currently supports English, Spanish, French, Hindi, Italian, Japanese, Brazilian Portuguese, and Chinese through its voices. German and Albanian voices are unavailable. Ask the user to choose a supported voice when relevant.

The Spoken summary button asks you to summarize the conversation using this skill. Also give a spoken summary when the user asks for one or clearly wants a quick catch-up or wrap-up. If the user asks for a summary after every turn, follow that preference; otherwise do not add one to every reply automatically.

Make summaries as short and simple as you can while conveying what matters. Use the words a real person would use in a meeting or on a call. Write plain spoken prose with no lists, bullets, numbered points, or headings. Leave out jargon, filenames, and implementation details unless they are needed to understand an important point. Include the result, an unresolved issue, or a next step only when it matters. Put the spoken summary in the speech fence above.
