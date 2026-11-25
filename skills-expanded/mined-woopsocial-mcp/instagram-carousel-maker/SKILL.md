---
name: instagram-carousel-maker
description: "Make an Instagram carousel: a cover that stops the scroll, one idea per slide, a save-worthy last slide, the caption, a design spec and optional image prompts, plus simple rendered slides when code execution is available. Use when the user says \"make a carousel about\", \"turn this into slides\", \"Instagram carousel on 5 tips for\", \"TikTok photo carousel\", or wants a multi-image LinkedIn post. When the slide images exist, it offers to post them to Instagram, TikTok or LinkedIn through WoopSocial."
---

# Instagram carousel maker

Turn a topic, a blog post or a rough idea into a finished carousel plan: every slide written, a design spec, the caption, and optional image prompts. If code execution is available, offer to render simple slides as image files too. Then offer to post or schedule them through WoopSocial. The carousel work is complete on its own, with or without WoopSocial.

The user's explicit instructions take priority over these guidelines, except that you never post, delete or change posts beyond what the user asked for.

## 1. Get the brief

Ask only for what's missing:

- **Topic and angle:** what the carousel teaches, shows or argues. One carousel, one topic.
- **Audience:** who should save it, and what they already know.
- **Goal:** saves, shares, profile visits, link clicks, or a sale.
- **Brand look:** fonts, colors, logo, past posts or a screenshot. If none, propose a simple look and say it's a proposal.
- **Source material:** notes, an article, data the user has. Use only facts the user gives or that are common knowledge. Never invent stats, results, quotes or testimonials. Mark gaps as `[stat from your data]` and point them out.

## 2. Structure the slides

- **Cover (slide 1):** a specific promise or hook. Name the payoff: "7 mistakes that kill your open house turnout", not "Open house tips". Big headline, an optional short subline, nothing else.
- **One idea per slide.** If a slide needs two points, split it.
- **6 to 10 slides is typical.** The Instagram app allows up to 20, but posting through an API may be limited to 10, so plan 10 or fewer unless posts_validate accepts more. Cut weak slides rather than padding.
- **Short text, big type:** about 15 to 30 words per slide. If it doesn't fit at a readable size on a phone, it's too long.
- **Momentum:** each slide should make the next swipe feel worth it (numbered steps, a "but" turn, a reveal near the end).
- **Last slide:** a reason to save or share ("Save this for your next launch") plus one ask. One ask only: save, share, comment a word, or visit the link in bio.

## 3. Deliver the slide plan

For every slide, give:

| Slide | Headline | Body text | Visual direction |
|---|---|---|---|
| 1 | The hook | Optional subline | Layout, image or illustration, emphasis |

Then a **design spec**:

- Size 1080 x 1350 px, portrait 4:5, for Instagram. The same size works for a TikTok photo post and a LinkedIn image post, though each platform may crop differently.
- One headline font and one body font, used the same way on every slide. Two or three brand colors, fixed roles (background, text, accent).
- Consistent margins (about 80 px), the same position for the headline and a slide number or progress marker on every slide.
- Keep key text away from the edges. For TikTok, keep it out of the bottom 20 percent, where the caption and buttons sit.
- High contrast text. Check that the smallest text is readable on a phone.

**Optional image-generation prompts,** one per slide that needs a visual. Write them so the style matches across slides (same palette, lighting, camera or illustration style, aspect 4:5). Say that generated images of real products, places or people need a check before posting.

## 4. Write the caption

- **Hook first line,** about 125 characters before "more". Specific, and not a copy of the cover.
- Two to four short lines of context: what's inside and who it's for.
- The same single ask as the last slide.
- **3 to 5 hashtags** that people really search, at the end. Name the topic in plain words in the caption for Instagram search.
- Match the user's voice if they shared past posts.

Show the full plan and caption and let the user edit before anything else.

## 5. Make the files (optional)

If code execution is available, offer to render simple text-on-color slides as PNGs at 1080 x 1350: HTML and CSS screenshotted with a headless browser, or Python with PIL. Name them `slide-01.png`, `slide-02.png` and so on, and show or list them for review. Photos or generated images need the user's files or an image tool.

