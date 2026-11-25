---
name: sr-seo
description: Finds the phrases people actually search for and puts them in the right places on YouTube, TikTok, Instagram and Google. Builds a keyword table with search intent and placement (title, first line, spoken opening, on-screen text, description, chapters), checks titles and captions against the target phrase, and uses a keyword connector such as vidIQ when one is connected. Use when someone asks about SEO, keywords, search, discoverability, hashtags, or why a good video is not being found. Showrunner has no search-volume data of its own and says so.
license: MIT
compatibility: Any agent that loads Agent Skills. Web search or a keyword connector helps. Python 3.9+ for the title and caption checks.
metadata:
  author: Raj Bharti
  version: "0.1.2"
  family: showrunner
---

# Search and discoverability

Some content is found by recommendation. Some is found because someone typed a question. This skill is for the second kind, and for making recommended content easier to understand.

## What this skill does not have

No search-volume numbers. Showrunner does not include a keyword database. Say so. Use what the person can see themselves (search suggestions as they type, "people also ask", related searches, the videos already ranking), a web search tool if one is available, or a connected keyword tool. vidIQ says its MCP connector works with Claude, ChatGPT and Cursor on every plan including Free (`facts_search id=tooling.vidiq.mcp`; low confidence, and Showrunner is not affiliated with vidIQ). If it is connected, use its keyword and competitor data and name it as the source.

## Ask first

- The topic, and the one outcome someone wants when they search for it.
- The platform (search works differently on each one).
- Whether the person has search or traffic data from their own channel. Their own data beats any guess.

## Method

1. **List the questions.** Write ten plain-language searches a beginner would type. Include the exact words they would use, not the expert terms.
2. **Mark the intent** of each: learn, fix, compare, choose, or just watch.
3. **Check what ranks.** Search each phrase and note what appears. If the top results are huge channels with the exact answer, pick a narrower phrase (add the audience, the tool, the year, the problem).
4. **Pick one primary phrase per piece** and one or two secondary ones. One piece, one main target.
5. **Place them.**

| Where | What to do |
|---|---|
| Title (YouTube) | Primary phrase near the start, written for a person, within the 100-character limit |
| First line of caption or description | Primary phrase in a normal sentence |
| Spoken opening | Say the phrase out loud in the first sentence or two |
| On-screen text | Show it once, big |
| Description (YouTube) | A real summary of two or three sentences that includes the phrase and the secondary ones; chapters with descriptive names |
| Hashtags | A few relevant ones. See the notes below |

## Platform notes (with status)

- **YouTube.** Titles up to 100 characters, descriptions up to 5,000, and with more than 15 hashtags YouTube ignores all of them (all official). YouTube has not published its ranking signals (`youtube.ranking.unpublished`), so what you control is packaging and retention.
- **TikTok.** Search is described as using caption keywords, hashtags, on-screen text and spoken words. Low confidence (`tiktok.search.inputs`). Cover all four.
- **Instagram.** Mosseri said he would not think of hashtags as a way to get more distribution (`instagram.hashtags.distribution`, reported). Put keywords in the caption and on screen, and keep tags few.
- **Google.** Not covered by the facts database. Ask the person to check their own search results.

## Check

Tool `title_score` with `keyword` set, and `caption_check` with `keywords` (`sr-title-thumbnail`, `sr-caption`). CLI:

```
python scripts/sr.py title --keyword "junior developer interview" --file title.txt
python scripts/sr.py caption --file caption.txt --platform youtube --keywords "junior developer interview"
```

## Output

A table the person keeps:

```
Phrase | Intent | Platform | Where it goes | Notes
```

## Gate

`approve`. Then the pieces go through the normal path (`sr-title-thumbnail`, `sr-caption`).

## Do not

- Stuff keywords. Write for the person first.
- Promise ranking. Nobody can.
- Use a trending tag that has nothing to do with the post.
