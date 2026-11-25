---
name: daily-brief
description: Generate and deliver a personalized daily morning brief for Mimi. Use when producing or sending the daily brief, or when the user asks about the daily brief. Triggered automatically each morning at 5 AM via cron.
---

# Daily Brief

Deliver a personalized morning brief each day with three sections: Weather, News, and Intention.

## User Preferences

- **Default location:** Naples, Florida
- **Override:** Use any location the user has specified since the last brief
- **Delivery:** Send via Telegram (current session)

---

## Section 1: Weather

Fetch from `wttr.in` using JSON format (`?format=j1`).

**Always include:**
- High temp for the day
- Low temp for the day
- Average temp for the day

**Weekdays (Mon–Fri):** Also include the average temperature between 8 AM–3 PM (use hourly data, slots for 9:00 and 12:00 cover this window well; average `FeelsLikeF` or `tempF` across those hours).

**Weekends (Sat–Sun):** Instead of the 8–3 avg, include the **peak UV index** for the day and what time it occurs (scan hourly `uvIndex` values).

```bash
curl -s "wttr.in/Naples+Florida?format=j1"
```

---

## Section 2: News

Search for 5 news stories using `web_search`. Run separate searches for each category:

1. **Local** — Naples FL or Southwest Florida news today
2. **National** — top US news today
3. **National** — second major US story today
4. **International** — top world news today
5. **Tech/Business/Innovation** — technology, computer science, or business news today

**Headline style:** Each bullet should read like a short punchy news headline — 8–12 words max. No fluff.

**Links:** Each bullet must include a clickable link to the full article. Format as Telegram markdown: `[Headline text](https://url)`. Use only free-to-access, relatively unbiased sources. Preferred sources (in order):
- Reuters (reuters.com)
- AP News (apnews.com)
- BBC News (bbc.com/news)
- NPR (npr.org)
- The Guardian (theguardian.com)
- axios.com
- Local: naplesnews.com, nbc-2.com, wink-tv.com

Avoid paywalled sites (NYT, WSJ, WaPo unless free article), partisan outlets, and opinion pieces.

---

## Section 3: Intention

Generate a thoughtful quote or fortune for the day. Make it feel personal, not generic. Rotate between:
- Classic philosophical quotes (Stoics, Eastern philosophy, etc.)
- Short poetic fortunes
- Practical wisdom

Keep it to 1–2 sentences max.

---

## Format

Send as a clean, nicely formatted Telegram message using Telegram's MarkdownV2 formatting. Use emoji section headers for visual separation. No tables.

Example structure:

```
☀️ *Good morning, Mimi!*

━━━━━━━━━━━━━━━
🌡 *WEATHER — Naples, FL*
High: 84°F  •  Low: 72°F  •  Avg: 79°F
📅 8AM–3PM avg: 81°F        ← weekdays
🕐 Peak UV: 10 at 1:00 PM   ← weekends

━━━━━━━━━━━━━━━
📰 *NEWS*
🔹 [Local headline here](https://url)
🔹 [National headline here](https://url)
🔹 [National headline here](https://url)
🔹 [World headline here](https://url)
🔹 [Tech/Business headline here](https://url)

━━━━━━━━━━━━━━━
🌟 *INTENTION*
_"Quote or fortune here."_
```

Keep tone warm but concise. No filler openers. Wrap links in angle brackets if embedding plain URLs to suppress previews, but use markdown link format `[text](url)` for clickable headlines.
