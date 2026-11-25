---
name: devrel-live-streaming
description: "Plans a developer-tools company's own live streaming program across Twitch, YouTube Live, LinkedIn Live and X: whether to host a show, the home platform and simulcast rule, live coding formats, a season cadence, chat moderation staffing, on-screen secret safety, raids, clips, and metrics beyond peak viewers. Use whenever someone wants to start, grow or fix a devrel stream, Twitch channel, YouTube Live show or LinkedIn Live event, asks about multistreaming or raids or why nobody shows up - even if they only say 'we should stream'. Not the on-demand channel - use samber/developer-relations-skills@devrel-youtube-channel; not webinars - use samber/developer-relations-skills@devrel-webinar-program; not office hours or AMAs - use samber/developer-relations-skills@developer-office-hours-program."
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# DevRel Live Streaming

You plan a developer-tools company's live show as a recurring program. The deliverable is a stream plan in the Output order below.

Live earns its cost only through what the audience changes while you are on air: questions answered, bugs found, code steered. A show that would run the same with chat switched off is a video; record it instead.

Stay in scope:

- The on-demand library, Shorts and channel ownership on YouTube: samber/developer-relations-skills@devrel-youtube-channel.
- Registration-gated webinar series with a sales handoff: samber/developer-relations-skills@devrel-webinar-program.
- A support Q&A rotation (office hours, ask-the-engineers): samber/developer-relations-skills@developer-office-hours-program.
- One demo's runbook, fallback and reset: samber/developer-relations-skills@developer-live-demo-design.
- One recorded video's script: samber/developer-relations-skills@technical-video-script.
- The community-wide code of conduct and enforcement ladder: samber/developer-relations-skills@developer-community-moderation.
- Streaming a conference's own talks: samber/dev-event-organizer-skills@virtual-event-production.

Label every platform claim **[platform]** when the platform's own help, legal or developer pages state it, **[law]** for a regulator's own rules, **[practitioner]** for streamers, agencies and blogs. Never present a practitioner figure as a rule. When you can browse, re-read the pages listed in [references/platform-facts.md](./references/platform-facts.md) before advising: live rules change often.

## Refuse these moves

| Tempting move                                                            | Why it fails                                                                                                                                                                                                   | Instead                                                                                                                |
| ------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Multistream every show to every platform with one merged chat            | One host cannot read four chats while coding, so questions go unanswered; Twitch's written rules also ban showing merged chat on the Twitch stream [platform]                                                  | One home platform; add a simulcast only with a moderator who triages its chat                                          |
| "Go live on LinkedIn whenever we're ready"                               | Every LinkedIn Live is a scheduled event; at start, event attendees are notified, not all followers [platform]                                                                                                 | Schedule the event at least two weeks ahead and invite connections [platform]                                          |
| Live-code on the engineer's daily machine and accounts                   | Keys leak through autofill, dashboards, terminal history, `.env` files; a leaked stream key lets anyone broadcast on the channel [practitioner]                                                                | The pre-flight safety checklist below, every episode                                                                   |
| Promise a daily stream from one advocate                                 | Burnout ends the show, and the slot viewers learned disappears with it                                                                                                                                         | A fixed weekly or fortnightly slot run in seasons                                                                      |
| Host alone, reading chat                                                 | Nobody acts on spam, raids or a vulnerability posted in chat; LinkedIn advises at least one dedicated moderator [platform]                                                                                     | One named moderator per chat on screen                                                                                 |
| Report peak viewers, followers or public views                           | Peak is one minute; YouTube counts a view from the first frame of play [platform]                                                                                                                              | The metric tiers below                                                                                                 |
| Trust the platform to keep the recording                                 | Twitch past broadcasts are off by default and expire after 7, 14 or 60 days [practitioner quoting Twitch help]; YouTube may not archive streams over 12 hours [platform]                                       | Record locally every time; export inside the window                                                                    |
| An employee streams the product on a personal channel with no disclosure | The US FTC Endorsement Guides treat employment as a material connection to disclose [law]; Twitch exempts only "your own products" from its branded-content tick, and an employee's case is unclear [platform] | Say the employer on screen, in the title and aloud; tick the branded-content box too, it costs no discovery [platform] |
| Stream a pre-recorded talk as "live" or sell from a LinkedIn Live        | LinkedIn's guidelines discourage both [platform]                                                                                                                                                               | A YouTube Premiere for recordings; teach, don't pitch                                                                  |

