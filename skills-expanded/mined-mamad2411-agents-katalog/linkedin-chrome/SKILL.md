---
name: linkedin-chrome
version: 1.0.0
description: "LinkedIn content management via Chrome browser automation. Use when the user asks to check LinkedIn comments, reply to LinkedIn comments, post on LinkedIn, schedule a LinkedIn post, review LinkedIn engagement, draft a LinkedIn post, check LinkedIn notifications, or manage LinkedIn content. Triggers on: 'LinkedIn', 'check my posts', 'reply to comments', 'schedule a post', 'LinkedIn engagement', 'post to LinkedIn', 'draft a LinkedIn post', 'LinkedIn comments', 'LinkedIn strategy'. Requires Chrome browser automation tools (claude-in-chrome or chrome-devtools-mcp)."
---

# LinkedIn Chrome

Manage LinkedIn content through Chrome browser automation: review engagement, reply to comments, publish posts, and schedule content.

## Prerequisites

- Chrome browser automation available (claude-in-chrome MCP or chrome-devtools-mcp)
- User signed into LinkedIn in the Chrome profile
- If using claude-in-chrome: load tools via ToolSearch before calling them

## Quick Check

Before starting, verify LinkedIn is accessible:

1. Navigate to `https://www.linkedin.com/feed/`
2. Take a snapshot. If you see a login wall, tell the user to sign in first. Do not enter credentials.
3. If signed in, proceed with the workflow.

## Workflows

### 1. Review Engagement

Check comments and reactions on recent posts.

```
Navigate to: https://www.linkedin.com/in/{username}/recent-activity/all/
```

**Steps:**

1. Navigate to the activity page
2. Take a snapshot to see post summaries
3. Use JavaScript to extract post data if the accessibility tree is limited:

```javascript
// Extract visible posts with engagement counts
Array.from(document.querySelectorAll('.feed-shared-update-v2')).slice(0, 10).map(post => {
  const text = post.querySelector('.feed-shared-text')?.innerText?.slice(0, 100) || '';
  const reactions = post.querySelector('.social-details-social-counts__reactions-count')?.innerText || '0';
  const comments = post.querySelector('.social-details-social-counts__comments')?.innerText || '0';
  return { text, reactions, comments };
});
```

4. For posts with comments, click into each post to read the comment threads
5. Summarize: post title snippet, reaction count, comment count, notable commenters

### 2. Reply to Comments

Post replies to specific commenters on your posts.

**Steps:**

1. Navigate to the specific post (use activity page or direct post URL)
2. Scroll to the comment section
3. Find the target commenter's comment
4. Click "Reply" under their comment (not the top-level comment box)
5. Take a snapshot to confirm the reply box is open and focused on the right comment
6. Type the reply text
7. Click the reply/submit button
8. Take a snapshot to confirm the reply posted

**Reply box targeting:**

LinkedIn nests reply boxes. After clicking "Reply" on a comment, the input area appears indented below that comment. Verify by snapshot that:
- The reply box mentions the commenter's name
- You are not accidentally typing in the top-level comment box

**Typing strategy:**

LinkedIn's editor is a contenteditable div, not a standard input. Use the fill or type tool, not JavaScript injection. If the editor doesn't accept input:
1. Click the reply box to focus it
2. Use the type/fill tool with the text
3. Take a snapshot to verify text appeared before submitting

### 3. Publish a New Post

**Steps:**

1. Navigate to `https://www.linkedin.com/feed/`
2. Click "Start a post" (the text input area at the top of the feed)
3. Wait for the post composer modal to appear
4. Take a snapshot to confirm the editor is open
5. Click into the text area of the composer
6. Type the post content
7. Take a snapshot to verify the full text is in the editor
8. Click "Post" to publish immediately

**After posting:**

1. Wait 2-3 seconds for LinkedIn to process
2. Find the new post (it may show a "View post" link or appear at the top of the feed)
3. If a first comment is needed (for links -- see Link Placement below), click "Comment" on the post and add it immediately

### 4. Schedule a Post

**CRITICAL: Use claude-in-chrome (computer tool), NOT chrome-devtools-mcp for scheduling.** LinkedIn's scheduler uses custom React inputs that reject CDP-level DOM manipulation. The chrome-devtools-mcp fill/type tools cannot set the date or time. The claude-in-chrome computer tool provides real mouse/keyboard interaction that works.

**Steps (using claude-in-chrome computer tool):**

