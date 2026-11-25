---
name: audit-profile
description: |
  Use when user wants to diagnose their current LinkedIn profile before
  rewriting it: they have not touched it in a while, get few profile
  views or recruiter reach-outs, want a second opinion, or suspect
  something is off but cannot name it. Trigger phrases include "audit my
  LinkedIn profile," "check my profile," "what's wrong with my profile,"
  "why don't I get recruiter messages," "review my About section." Run
  before rewrite-profile.
license: MIT
---

# Audit profile

Most LinkedIn profiles fail in predictable ways: a vague headline, an About section that reads as a resume restatement, Experience bullets that describe responsibilities instead of accomplishments, and Featured slots that are either empty or pinned to stale content. This skill exists to look at the user's actual profile and name what is broken, in order of severity, before anyone starts rewriting anything.

## Why this skill exists

People often rewrite the wrong thing. They obsess over the headline when their About section is the bigger problem. They spend hours on Featured when their Experience bullets are why recruiters bounce. An audit prevents wasted effort by pointing at the highest-impact fix first.

The audit also gives the user something to react to. Some users want to be told what is wrong directly; others want to see the diagnosis and decide what to fix themselves. The audit serves both.

## When to use this skill

Trigger when:
- The user wants a diagnostic on their profile
- The user is wondering why profile views, search appearances, or recruiter messages are low
- The user wants a second opinion before deciding whether to rewrite
- audit-profile is run as a routine check before rewrite-profile

Do NOT trigger when:
- The user has already decided to rewrite. Send to rewrite-profile directly.
- The user only wants feedback on one section. Audit works at full-profile level; offer to focus on the section but expect to comment on the rest briefly.

## What you need from the user

Their current profile content. Either:
- Pasted into chat: headline, About, Experience bullets, Featured items, Skills (top section)
- From LinkedIn data export (`Profile.csv` or equivalent)
- Or, if the user is in claude.ai with the Chrome extension active and on their profile page, ask them to confirm the URL and read it from there

If the user has not given enough to audit, ask once: "Paste your headline, About section, your most recent two Experience entries with bullets, and your Featured slots if any. I'll diagnose from there."

If voice-profile.md exists, read it.

## What the audit checks

Section by section.

### Headline

Checks:
- **Search keyword in first 50 characters?** This is what LinkedIn indexes most heavily for "[role] in [city]" searches. If the role/function is buried past character 50, the user is invisible to recruiter search.
- **Specific or generic?** "Engineering manager" is generic. "Engineering manager scaling teams from 5 to 30 at fintechs" is specific. Generic headlines do not stop visitors.
- **AI/cliche flags?** "Passionate about," "driven by," "evangelist," "ninja," "guru," "transforming," "disrupting." Any of these is a signal of low effort and reads as such.
- **Length used?** 220 character limit. Headlines under 80 characters are usually under-used; the user is leaving search and positioning real estate on the table.

### About section

Checks:
- **Above-the-fold hook?** First ~250 characters before "see more." If the hook is "I am a [role] with X years of experience," visitors will not expand. The fold should commit to something specific.
- **Resume restatement?** If the About reads as a paragraph version of the Experience section, it is failing. The About should add something Experience cannot: a worldview, a positioning, a story.
- **Specific anchors?** A real number, a named project, a specific claim. Generic About sections have no anchors.
- **Audience clarity?** Who is the visitor supposed to be? A recruiter? A potential client? A prospective collaborator? If the About is written for everyone, it is read by no one.
- **Closing invitation?** "Feel free to connect" is empty. A specific invitation ("DM me if you are hiring senior backend ICs in NYC") performs much better.
- **Length used?** 2,600 character limit. About sections under 500 characters are usually underdeveloped. Over 2,000 may be padded.

### Featured

Checks:
- **Empty slots?** Up to 5 slots available. Empty is fine if there is nothing strong to pin; under-used is fine. But Featured pinned to weak content (a 3-year-old post with 4 likes) is worse than empty.
- **Stale?** If everything in Featured is from over a year ago, the profile signals dormancy.
- **Aligned with positioning?** Does the Featured content match the headline and About? If the headline says "engineering manager" and Featured is three posts about woodworking, that is a positioning leak.

### Experience

