---
name: arrows-daily-brief
description: "Arrows daily brief. A short read for the start of the day, built for a phone: what to do first, what changed since yesterday (new replies, stage changes), today's calls with deal context, messages waiting on a reply, deals at risk, and open time. Sales leaders also get a line per rep. Pulls calendar, CRM, call recordings, email and chat, and uses the person's sales profile. Use whenever someone says 'Run my Arrows daily brief', asks what's on today, what they missed overnight, what needs them this morning, or wants a rundown of their day and pipeline, even if they don't say 'brief'."
---


A daily brief for today, short enough to read on a phone before the first call:

| Section | What's in it |
|---|---|
| Do first | The 2–5 things that matter most today, in order |
| Since yesterday | Buyer replies, stage changes, wins, losses, signed contracts |
| Today's calls | Each external call: who, where the deal stands, what's open |
| Replies waiting | Buyers who are waiting on the person |
| At risk | Deals that are going quiet or slipping |
| Team (leaders) | One line per rep: what's at risk, what's closing, what needs the leader |
| Open time | Free blocks of 30+ minutes |

## Step 1: Read the profile

Use the profile files (see the shared context) to decide what matters, not just to describe it:

- `arrows-how-i-work.md`: `## What slips` is the person's own list of things to flag; check today's calls and deals for each one. `## Where my time goes` tells you which prep to do for them. `## My rules` apply to every suggested action.
- `arrows-sales-process.md`: stage names, what has to be true to move on, and the methodology under `## Discovery and qualification`. Use them to judge whether a deal is stuck.
- `arrows-buyers-and-competitors.md`: competitor names, so you recognize them when they come up.
- `arrows-how-we-work.md` or a leader role in `## About me`: turn on the Team section (Step 3).

No profile, or it doesn't say: they lead a team if other people own most deals they're involved in (as a contact, follower or meeting attendee), or their calendar has recurring 1:1s with reps. If so, turn on Team.

No profile: run the brief anyway and use the CRM's stage names.

## Step 2: Gather

Read everything before writing. Stay inside this budget so the brief finishes quickly:

