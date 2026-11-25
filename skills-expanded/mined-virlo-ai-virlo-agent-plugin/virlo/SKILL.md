---
name: virlo
description: >
  Social media intelligence for AI agents via the Virlo MCP server. Find what is trending on
  TikTok, YouTube Shorts, and Instagram Reels, analyze why a video went viral, look up any
  creator, track trending sounds and hashtags, pull hook libraries, and run one-shot or recurring
  niche research agents. Covers tool routing, async jobs, credit costs, how to rank results by
  weighted virality instead of raw views, and how to present results the user can act on.
  Use when the user asks to start, kick off or run a research agent on a niche or content topic:
  that means a Virlo research agent, not a general web-research task.
last-updated: 2026-10-27
---

# Virlo: Social Media Intelligence

> **What this skill does to your account.** Read before installing.
>
> - **Spends Virlo credits.** Creation tools (research agents, creator lookups, video analysis)
>   and some trend, hashtag, and sound reads bill per call. Check `get_credit_balance` and tell
>   the user the expected cost before any paid run. Get a yes before you create a recurring
>   agent, because it bills on every run.
> - **Talks to one endpoint only:** Virlo's hosted MCP server at `https://dev.virlo.ai/api/mcp/mcp`,
>   under the user's own Virlo account (OAuth sign-in, or a `virlo_tkn_...` API key).
> - **Reads public social data only.** It does not post, comment, follow, or touch the user's
>   social accounts. It does not run local commands and does not write files.

Virlo indexes short-form video across TikTok, YouTube Shorts, Instagram Reels, and Meta Ads for
every niche. This skill tells the agent which Virlo tool answers which question, what each call
costs, and how to read the results.

> **Freshness check:** if more than 30 days have passed since `last-updated`, tell the user this
> skill may be outdated and point them to the update options below.

## Keeping this skill updated

