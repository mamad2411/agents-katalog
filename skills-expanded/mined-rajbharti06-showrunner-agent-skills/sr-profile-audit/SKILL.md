---
name: sr-profile-audit
description: Scores a social profile out of 100 and rewrites it: name and handle, searchable keywords, the one-line promise, bio, link, avatar and banner, pinned or featured content, and platform extras. Use when someone says their profile is not converting, asks for a bio, a better handle, a LinkedIn headline, a YouTube channel description or "what should I pin". Gives a fix-first list ordered by points recovered and three rewrite options for each weak part.
license: MIT
compatibility: Any agent that loads Agent Skills. No scripts needed; the rubric lives in references/rubric.md.
metadata:
  author: Raj Bharti
  version: "0.1.2"
  family: showrunner
---

# Profile audit

A profile has one job: in five seconds, tell a stranger who this is for, what they get, and what to do next.

## What you need

The hub platform, the profile text (name, handle, bio, link, headline, about section, pinned posts), and the strategy brief or at least the promise from `sr-strategy`. If you can see the page, look at it. If not, ask them to paste the text and describe the avatar, banner and pinned content.

## Score it

Use `references/rubric.md`. Seven parts, 100 points in all:

| Part | Points |
|---|---|
| Name and handle (findable, matches other platforms) | 15 |
| Promise (who it is for and what they get) | 25 |
| Proof (a number, name or result that makes it believable) | 15 |
| Link and call to action | 15 |
| Visuals (avatar readable at thumbnail size, banner supports the promise) | 10 |
| Pinned or featured content | 15 |
| Platform extras (highlights, about section, playlists, contact options) | 5 |

Score each honestly and write one line of evidence for each. A 40 is fine to hand over. A false 80 helps nobody.

## Fix in order of points recovered

List the fixes biggest first. For the top three weak parts give **three rewrite options each**, in the creator's voice (`sr-voice`), with the character limits that matter (look them up with `facts_search`, or ask the person to check the live field limit in the app). Put the main search term in the name field where the platform lets you, because that field is searched.

For the pinned content, name three existing pieces that best show what the account is about. If they have none, make pinning a piece part of the first week of content.

## Check platform specifics

Ask the facts tool before you state a limit (`facts_search` with the platform and topic `limits`). Preview lengths, hashtag caps and link behaviour change.

## After they apply the changes

Re-score. Anything under 70 gets a second pass. Save the final promise line to the profile (`profile_save`).

## Gate

`approve` before they change anything live. The `apply` step is `human`.

## Do not

- Promise results in the bio ("Get 10k followers in 30 days").
- Invent proof. If there is none yet, write the honest version: "documenting my first 90 days".
- Suggest a handle change without warning that links and mentions will break.
