---
name: facebook-research-engage
version: 3.1.0
description: |
  Engagement state — uses Chrome DevTools CLI to visit competitor Facebook pages
  AND search for niche-relevant trending posts, extract top comments, analyze
  patterns, and generate 10+ engagement opportunities. Each opportunity includes
  a sarcastic reply to the top-liked comment AND a standalone post comment, both
  using Mexican slang. Takes screenshots of target posts and comments.

allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - ChromeDevTools
  - WebSearch
  - Question
---

# Facebook Research — Engage State (v3.1.0)

Finds 10+ engagement opportunities by scraping competitor posts AND niche-relevant trending posts. For each post, generates two response drafts using sarcasm + Mexican slang: one reply to the top-liked comment, and one standalone post comment.

## Preconditions

- Config exists: `.fb-research/projects/<project-name>/config.json`
- Competitors: `.fb-research/projects/<project-name>/discovered-competitors.json` (or `config.json` competitors as fallback)
- Screenshots dir: `.fb-research/projects/<project-name>/<YYYY-MM-DD_HHMMSS>/screenshots-engagement/  # per-run; legacy at project root`

## Core Approach

Instead of only targeting competitor pages, this skill:
1. Visits competitor pages AND searches Facebook for niche-relevant trending posts
2. Navigates into each post to get the real permalink URL
3. Identifies the **top-liked comment** (most reactions) + extracts top 10 comments
4. Generates **two response drafts per post**:
   - **Reply to top comment**: Sarcastic reply to the most-liked comment, using Mexican slang
   - **Post comment**: Standalone sarcastic comment on the post itself, using Mexican slang
5. Saves 10+ engagement opportunities with clickable post URLs and screenshots

## Steps

### 1. Load Config and Data

```bash
cat .fb-research/projects/<project-name>/config.json
cat .fb-research/projects/<project-name>/discovered-competitors.json 2>/dev/null || echo '{"competitors": []}'
mkdir -p .fb-research/projects/<project-name>/<YYYY-MM-DD_HHMMSS>/screenshots-engagement/  # per-run; legacy at project root
```

Extract: `niche`, `targetKeywords`, `yourTopics`, `pageName`, language.

### 2. Source Posts from Two Channels

#### 2a. Competitor Pages (At least 5 opportunities)

Load competitor pages from discovered-competitors.json (preferred) or config.json fallback.

```bash
cat .fb-research/projects/<project-name>/discovered-competitors.json 2>/dev/null | python3 -c "import sys,json; data=json.load(sys.stdin); [print(c['url']) for c in data.get('competitors',[])]" 2>/dev/null || cat .fb-research/projects/<project-name>/config.json | python3 -c "import sys,json; data=json.load(sys.stdin); [print(c['pageUrl']) for c in data.get('competitors',[])]"
```

For each competitor, follow steps 3-7 to extract posts and comments.

#### 2b. Niche-Relevant Trending Posts (At least 5 opportunities)

Search Facebook for the niche keyword to discover trending posts from pages the audience actually follows:

```bash
chrome-devtools navigate_page --url "https://www.facebook.com/search/posts/?q=<URL_ENCODED_NICHE_KEYWORD>"
```

Scroll to load results:

```javascript
async () => {
  await new Promise(r => setTimeout(r, 5000));
  let lastHeight = 0;
  for (let i = 0; i < 5; i++) {
    window.scrollTo(0, document.body.scrollHeight);
    await new Promise(r => setTimeout(r, 2000));
    const h = document.body.scrollHeight;
    if (h === lastHeight) break;
    lastHeight = h;
  }
  return "Scrolled search results";
}
```

Extract post links from search results:

```javascript
() => {
  const links = document.querySelectorAll('a[href*="/posts/"], a[href*="/videos/"], a[href*="story.php"], a[href*="/reel/"]');
  const seen = new Set();
  const posts = [];
  links.forEach(a => {
    const href = a.getAttribute('href');
    if (!href || seen.has(href)) return;
    const text = a.innerText?.trim();
    if (text && text.length > 10) {
      seen.add(href);
      const fullUrl = href.startsWith('http') ? href : 'https://www.facebook.com' + href;
      const parent = a.closest('[role="article"]') || a.parentElement;
      const context = parent ? parent.innerText?.substring(0, 200) : '';
      posts.push({ text: text.substring(0, 150), url: fullUrl, context: context?.trim() });
    }
  });
  return JSON.stringify(posts.slice(0, 15), null, 2);
}
```