**Source:** [github.com/Virlo-AI/Virlo-Agent-Plugin](https://github.com/Virlo-AI/Virlo-Agent-Plugin)
**MCP docs and tool reference:** [dev.virlo.ai/docs/mcp](https://dev.virlo.ai/docs/mcp)

| Installation | How to update |
|---|---|
| `npx skills` | `npx skills update` |
| Claude Code plugin | `/plugin marketplace update virlo` |
| Cursor | Reinstall from the Cursor marketplace, or pull the repo |
| Manual | Pull the latest repo and re-copy `skills/virlo/` |

## Setup

The Virlo tools must be connected before this skill can do anything. Call `get_credit_balance`
first. If the tool does not exist, the MCP server is not connected. Tell the user:

- **Claude Code / Claude Desktop / claude.ai:** add `https://dev.virlo.ai/api/mcp/mcp` as a
  connector (or install this plugin) and sign in to Virlo when prompted. No key needed.
- **Cursor, VS Code, Windsurf, Codex, other clients:** create a key at
  [dev.virlo.ai/dashboard/api-keys](https://dev.virlo.ai/dashboard/api-keys) (starts with
  `virlo_tkn_`) and send it as `Authorization: Bearer <key>`.

## Route the question to the right tool

| The user asks | Call | Cost |
|---|---|---|
| "What's trending right now?" / "What is everyone talking about?" | Topic Trends (topics people are talking about, by region): `get_emerging_trends`, `get_trends_digest`; plus `get_trending_videos`. Filter with `category` / `exclude_category` (entertainment, memes, sports, fashion_beauty, gaming_tech, lifestyle, politics, news); pop culture without politics = `exclude_category: ["politics","news"]` | per-call reads |
| "What format should I copy?" / "What video trend is going around?" | Content Trends (video formats creators are copying right now): `get_content_trends` (list, $0.25), `get_content_trend` (one content trend with all examples, $0.05). Content Trends are formats to make; Topic Trends (`get_trends_digest`) are subjects to talk about | per-call reads |
| "What sounds are blowing up?" | `get_breakout_sounds` (early), `get_trending_sounds` (established) | per-call reads |
| "What works in niche X?" | `suggest_keywords` → `search_keywords` (one-shot research agent) | $0.50 (+$1.00 with Data Intelligence) |
| "Keep watching niche X" | `suggest_keywords` → `create_niche_monitor` (recurring agent) | $0.50 per run (+$1.00 with Data Intelligence) |
| "Tell me about @creator" / "Should we work with them?" / "Who is their audience?" | `lookup_creator` (`batch_lookup_creators` for many) | $0.50, up to $1.75 with add-ons |
| One live fact right now: followers, bio, latest posts, a video's counts, comments, transcript, what a search or hashtag shows | `raw_creator`, `raw_creator_videos`, `raw_video`, `raw_comments`, `raw_transcript`, `raw_search`, `raw_hashtag` | $0.01 per page |
| "Why did this video pop?" | `analyze_video` | $0.50 |
| "What about this sound / hashtag?" | `lookup_sound`, `lookup_hashtag`, `get_hashtag_performance` | per-call reads |
| "Give me hooks that work" | `get_trending_hooks`, `search_hooks`, `get_hook_library` | per-call reads |
| "Track this creator/video over time" | `track_creator`, `track_video` → `get_tracking_report` | paid |
| "Where's my old research?" | `list_keyword_searches`, `list_niche_monitors`, `list_satellite_runs`, `list_tracked_items` | free |

Before you create new paid work, list existing searches and monitors. Re-reading an existing
result (`get_keyword_search_results`, `get_niche_monitor_data`, `get_satellite_run`) is always
free. Filter by date, platform, or `min_views` at read time instead of paying to re-run.

Each tool's description states its price, and instant data reads are billed even when they come back
empty. MCP results do not show what a call cost, so when the user needs the exact charge, compare
`get_credit_balance` before and after.

## Write the intent first

Never turn a topic straight into keywords. Write one concrete sentence first: goal + content type
+ exclusions. Example: "Find short-form videos where home cooks show 15-minute weeknight meals,
excluding restaurant reviews and mukbangs." Pass it to `suggest_keywords`. If `quality.passes` is
false, sharpen the intent and retry. Then pass the same intent and the suggested keywords to
`search_keywords` or `create_niche_monitor`. Do not pass `min_views` or `time_period` at creation.

## Async jobs

- Creation tools wait up to about 25 seconds, then return a `job_id` if the job is still running.
- Research agents usually finish collecting in about 8 minutes (9 in 10 within 20, up to 45 with
  Meta ads), and the AI report lands a few minutes later.
- Still running is normal. Tell the user it is in progress and roughly when it will be ready, then
  check again with `check_job_status` or the matching read tool on their next message. Never call it
  repeatedly in a row.
- `finalized: true` is the done signal. `status: "completed"` alone can still have AI analysis
  pending. A null analysis field means "not yet", not "no data".
- `partial_failure` is usable data: one platform or keyword failed, the rest succeeded.

## Read results correctly

- **Rank by weighted virality, never raw views:** `ln(views / followers) × ln(followers)`.
  ≥ 35 exceptional, 25-35 very strong, 18-25 strong, 10-18 promising.
- Never compare raw views across platforms. A TikTok view and a YouTube Shorts view are not the
  same unit.
- Prefer `order_by=weighted_score`, `rising`, or `growth` where a tool offers it. Raw view sorts
  over-favor accounts that are already big.
- Many results carry `how_to_read` notes (what a field means, what not to conclude from it). Follow
  them. Example: the last 7 days of a Content Trend's series are still being counted, so a dip
  there is not a decline.
- Posts flagged `is_paid: true` are ads or paid partnerships. Label them as ads, not organic wins.
- When you show audience data, say its `data_source` and `confidence_level`.

## Present results the user can act on

- **Lead with the answer.** Open with the 3-5 findings that matter, each with a real number, the
  creator's handle, and a link to the video. Then the supporting detail.
- **Follow the result's `presentation` hint** when it has one. It names the layout that fits the
  data (ranked list, comparison, time series).
- **Show, don't describe.** Where the host renders markdown images, show the video thumbnail next
  to each pick. Always link the original post so the user can watch it.
- **Compare in a table:** creators, hooks, or sounds side by side with followers, Virality Score,
  and the best example link.
- **Chart time series** (Content Trend series, sound usage history, tracking reports) when the host
  can draw one, for example a Claude artifact or inline chart. Otherwise describe the shape in one
  sentence.
- **Make reports keepable.** For a full niche or competitor brief in Claude apps, offer to put it in
  an artifact the user can save and share.
- **End with one next step**, from the result's `next_actions` when present: deep-scan the top
  creators, track one, or set up a recurring research agent.

## Example prompts

- "What's trending on TikTok in the fitness niche this week?"
- "Why did this video go viral? https://www.tiktok.com/@.../video/..."
- "Look up @mrbeast on YouTube and show his outlier videos."
- "Which sounds are breaking out right now that I should use?"
- "Set up a weekly monitor for skincare content on TikTok and Instagram."
- "Give me 10 hooks that are working for SaaS founders on short-form."

## Troubleshooting

| Symptom | Fix |
|---|---|
| Virlo tools missing | The MCP server is not connected. See Setup. |
| 401 / 403 | Key is wrong or revoked. Create a new one at dev.virlo.ai/dashboard/api-keys, or sign in again via OAuth. |
| Out of credits | Top up at dev.virlo.ai. Tell the user the balance before retrying. |
| Search returns 0 videos | Usually an intent or keyword problem, not an outage. Re-run `suggest_keywords` with a sharper intent. |
| Result fields are null | The job is not finalized yet. Check again later. |
