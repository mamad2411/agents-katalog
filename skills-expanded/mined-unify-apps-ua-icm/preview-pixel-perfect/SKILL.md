---
name: preview-pixel-perfect
description: Use when a builder task is about how the page LOOKS — matching a reference image or live site, polishing look and feel, or verifying visual work in the real running app. Opens the live preview in a logged-in Chrome (the preview-browser tools), drives states, measures the real DOM, and loops edit → reload → look until it reads right. Needs /start coordinates.
---

# Preview Pixel-Perfect

Use the real browser as eyes and hands on the page you are building. The
preview-browser tools open a Chrome that is already logged in to this clone's
platform, so you can land on the live preview, click and hover, read true
sizes and colors out of the running DOM, and screenshot what a user will
actually see.

One inversion to hold on to if you know pixel-perfect cloning from a code
repo: there the browser held the REFERENCE and code was the build. Here the
browser holds the BUILD — the preview of the page you are editing — and the
reference is whatever the user gave you: an image, another live site, or just
"make it nice". The browser never edits anything. Every change still goes
through apply_page_edits under the normal knowledge-sheet rules; the browser
only tells you the truth about what those edits produced.

## The loop

1. **Find the preview URL — never guess it.** URL shapes are platform facts:
   read `concepts/pages/routing-and-urls` and use get_page_paths, and build
   the URL from the session's `host`. A guessed path 404s or lands on the
   wrong page, and everything you measure after that is about the wrong thing.

2. **Open it and prove the login.** Navigate, then check what actually
   loaded. A login screen or an auth redirect means the cookie is stale — say
   so and stop; the fix is the user's (paste a fresh `_at` into `.env.local`,
   `node scripts/page.mjs up`, restart Claude Code). Never screenshot a login form and
   reason about it as if it were the page.

3. **Look at the truth.** Screenshot the rendered page for composition. But
   when a specific value matters — a gap, a radius, a color, a font size —
   read it from the live DOM with the evaluate tool and `getComputedStyle`,
   for the element in the state you care about. Screenshots tell you the
   rough layout; they lie about radius, shadow opacity, and sub-pixel
   spacing.

4. **Drive states.** Styles only exist while the state does. Hover with a
   real pointer move, focus with Tab, open the drawer or modal, empty the
   list. Verify the states the user will meet, not only the happy rest
   state — and remember the builder's sample data exists ONLY in preview;
   the published app renders empty, so look at the empty case on purpose.

5. **Edit → reload → look again.** Make the change with apply_page_edits
   (sheets first, as always), reload the preview, and look again. Reading
   the stored config back tells you what saved; only the browser tells you
   how it reads. Repeat until it reads right — this is a loop, not a
   checklist.

6. **Map measurements to tokens.** A value measured from a reference — a
   px, a hex — is not a value to inline. Find the platform token that holds
   the same relationship via get_style_options. You now have exact numbers
   in hand, which is exactly when inlining is most tempting and most wrong:
   a raw value will not theme and is silently ignored where a token id is
   expected.

7. **Fresh-eyes finish.** Before calling it done, hand ONLY the aligned
   screenshots — reference beside preview when a reference exists, the
   whole surface, same viewport — to a subagent asked to "list every
   visible difference", blind to what you changed or meant. You always see
   what you intended, not what is on screen. Done needs an outside look
   plus your measured checks, not a feeling.

Keep screenshots and style dumps in the scratchpad directory, not pasted
into the conversation — bring back the finding, not the dump.

## Red flags — stop and fix

| Thought | Reality |
|---|---|
| "I'll eyeball it from the screenshot." | Screenshots hide radius, shadow, and sub-pixel truth. Measure the live DOM. |
| "I'll just try a URL that looks right." | Preview URLs are platform facts. get_page_paths + the routing sheet. |
| "Looks faithful, marking it done." | Done is the fresh-eyes verdict plus measured checks, not a vibe. |
| "I verified it myself, it matches." | You are blind to your own intent. Outside eyes, only the images. |
| "Rest state matches, ship it." | Hover, focus, open, empty, error are part of the surface. Drive them. |
| "I'll hardcode the 7px I measured." | Raw values don't theme and are ignored where tokens are expected. Map to a token. |
| "I'll fix it directly in the browser." | The browser is read-only eyes. Edits go through apply_page_edits or they don't exist. |
| "The table has data, the page works." | That's builder sample data. Published pages start empty — check that state. |
