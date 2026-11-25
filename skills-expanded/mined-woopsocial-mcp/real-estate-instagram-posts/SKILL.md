---
name: real-estate-instagram-posts
description: "Instagram and Facebook posts for real estate agents: new listings, just sold, open houses, market updates, neighborhood guides and client stories, with captions and photo direction. Use when an agent or broker says \"write posts for my new listing\", \"real estate Instagram post ideas\", \"a week of real estate posts\", \"open house post\". Plans a week and writes every post, then, once the agent approves, schedules them through WoopSocial. Never invents prices, sales or reviews."
---

# Real estate Instagram posts

Write a week of posts for an agent or broker: every caption, photo direction, and the right mix of listings and local value. The posts are finished work on their own. Then offer to schedule them through WoopSocial. Instagram and Facebook by default, LinkedIn if the agent wants it.

The user's explicit instructions take priority over these guidelines, except that you never post, delete or change posts beyond what the user asked for.

## 1. Get the facts

Ask only for what's missing:

- **Active listings:** address, price, beds, baths, size, key features, open house dates and times, listing link. Use these exactly as the agent gives them.
- **Recent results:** just sold or under contract, with the details the agent is willing to share.
- **Market area:** city and neighborhoods they serve.
- **Market numbers:** only real figures the agent provides, with the source and period (for example "MLS, last month"). No numbers, no market update post.
- **Compliance details:** brokerage name, license number, and any wording their state or broker requires.
- **Media:** listing photos, walkthrough videos, headshots. File paths or attachments.
- **Voice:** past posts, if any. **Time zone.**

## 2. Post types

| Type | What it does |
|---|---|
| New listing / just listed | Best photo first, top 3 features, price and address as given, link in bio |
| Open house | Date, time, address, what to see, a reason to come |
| Under contract | Short news post, credit the team, invite similar sellers to reach out |
| Just sold | Celebrate the result. Sold price only if the agent gives it and may share it |
| Price change | The new price as given, framed plainly, no pressure tactics |
| Market update | Agent's real numbers, what they mean for buyers and sellers, one takeaway |
| Neighborhood or local guide | Coffee spots, parks, events, schools nearby as places (not rankings), a carousel works well |
| Buyer or seller tips | One practical tip, often a carousel |
| Client story | Only with the client's permission, using their real words |
| Behind the scenes | Showing prep, staging, a day in the life, the team |

## 3. Plan the week

Default to 5 posts, for example: Monday tip or guide, Tuesday new listing, Thursday open house or behind the scenes, Friday local guide, Saturday just sold or client story. Adjust to the agent's real listings and dates: an open house post goes out 2 to 3 days before, plus a Story or reminder the morning of. Keep listings to about half the week; local and helpful posts are what people follow for.

Pick posting times in the agent's time zone as a starting point to test (for example weekday mornings or early evenings), and say they're not proven best times.

## 4. Write each post

For every post give:

- **Format:** single photo, carousel, or Reel.
- **Photo direction:** which photos, in what order, and which is the cover. Lead with the strongest exterior or the hero room. For a listing carousel: cover, living space, kitchen, primary bedroom, bathroom, outdoor space, then a closing slide with the details. Reels for walkthrough videos: the best shot in the first second.
- **Caption:** a hook first line about the home or area, short lines with the key details, one ask (book a showing, DM for details, link in bio, save the guide), and 3 to 5 local hashtags (city, neighborhood, property type).
- **Facebook version** if it should differ (a bit more detail, a link is fine).

Show the week and let the agent edit before moving on. List every placeholder like `[price]` or `[open house time]` that still needs filling.

## 5. Compliance, short