1. Get tab context with `tabs_context_mcp`, create a new tab with `tabs_create_mcp`
2. Navigate to `https://www.linkedin.com/feed/`
3. Click "Start a post" using computer tool `left_click`
4. Click into the text area and use `type` to enter post content
5. Click the clock/schedule icon (bottom-left of composer, next to Post button)
6. The schedule dialog opens with Date and Time fields
7. **Set the date:** Triple-click the date field to select all, then `type` the new date (e.g., "3/27/2026"). A calendar picker appears. Click the target date on the calendar.
8. **Set the time:** The time field defaults to the next available slot. If it needs changing, triple-click and type (e.g., "8:00 AM"), then Tab out.
9. Verify the header shows the correct "Fri, Mar 27, 8:00 AM" confirmation
10. Click "Next" to proceed to the confirmation screen
11. The Post button changes to "Schedule". Click "Schedule" to confirm.
12. Verify "Post scheduled" toast appears at the bottom.

**Important:** Scheduled posts cannot have a first comment added at schedule time. Create a calendar reminder for the user to add the first comment when the post goes live.

### 5. Draft Content (No Browser Needed)

Draft post content based on existing blog posts, engagement patterns, or user direction. This step does not require browser automation.

**Process:**

1. Read the LinkedIn campaign memory file if it exists
2. Check existing blog content for untapped post material
3. Draft the post following the Content Guidelines below
4. Get user approval before publishing or scheduling

## Content Guidelines

### Voice

Match the user's established LinkedIn voice:
- Direct, conversational, like telling a story over beers
- Specific details: names, years, technologies, outcomes
- No marketing language, no keynote-style closers
- Short paragraphs. One idea per paragraph. Let the reader breathe.

### AI Tell Avoidance

These patterns signal AI-generated content. Avoid them:

| Pattern | Fix |
|---------|-----|
| Triple repetition ("real X, real Y, real Z") | Say it once, plainly |
| Balanced closing sentences | End abruptly or casually |
| Parallel structure punchlines | Make it conversational |
| Lists of exactly four items | Use three, or five, or just prose |
| "Here's what I'd tell you" framing | Just say it |
| Keynote-style one-liner endings | End mid-thought or with a short sentence |
| Em dashes | Use periods or commas |

### Link Placement

**Never put external links in the post body.** LinkedIn's algorithm suppresses posts with outbound links.

Always place links in the **first comment** posted immediately after the post goes live. Format:

```
The full breakdown: {url}
```

### Post Structure

What works (based on engagement data):
- **Open with a scene:** Year, place, specific situation
- **Build with concrete details:** Technology names, numbers, outcomes
- **Land on a lesson:** One sentence. Not a motivational quote.

What doesn't work:
- Abstract positioning without a story
- General advice not grounded in experience
- Long analytical posts without a narrative arc

### Posting Cadence

- Space posts 1-2 days apart so they don't cannibalize each other's reach
- Best days: Tuesday, Wednesday, Thursday
- Best times: 8-9 AM or 12-1 PM local time
- Reply to comments on existing posts between new posts to maintain engagement

## Agentic Workflow & Vibe Coding

- **Iterative Drafting:** Do not expect the perfect LinkedIn post on the first attempt. Draft a V1, review against the Content Guidelines (checking for "AI tells"), isolate specific tonal issues or formatting errors, refine exactly ONE section at a time, and regenerate until the voice matches the user.
- **Vibe Coding:** Save your working drafts locally (e.g., in a `.md` file) before attempting to use browser automation to publish or schedule. If automation fails, you still have the approved content.

## DOM Reference

LinkedIn's DOM changes frequently. These selectors are starting points. Always verify with a snapshot before interacting.

### Activity Page

```
URL: https://www.linkedin.com/in/{username}/recent-activity/all/
Posts: .feed-shared-update-v2
Post text: .feed-shared-text
Reactions count: .social-details-social-counts__reactions-count
Comments count: .social-details-social-counts__comments
```

### Post Composer

```
Trigger: Click "Start a post" on feed page
Text area: contenteditable div inside the modal (.ql-editor or [role="textbox"])
Post button: button with text "Post" (becomes blue/active when text is entered)
Schedule icon: Clock icon button next to Post button
```

### Comment Box

```
Top-level: .comments-comment-box__form [role="textbox"]
Reply box: Appears after clicking "Reply" on a comment, nested under that comment
Submit: Button with text "Comment" or "Reply" inside the comment form
```

## Troubleshooting

### Login wall

LinkedIn requires authentication. Do not attempt to log in. Tell the user to sign in manually in the Chrome profile, then retry.

### Editor not accepting text

LinkedIn uses a rich text editor (contenteditable). If typing doesn't work:
1. Click the editor to ensure focus
2. Try using the keyboard type tool instead of fill
3. As a last resort, use JavaScript: `document.querySelector('[role="textbox"]').innerText = 'your text'` followed by dispatching an `input` event

### Post not appearing after publish

After clicking "Post", LinkedIn may show a brief confirmation. The post sometimes doesn't appear at the top of the feed immediately. Navigate to the activity page to verify.

### Stale snapshots

LinkedIn dynamically loads content. If elements from a snapshot are gone, take a fresh snapshot. Comment sections especially change as threads expand/collapse.