Filter to the 5+ most relevant posts that:
- Have visible engagement (likes/comments/shares)
- Match the page's niche
- Are from different pages (diverse reach)
- Have at least some comments visible (active threads)

### 3. Navigate to Each Post and Get the Real URL

For each post (competitor + niche search), navigate into it to get the actual permalink:

```bash
chrome-devtools navigate_page --url "<post_url>"
```

Wait for load and get the real URL:

```javascript
async () => {
  await new Promise(r => setTimeout(r, 5000));
  return window.location.href;
}
```

### 4. Take Screenshot of the Post

```bash
chrome-devtools take_screenshot --filePath ".fb-research/projects/<project-name>/<YYYY-MM-DD_HHMMSS>/screenshots-engagement/opp-<id>-post.png" --fullPage true
```

### 5. Extract Top Comments (Especially the Top-Liked One)

```javascript
() => {
  const commentElements = document.querySelectorAll('[role="article"]');
  const comments = [];
  commentElements.forEach(el => {
    const text = el.innerText?.trim();
    if (!text || text.length < 10) return;
    const likeText = el.innerText?.match(/(\d+[KMB]?)\s*(reactions?|likes?)/i);
    const likeCount = likeText ? likeText[1] : '0';
    const nameLink = el.querySelector('a[href*="/user/"], a[href*="/profile.php"]');
    const commenterName = nameLink ? nameLink.innerText?.trim() : 'Unknown';
    if (text && text.length < 500) {
      comments.push({ commenter: commenterName, text: text.substring(0, 300), likes: likeCount });
    }
  });
  return JSON.stringify(comments.slice(0, 15), null, 2);
}
```

**Identify the top-liked comment** — the one with the highest reaction count. This is the comment you'll generate a reply to.

### 6. Take Screenshot of the Comments Section

```bash
chrome-devtools evaluate_script --function "async () => { const els = document.querySelectorAll('div[role=article]'); if(els.length > 1) els[els.length-1].scrollIntoView(); await new Promise(r => setTimeout(r, 1000)); return 'Scrolled'; }"
chrome-devtools take_screenshot --filePath ".fb-research/projects/<project-name>/<YYYY-MM-DD_HHMMSS>/screenshots-engagement/opp-<id>-comments.png"
```

### 7. Analyze Comment Patterns

For each post, analyze the extracted comments:

1. **Top-liked comment**: What is it? Why did it get the most likes? (sarcasm, anger, humor, hot take?)
2. **Tone**: Supportive? Angry? Sarcastic? Meme-heavy?
3. **Slang/Regionalisms**: What specific Mexican slang appears? ("wey", "no mames", "pedo", "carnal", "neta")
4. **Inside jokes**: Recurring references, player nicknames, meme formats
5. **What gets likes**: What type of comment gets the most engagement in THREAD?
6. **Arguments**: What fault lines are people arguing over?

### 8. Generate Two Response Drafts Per Post

For each post, generate exactly **two response drafts**:

#### Draft A: Reply to the Top-Liked Comment

A sarcastic reply directed AT the top commenter. This is a response to their specific take, not a standalone comment.

**Rules for Draft A**:
- Address the top commenter directly (use their name or "wey")
- Disagree or one-up their take with sarcasm
- Must use Mexican slang
- Short (1-3 sentences)
- End with a jab or rhetorical question

**Example structure**:
```
@[commenter], [sarcastic disagreement]. [slang-laden follow-up jab]. [rhetorical question or zinger].
```

#### Draft B: Standalone Post Comment

A separate comment on the post itself — not a reply to anyone. This looks like a new top-level comment.

**Rules for Draft B**:
- Does NOT reference any specific commenter
- Could be either:
  - **Hot take**: Strong controversial opinion about the post topic
  - **Sarcastic zinger**: Short, meme-like, funny observation
  - **Analysis + jab**: Shows knowledge then takes a shot
