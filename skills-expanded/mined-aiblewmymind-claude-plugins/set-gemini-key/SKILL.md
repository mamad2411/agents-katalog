---
name: set-gemini-key
description: Walk the user through getting and saving a Gemini API key for image generation.
user-invocable: true
---

# Set Up Your Gemini API Key

Help the user get a free Gemini API key:

1. Tell them: "Go to **aistudio.google.com** and sign in with your Google account."
2. Tell them: "Click **Get API Key** → **Create API Key** → copy the key."
3. Ask them to paste the key here.
4. When they paste it, call the `set_gemini_key` tool with the key.
5. Confirm: "Your key is saved locally and will never be sent to AI Blew My Mind servers. You can now generate unlimited images."