## Interview

Ask one question per message, multiple-choice when possible. Skip what the request already answers; if the user wants one pass, state an assumption per gap.

**Memory: Store a few info about the current task or project context. When memory lives in a file, use `devrel-context.md`; if a different memory system is in use, rely on that instead. Separate task info in different sections. Remove finished tasks. Add a date to a task; no date for general project context. Some interview responses may differ between 2 tasks.**

1. Goal: reach new developers, activate signups, retain users, launch moment, or recruiting?
2. Who should watch: role, stack, time zone, and where they already watch live (Twitch category, YouTube, LinkedIn)?
3. Existing accounts: which platforms, who owns each login, follower counts, Twitch status (none, Affiliate, Partner)?
4. Hosts: who can be on air, hours a week each, and who can moderate during the slot?
5. Date the result must land by, one-off moment or compounding show, and the effort ceiling (hours, budget for guests or paid streamers, sign-offs)?
6. Can the product be shown working live from a clean demo account?
7. Which developer streamers or community members already build with you or your category?
8. Can you count signups by source today: tagged links, a "how did you hear about us" field, both, neither?

## Workflow

1. **Check the request against Refusals** and name every move you will decline.
2. **Run the interview.** For an existing show, pull the last 6 episodes' average viewers, chatters and attributed signups before proposing anything.
3. **Pass the existence gate.** Rank Menu 1 for this user and recommend one rung. A show is a standing job; say so.
4. **Pick the home platform** and the simulcast rule.
5. **Brainstorm show concepts.** Propose 2-3, each a format from Menu 2 with a slot and a guest source, state the trade-off, recommend one, and wait for the pick. In a one-pass request, proceed with the recommendation and mark it as an assumption.
6. **Derive the season cadence from capacity.**
7. **Staff moderation and write the pre-flight checklist.**
8. **Write the engagement recipe** for the home platform, plus each simulcast target.
9. **Plan repurposing.**
10. **Set metrics,** baselines from episodes 1-3, the continue bar and the stop rule, before episode 1.
11. **Present** in the Output order, one section at a time, validated before the next; in a one-pass request, deliver all sections at once. When the plan declines most of the request, offer a staged route to what the user wanted (home platform first, a simulcast target once its moderator exists). If your harness has persistent memory, store the verdict, platform, slot, roster and continue bar.

## Output

Deliver in this order:

1. Refusals triggered.
2. Existing-show diagnosis, if a show exists.
3. Existence verdict, with Menu 1 ranked and what moved.
4. Home platform and simulcast rule.
5. Chosen concept and format.
6. Season cadence.
7. Moderation roster and pre-flight checklist.
8. Engagement recipe, with dated cadence.
9. Repurposing.
10. Metrics, continue bar and stop rule.
11. Open questions.

## Menu 1: whether to host

Efficiency (value per team hour, starting from zero): guest on established developer streams > guest-led show on one home platform > launch-day streams only > solo build-along on an advocate's channel > multistream variety show.

- value: guest-led show > solo build-along > guest on other streams > launch-day streams > multistream variety show
- effort: multistream variety show > solo build-along > guest-led show > launch-day streams > guest on other streams
- compliance cost: solo build-along (employee disclosure) == guest on other streams (disclosure if paid, their channel's rules), tied because each adds one disclosure duty > multistream variety show (each platform's simulcast rules) > guest-led show == launch-day streams with unpaid guests, tied because each carries only your own platform's rules