- Must use Mexican slang
- 1-3 sentences
- Ends with engagement bait (rhetorical question or provocative statement)

**Mexican Slang Reference** (use these heavily):
| Slang | Meaning | When to use |
|-------|---------|-------------|
| "No mames" | No way / You're kidding | Disbelief at a bad take |
| "Wey / güey" | Dude | General address |
| "Qué pedo con..." | What's up with... | Questioning something absurd |
| "Está cabrón" | It's crazy/difficult | Intense situation |
| "Neta" | Really? / For real | Expressing disbelief |
| "Me cae" | I swear | Emphasizing agreement |
| "Ándale" | Come on / Let's go | Encouraging / dismissing |
| "A poco" | No way, really? | Sarcastic disbelief |
| "Qué hueva" | How lame | Dismissing something |
| "Carnal" | Bro | Friendly address |
| "Valió madre" | It went to hell | Something failed badly |
| "Ni madres" | Hell no | Strong rejection |
| "Sale" | Okay / Deal | Agreement |
| "Chingón" | Awesome | Approval (use sparingly) |
| "Chale" | Damn / That sucks | Disappointment |

**Sarcasm patterns that work in Mexican football Facebook**:
- "Claro que sí, [obvious sarcasm]" — obvious reverse psychology
- "[Absurd comparison]... pero ok" — dismissing with absurdity
- "Ay wey, no mames" + factual correction — laughing at bad takes
- "El clásico [thing] de [group]" — stereotyping playfully
- "[Fact], pero la raza no está lista para esa conversación" — intellectual superiority bait

### 9. Save Engagement Opportunities

Create `.fb-research/projects/<project-name>/engagement-opportunities.json`:

```json
{
  "project": "<project-name>",
  "niche": "<niche>",
  "language": "es",
  "usesMexicanSlang": true,
  "generatedAt": "<YYYY-MM-DD HH:MM:SS>",
  "analysisRound": <round>,
  "totalOpportunities": 10,
  "sourceBreakdown": {
    "fromCompetitors": 5,
    "fromNicheSearch": 5
  },
  "opportunities": [
    {
      "id": 1,
      "sourceType": "competitor",
      "sourceName": "<page name>",
      "sourceUrl": "https://www.facebook.com/<page_url>",
      "postUrl": "<real_post_permalink>",
      "postPreview": "<first 150 chars of post>",
      "screenshot": "screenshots-engagement/opp-1-post.png",
      "commentsScreenshot": "screenshots-engagement/opp-1-comments.png",
      "topComment": {
        "commenter": "<name>",
        "text": "<full text>",
        "likes": "<count>"
      },
      "commentPatterns": {
        "tone": "sarcastic/angry/supportive",
        "slangUsed": ["wey", "no mames"],
        "commonThemes": ["bad reffing", "player x is overrated"],
        "whyTopCommentWon": "Called out a popular player — gets agreement from haters and defense from fans → engagement"
      },
      "draftReply": {
        "type": "reply_to_top_comment",
        "target": "<top commenter name>",
        "text": "@[commenter], [sarcastic reply using mexican slang]",
        "whyItGetsLikes": "Riding the top comment's coattails + adding a fresh sarcastic angle"
      },
      "draftPostComment": {
        "type": "standalone_comment",
        "variant": "hot_take / sarcastic_zinger / analysis_jab",
        "text": "[sarcastic standalone comment using mexican slang]",
        "whyItGetsLikes": "Psychological trigger explanation"
      },
      "bestTimeToEngage": "Evening (7-10pm local)",
      "value": "high/medium",
      "used": false
    }
  ],
  "strategySummary": {
    "totalOpportunities": 10,
    "sourceBreakdown": "X from competitors, Y from niche search",
    "competitorsTargeted": ["<name1>", "<name2>"],
    "postsAnalyzed": 10,
    "commentsExtracted": "~10 per post",
    "bestTimesToEngage": "Evening (7-10pm local) for max visibility",
    "topCommentReplyStrategy": "Reply to the most-liked comment within 1 hour of posting your reply — the reply notification brings people back to the thread",
    "postCommentStrategy": "Post as a fresh top-level comment — make it controversial or sarcastic enough to get replies",
    "nicheTips": [
      "Post the reply FIRST (to the top comment), then the standalone comment — spreading them out avoids looking spammy",
      "Don't reply AND comment on the same post from the same account — pick ONE per post per session",
      "Max 2 engagements per competitor page per day",
      "Prioritize posts with 10+ comments already — active threads",
      "Reply to replies on your comments to deepen the thread"
    ]
  }
}
```