- **Calendar:** every meeting on today. Sort them into sales calls (with a buyer, prospect or customer: a CRM deal or contact, or a booking from a prospect), other external meetings (vendors, partners, agencies, recruiting) and internal ones. Note open blocks of 30+ minutes.
- **Each sales call:** the matching CRM deal (stage, amount, close date, next step), the last 3–5 activities, the most recent call summary, and the latest email or chat thread with the attendees. Look for what was promised and whether it happened. If CRM is thin on a new contact, a quick web search for their role is enough. Deeper research belongs to pre-call prep.
- **Since yesterday:** everything since the start of the previous working day (on Monday, since Friday morning): buyer emails and chat messages received, deal stage changes, deals created, won or lost, contracts signed or viewed. Use CRM activity or stage history where it exists; otherwise compare last-modified dates and say the stage change is inferred.
- **Replies waiting:** buyer or prospect emails and direct messages from the last 7 days where the buyer wrote last and the person hasn't answered. Skip newsletters, automated mail, internal threads, group channels, and replies to a mass email (a webinar or newsletter) unless they ask the person something.
- **Pipeline:** open deals the person owns (for leaders, their team's), up to 150, using filtered queries rather than reading each record. Read notes only on deals that look at risk. If there are more, say how many you read.

**At risk** means any of: no two-way touch (a buyer reply, call or meeting) in 14+ days, no next step on the deal, or a promised next step that didn't happen (a date passed, a deliverable not sent, a meeting that never got booked). Check email, chat and call history before calling a deal quiet: a buyer reply in chat yesterday means it isn't quiet, even if the CRM says otherwise. A passed close date on its own is "slipped", not at risk: mention it in the deal's `why` when the deal is at risk for another reason. A contract unsigned for 7+ days counts as a promised next step that didn't happen. Deals with no activity in 60+ days (often in an old pipeline) go in `closeOut` by name instead of `atRisk`, so the at-risk list stays about deals that can still be saved. A deal created in the last 14 days isn't at risk just for having no next step yet; that's noise on a new deal.

## Step 3: Write the brief

The brief is a report page with a fixed design. Copy the template under `## Report template` at the end of this file exactly and replace only the `DATA` object. Don't restyle it, add or drop sections, or write your own HTML: the person should find everything in the same place every morning, scheduled runs included. Empty lists show a short "nothing here" line, which is right on a quiet day.

Show it as an artifact. If you can't, save the filled template as `daily-brief.html` and share the file. Only if you can't show or save HTML at all, write the same sections in the same order as Markdown (below). On someone's first run, add one chat line: "You'll get the same page every morning; 'How this report works' at the bottom explains each section."

**Filling `DATA`.** Rows are a few words; the full story goes in `detail` (a list of dated facts with their source, for example "Sep 30 call: asked for the security doc"). Amounts are plain numbers (24000); leave them out when they're 0 or unknown. Use first names for people, including in `owner`. Never write "you" or "your" in `DATA`: use the person's first name ("Dana owes this"), reps' first names, or "the team", since the page gets forwarded and "you" means nothing to the next reader. Quoted text (email subjects, call quotes) can keep it; the chat message can still speak to the person directly. Use company names, not CRM deal names.

| Field | What goes in it | Limit |
|---|---|---|
| `name`, `company`, `date`, `view`, `updated` | First name; their company (from the profile, CRM or email domain; titles the page when there's a Team section, "Sales team" if unknown); "Tuesday, October 6"; "My day" or "My day + team · 3 reps"; when this ran | |
| `numbers` | `calls` (sales calls today), `replies`, `atRisk` (the full count, even if fewer are listed), `changes` (items in New since yesterday) | numbers |
| `doFirst` | `deal` (the company, shown in bold so the eye finds the account first), `amount`, `owner` (leaders: whose deal), `action` (starts with a verb and names who to contact, "Email Dana to book the security review"), `why`, `steps` (required: 2–3 numbered steps, who, how, by when), optional `context` (date and source) | 2–5 items; action 8 words, why 12 |
| `sinceYesterday` | `kind` ("good": moved forward, won, signed; "bad": lost, slipped; "" for a reply or neutral news), `deal`, optional `amount` and `owner`, `what`, `detail` | 6 items; what 10 words |
| `atRisk` | Every at-risk deal, worst first (up to about 40; the page shows the top 5, or the 6 biggest team-wide for leaders, and groups the rest by rep): `deal`, `amount`, `owner`, `stage`, `quietDays` (number, or null if no touch is logged), `channel` of the last touch, `why` (which at-risk reason), `next` (one action), `detail` | why 12 words |
| `calls` | `time`, `company`, `type`, `people` ("Name (title) · Name (title)"), `deal` ("Stage · $24k · close Nov 16 · last two-way touch 6 days ago"), `open` (what happened last time and what's still open), optional `prep` (one action), `detail` | sales calls only; open 25 words |
| `otherMeetings` | One line for vendor, partner and internal meetings | 15 words |
| `closeOut` | Names of deals with no activity in 60+ days, shown as one line | names only |
| `replies` | `name`, `company`, `channel`, `ask`, `waitingDays` (number), `detail` | 5 items |
| `team` | Leaders only, one per rep, most at risk first: `name` (exactly as in `owner`, since opening a rep lists their at-risk deals), `atRiskCount`, `closingCount` (this week), `ask` (the one thing that needs the leader), optional `detail` | ask 15 words |
| `openTime` | `start`, `end`, `length` for blocks of 30+ minutes | |
| `howBuilt` | What was read, any sampling, anything that failed or isn't connected | 40 words |

Markdown version, only when HTML isn't possible:

```
**Daily brief · [Weekday], [Month] [Day]**
[N] calls · [N] replies waiting · [N] at risk

**Do first**
1. [Specific action] — [why today, one line]
2. [Specific action] — [why today]

**Since yesterday**
- [Company]: [Buyer] replied — [what they said or asked, a few words]
- [Company]: moved [stage] → [stage]
- [Company]: [won / lost / contract signed]

**Today's calls**
**[Time] · [Company]** · [call type]
[Name] ([title]) · [Name] ([title])
[Stage] · $[amount] · close [date] · last two-way touch [N] days ago
[One or two lines: what happened last time and what's still open.]
→ [One action before the call, if there is one]

**Replies waiting**
- [Name], [Company] · [email / chat] · [what they asked] · [N] days

**At risk**
- [Company] · [stage] · $[amount] · [the reason: quiet [N] days / no next step / promised [X] by [date], not done] → [action]

**Team**
- [Rep]: [N] at risk, [N] closing this week. [The one deal or decision that needs the leader.]

**Open time**
[Start]–[End] · [Start]–[End]
```


**Do first** pulls the most important items from every other section, ranked by what's due soonest: something blocking a call today goes first. Each item is concrete ("Send the security doc to [Buyer] before the 2pm call"), not general ("Follow up with [Company]"). Use `## What slips` from the profile to decide what rises to the top. On a clean day write "Nothing urgent. Just show up to your calls."

**Today's calls:** sales calls only, at most five lines each. Mark a first call, or a person new to the deal (with their LinkedIn link, since that's the one time it's worth the space). If a profile methodology gap is glaring for this stage (for example a pilot with no economic buyer named), say it in the "still open" line. Vendor, partner and internal meetings share one line at the end ("Also: 8:00 agency kickoff, 3 internal"), plus one flag only if something is due before it.

**At risk:** list every at-risk deal in `DATA`, worst first; the page shows the top few and summarizes the rest. Every line names the specific reason and one action.

**Team (leaders only):** one line per rep, under 30 words, worst first: counts, then the single deal or decision that most needs the leader (a close this week going quiet, an approval, an exec intro, a call they're on). The full list belongs in the weekly pipeline review, not here. Keep the leader's own deals in the sections above.

**Open time:** list the blocks and stop. Don't plan the time for them.

**Length:** the visible rows should read in a minute (about 400 words, 500 for a leader); everything else goes in `detail`. Stick to the item limits above and group the rest ("+4 stage moves on the team"). In the Markdown version, if they say they're on their phone or in a hurry, keep it under 300 words: Do first and Since yesterday in full, then only what needs action today.

## Step 4: Close

The chat message next to the page stays short, four lines at most: (1) what's most urgent; (2) on a first run only, the first-run line; (3) one offer: the scheduling offer if it applies, otherwise the next skill (with no profile, the setup suggestion); (4) a missing-source note, if any.

1. **One next skill, only if earned:** "Want me to run pre-call prep on the [time] [Company] call?" or "The [Company] call yesterday has no follow-up yet. Want me to run post-call on it?" or "Want me to draft a nudge for [Company]?" Skip it on a clean day.
2. **Scheduling, only if you can create scheduled tasks and none already runs the daily brief:** "Want this waiting for you every weekday at 7am? Say yes, or give me a time." Check the existing scheduled tasks first. If they say yes, create a weekday task (default 7:00 local) whose prompt is "Run my Arrows daily brief", confirm it in one line, and don't offer again. If you can't create scheduled tasks, say nothing about scheduling.

## Special cases

- **No calendar connected:** use the pasted calendar if given; otherwise skip Today's calls and Open time, and add one line at the end: "Connect your calendar (your name at bottom left, then Settings, then Connectors) and I'll include today's calls."
- **No CRM connected:** use pasted deals if given. Otherwise build the call and pipeline view from email, calls and calendar, mark deal stages as inferred, and mention once at the end that connecting the CRM or pasting a CSV export of open deals makes the at-risk list complete.
- **A source fails partway:** retry once, then continue with what you have and say so in one line at the end ("Email didn't load, so Replies waiting may be incomplete").
- **No calls today:** lead with Do first, then Since yesterday and At risk. That's still a useful brief.
- **Weekend or holiday date:** brief the next working day and say so in the header.
- **Leader with no deals of their own:** skip Today's calls if they have no external meetings; Team becomes the main section, right after Since yesterday.

## Rules

- **Only what you verified.** If there's no data for a call, write "No history found", rather than guessing what the call is about. A wrong fact in a daily read teaches the person to stop trusting it.
- **Specific over general.** Quote the commitment and the date ("You said you'd send the case study by Friday. Not sent yet."). Vague flags get skipped.
- **No cheerleading, no padding.** It's a memo, not a pep talk. Suggested actions after → are fine; "Big day!" isn't.
- **Background research only when it changes the call.** Company news, funding or LinkedIn posts go in only if they tie to something in the deal. Competitors only when they came up in a real conversation.
- **No emojis.** The template carries the structure; in the Markdown version, bold labels do.
- **Read only.** Don't update the CRM, send, draft into the inbox or create anything without the person approving it. The scheduling task is created only after they say yes.

## Report template

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Daily brief</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{
  color-scheme:light;
  --paper:#F7F6F3; --card:#FFFFFF; --ink:#171614; --ink-70:rgba(23,22,20,.7); --ink-50:rgba(23,22,20,.58); --ink-30:rgba(23,22,20,.3);
  --line:#E9E8E4; --chip:#F3F2EF; --track:#ECEAE6;
  --green:#1F8A4C; --green-soft:#E8F4EC;
  --red:#D33A24; --red-soft:#FCEAE6;
  --gold:#FEBC22; --gold-soft:#FFF4D6; --gold-text:#8A5A00;
  --display:'Plus Jakarta Sans','Segoe UI',sans-serif;
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:14px/1.5 "Plus Jakarta Sans","Segoe UI","Helvetica Neue",Arial,sans-serif;-webkit-font-smoothing:antialiased}
.wrap{max-width:960px;margin:0 auto;padding:16px 16px 40px}
.num{font-variant-numeric:tabular-nums}
.chip{display:block;font-family:var(--display);font-size:18px;font-weight:700;letter-spacing:-.2px;color:var(--ink)}
.hero{background:#171614;color:#FFFFFF;position:relative;border-radius:4px;padding:20px 24px 18px}
.hero h1{font-family:var(--display);font-feature-settings:"lnum","tnum";color:#FFFFFF;font-size:32px;line-height:1.12;letter-spacing:-.6px;font-weight:700;margin:0 0 4px;max-width:760px}
.hero .sub{color:rgba(255,255,255,.75);font-size:15px;margin:0 0 16px}
.health{display:flex;height:10px;border-radius:2px;overflow:hidden;background:rgba(250,248,245,.15)}
.g-fill{background:var(--green)}
.r-fill{background:var(--red)}
.stats{display:grid;grid-template-columns:repeat(4,1fr);margin-top:14px;border-top:1px solid rgba(250,248,245,.16)}
.stat{padding:14px 12px 0 0}
.stat+.stat{padding-left:16px;border-left:1px solid rgba(250,248,245,.16)}
.stat .n{font-family:var(--display);font-feature-settings:"lnum","tnum";font-size:28px;font-weight:700;letter-spacing:-.5px}
.stat .l{font-size:12px;color:rgba(255,255,255,.75)}
.stat .key{display:inline-block;width:8px;height:8px;border-radius:2px;margin-right:6px;vertical-align:1px}
.card{background:var(--card);border:1px solid var(--line);border-radius:4px;padding:20px 22px;margin-top:16px}
.head{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:6px;padding-bottom:10px;border-bottom:1px solid var(--line)}
.hint{font-size:12px;color:var(--ink-50)}
.item{border-top:1px solid var(--line)}
.head + .item{border-top:0}
.row{display:grid;grid-template-columns:26px 1fr 14px;gap:6px;padding:10px 0;align-items:start}
details.item summary{list-style:none;cursor:pointer}
details.item summary::-webkit-details-marker{display:none}
details.item summary .row::after{content:"";width:7px;height:7px;border-right:1.5px solid var(--ink-30);border-bottom:1.5px solid var(--ink-30);transform:rotate(-45deg);margin-top:7px;transition:transform .15s}
details.item[open] summary .row::after{transform:rotate(45deg)}
details.item summary:hover .row::after{border-color:var(--ink-70)}
.mark.dot::before{content:"";display:inline-block;width:8px;height:8px;border-radius:50%;background:var(--ink-30);margin-top:6px}
.mark.dot.r::before{background:var(--red)}
.mark.dot.g::before{background:var(--green)}
.tick{width:16px;height:16px;border-radius:50%;background:var(--green);color:#fff;font-size:10px;font-weight:700;display:flex;align-items:center;justify-content:center;margin-top:2px}
.title{font-weight:600}
.who{font-size:12px;color:var(--ink-50);font-weight:400;margin-left:6px}
.sub2{font-size:13px;color:var(--ink-70)}
.detail{margin:0 20px 12px 28px;padding:10px 12px;background:#F5F4F1;border-radius:6px;font-size:13px;color:var(--ink-70)}
.detail ul,.detail ol{margin:0;padding-left:18px}
.detail ol li{color:var(--ink)}
.detail .ctx{margin-top:8px;font-size:12px;color:var(--ink-50)}
a.stat{display:block;color:inherit;text-decoration:none;cursor:pointer}
a.stat:hover .l{text-decoration:underline;text-underline-offset:2px}
section[id]{scroll-margin-top:12px}
.cols{display:grid;grid-template-columns:1fr 1fr}
.cols > .item:nth-child(odd){padding-right:22px;border-right:1px solid var(--line)}
.cols > .item:nth-child(even){padding-left:22px}
.num-badge{width:22px;height:22px;border-radius:50%;background:var(--ink);color:#fff;font-size:12px;font-weight:700;display:flex;align-items:center;justify-content:center;margin-top:-1px}
.cols > .item:nth-child(-n+2){border-top:0}
.detail li+li{margin-top:3px}
.next{color:var(--ink);font-size:13px}
.next::before{content:"→ ";color:var(--ink-30)}
.qline{margin:3px 0 2px}
.tag.r{background:var(--red-soft);color:var(--red)}
.tag.g{background:var(--green-soft);color:var(--green)}
.tag.n{background:var(--chip);color:var(--ink-70)}
.empty{font-size:13px;color:var(--ink-50);padding:6px 0}
.rep-row{display:grid;grid-template-columns:190px 1fr;gap:12px}
.minibar{display:flex;height:8px;border-radius:2px;overflow:hidden;background:var(--track);margin-top:6px;max-width:220px}
.more{font-size:12px;color:var(--ink-50);padding-top:10px;border-top:1px solid var(--line)}
.r-al{text-align:right}
.meta{font-size:12px;color:var(--ink-50)}
footer{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-top:20px;font-size:12px;color:var(--ink-50)}
footer details summary{cursor:pointer}
footer a{color:var(--ink-70);text-decoration:underline;text-underline-offset:2px}
footer a:hover{color:var(--ink)}
.about{max-width:680px;margin-top:6px;padding:12px 14px;background:var(--card);border:1px solid var(--line);border-radius:4px;color:var(--ink-70);font-size:13px}
.about p{margin:0 0 8px}
.about p:last-child{margin:0}
.about b{color:var(--ink);font-weight:600}
.tag.g{color:#127A3E!important}
.y-fill{background:var(--gold)}
.mark.dot.y::before{background:var(--gold)}
.tag.y{background:var(--gold-soft);color:var(--gold-text)}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:16px;align-items:start}
.grid2 .card,.grid3 .card{margin-top:0}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:16px;align-items:start}
.card.won{border-top:3px solid var(--green)}
.card.lost{border-top:3px solid var(--red)}
.card.won .head,.card.lost .head{border-bottom:0}
.mark{font-weight:700;color:var(--ink-30);font-size:14px}
.tag{display:inline-block;font-size:12px;font-weight:600;border-radius:2px;padding:1px 6px;white-space:nowrap;margin-left:6px}
.qline .tag{margin-left:0}
.stage{display:grid;grid-template-columns:170px 1fr 100px;gap:14px;align-items:center;padding:9px 0;border-top:1px solid var(--line)}
.head + .stage{border-top:0}
.stage .bar{display:flex;height:12px;border-radius:2px;overflow:hidden}
.stage .gap{grid-column:2/4;font-size:12px;color:var(--ink-50);margin-top:-6px}
.legend{display:flex;gap:16px;font-size:12px;color:var(--ink-50);margin-top:10px}
.legend i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:5px;vertical-align:-1px}
footer details p{max-width:640px;margin:6px 0 0}
@media (max-width:720px){
  .hero{padding:22px 18px 18px}
  .hero h1{font-size:25px}
  .stats{grid-template-columns:repeat(2,1fr)}
  .stat:nth-child(3){padding-left:0;border-left:0}
  .stat:nth-child(n+3){margin-top:10px}
  .grid2,.grid3,.cols{grid-template-columns:1fr}
  .cols > .item:nth-child(2){border-top:1px solid var(--line)}
  .cols > .item:nth-child(odd){padding-right:0;border-right:0}
  .cols > .item:nth-child(even){padding-left:0}
  .card{padding:16px}
  .detail{margin:0 0 12px 28px}
  .rep-row{grid-template-columns:1fr;gap:4px}
  .stage{grid-template-columns:1fr 90px}
  .stage .bar{grid-column:1/3}
  .stage .gap{grid-column:1/3;margin-top:0}
}
.row.t{grid-template-columns:52px 1fr 14px}
.time{font-weight:700;font-size:13px;color:var(--ink);margin-top:1px}
</style>
</head>
<body>
<div class="wrap" id="app"></div>
<script>
/* Fill in DATA only. Leave everything else as is. */
const DATA = {
  name: "[First name]",
  company: "[Company, for the team view]",
  date: "[Weekday, Month Day]",
  view: "[My day | My day + team · N reps]",
  updated: "[date, time]",
  numbers: { calls: 0, replies: 0, atRisk: 0, changes: 0 },
  doFirst: [],
  sinceYesterday: [],
  atRisk: [],
  closeOut: [],
  calls: [],
  otherMeetings: "",
  replies: [],
  team: [],
  openTime: [],
  howBuilt: "[What was read, any sampling, anything missing]"
};

const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
const money = n => n == null || n === "" ? "" : n >= 1e6 ? "$" + (n / 1e6).toFixed(1).replace(/\.0$/, "") + "M" : n >= 1e3 ? "$" + Math.round(n / 1e3) + "k" : "$" + n;
const list = a => (a || []).filter(Boolean);
const detailBox = d => {
  const lines = Array.isArray(d) ? list(d) : d ? [d] : [];
  return lines.length ? `<div class="detail"><ul>${lines.map(l => `<li>${esc(l)}</li>`).join("")}</ul></div>` : "";
};
const stepsBox = (steps, context) => {
  const st = list(steps);
  if (!st.length && !context) return "";
  return `<div class="detail">${st.length ? `<ol>${st.map(x => `<li>${esc(x)}</li>`).join("")}</ol>` : ""}${context ? `<div class="ctx">${esc(context)}</div>` : ""}</div>`;
};
const item = (mark, title, sub, detail, box0, cls) => {
  const body = `<div class="row${cls ? " " + cls : ""}">${mark}<div>${title}${sub ? `<div class="sub2">${sub}</div>` : ""}</div></div>`;
  const box = box0 || detailBox(detail);
  return box ? `<details class="item"><summary>${body}</summary>${box}</details>` : `<div class="item">${body}</div>`;
};
const quiet = d => d.quietDays == null ? `<span class="tag r">no touch logged</span>` : `<span class="tag ${d.quietDays >= 14 ? "r" : "n"}">${d.quietDays === 0 ? "today" : d.quietDays + "d quiet"}${d.channel ? " · " + esc(d.channel) : ""}</span>`;
const kindMark = k => k === "good" ? `<span class="tick">✓</span>` : `<span class="mark dot ${k === "bad" ? "r" : ""}"></span>`;
const D = DATA, N = D.numbers, team = list(D.team).length > 0;

const go = id => `href="#${id}" onclick="const t=document.getElementById('${id}');if(t){t.scrollIntoView({behavior:'smooth'});}return false;"`;
const cols = items => items.length ? `<div class="cols">${items.join("")}</div>` : "";
const AR = list(D.atRisk), cap = team ? 6 : 5;

let h = "";
h += `<section class="hero"><h1>${team ? esc(D.company || "Sales team") + " daily brief" : esc(D.name) + "'s daily brief"}</h1><p class="sub">${esc([D.date, D.view].filter(Boolean).join(" · "))}</p>`;
h += `<div class="stats num">
  <a class="stat" ${go("calls")}><div class="n">${N.calls}</div><div class="l">Sales calls today</div></a>
  <a class="stat" ${go("replies")}><div class="n">${N.replies}</div><div class="l">Replies waiting</div></a>
  <a class="stat" ${go("at-risk")}><div class="n">${N.atRisk}</div><div class="l"><span class="key r-fill"></span>Deals at risk</div></a>
  <a class="stat" ${go("since")}><div class="n">${N.changes}</div><div class="l">New since yesterday</div></a>
</div></section>`;

h += `<section class="card" id="do-first"><div class="head"><span class="chip">Do first</span><span class="hint">Open any item for the steps</span></div>`;
h += list(D.doFirst).length ? cols(list(D.doFirst).map((t, i) => item(`<span class="num-badge">${i + 1}</span>`, `<span class="title">${esc(t.deal)}</span><span class="who num">${esc([money(t.amount), t.owner].filter(Boolean).join(" · "))}</span><div>${esc(t.action)}</div>`, esc(t.why), null, stepsBox(t.steps, t.context) || detailBox(t.detail) || detailBox(t.why ? [t.why] : [])))) : `<div class="empty">Nothing urgent today.</div>`;
h += `</section>`;

h += `<section class="card" id="since"><div class="head"><span class="chip">New since yesterday</span><span class="hint">Replies, stage moves, wins and losses</span></div>`;
h += list(D.sinceYesterday).length ? cols(list(D.sinceYesterday).map(s => item(kindMark(s.kind), `<span class="title">${esc(s.deal)}</span><span class="who">${esc([money(s.amount), s.owner].filter(Boolean).join(" · "))}</span>`, esc(s.what), s.detail))) : `<div class="empty">Nothing changed since yesterday.</div>`;
h += `</section>`;

h += `<section class="card" id="at-risk"><div class="head"><span class="chip">${team ? "Biggest at risk" : "At risk"}</span><span class="hint">${AR.length > cap || N.atRisk > cap ? `Top ${Math.min(cap, AR.length)} of ${Math.max(N.atRisk, AR.length)}` : ""}</span></div>`;
if (AR.length) {
  h += cols(AR.slice(0, cap).map(d => item(`<span class="mark dot r"></span>`,
    `<span class="title">${esc(d.deal)}</span><span class="who num">${esc([money(d.amount), d.owner, d.stage].filter(Boolean).join(" · "))}</span><div class="qline">${quiet(d)}</div>`,
    `${esc(d.why)}<div class="next">${esc(d.next)}</div>`, d.detail)));
  const rest = AR.slice(cap);
  if (rest.length) h += `<div class="more">${rest.length} more${team ? ", grouped by rep in Team below" : ": " + esc(rest.map(d => d.deal).join(", "))}</div>`;
} else h += `<div class="empty">No deals at risk today.</div>`;
if (list(D.closeOut).length) h += `<div class="more">Close out (${list(D.closeOut).length}, no activity in 60+ days): ${esc(list(D.closeOut).join(", "))}</div>`;
h += `</section>`;

if (team) {
  const repBox = r => {
    const mine = AR.filter(d => d.owner === r.name).map(d => [d.deal, money(d.amount), d.stage].filter(Boolean).join(" · ") + ": " + (d.why || ""));
    return detailBox([...mine, ...(Array.isArray(r.detail) ? r.detail : r.detail ? [r.detail] : [])]);
  };
  h += `<section class="card" id="team"><div class="head"><span class="chip">Team</span><span class="hint">Most at risk first · open a rep for their deals</span></div>`;
  h += list(D.team).map(r => item(`<span class="mark dot ${r.atRiskCount ? "r" : "g"}"></span>`,
    `<div class="rep-row"><div><span class="title">${esc(r.name)}</span><div class="meta num">${r.closingCount || 0} closing this week</div></div><div><span class="sub2">${esc(r.ask)}</span>${r.atRiskCount ? `<span class="tag r">${r.atRiskCount} at risk</span>` : `<span class="tag g">On track</span>`}</div></div>`,
    "", null, repBox(r))).join("");
  h += `</section>`;
}

h += `<section class="card" id="calls"><div class="head"><span class="chip">Today's calls</span><span class="hint">${list(D.calls).length ? list(D.calls).length + " sales calls" : ""}</span></div>`;
h += list(D.calls).length ? list(D.calls).map(c => item(`<span class="time num">${esc(c.time)}</span>`,
  `<span class="title">${esc(c.company)}</span><span class="who">${esc(c.type)}</span><div class="meta">${esc(c.people)}</div><div class="meta num">${esc(c.deal)}</div>`,
  `${esc(c.open)}${c.prep ? `<div class="next">${esc(c.prep)}</div>` : ""}`, c.detail, "", "t")).join("") : `<div class="empty">No sales calls today.</div>`;
if (D.otherMeetings) h += `<div class="more">Also: ${esc(D.otherMeetings)}</div>`;
h += `</section>`;

h += `<section class="card" id="replies"><div class="head"><span class="chip">Replies waiting</span><span class="hint">${list(D.replies).length || ""}</span></div>`;
h += list(D.replies).length ? cols(list(D.replies).map(r => item(`<span class="mark dot ${r.waitingDays >= 2 ? "r" : "y"}"></span>`, `<span class="title">${esc(r.name)}</span><span class="who">${esc([r.company, r.channel].filter(Boolean).join(" · "))}</span>`, `${esc(r.ask)} <span class="tag ${r.waitingDays >= 2 ? "r" : "y"}">${r.waitingDays === 0 ? "today" : r.waitingDays + "d waiting"}</span>`, r.detail))) : `<div class="empty">No buyer is waiting on a reply.</div>`;
h += `</section>`;

h += `<section class="card" id="open-time"><div class="head"><span class="chip">Open time</span></div>`;
h += list(D.openTime).length ? cols(list(D.openTime).map(o => `<div class="item"><div class="row"><span class="mark dot g"></span><div><span class="title num">${esc(o.start)}–${esc(o.end)}</span><span class="who">${esc(o.length)}</span></div></div></div>`)) : `<div class="empty">No open blocks of 30+ minutes.</div>`;
h += `</section>`;

h += `<footer><details><summary>How this report works</summary><div class="about">
<p>This page is rebuilt from the calendar, CRM, email and calls each time it runs, in the same layout and order, so every section is always in the same place. It only reads those tools: nothing in the CRM, inboxes or calendars was changed.</p>
<p><b>New since yesterday</b> covers buyer replies, stage changes, wins, losses and signed contracts since the start of the previous working day. <b>At risk</b> means one of three things: no two-way contact in 14+ days, no dated next step, or a promised next step that didn't happen. <b>Slipped</b> means the close date has passed and the deal is still open. <b>Close out</b> names deals with no activity in 60+ days: close them with a reason or restart them. <b>Replies waiting</b> are buyers who wrote last and haven't heard back. <b>Today's calls</b> lists sales calls only; other meetings are on one line below them.</p>
<p>Open the arrow on any row for the details and where they came from.</p>
<p><b>Today:</b> ${esc(D.howBuilt)}</p></div></details><span>Updated ${esc(D.updated)} · Built with Sales Skills by <a href="https://arrows.to/claude-for-teams/?utm_source=sales-skills&utm_medium=report&utm_campaign=daily-brief" target="_blank" rel="noopener">Arrows</a></span></footer>`;
document.getElementById("app").innerHTML = h;
</script>
</body>
</html>
```

---

# Shared context for every Sales Skill (read before starting)

## The person's sales profile

(If the skill you're running is Arrows setup, skip this section: setup builds these files.)

Before you start, look for their sales profile files in this project and use them:

- `arrows-voice.md`: how they write and talk. Use it for anything you draft as them.
- `arrows-sales-process.md`: stages, what moves a deal, methodology, why they win and lose.
- `arrows-buyers-and-competitors.md`: what they sell, who buys, pricing, competitors.
- `arrows-how-i-work.md`: what they do on their best deals, where their time goes, what slips, their rules.
- `arrows-how-we-work.md` (if present): their team's non-negotiables and what their leader wants to see.
- `arrows-crm-guide.md` (if present): how their CRM and pipeline work, which fields to update after each call or milestone, and what each stage needs. Use it whenever you suggest CRM updates.

Look sections up by their `##` heading. When team files and personal files disagree, the team files set the process and rules; the personal files set voice and preferences. Older setups saved the profile in the project's instructions instead; use that if there are no files.

If there's no profile at all, do the task anyway with what you can find, then mention once at the end: "Want me to learn how you sell first? Say 'Build my sales profile'. It takes about 5 minutes and makes every skill sound like you."

---

## Before you start

Check what other tools and data sources you have access to. Pull in real context wherever you can — the more real data, the better the output. Don't ask the rep to go find information you can look up yourself.

**Core sources:**
- **CRM (HubSpot, Salesforce, etc.):** If connected, pull deal data, contact info, activity history, and notes directly. Cross-reference what the rep says with what's actually in the CRM.
- **Call recordings (Gong, Fathom, Fireflies, etc.):** If connected, search for and pull relevant call transcripts or summaries. Look for recent calls with the companies mentioned.
- **Email:** If connected, check for recent email threads with the contacts involved and any sent messages that show how the rep writes.
- **Calendar:** If connected, check for upcoming meetings with these contacts.

**Extra sources (often overlooked but high value):**
- **Chat (Slack, Teams, etc.):** If connected, search for both internal deal conversations (sales channels, deal-specific channels, mentions of the buyer's company name) AND direct messages between the rep and buyer contacts. Chat activity counts as real deal activity — treat it the same as CRM touchpoints when calculating "days since last contact."
- **Contracts and signing (DocuSign, PandaDoc, etc.):** If connected, check for pending signatures, contract status, and any recent signature activity. Contracts sitting unsigned are often where deals quietly die.
- **Documents and knowledge (Notion, Google Drive, Confluence, etc.):** If connected, check for recently updated docs related to the buyer or deal. Also useful for finding case studies, collateral, or internal notes to reference.
- **Quoting and proposals (CPQ tools, Proposify, etc.):** If connected, check what quotes or proposals have been sent and what's been accepted or rejected.

Use everything you find. The rep's time is valuable — do the legwork so they don't have to.

---

## The Arrows skills available to suggest

Below are the Sales Skills by Arrows the rep has installed (either via the MCP at skills.arrows.to or as standalone skill files). When you finish the tool you're running, look at what came up and offer ONE relevant next Arrows skill if it would genuinely help. Concrete suggestion, not a pile. Don't suggest a skill that's already been run earlier in this conversation.

**Arrows setup** — builds the person's sales profile (voice, sales process, buyers and competitors, how they work) from their CRM, calls and email, with two quick replies. Saves it as arrows-*.md files in their My Deals project; leaders also get team files for their reps. Run first, or to refresh. Trigger: "Build my sales profile."

**Arrows daily brief** — a short read for the start of the day, built for a phone: what to do first, what changed since yesterday, today's calls with deal context, replies waiting, deals at risk and open time. Leaders also get a line per rep. Trigger: "Run my Arrows daily brief."

**Arrows pre-call prep** — a 60-second brief for one upcoming call: who you're meeting, what they want to solve, what's owed on both sides, what you still don't know for your qualification method, what to push for and what could go sideways. Finds the call by itself. Trigger: "Run the Arrows meeting prep for [company]."

**Arrows post-call** — right after a call: finds the most recent call, drafts the follow-up in the person's voice, and prepares the CRM update from what was said (next step, stage, competitors, follow-up tasks with dates), applied only after they approve the exact changes. Trigger: "Run my Arrows post-call."

**Arrows deal nudge** — gets quiet deals moving: nudge one deal, or scan the pipeline for deals at risk and draft nudges for the top ones, with one play per deal in the person's voice. Leaders get it by rep. Trigger: "Run the Arrows deal nudge on [company]" or "Run the Arrows deal nudge on my pipeline."

**Arrows weekly pipeline review** — a visual one-page review of every open deal: what's moving forward, what's at risk and why, what to do this week, and what's expected to close. Leaders get a rollup by rep with what to raise in each 1:1. Same page every week; can run every Monday. Trigger: "Run my weekly pipeline review."
**Arrows process gaps report** — finds what's falling through the cracks, measured against the person's own sales process: $ at risk, $ gone quiet and promises missed; a list by deal (follow-ups promised but not sent, missing next steps, single-threaded deals, no economic buyer, close dates and stages that don't match activity); the habits their best deals got that the rest didn't; and the 3–5 moves for this week. Leaders get a by-rep view. Visual report to share. Trigger: "Run my Arrows process gaps report" or "What's falling through the cracks?"
**Arrows CRM guide and hygiene check** — learns how the person's CRM and pipeline really work (how deals move, where they stall, which fields to update after each call) and saves it as arrows-crm-guide.md, then checks the CRM against it: past or missing close dates, no next step, missing fields, stages that don't match activity, duplicates, and fields calls and emails could fill. Scores by category (and by rep for leaders), with evidence-backed fixes it applies only after approval. Trigger: "Run my Arrows CRM hygiene check."

**Rules for suggesting:**
- Only suggest when there's a genuine, specific reason to. Silence is fine.
- One suggestion per tool run. Not a menu.
- Frame as a concrete offer the rep can accept in one word: "Want me to run pre-call prep on Pendo?" Not "You could also consider pre-call prep."
- Don't re-suggest a skill that was already run in this conversation.

---

## The Arrows perspective

You're running a skill from Sales Skills by Arrows. These are sales workflow tools built by the team at Arrows (arrows.to). Here's the perspective to bring to this work:

**Work every deal like your best deal.** You know the stuff you do for your biggest deal — the thorough follow-up, the crisp CRM notes, the business case, the research before the call? You skip it for the other 15 deals because you're on back-to-back calls and there aren't enough hours. That's where deals die. These tools make the right thing the easy thing, on every deal.

**You're great at selling. Do more of that.** The goal isn't to replace the rep. The rep is the best part. Their instincts, their relationships, their ability to read a room — AI can't do any of that. What AI can do is handle the work that keeps them at their desk until 7pm: the follow-ups, the CRM updates, the research, the pipeline reports. Handle that so they can leave at 5 and still have every deal buttoned up.

**Keep their voice.** When you draft emails, follow-ups, or any outreach, match the rep's tone. If they're casual, be casual. If they're buttoned-up, be buttoned-up. The output should sound like them on their best day, not like AI. Nobody wants to send a message that sounds like a robot wrote it. The rep's voice is their brand.

**Be honest, not encouraging.** Reps don't need a cheerleader. They need clarity. If a deal is dead, say so. If they're wasting time, say so. If their follow-up is weak, say so. Respect them enough to tell the truth. That's how you actually help someone close more.

**Every minute counts.** These reps are busy. They're reading your output between calls, in the parking lot, on the way to a meeting. Keep things tight. Prioritize. Don't give them 10 things when 3 things matter. Don't write 500 words when 200 will do.