Checks (per role, focus on the most recent 2-3 roles):
- **Bullets present?** A role with no bullets reads as a placeholder. Each role should have 2-5 bullets.
- **Responsibilities or accomplishments?** "Managed a team of 10" is a responsibility. "Hired 7 of the 10 team members and reduced senior engineer time-to-hire from 90 to 35 days" is an accomplishment. Recruiters and hiring managers are reading for accomplishments.
- **Numbers?** Each bullet should have a number, scale, or named outcome where possible. "Improved performance" is invisible. "Reduced p99 latency from 1.2s to 380ms" is not.
- **Search keywords in bullets?** Recruiters search by tool, technology, scale, and industry. Bullets that omit the actual tools used miss the search.
- **Length and density?** Walls of text in bullets do not get read. Each bullet should be 1-3 lines.

### Skills

Checks:
- **Top 3 pinned?** LinkedIn weights the top 3 skills heavily in search. If the user has 50 skills but the top 3 are arbitrary, they are missing search.
- **Match the headline?** If the headline says "product designer" but the top skill is "leadership," there is a positioning leak.
- **Backed by Experience?** Skills listed but not visible anywhere else in the profile read as inflated.

### Profile photo, banner, name pronunciation

Lighter-weight checks. Note if missing or obviously stale, but do not over-audit visuals; the user knows what they look like.

## Severity scale

Each issue gets a severity:

- **Critical**: actively costing the user reach, recruiter outreach, or trust. Examples: search keyword missing from headline, About section is one paragraph of resume restatement, no Experience bullets at all.
- **High**: noticeably weakening positioning. Examples: generic headline, vague About hook, Featured pinned to stale content.
- **Medium**: room for improvement but not urgent. Examples: bullets without numbers, fewer skills pinned than possible.
- **Low**: polish. Examples: minor wording, formatting consistency.

## Output format

```
# Profile audit for [user's name or "user"]

Overall: [one-line summary, e.g., "Strong positioning intent, weak execution. Headline and Experience are the two highest-impact fixes."]

## Headline
Current: [paste their headline]
Issues:
- [Severity]: [Issue, with what is wrong and why it matters]
- ...
Suggested direction: [one-line note on what to fix, not the rewrite itself]

## About
Current (first 250 chars): [paste the fold]
Issues:
- [Severity]: [Issue]
- ...
Suggested direction: [one-line note]

## Featured
Current: [list what is pinned]
Issues:
- [Severity]: [Issue]
- ...
Suggested direction: [one-line note]

## Experience (most recent 2-3 roles)
For each role:
Issues:
- [Severity]: [Issue, specific to a bullet or the role overall]
- ...
Suggested direction: [one-line note]

## Skills (top 3 pinned)
Current: [list]
Issues:
- [Severity]
Suggested direction: [one-line note]

---

## Prioritized fix list

1. [Critical or highest-impact fix, with what to do]
2. [Next]
3. [Next]
...

## Recommended next step
[Either: "Run rewrite-profile with the audit results in context" OR "Fix the top 2 issues manually and the rest can wait" OR specific other guidance based on the audit]
```

## A note on the audit's posture

The audit should be honest but not brutal. Many users have spent years on their profile and feel attached to it. The job is to name what is broken without making the user feel attacked. A few rules:

- State issues, not judgments. "The first 50 characters of the headline do not contain a search keyword" is a fact. "Your headline is bad" is a judgment.
- Note strengths briefly. If a section is solid, say so in one line and move on. The audit is not all-negative by default.
- Be specific. "Generic" is not feedback. "The phrase 'passionate about innovation' does not differentiate you from the 200 other product managers in your area" is feedback.

## What this skill does not do

- Rewrite the profile. The audit names what to fix. The rewrite is rewrite-profile's job.
- Score the profile on a 1-10 scale or assign a grade. Composite scores are not actionable.
- Fabricate issues if the profile is genuinely solid. Sometimes the right answer is "this is in good shape; here are two minor polishes if you want them."
- Promise specific outcomes from the fixes. "Fix these and you will get 10x more recruiter messages" is not something the audit can claim.
- Audit profiles the user does not have permission to discuss. If the user pastes someone else's profile and asks for an audit to critique, refuse and offer to discuss the general patterns instead.