### 10. Generate HTML Report Section

Generate the engagement section HTML for the report:

```html
<h2>💬 Engagement Opportunities (10+)</h2>
<p>Each opportunity includes a sarcastic reply to the top-liked comment AND a standalone post comment, using Mexican slang.</p>

<!-- Source breakdown -->
<div class="source-breakdown">
  <span class="tag blue">X from competitor pages</span>
  <span class="tag purple">X from niche trending search</span>
</div>

<!-- For each opportunity -->
<div class="opp-card">
  <div class="opp-header">
    <span class="opp-number">#N</span>
    <span class="opp-source">[competitor / niche]</span>
    <span class="opp-page">[Page Name]</span>
  </div>
  <div class="target-links">
    📍 Page: <a href="...">[page]</a>
    📌 Post: <a href="...">View Post</a>
    🖼️ <a href="...">Screenshot</a> · 💬 <a href="...">Comments</a>
  </div>

  <div class="top-comment">
    <strong>🏆 Top Comment</strong> ([likes] likes)<br>
    <em>"[comment text]"</em> — <strong>[commenter]</strong>
  </div>

  <div class="draft reply">
    <strong>✍️ Draft A — Reply to @[commenter]</strong>
    <div class="comment-text">"[sarcastic reply with mexican slang]"</div>
    <div class="why-works">Why it gets likes: [explanation]</div>
  </div>

  <div class="draft post">
    <strong>✍️ Draft B — Post Comment</strong>
    <div class="comment-text">"[sarcastic standalone comment with mexican slang]"</div>
    <div class="why-works">Why it gets likes: [explanation]</div>
  </div>
</div>
```

### 11. Save Engagement Section Report

Save the engagement data to a markdown file:

```bash
cat > ".fb-research/projects/<project-name>/<YYYY-MM-DD_HHMMSS>/screenshots-engagement/engagement-summary.md" << 'EOF'
# Engagement Strategy — Round <N>

## Source Breakdown
- **Competitor posts**: <N> opportunities
- **Niche trending posts**: <N> opportunities
- **Total**: <N> opportunities

## Quick Reference: 10 Drafts

### Opp 1 — [Page Name] — [post topic]
**Reply to @[top commenter]**: "[sarcastic reply]"
**Post comment**: "[sarcastic standalone]"

### Opp 2 — [Page Name] — [post topic]
...

## Commenting Workflow
1. Open the post URL
2. Read the top comments to confirm tone
3. Post Draft A (reply to top comment) OR Draft B (post comment) — not both on same post
4. Reply to replies on your comment
5. Mark as used

## Best Times
- Evening 7-10pm local time
- Weekend afternoons
EOF
```

### 12. Report Completion

```
✅ Facebook Research Engage Complete! (v3.1.0)

Project: .fb-research/projects/<project-name>/
Analysis Round: <N>

Results:
  Total engagement opportunities: 10+
    - From competitor pages: <N>
    - From niche trending search: <N>

Per opportunity:
  - Real post URL (clickable)
  - Screenshot of post
  - Screenshot of comments
  - Top-liked comment identified
  - Draft A: Sarcastic reply to top comment
  - Draft B: Sarcastic standalone post comment
  - Why it gets likes

Slang: Mexican 🇲🇽
Tone: Sarcasm + rage-bait
```

### 13. Fallback: If Chrome DevTools Fails

If Chrome DevTools can't access Facebook:

```bash
websearch "site:facebook.com <niche_keyword> post 2026"
websearch "<niche_keyword> viral Facebook post comments 2026"
```

Extract page names and post URLs from search results. For each result found, note the URL and generate engagement drafts manually based on the search snippet and URL context. At minimum produce the 10 engagement drafts with Mexican slang — the user can visit the posts manually.