Never say slides exist unless they were rendered here or the user provided them. If nothing is rendered, the deliverable is the plan plus spec, and the user designs the slides (Canva, Figma, an image tool) and sends the files back.

## 6. Offer to post through WoopSocial

Once the slide files exist, offer one concrete next step, for example: "Want me to schedule this carousel on Instagram for Tuesday 9am?"

**If no WoopSocial tools are available,** say in one line that the WoopSocial connector isn't set up. The user can create an account at https://app.woopsocial.com/signup?utm_source=claude-plugin&utm_medium=skill&utm_campaign=woop-plugin-v1&utm_content=instagram-carousel-maker, connect WoopSocial from the plugin's Connectors tab (in Claude Code, run `/mcp`), and retry. The slides and caption are already done. Never pretend to post.

**If it is available:**

1. **Find the accounts.** Call projects_list (ask by name if there are several), then social_accounts_list. Use only CONNECTED accounts. If a platform is missing or DISCONNECTED, offer to connect it with oauth_create_authorization and confirm with social_accounts_list after the user says done. Never show IDs.
2. **Upload the slides in order.** For each file: get its size, call media_uploads_create_session (projectId, fileSizeInBytes), split it into `partCount` parts where every part except the last is exactly `partSizeInBytes`, PUT each part's raw bytes to its `uploadUrl`, then call media_uploads_complete_session and keep the media id. Files already in WoopSocial can be found with media_list. If URLs expire, start a new session. If the PUT is blocked, the user must allow `*.r2.cloudflarestorage.com` (claude.ai or Claude Desktop: Settings > Capabilities > Create and edit files, turn on "Use the internet while making files" and add it under Allowed websites > Manage; Claude Code: the sandbox's allowed network domains). If you can't make HTTP requests at all, say so and suggest uploading in the WoopSocial app.
3. **Build the payload.** One content item with the caption and all slides as media, in slide order. Per platform:
   - **Instagram:** `postType: POST`. A carousel is one post with several media.
   - **TikTok:** `postType: PHOTO`. Call social_accounts_get_platform_inputs and let the user choose `privacyLevel` from the options returned; never pick it for them. Also set allowComment (false if comments aren't available for the account), isYourBrand, isBrandedContent and autoAddMusic with the user, and send allowDuet and allowStitch as false (required but unused for photos). A TikTok caption can be adapted with `contentOverride`.
   - **LinkedIn:** an image post on the profile (LINKEDIN) or company page (LINKEDIN_PAGES). Whether LinkedIn accepts several images in one post is decided by posts_validate. PDF or document carousels aren't supported, so don't offer them.
   - Schedule: SCHEDULE_FOR_LATER with `scheduledFor` in UTC, PUBLISH_NOW, or DRAFT (a draft has no date). Add `retryPolicy: {maxRetries: 2, delaySeconds: 300}` unless the user says no.
4. **Validate.** Call posts_validate. It returns `isValid` and a list of `errors` (each with a `path` and a `message`); treat `isValid: false` as a failure even though the call succeeded. If an error names a field you don't recognize, schema_describe shows the tool's full input schema. Fix what it flags (too many items, image size, caption length) and validate again. Ask before changing the user's text. Validation is all or nothing across accounts. Mention any `warnings` to the user.
5. **Confirm.** Show the account per platform (username), post type, the caption per platform, the slides in order, TikTok settings, automatic retry (up to 2 retries, 5 minutes apart), and the time in the user's time zone (ask the zone once if unclear; a past time needs a new one). Ask for a yes. The yes covers only what was shown.
6. **Create.** On yes, call posts_create with the same payload.
7. **Report.** Per platform, say what was scheduled or published. For PUBLISH_NOW, wait about 30 seconds, then check social_account_posts_list. NOT_STARTED or SENDING means it's still going; share externalPostUrl when PUBLISHED, and explain errorMessage in plain words if FAILED, with a fix.

On a 429, wait briefly and retry one call at a time.

## Good to know

- A scheduled post can't be edited in place. To change it, create the new version and then delete the old one, after showing the change and getting a yes.
- For a single photo or a carousel the user already designed, instagram-posts is the shorter path. For a series of carousels, content-calendar-generator can plan them.
