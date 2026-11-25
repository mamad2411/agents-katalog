---
name: reddit-crosspost
description: Crosspost X/Twitter posts to Reddit. Use when the user shares an X post URL and wants to distribute it across relevant subreddits. Handles subreddit discovery, content adaptation, approval, and browser-automated posting to Reddit.
---

# Reddit Crosspost

## Workflow

1. **Extract post content** — Use the browser to read the X post (web_fetch often fails on X). Get the full tweet text, media type, and topic.

2. **Find subreddits** — Search Reddit via browser for relevant communities:
   - Search `reddit.com/search/?q=<topic keywords>&type=sr` for active subreddits
   - Also check the user's subscribed communities in the sidebar for relevant ones
   - Check each subreddit's rules before recommending (karma reqs, flair requirements, anti-promo rules)
   - Aim for 3-7 subreddits. Prefer ones where the user has existing karma.
   - Skip subreddits with strict anti-AI or anti-promotion rules unless the post genuinely fits as discussion

3. **Present all subreddits** — Return a complete list of every relevant subreddit found:
   - Subreddit name, size, and brief description
   - Why it's relevant to this post
   - Any posting restrictions or rules to watch out for
   - A draft title and body tailored to that subreddit
   - Let the user pick which ones to post to — do NOT post until explicitly approved

4. **Adapt content for each subreddit** — This is critical. See Writing Style below.

5. **Choose post type** — Not everything should be a Text post:
   - **Text post**: Best for discussion starters, opinions, questions. Use when the X post is mostly text/takes.
   - **Link post**: Best when the X post has a video or rich media. The link becomes the main content and Reddit may embed a preview.
   - Check what format performs best in each subreddit (scroll recent top posts to see what gets upvotes — link posts? text? images?)

6. **Post via browser** — Use browser automation to post:
   - Navigate to `https://www.reddit.com/r/<subreddit>/submit`
   - Read the submit page for any requirements (flairs, title formats)
   - Fill in title and body
   - Add required flair if needed
   - Submit the post

7. **Verify each post landed** — Don't assume success just because Reddit redirected:
   - After posting, visit the post URL directly
   - Check it appears in `/r/<subreddit>/new/` — if it doesn't show up within a minute, it was likely spam-filtered
   - Check your profile (`/user/<username>/posts`) to confirm the post exists and isn't marked [removed]
   - If a post got silently removed, tell the user — they may want to message the mods

8. **Post-run report** — After all posts are submitted, give the user a clear summary:
   - ✅ Successful: subreddit name + direct post URL
   - ❌ Failed: subreddit name + reason (spam filter, karma req, flair missing, etc.)
   - ⏭️ Skipped: subreddit name + why
   - Total: X posted, X failed, X skipped

9. **Engage with replies** — Crossposting without engagement looks like spam:
   - After posting, check back on posts within 30-60 minutes (use a cron reminder if needed)
   - Upvote and reply to early comments — even a short "yeah exactly" or "good point" helps
   - This boosts the post in Reddit's algorithm and makes the account look real
   - Don't reply to every single comment — pick 1-2 genuine ones

## Writing Style — Sound Human, Not Like an Agent

This is the most important section. Reddit users instantly detect and downvote "AI slop." Every post must read like a real person typed it casually.

**Title rules:**
- Lowercase unless it's a proper noun. No Title Case.
- Keep it conversational — like you're talking to a friend
- Use incomplete thoughts, questions, or mild takes: "distribution > product in 2026?" not "The Importance of Distribution Strategy in 2026"
- Okay to be slightly messy/informal
- No marketing language: avoid "game-changing," "revolutionary," "here's why," "you need to know"

**Body rules:**
- **Keep it short.** 2-4 sentences is ideal. Reddit rewards punchy posts, not essays. If you can say it in 2 lines, don't use 5.
- Write like a Reddit user, not a marketer. Short paragraphs. Casual tone.
- Start with a personal observation or opinion, not a pitch
- Don't over-explain. Reddit users are smart — imply, don't spell out
- Use lowercase "i" sometimes. Skip a comma. Be slightly imperfect.
- The X link should feel like an afterthought, not the point: "saw this discussed on x the other day" or "full convo here if anyone's curious:" — NOT "Originally shared on X:"
- NO bullet points listing features or takeaways (dead giveaway of AI)
- NO "Let me know what you think!" or "What are your thoughts?" at the end (cliché)
- Vary sentence length. Mix short punchy lines with longer ones.
- Match the specific subreddit's vibe — r/founder is different from r/marketing
- **Cut ruthlessly.** If a sentence doesn't add value, delete it. The best Reddit posts feel effortless, not thorough.

