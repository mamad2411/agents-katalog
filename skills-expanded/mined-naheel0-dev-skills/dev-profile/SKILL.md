---
name: dev-profile
description: >-
  Score a dev.to profile out of 100 against a 13-part rubric and rewrite the
  parts that lose points - bio, avatar, currently-hacking-on, available-for,
  pronouns, website, social links, experience level, featured repos, tags
  followed, orgs, badges, SEO. Use when the user says "optimize my dev.to
  profile", "score my dev.to profile", "rewrite my bio", or pastes their
  profile and asks how it reads.
---

# dev-profile

A dev.to profile is not a resume. A resume answers "what have you done". A
profile answers "should I follow this person" in about four seconds, from the
name, bio, and first line.

## Input

Ask the user to paste: name/handle, bio, location, website, work line,
skills/languages, currently hacking on, available for, pronouns, social links
(GitHub/Twitter), featured GitHub repos, org memberships, tags followed count,
badges, and whether they have a pinned post. A screenshot of the profile card
is enough for the first pass. Do not log into dev.to on their behalf.

## Score it

Read `rubric.json` in this folder. Thirteen items, 100 points, each with what
full marks looks like. Score every item, show the table, and give the total.
Be honest - most profiles land in the 30s and 50s on the first pass.

Each rubric item carries a `weight` (starts at 1.0) in `rubric.json`.
After auditing ≥10 profiles, run `dev-learn.py audit --apply` to review
which items users actually fix vs skip. Re-weight manually based on that
data — the script flags items but does not auto-reweight (follower-growth
correlation requires more data than log.md currently captures).

```
PROFILE SCORE  47/100

  bio                  6/12   generic, no stack, no contact
  avatar               4/6    default or low-res
  currently hacking on 0/8   empty
  available for        0/8   empty - biggest missed signal
  pronouns             2/4   missing
  website              3/4   present
  social links         4/6   GitHub only, no Twitter
  experience level     2/4   not set
  featured repos       2/8   1 repo, no description
  tags followed        3/6   5 tags - too few
  orgs                 2/4   0 orgs
  badges               4/8   no Top 7
  pinned post          2/6   none pinned
```

## Then rewrite, in this order

Fix in descending order of points lost. Do not rewrite everything at once -
the user has to paste each section into `/settings/profile` themselves.

**1. Bio (max 200 chars).** The formula that works:
`{what you do} + {stack} + {how to reach you}`. Not your job title. No
"passionate about", no "results-driven", no third-person bio. Under 200
chars because dev.to caps the bio field.

**2. Avatar.** Upload a clear, well-lit headshot; platform crops to square.
No official pixel spec, but UI renders 90×90 in feed cards and 50×50 in
comments — upload at least 400×400 for crispness. Formats: jpg, jpeg, gif,
png, ico, bmp, webp. Max 8MB. No in-app crop UI.

**3. Available for.** Explicitly list services + engagement types (freelance,
agency collabs, long-term partnerships). This is dev.to's native "hire me"
signal — be specific. Max 100/200 chars (dynamic profile field).

**4. Currently hacking on.** Concrete, current work (e.g. "Rebuilding my
site, expanding SEO for X, exploring AI/ML workflows"). Signals activity and
invites collaboration. Max 100/200 chars.

**5. Pronouns.** Optional but encouraged for inclusivity; displayed
prominently. Max 100 chars.

**6. Location + website.** Location max 100 chars. Website max 100 chars —
personal site preferred over LinkedIn as primary link.

**7. Social links.** OAuth-based only: GitHub, Twitter/X, Facebook. LinkedIn
and Mastodon can only go in the bio. Connected via account settings.

**8. Experience level.** Set in `/settings/customization`. Cookie-persisted.

**9. Featured GitHub repos.** Connect via `/settings/extensions` (GitHub
OAuth). Pin 3–5 of your best, well-documented repos. Shows name, description,
fork flag, language, stars count. No hard limit, but 3–5 is the sweet spot.

**10. Tags followed.** Follow 10–30 relevant tags; count is public and feeds
your feed + discoverability. No dedicated settings page; managed via tag
pages.

**11. Orgs.** Join 2–4 relevant orgs (free, unlimited members, invite-by-code,
multiple admins). Shown in profile sidebar with logos. Boosts credibility and
distribution.

**12. Badges.** Earned automatically (Top 7, year-club, tech stickers, tag
moderator, trusted member). Not editable. Top 7 is the standout credibility
marker.

**13. Pinned post.** Pin your highest-value post to the top of your profile.

## Output

Score table, then the rewrites as copy-ready blocks in fix-first order.
Re-score at the end and show the delta honestly - if the rewrite gets to 88
and not 98, say 88, and say what the remaining points need (usually
recommendations, posting history, org membership).

## SEO / discoverability

dev.to profiles are Google-indexable:
- Title: `Name - DEV Community`
- Meta description: user's bio (keyword-rich bio matters)
- Canonical: self URL
- `schema.org/Person` JSON-LD with `name`, `description`, `url`, `image`,
  `sameAs` (Twitter, GitHub, website)
- Open Graph / Twitter cards with summary_large_image

Tips: keyword-rich bio, photo, location, work, website, GitHub/Twitter links
(sameAs), skills/languages, GitHub repos, org memberships, publish quality
posts with relevant popular tags (4 slots), engage in comments, follow
relevant tags/users.

## Nothing is saved to dev.to by this skill

The user pastes each section into `/settings/profile` themselves.

## Skipped (ponytail)

- No profile self-update automation (Forem only exposes admin PATCH; edits go
  through web UI).
- No profile cover/banner image (dev.to doesn't have one for profiles; brand
  color only).
