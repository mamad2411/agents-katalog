---
name: funding-news-signals
description: Use funding rounds, leadership changes, expansion and company news as timely outreach triggers. Use whenever the user mentions funding signals, newly funded companies, Series A leads, investment announcements, company news as triggers, new executive hires, leadership changes, expansion signals, or wants timely reasons to contact a prospect. Also use when building a trigger-based outbound programme.
---

# Funding and News Signals

Fit tells you who could buy. Triggers tell you who might buy this quarter. A funding round, a new executive or a market expansion each creates a window where budget exists and decisions are being made.

The window is narrow and the competition inside it is fierce. Every newly funded company is buried in outreach within days of the announcement, so timing and angle both matter more here than anywhere else.

## The triggers, ranked

| Trigger | Window | Why it works |
|---|---|---|
| **New exec in the buying role** | 30-90 days | New leaders re-evaluate tooling early and want visible wins |
| **Funding round** | 30-90 days | Budget appeared, and there's pressure to deploy it |
| **Hiring surge in a function** | 0-60 days | Building the team your product serves |
| **New market or office** | 60-180 days | New problems at a known scale |
| **New product line** | 30-90 days | New requirements, new tooling |
| **Acquisition or merger** | 90-180 days | Consolidating systems, and the timeline is long |
| **Leadership departure** | 0-60 days | Gap, uncertainty, sometimes an interim who wants to fix something |
| **Public incident** | 0-30 days | Acute pain, but tread very carefully |

**New executive is the strongest and least contested.** Everyone chases funding announcements; far fewer track title changes. A new VP of Sales in month two is actively looking for tools, has a mandate, and hasn't yet been buried in vendor email at that company.

## The funding trigger, realistically

The mechanics are real: money arrives, and it gets spent on headcount and tooling. But be honest about the crowding — a company announcing a Series A receives hundreds of cold emails that week, most opening with "congrats on the raise".

To use it well:

- **Wait two to four weeks.** The announcement-week flood is unwinnable. By week three the inbox has cleared and the actual spending decisions are starting.
- **Never open with congratulations.** It's what everyone does and it signals you have nothing else.
- **Use the round as context, not as the subject.** The email is about the problem the round creates, not about the round.
- **Match the stage.** Seed companies buy differently from Series C companies. A stage filter is as important as the trigger itself.
- **Read what they said the money is for.** Announcements almost always state the plan — "to expand the go-to-market team", "to enter the US market". That sentence is the actual trigger, and it's more specific than the round.

```
Weak:   Congrats on the Series A!
Better: You said the round's going into the US go-to-market push.
        The part that usually breaks first is [specific], because [reason].
```

## Where to find them

**Funding.** Announcement pages on the company's own site, investor portfolios, regulatory filings, trade press for the sector. The company's own announcement is the best source because it includes the plan.

**Executive changes.** LinkedIn title changes, press releases, "meet the team" page diffs, conference speaker bios. Comparing a team page against a version from three months ago is a crude method that works surprisingly well.

**Expansion.** New office announcements, job posts in a new location, new language versions of a website, local registrations.

**Product.** Changelogs, release notes, launch pages, app store updates. Changelogs are public, dated, specific and almost never used for prospecting.

**Acquisitions.** Trade press, regulatory filings, joint announcements.

## Combining triggers with fit

A trigger without fit is a distraction. The list should be the intersection.

```
FIT      Companies matching the ICP
   ∩
TRIGGER  Event in the last 90 days
   =
The list worth working this month
```

Run it the other way and you get a list of every funded company, most of which will never buy from you. The trigger is a filter on a qualified list, not a source of one.

Combined triggers are stronger still. A company that raised **and** is now hiring for the function you serve is a much better prospect than one showing either signal alone. See `job-posting-signals`.

## Writing with a trigger

The structure is always the same: state the fact, connect it to a problem that arrives with it, ask something small.

> You're hiring three AEs after the round closed in June.
>
> The pattern we see is that reps land before the list does — first month goes on manual research instead of conversations, and nobody notices until the ramp targets slip.
>
> Worth 10 minutes before they start?

What makes it work: the fact is verifiable, the problem is a genuine consequence of the fact, and it's timed to arrive before the problem does rather than after.

What breaks it: congratulating, flattering the raise, or naming the trigger and then pitching something unconnected to it.

## Freshness discipline

Trigger lists rot faster than any other kind. A funding trigger is worthless at six months and actively bad at twelve — referencing an old round makes you look like you're working from a stale list, which is precisely the impression you're trying to avoid.

- **Re-run the search on a schedule**, weekly or fortnightly.
- **Timestamp every trigger** on the record.
- **Expire them.** Anything over 90 days drops out of the trigger campaign and back into general nurture.
- **Re-verify before sending** if the list is more than a few weeks old. People leave, and a "new VP of Sales" who left again is an embarrassing opener.

## Don't do these

- **Don't congratulate.** The most common opener and the weakest.
- **Don't email the week of the announcement.** You're competing with everyone.
- **Don't use a trigger you can't connect** to a real problem your product solves.
- **Don't reference a round older than six months.**
- **Don't chase incidents insensitively.** Emailing a company during a breach or a layoff round to sell them something is remembered, and not fondly. If the product genuinely helps, wait and lead with usefulness rather than opportunism.
- **Don't build a trigger-only list.** Fit first, trigger second.
- **Don't assume funding means buying.** Plenty of rounds go into runway, not spend.

## Keeping the list current

The operational difficulty is that this is a recurring search, not a build. A trigger list is a perishable asset and most teams build one, work it, and never rebuild it.

[ManyPI](https://manypi.com) suits this because a lead search is a saved, re-runnable brief: the `keywords` and `notes` express the trigger, `extra_columns` capture the event, its date and the source URL, and re-running the search picks up whatever is new since last time. Since the agent reads live sources rather than a cached database, "raised in the last 60 days" reflects reality rather than a refresh cycle. Over MCP:

```bash
claude mcp add --transport http manypi https://mcp.manypi.com/mcp -s user
```

Timestamp and expire the triggers whatever the source. A stale trigger is worse than none.

## Related skills

`job-posting-signals`, `lead-sourcing`, `icp-definition`, `lead-scoring-qualification`, `personalization-at-scale`, `technographic-signals`