| Rung                                      | Payoff                                                 | Time to effect  | Effort | Value bought                                         |
| ----------------------------------------- | ------------------------------------------------------ | --------------- | ------ | ---------------------------------------------------- |
| Guest on established developer streams    | one-shot per stream, compounding as invitations repeat | weeks           | +      | A trusting live audience with no production          |
| Guest-led show on one home platform       | compounding                                            | a season or two | -      | Your own audience; each guest promotes their episode |
| Launch-day streams only                   | one-shot                                               | days            | +      | Questions answered while attention peaks             |
| Solo build-along on an advocate's channel | compounding, tied to one person                        | quarters        | --     | Peer credibility; channel leaves with the person     |
| Multistream variety show                  | slow                                                   | quarters        | ---    | Reach split across chats nobody fully serves         |

- **Default rung:** guest on 2-3 established streams while a guest-led show runs one season on one home platform. Prepare each guest appearance with samber/developer-relations-skills@tech-podcast-interview-prep.
- **Paying a streamer** for a session: put the disclosure and the branded-content or paid-promotion tick [platform] in the contract; brief 2-3 points and let the streamer write their own words; give them a tagged link.
- **The order starves** the solo build-along, the deepest community bond and the costliest. Promote it when an advocate already streams and wants to, and the company account (not theirs) holds the show.
- **Delete** every hosting rung when nobody can moderate during the slot or capacity is below one episode a fortnight: guest on others' streams and hand recorded video to samber/developer-relations-skills@devrel-youtube-channel.
- **Re-rank** on the interview: a launch date promotes launch-day streams; a buyer or executive audience moves LinkedIn Live up and the solo build-along down. Say which answer moved which rung.

## Home platform and simulcast

| Home                   | Pick when                                                                           | Watch out                                                                                                                              |
| ---------------------- | ----------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| YouTube Live           | You want the archive found by search later; default for most devtools companies     | Streams over 12 h may not archive [platform]; vertical copy goes to the Shorts feed without clickable links [platform]                 |
| Twitch                 | The audience lives in developer live culture and chat-first community; raids matter | Live channels usually get priority over offline ones [platform]; archive expires; Affiliate status sits with whoever owns the login    |
| LinkedIn Live          | Buyers, architects, enterprise practitioners; panels and customer sessions          | 150+ followers, 30-day-old account; scheduled events only; 4 h max; no promotional streams; links in comments not clickable [platform] |
| X (live video, Spaces) | Launch-day reaction, news AMAs                                                      | Encoder streaming needs Premium; Spaces are audio, poor for code [practitioner]                                                        |

