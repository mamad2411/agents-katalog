---
name: restaurant-instagram-posts
description: "Instagram, Facebook and TikTok posts for restaurants, cafes and bars: menu items, daily specials, events, behind the scenes, staff and real guest reviews (with permission), with captions and photo ideas. Use when the owner says \"write our Instagram posts\", \"restaurant post ideas\", \"post today's special\", \"a week of posts for my cafe\". Plans a week around opening hours and specials, writes every post, then, once the owner approves, schedules them through WoopSocial."
---

# Restaurant Instagram posts

Write a week of posts for a restaurant, cafe or bar: captions that make people hungry, photo direction, and timing around when guests decide where to eat. The posts are finished work on their own. Then offer to schedule them through WoopSocial. Instagram and Facebook by default, TikTok for short videos.

The user's explicit instructions take priority over these guidelines, except that you never post, delete or change posts beyond what the user asked for.

## 1. Get the facts

Ask only for what's missing:

- **Opening days and hours,** plus any holiday or changed hours coming up.
- **This week's specials and menu highlights,** with names, prices and descriptions exactly as the owner gives them.
- **Events:** live music, quiz night, tastings, with date, time and whether booking is needed.
- **How guests act:** book (link or phone), order (delivery or takeaway link), or walk in.
- **Location:** city and neighborhood, for local hashtags. **Time zone.**
- **Media:** photos or short videos of dishes, the room, the team. File paths or attachments.
- **Voice:** past posts, if any.

## 2. Post types

| Type | What it does |
|---|---|
| Dish or menu highlight | One dish, close up, what makes it good |
| Daily or weekly special | What, when, until it runs out, price as given |
| Event | Live music, quiz night: date, time, what to expect, how to book |
| Behind the scenes | Kitchen prep, sourcing, suppliers, staff, the person behind a dish |
| Seasonal menu | What's new and why now |
| Review or UGC reshare | Only real ones, used with the guest's permission and credited to them |
| Opening and holiday hours | Plain and easy to read, often a Story too |

## 3. Plan the week

Build around the days they're open. A typical 5-post week: a dish highlight early in the week, the weekly special, a behind the scenes post, the weekend event or Friday special, and a weekend brunch or Sunday post. Skip days they're closed.

Timing: post before the decision moment, for example late morning before lunch and late afternoon before dinner, in the restaurant's time zone. Say these are starting points to test, not proven best times. Specials go out the morning of, events 2 to 5 days before plus a reminder on the day.

## 4. Write each post

For every post give:

- **Format:** single photo, carousel, or Reel / short video.
- **Photo direction:** what to shoot and how. Natural light near a window, the dish at its best angle (overhead for flat plates, 45 degrees for burgers and drinks), steam, a pour, a hand reaching in. For video: the most appetizing moment in the first second, vertical, no long intros. Name the cover photo.
- **Caption:** short and sensory. A hook first line (taste, texture, the moment), one or two lines of detail, a clear ask (book a table, order now, come by tonight) with how to do it, and 3 to 5 local hashtags (city, neighborhood, cuisine).
- **Facebook version** if it should differ, with the booking or order link.
- **TikTok version** for videos: a short caption and a few hashtags.

Show the week and let the owner edit. List every placeholder like `[price]` or `[booking link]` that still needs filling.

## 5. Accuracy and rules

- **Never invent** prices, ingredients, allergens, awards, reviews or quotes. Use what the owner gives, or a placeholder.
- **Allergens and dietary claims** ("gluten free", "vegan", "nut free") must be confirmed by the owner before posting. Ask each time. Never call a dish "allergen free" or "safe for allergies"; point guests to staff for allergen questions.
- **Reviews and guest photos:** only real ones, used with the guest's permission and credited. Never write or edit a review's words.
- **Alcohol:** promotions must follow local rules, and posts must not target or appeal to minors. No pressure to drink more. Ask the owner if unsure what's allowed where they are. On Instagram and Facebook, alcohol businesses should turn on the account's age restriction in the app (WoopSocial can't set it). On TikTok, posts that promote alcohol can be restricted, so lead with food or the venue there.

## 6. Schedule through WoopSocial

Offer: "Want me to schedule this week's posts on Instagram and Facebook?"

**If no WoopSocial tools are available,** say in one line that the WoopSocial connector isn't set up. The owner can create an account at https://app.woopsocial.com/signup?utm_source=claude-plugin&utm_medium=skill&utm_campaign=woop-plugin-v1&utm_content=restaurant-instagram-posts, connect WoopSocial from the plugin's Connectors tab (in Claude Code, run `/mcp`), and retry. The posts are already written. Never pretend to post.

**If it is available:**

1. **Find the accounts.** Call projects_list (ask by name if there are several, for example one per location), then social_accounts_list. Use only CONNECTED accounts. Offer oauth_create_authorization for anything missing or DISCONNECTED, and confirm with social_accounts_list. Never show IDs.
2. **Upload the media.** Per file: get its size, call media_uploads_create_session (projectId, fileSizeInBytes), split into `partCount` parts where every part except the last is exactly `partSizeInBytes`, PUT the raw bytes to each `uploadUrl`, then media_uploads_complete_session. Use media_list for files already in WoopSocial. If URLs expire, start a new session. If the PUT is blocked, the user must allow `*.r2.cloudflarestorage.com` (claude.ai or Claude Desktop: Settings > Capabilities > Create and edit files, turn on "Use the internet while making files" and add it under Allowed websites > Manage; Claude Code: the sandbox's allowed network domains). If you can't make HTTP requests at all, say so and suggest uploading in the WoopSocial app.
3. **Build one payload per post.** One content item with caption and media in order. Instagram: `POST` for photos and carousels, `REEL` for video, `STORY` for hours (Stories show no caption, so the text must be on the image). Facebook: `IMAGE`, `VIDEO`, `REEL` or `TEXT_ONLY`, with `link` for booking or ordering. TikTok: `VIDEO` (or `PHOTO` for a photo carousel); call social_accounts_get_platform_inputs and let the owner choose `privacyLevel`, and set allowComment, isYourBrand, isBrandedContent and autoAddMusic with them, and allowDuet and allowStitch for VIDEO (send both as false for PHOTO). Use `contentOverride` for platform-specific captions. Schedule with SCHEDULE_FOR_LATER and `scheduledFor` in UTC, or DRAFT (undated). Add `retryPolicy: {maxRetries: 2, delaySeconds: 300}` unless declined.
4. **Validate each post** with posts_validate, fix what it flags, re-validate. It returns `isValid` and a list of `errors` (each with a `path` and a `message`); treat `isValid: false` as a failure even though the call succeeded. If an error names a field you don't recognize, schema_describe shows the tool's full input schema. Ask before changing the owner's text.
5. **One confirmation for the week:** per post the day and time in the restaurant's zone, accounts, type, caption first line, media, TikTok settings, automatic retry. Full text on request. Ask for a yes, which covers only what was shown.
6. **Create one at a time** with posts_create. On a 429, wait and retry.
7. **Report per post:** scheduled, draft, or failed with the reason in plain words and a fix.

## Good to know

- A special sold out or an event cancelled? Scheduled posts can't be edited in place. Offer to create the corrected posts, then delete the old ones, after a yes; manage-post-queue can help.
- For a menu carousel designed slide by slide, instagram-carousel-maker goes deeper. For a full month, content-calendar-generator.
