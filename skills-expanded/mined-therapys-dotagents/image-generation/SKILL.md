---
name: image-generation
description: "Generate and download images through ChatGPT in the user's signed-in browser, using their ChatGPT subscription rather than API keys or API billing. Use whenever the user asks to generate an image, illustration, hero image, product artwork, concept art, social creative, or other AI-generated visual asset. Not for stock-photo search, precise charts/diagrams, or image-generation integration code."
---

# Image generation

Use ChatGPT's image-generation UI in the user's existing signed-in browser. This workflow uses their ChatGPT subscription and its image-generation limits, not the OpenAI Images API. No API key is required.

## Browser access

Discover the session's browser-control tools and read their instructions before using them. Use a tool that can access the user's existing authenticated browser/profile. An isolated browser may not have their ChatGPT login; do not assume it does.

If browser control is unavailable, explain the blocker and ask the user to enable/connect a browser tool. Do not claim to have generated an image. If ChatGPT is logged out, let the user sign in manually, then resume. Never extract cookies or tokens, read agent auth stores, ask for passwords, or attempt to turn subscription credentials into API credentials. Do not fall back to an API, another provider, or an upgrade/purchase flow without the user's explicit approval.

## Workflow

1. Extract the subject, intended use, style, composition, palette, exact text (if any), and output path from the request. Ask one question at a time only when a missing detail materially changes the result; otherwise use sensible defaults.
2. Open `https://chatgpt.com/` in the authenticated browser. Start a new conversation unless continuing the same image task, so unrelated personal conversations are not read or modified. Check that image generation is available in the UI. If access or a subscription limit blocks it, report that and stop.
3. Compose a concrete prompt: explicitly ask to **generate an image**, then describe subject → composition → style/material/lighting → colors → constraints. Preserve requested text verbatim in quotes. For web heroes, reserve negative space for overlays rather than baking UI text into the image. Do not silently add logos or watermarks. Specify the desired aspect ratio and transparency when relevant, but do not claim that the UI guarantees exact dimensions or format.
4. Submit one image request by default. Use the UI's image-creation control if needed. Wait for generation to finish, inspecting browser state rather than repeatedly submitting. Stop on errors or quota messages. Do not purchase credits, change plans, or run unsolicited batches. Before uploading reference images or private project material, confirm permission unless the user already explicitly requested that upload.
5. Inspect the generated image against the brief: composition, required details, text accuracy, and artifacts. Continue in the same conversation for requested edits, stating what to preserve and what to change. Ask before additional attempts unless iteration was already authorized; subscription image limits still matter.
6. Use the generated image's download control to save the original asset, not a screenshot of the ChatGPT page or a thumbnail. Follow the browser tool's download workflow, verify the download completed, and copy/move the resulting file to the requested destination. Otherwise use `generated-images/<descriptive-name>.<actual-extension>` in the working project. Preserve the actual format/extension; never rename JPEG or WebP bytes to `.png`. Avoid overwriting existing files.
7. Open the saved file with an image-reading tool to verify it is the intended image. If visual inspection or local download is unavailable, say so clearly. Return the real local path with a preview when supported; if only the ChatGPT result is accessible, provide its conversation link and explain that no local file was saved. Never present a prompt, placeholder, or screenshot as the downloaded generated asset.

## Example prompt

> Generate a wide landscape image for a children's-book website hero: a baby otter having a gentle veterinary checkup, watercolor on warm cream paper, soft teal accents and natural light. Place the otter on the right and leave the left third uncluttered for a heading. No lettering, logos, or watermark.

Keep the final response short: the file path and any unmet constraint. Do not claim API access, exact pixel dimensions, transparent output, or successful download unless verified.