- Simulcast only when each extra chat has its own moderator who relays questions to the host. A merged-chat overlay without Twitch is allowed, but still needs a moderator triaging it.
- A multistream service holds every destination's credentials: own it on a company login with 2FA. LinkedIn accepts its listed partner tools or any encoder through a custom RTMP stream [platform].
- With Twitch in the mix [platform, Simulcasting Guidelines]: no merged chat on the Twitch stream (Twitch's CEO said in 2026 enforcement would pause [practitioner]; follow the written rule); the Twitch experience no worse than elsewhere, chat engagement included; nothing sending Twitch viewers to another streaming platform, so moderators never paste the YouTube link in Twitch chat.
- A LinkedIn Live streams into one destination, never two: a member streams as their profile, a Page admin as the Page [platform]. Pick the Page for a company show and reshare from profiles; a member's profile may reach more people but ties the show to one person [practitioner].
- Own every account through a company login with 2FA and named editor or moderator roles; a host's personal account carries the show away when they leave.

## Menu 2: formats

Every format names what chat changes. Efficiency: pair programming with a guest > release-day stream > viewer code or architecture review > solo live build > AMA > news or panel show.

| Format                                                      | What chat changes                            | Payoff                                       | Effort |
| ----------------------------------------------------------- | -------------------------------------------- | -------------------------------------------- | ------ |
| Pair programming with a community or customer guest         | Steers the build, spots bugs                 | compounding; the guest brings their audience | -      |
| Release-day stream: build with the new feature              | Asks what the docs missed                    | one-shot spike                               | +      |
| Viewer code or architecture review (submitted with consent) | Supplies the material                        | compounding                                  | -      |
| Solo live build of a real sample app                        | Debugs alongside the host                    | compounding while the series runs            | --     |
| AMA with engineers                                          | Is the content; collect questions 24 h ahead | one-shot                                     | +      |
| News or panel show                                          | Little                                       | slow                                         | +      |

- Plan each episode as a goal plus a fallback task; viewers come to watch problem-solving, getting stuck included [practitioner]. Demo-breaking risk goes to samber/developer-relations-skills@developer-live-demo-design.
- Never review a viewer's private repository on air without written consent, and never show their secrets.

## Season cadence

- Pick one slot: same weekday and hour, inside working hours of the time zone where most signups or docs visitors sit, published on the platform's schedule (Twitch schedule, YouTube scheduled stream, LinkedIn event).
- Run seasons of 6-8 episodes with a break of a few weeks between, used to book guests and read metrics.
- Host hours per episode, order of magnitude: the stream length, plus the same again for prep, plus a few hours for clips and the recap. Moderation is another person's stream length.
- Episodes per month: `(host hours per week × 4) ÷ host hours per episode`, rounded down. Below two a month, take the guest rung instead.
- Fix one episode length the host can sustain, so viewers can plan; start around an hour and lengthen only while chat is still active at the end. LinkedIn advises at least 15 minutes and a starting screen under 1-2 minutes [platform]; its maximum is 4 hours [platform].

## Moderation and pre-flight safety

**Roster:** one named moderator per chat shown, never the host. Moderators get the rules, the escalation ladder from samber/developer-relations-skills@developer-community-moderation, and platform roles before episode 1.

**Preset before every episode** (each platform's names in [references/platform-facts.md](./references/platform-facts.md)): blocked terms, held-message filter, slow mode ready, follower- or subscriber-only mode ready, a one-click raid preset where the platform has one, link policy (only moderators post links).

**Live escalation:**

1. Spam or abuse: delete, time out, hide; the host never reads it aloud.
2. Raid flood or hate raid: moderator switches the preset on; host keeps going; review recent raiders afterwards.
3. Vulnerability posted in chat: delete, thank, move the reporter to the security disclosure channel; never reproduce it live; note the timestamp, cut it from the archive, and find and delete viewer clips of that window.
4. Product bug or angry customer: acknowledge, moderator files the issue with the link, host returns to the plan.

**Pre-flight checklist, every episode:**

- Demo account with scoped, low-limit keys; rotate them after the stream. Same for connection strings and tokens; no customer data in any dashboard on screen; shell history cleared.
- Separate OS user or browser profile: no saved passwords, no personal tabs, notifications off.
- A privacy scene ready to cut to before any credential screen; the encoder's settings window never in a captured scene.
- Stream key in a password manager, never in the run-of-show document; prefer RTMPS.
- Local recording running; audio checked first; code font readable on a phone.
- Disclosure set: employer named for staff on personal channels (FTC in the US [law], or your market's advertising rules); branded-content or paid-promotion box ticked when someone is paid or staff stream the employer's product [platform].
- No copyrighted music or rebroadcast feeds: they get archives muted, claimed or the stream restricted [platform].
- Guests: a test call before the day, written consent to record and reuse their face, voice and code in clips, and a fallback segment if they do not show.
- Failure plan: a holding scene, a backup encoder or connection, and a line the moderator posts; a LinkedIn Live must start between 15 minutes before and 2 hours after its scheduled time [platform].

**Exposure already happened** (a key, token or customer record shown on a past stream): revoke and rotate it now, audit past archives, Highlights and viewer clips, and hand it to the security team as an incident, not a stream fix.

## Engagement recipe

**Surfaces** (C = compounding, O = one-shot): the scheduled stream page or event (O); the platform schedule (C); the archive with chapters (C); clips (O, compounding when collected); raids sent at the end (O); guest episodes on others' channels (O); the post-show recap post (O); a community space where regulars wait between episodes (C).

**What ranking rewards and punishes:**

- Twitch [platform]: live channels are more often given priority over offline ones; Browse sorts by category or tag, by viewers or recommendation; a channel page lists "channels also watched by viewers". Do more: a correct category and tags, co-viewing through raids and guest swaps, clips for the mobile clips feed. Do less: off-schedule streams nobody expects.
- YouTube [platform]: publish time matters for Live and Premieres; subscribers get one go-live notification; A/B title and thumbnail tests work on live archives. Do more: scheduled streams announced days ahead, a title that names the problem solved.
- LinkedIn [platform]: attendees get reminders 3 days and 15 minutes before and a notification at start; a subset of followers likely to watch also gets one. Do more: two weeks of event promotion and connection invites. Do less: promotional content, long starting screens.
- Practitioner only: "Twitch boosts streams with active chat", "stream 3+ hours to rank". Mention as folklore or not at all.

**Cadence:**

1. **Weeks -4 to -1:** company accounts, 2FA, roles; LinkedIn eligibility check (150+ followers, 30-day account) and X Premium if needed; moderation presets; schedule the first three episodes; invite the first three guests.
2. **Week -2:** announce the season with dates; LinkedIn events open; ask for questions.
3. **Each show week:** reminder on the day; stream; on Twitch, raid an aligned channel at the end (elsewhere, name a partner's next stream); recap and clips within 48 hours.
4. **Weekly, off-air:** watch and chat on 2-3 aligned developer streams; never post your links there.
5. **End of season:** read metrics against the continue bar; book the next guests or stop.

**Limits:** see [references/platform-facts.md](./references/platform-facts.md) for each platform's enforced rules and policed norms, marked enforced or policed.

**Templates:** read [references/templates.md](./references/templates.md) for the season announcement, LinkedIn event text, pinned chat rules, moderator brief, guest invitation, raid message, disclosure line and recap. Fill them with the user's facts; never invent a feature or number.

## Repurposing

- Drop a stream marker or note the timestamp at every answer worth keeping.
- Within 48 hours: export the archive before it expires, add chapters, cut 2-4 clips, link docs pages fixed after viewer questions. Raw live coding edits poorly into tutorials [practitioner]: cut answers, not hours.
- Hand the archive and clips to the on-demand plan in samber/developer-relations-skills@devrel-youtube-channel; it owns titles, Shorts and playlists.

## Metrics and stop rule

- **Outcome:** signups from tagged links in descriptions, pinned messages and recaps; "how did you hear" answers naming the show; docs or product fixes traced to viewer questions.
- **Show health:** average concurrent viewers (not peak); unique chatters ÷ average viewers; returning viewers across episodes; archive watch time and average view duration (not public views: since 24 August 2026 YouTube counts a view the moment any video starts to play [platform], so never compare public views across that date).
- **Diagnostic:** attendee-to-viewer rate on LinkedIn; minutes to first chat message; clips views.
- No published benchmark exists for developer streams; set targets from episodes 1-3.
- **Continue bar,** written before episode 1 in this form: `episodes 6-8 vs 1-3: average viewers [up/flat], chat rate [up/flat]; at least [n] attributed signups or [n] docs fixes over the season`. Choose `n` from the goal and current signup volume; never set or move it after seeing results. For an existing show, write the bar now against the last 3 episodes and judge only the next season.
- **Stop rule:** at season end, below the bar, drop to the guest rung and say so.

A plan passes when the home platform, slot, moderator and continue bar each have a named owner (in a one-pass run, `owner: to confirm` plus an open question) and every [practitioner] figure carries its label.

## References

- samber/developer-relations-skills@devrel-metrics - the DevRel scorecard these metrics feed.
- samber/developer-relations-skills@devrel-analytics - tagged links, signup-source fields, dashboards.
- samber/developer-relations-skills@devrel-content-calendar - the season on the quarter's calendar.
- samber/developer-relations-skills@build-in-public - streaming your own product's build as a founder.
