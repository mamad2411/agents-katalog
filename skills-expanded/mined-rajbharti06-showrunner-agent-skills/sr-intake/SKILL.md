---
name: sr-intake
description: Asks a creator what they want to make, who it is for, where it will go, what they want out of it, where they are now, how many hours a week they really have and whether they will be on camera, then recommends one hub platform, one or two spokes, what to skip for now, a weekly load that fits their hours, and a first seven days. Use at the very start, when someone says they want to start posting, grow a channel, pick a platform, or asks "where should I post" or "what should I make". Never recommends a platform before the questions are answered.
license: MIT
compatibility: Any agent that loads Agent Skills. Optional Python 3.9+ for the recommendation tool; the by-hand method below works without it.
metadata:
  author: Raj Bharti
  version: "0.1.2"
  family: showrunner
---

# Intake: ask first, then recommend

People who start with "which platform should I use?" usually have not decided what they are making, for whom, or how much time they have. Fix that first. The recommendation is only as good as the answers.

## The questions

Ask at most two in a message, in the person's own words, then wait for the answer. Do not send a numbered list of all seven: that is a form. If they answer several at once, skip what they already told you. Accept "not sure" and help them decide.

1. **What do you want to make?** Short vertical video, long video, carousels or slides, written posts, or a mix. If they say "everything", ask which one they would still enjoy in six months.
2. **Who is it for?** One sentence about a real person: their situation, region, what they are trying to do. "Everyone" is not an answer. Push gently for a specific person.
3. **What do you want out of it?** Audience or personal brand, leads and customers, credibility and career, creator income, or community.
4. **Where do you already post, or want to?** Note it, and say you will tell them if it is too many.
5. **Where are you now?** Just starting, under 1,000 followers, 1,000 to 10,000, or over 10,000.
6. **How many hours a week can you honestly give this?** Filming, editing and replying included. Say that the plan will be sized to this number, so a generous guess hurts them.
7. **Are you willing to be on camera?** Faceless formats exist and plan differently.

If you are connected to the tools, `intake_questions` returns this list in a structured form.

## Listen for these

- **Hours and ambition do not match.** Two hours a week and five platforms. Say so kindly, and show the arithmetic.
- **Goal and platform do not match.** Wants B2B leads, wants to start on TikTok. Not wrong, but ask why.
- **No clear audience.** Help them pick one real person they have helped or could help.
- **A platform that may not be available or allowed where they live.** Check before building on it.
- **"I want to go viral."** Reach is not the goal for most people. Ask what a good result would look like in 90 days, in numbers they could verify.

## Recommend

Call `intake_recommend` with the answers (CLI: `python scripts/sr.py intake --content-types short_video --audience "..." --goal leads --stage zero --hours-per-week 5 --platforms instagram,youtube --no-on-camera`). Always pass the camera answer: `--on-camera` or `--no-on-camera`. Left out, it counts as unknown and the faceless advice is skipped. Run `scripts/sr.py` by its full path inside this skill's folder, without changing directory. It returns:

- a fit ranking of seven platforms with the reasons
- one **hub** (where you make things first), up to two **spokes** (where you adapt them), and **skip for now**
- a weekly load in minutes against their creation budget, with 15% held back for replies
- the first seven days, each tied to a skill

Present it as a short story, not a data dump: "Start with X because..., adapt the best pieces to Y, leave Z for later. That is about N hours of making and M hours of replying a week."

Always say: this is a starting hypothesis from editable priors in `data/fit.json`, not a prediction. After six to eight posts their own numbers replace it.

## By hand (no tools)

Pick the hub where three things overlap: where their audience already spends time, where their preferred format is native, and where their goal gets served (B2B leads: LinkedIn first; deep teaching and search: YouTube; fast reach for short video: TikTok or Instagram Reels; community and local: Facebook; ideas and builders: X). Choose spokes that reuse the hub piece cheaply. Count minutes: a short video takes about an hour to make and 20 minutes to adapt, a carousel about an hour, a text post about 15 minutes, a long video about six hours. Fit that into 85% of their hours.

## Gate

`approve`. Show the recommendation and ask: "Does this match how you see it? What would you change?" Then offer to save the profile and to start the `zero-to-first-1000` playbook. `profile_save` takes the same flags as `intake` (CLI: `python scripts/sr.py profile save --content-types short_video --goal leads --stage zero --hours-per-week 5 --hub instagram --no-on-camera`).

## Do not

- Recommend before you have the answers.
- Claim a platform will "work" for them. Say what it fits and why.
- Save anything about them without asking.