**Examples of BAD (sounds like AI):**
> "Building products has changed more in the last month than in the last decade. Everyone is more focused on distribution than ever. Here's a great conversation about the 2026 tech media strategy. Originally shared on X: [link]"

**Examples of GOOD (sounds human):**
> "anyone else feel like the distribution conversation has completely taken over? like six months ago everyone was heads down shipping, now it's all about how you get seen. caught this pod ep that actually had decent takes on what's working rn — not the usual 'just post on twitter' advice. https://x.com/..."

> "distribution > building right now and i don't think it's even close. this convo breaks it down better than i can https://x.com/..."

## Human-Speed Pacing

The goal: look indistinguishable from a person alt-tabbing between Reddit and other stuff. Bots are fast and predictable. Humans are slow and erratic.

**Typing:**
- Use `slowly: true` on all type actions — never dump a wall of text instantly
- Pause between filling the title and starting the body (1-3 seconds, click around)
- Don't fill both fields in rapid succession like a script would

**Between posts:**
- Wait **3-5 minutes** between subreddit posts (randomize — never the same gap twice)
- After every 2-3 posts, take a longer break (**6-10 minutes**)
- During waits, do something human: scroll the subreddit feed, visit a post, read comments. Don't just sleep and then navigate straight to /submit.
- Vary the order slightly — don't always go submit → type title → type body → post in identical sequence. Sometimes scroll the sub first, sometimes check the rules page.

**Navigation:**
- Don't jump directly to `/r/subreddit/submit` every time — sometimes navigate to the subreddit first, browse for a few seconds, then click "Create post"
- After posting, linger on the confirmation page or the subreddit for a moment before moving on
- Occasionally visit your own profile or inbox between posts (humans do this)

**Time-of-day awareness:**
- Best posting times are generally 8-10am and 6-8pm in the subreddit's dominant timezone (usually US Eastern or Pacific)
- Avoid posting between midnight-6am — posts get buried with zero engagement
- If the user is posting late at night, suggest scheduling for morning instead
- Check the subreddit's recent "hot" posts — if the newest hot post is 12+ hours old, the sub is slow and timing matters less

**Red flags to avoid:**
- Identical time gaps between posts
- Posting to 5+ subs within 10 minutes
- Never visiting any page except /submit
- Typing at inhuman speed (entire paragraphs appearing in <1 second)
- Cookie-cutter identical content across subs (always rewrite per sub — see Content Variation below)

**If Reddit shows a rate limit warning, CAPTCHA, or "you're doing that too much":** stop immediately and tell the user. Don't retry.

## Content Variation

Reddit's spam filter detects near-identical posts across subreddits. Every post must be meaningfully different — not just a word swap.

- **Different angle per sub**: r/marketing post should focus on distribution tactics, r/micro_saas should focus on the builder's dilemma, r/SaaS should focus on market shifts. Same source material, different lens.
- **Different title structure**: question in one, hot take in another, observation in a third. Never the same title pattern twice.
- **Different opening line**: Don't start every post with "i've been building..." — one can start with a question, another with a bold claim, another with "so i saw this thing..."
- **Different length**: Some posts should be 2-3 sentences. Others can be a full paragraph. Variety signals human.
- **The X link should appear in different positions**: middle of the post in one, end in another, as a parenthetical in a third.
- **At least 40% of the words should differ** between any two posts. If you can swap subreddit names and the posts look interchangeable, rewrite harder.

## Browser Resilience

The browser service can be flaky — timeouts, crashes, Reddit's JS being heavy. Plan for it.

- If the browser times out mid-post, wait 15-30 seconds and retry once. If it fails again, save the draft content and tell the user.
- If a post was partially submitted (title filled but body not, or post clicked but no confirmation), check `/user/<username>/new` to see if it went through before retrying — don't double-post.
- If the browser service is fully down, provide all remaining drafts as formatted text so the user can post manually.
- After a browser crash, re-check which tab/targetId is active — they change after restarts.

## Subreddit Rules Awareness

Before posting to any subreddit, check:
- Karma requirements (some need X karma in that specific sub)
- Flair requirements (some won't let you post without selecting a flair)
- Title format requirements (some need prefixes like [Discussion])
- Self-promotion rules (some ban any links to your own content)
- AI content rules (some auto-remove AI-detected content)

If a subreddit is too strict, skip it and tell the user why.

## Error Handling

- If Reddit login is needed, ask the user to log in via the browser first
- If a subreddit blocks the post (spam filter, karma requirements), report it and move on
- If browser automation fails, provide the draft content so the user can post manually