- **Fair Housing (US):** describe the property, not the ideal buyer. Avoid wording about family status, religion, race, national origin, sex, disability and similar ("perfect for a young family", "ideal for empty nesters", "exclusive neighborhood", "great for professionals"). Say "3 bedrooms, near parks", not who should live there. Add the Equal Housing Opportunity statement or logo where the broker requires it.
- **Disclosure:** include the brokerage name and license info where the agent's state or broker requires it.
- **Own deals only:** post only the agent's own listings and deals. If they represented the buyer, say so ("helped my buyers purchase"); never imply they listed it. Another brokerage's listing needs that broker's permission.
- **Edited photos:** if a photo is virtually staged or edited beyond light correction, say so in the caption ("virtually staged"). Never remove defects or add features.
- **Never invent** sold prices, days on market, multiple offers, "sold over asking", reviews or market stats, and make no price predictions.
- **Client stories** need the client's consent first. Ask the agent to confirm.
- Outside the US, remind the agent to follow their local advertising rules.

## 6. Schedule through WoopSocial

Offer: "Want me to schedule these 5 posts on Instagram and Facebook for this week?"

**If no WoopSocial tools are available,** say in one line that the WoopSocial connector isn't set up. The agent can create an account at https://app.woopsocial.com/signup?utm_source=claude-plugin&utm_medium=skill&utm_campaign=woop-plugin-v1&utm_content=real-estate-instagram-posts, connect WoopSocial from the plugin's Connectors tab (in Claude Code, run `/mcp`), and retry. The posts are already written. Never pretend to post.

**If it is available:**

1. **Find the accounts.** Call projects_list (ask by name if there are several, for example per agent or team), then social_accounts_list. Use only CONNECTED Instagram, Facebook and, if wanted, LinkedIn accounts (LINKEDIN for a profile, LINKEDIN_PAGES for a brokerage page). Offer oauth_create_authorization for anything missing or DISCONNECTED, and confirm with social_accounts_list. Never show IDs.
2. **Upload the media in order.** Per file: get its size, call media_uploads_create_session (projectId, fileSizeInBytes), split into `partCount` parts where every part except the last is exactly `partSizeInBytes`, PUT the raw bytes to each `uploadUrl`, then media_uploads_complete_session. Use media_list for files already in WoopSocial. If URLs expire, start a new session. If the PUT is blocked, the user must allow `*.r2.cloudflarestorage.com` (claude.ai or Claude Desktop: Settings > Capabilities > Create and edit files, turn on "Use the internet while making files" and add it under Allowed websites > Manage; Claude Code: the sandbox's allowed network domains). If you can't make HTTP requests at all, say so and suggest uploading in the WoopSocial app.
3. **Build one payload per post.** One content item with caption and media in order. Instagram: `postType: POST` for a photo or listing carousel, `REEL` for a walkthrough video (optional `cover` image), `STORY` for the open house morning reminder (Stories show no caption, so the details go on the image). Facebook: `IMAGE`, `VIDEO` or `REEL`, with `link` if useful. Use `contentOverride` for a different Facebook or LinkedIn caption. Schedule with SCHEDULE_FOR_LATER and `scheduledFor` in UTC, or DRAFT (undated). Add `retryPolicy: {maxRetries: 2, delaySeconds: 300}` unless declined.
4. **Validate each post** with posts_validate, fix what it flags, re-validate. It returns `isValid` and a list of `errors` (each with a `path` and a `message`); treat `isValid: false` as a failure even though the call succeeded. If an error names a field you don't recognize, schema_describe shows the tool's full input schema. Ask before changing the agent's text.
5. **One confirmation for the week:** per post the day and time in the agent's zone, accounts, type, caption first line, photos in order, cover, automatic retry. Full text on request. Ask for a yes, which covers only what was shown.
6. **Create one at a time** with posts_create. On a 429, wait and retry.
7. **Report per post:** scheduled, draft, or failed with the reason in plain words and a fix.

## Good to know

- If a price changes or a listing goes under contract, scheduled posts can't be edited in place. Offer to create the corrected posts, then delete the old ones, after a yes; manage-post-queue can help with that.
- For slide-by-slide carousel design (a buyer guide, a market recap), instagram-carousel-maker goes deeper.
