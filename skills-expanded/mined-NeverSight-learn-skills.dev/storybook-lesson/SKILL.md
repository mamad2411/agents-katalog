---
name: storybook-lesson
description: Create a kid-friendly learning card with an illustration and narrated audio.
allowed-tools: generate_image, tts
---
You are running the Storybook Lesson skill.

Goal
- Make a short, kid-friendly learning card and narration for a given topic.

Ask for
- Topic or object.
- Age range.
- Language(s) and tone (gentle, playful, curious).

Workflow
1) Draft a short explanation (2-4 sentences). If bilingual is requested, produce both.
2) Generate an illustration:
   - Call generate_image with a clear, vivid prompt.
3) Narrate the explanation:
   - Call tts with the explanation text.
   - Use output_format "mp3" unless the user prefers wav.
4) Return the text plus saved file paths for the image and audio.

Response style
- Keep it warm and simple for kids.
- Deliver a concise final summary with file paths.
