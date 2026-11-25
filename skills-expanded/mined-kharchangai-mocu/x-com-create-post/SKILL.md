---
name: x-com-create-post
description: Create and publish a post (with optional image) on X.com. Use when the user asks to write, draft, or publish a post/tweet on X. Navigate with the Browser Use agent, and perform every on-page mouse/keyboard action with the Computer Control extension.
---

# X.com Create Post

## Purpose
Publish a text post, optionally with one image, on `https://x.com` for the signed-in account. Every on-page interaction (clicking, typing, uploading, submitting) must be done through visible mouse and keyboard control. Never replace required mouse interaction with DOM actions, scripts, direct page APIs, or hidden browser automation.

## Required input
- The final post text (English unless the user requests another language).
- Optional image path, or permission to generate/improve an image.

If the post text is missing, ask the user for it before starting.

## Tool responsibilities
- **`/agent Browser Use`**: Open or focus Chrome, navigate to `https://x.com/home`, and inspect the active tab and visible page content to verify the home page, the composer, and the final state. Do not use it to click, hover, scroll, or type inside X.
- **`/extension Computer Control`**: Use the mouse for all on-page interaction and keyboard input for typing. Locate targets from the current visible screen via the screen-coordinate finder; never guess coordinates.
- **Image generation tool**: Only if the user's image needs improvement or a new image is requested.

## Procedure

### 1. Open X home
1. Use `/agent Browser Use` to open or focus Chrome and navigate to exactly `https://x.com/home`.
2. Verify with Browser Use that the home page is loaded and the **What's happening** composer box is visible. If it is not usable, use Computer Control to click the visible page and press `F5` once, then verify again. If it remains unusable, stop and report the issue.

### 2. Start the post
3. Using Computer Control, move the mouse over the visible **What's happening** box and click it. Confirm with Browser Use that the composer opened and the text cursor is active.

### 3. Type and check the text
4. Type the post text with the keyboard.
5. Respect the account's character limit. For a non-premium account the limit is 280 characters (or 25,000 for premium).
6. After typing, inspect the composer. If any part of the text is highlighted red, the post exceeds the limit: press `Ctrl+A` to select all, delete the entire text, and retype a shorter version.
7. Never post a red-highlighted draft.

### 4. Verify the text
8. Before posting, check the whole text carefully: correct spelling, no typos, correct wording, and all required parts present. If anything is wrong, fix it before continuing.

### 5. Optional image
9. If the post should include an image, first make sure the image is good quality. If it needs improvement, use the image generation tool to enhance it (or create one), and use the improved file.
10. Using Computer Control, click the **image/upload** icon inside the **What's happening** box, then click **Upload** so the file-selection dialog opens.
11. In the file dialog, type the full absolute image path into the **File name** field and click **Open** so the image is attached to the post.
12. Confirm with Browser Use that the image is attached.

### 6. Review and publish
13. Confirm everything is ready: text correct, no red highlight, and image attached (if requested).
14. Using Computer Control, move the mouse over the visible **Post** button and click it.
15. Confirm with Browser Use that the post was published successfully, then report the result.

## Boundaries
- Use ordinary, transparent browser interaction. Do not pretend to be human, disguise automation, evade detection, or bypass X safeguards.
- Do not like, repost, reply, follow, message, or make other account changes.
- Do not invent post details, character limits, or capabilities.
- Keep all instructions, typed content, and the final response in English unless the user requests otherwise.
