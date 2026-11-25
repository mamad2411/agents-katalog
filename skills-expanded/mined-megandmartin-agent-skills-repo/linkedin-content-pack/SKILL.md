---
name: linkedin-content-pack
description: Turns a topic or research brief into a complete LinkedIn pack — hook-first post, visual direction, hashtags, first comment, and best posting window — delivered as drafts, never posted. Use when the user asks to "write a LinkedIn post", "LinkedIn content about", "post about [topic]", "turn this brief into a post", or needs LinkedIn-ready content. Don't use for X/Twitter threads (x-thread-builder), multi-platform spreads (content-repurposer), or scoring drafts (brand-voice-guardian).
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Content & Marketing, LinkedIn, Social, Drafting]
    related_skills: [deep-research-brief, brand-voice-guardian, content-repurposer]
---

# LinkedIn Content Pack

Produces everything needed to publish one strong LinkedIn post: the post itself (hook-first, substance-forward), a visual direction the user can execute, 3–5 targeted hashtags, a value-adding first comment, and a posting-window recommendation. Everything ships as a draft — this skill never posts on the user's behalf.

## When to Use

- The user has a topic, story, or research brief and wants LinkedIn content from it.
- A `deep-research-brief` output needs turning into a post.
- **Not for:** X/Twitter threads (`x-thread-builder`), multi-platform spreads from one source (`content-repurposer`), or scoring an existing draft against brand voice (`brand-voice-guardian`).

## Quick Reference

| Action | Command / Call |
|---|---|
| Check hook length | `python3 -c "print(len('''HOOK TEXT'''))"` — first line ≤ ~200 chars (pre-"see more" cutoff) |
| Check post length | Same one-liner on full text — target 900–1,800 chars, hard cap 3,000 |
| Hashtag count | Exactly 3–5, niche over broad |
| Anti-slop scan | Grep the draft for banned patterns (step 5) |
| Deliver | Draft in chat / file — never call any posting API |

## Procedure

1. **Precheck** — confirm you have: topic or source brief, the audience (who should stop scrolling), and the goal (authority, discussion, traffic). Ask for whichever is missing — a post without a defined audience is a coin flip.
2. **Angle** — extract ONE idea from the source. One post, one idea. Write the "so what" in a single sentence before drafting; if you can't, the angle isn't ready.
3. **Draft the post** —
   - **Hook (line 1):** a specific claim, number, or tension that earns the "see more" click. Under ~200 characters. No questions-as-bait, no "Unpopular opinion:", no "I'm humbled to announce".
   - **Body:** short paragraphs (1–2 lines each), white space between them. Deliver the substance IN the post — never tease content that lives elsewhere. One concrete example or number beats three abstractions.
   - **Close:** a genuine invitation tied to the content, or a clean CTA. Never "Agree?", "Thoughts?", or "Comment YES for the guide".
4. **Length check** — run the python3 counts from Quick Reference. Hook ≤200 chars; body 900–1,800 chars (long-form up to 3,000 only if every paragraph earns it). Trim from the middle, never the hook.
5. **Anti-slop scan** — the draft must contain none of: engagement-bait closers, "I'm humbled/thrilled to announce", hashtag walls (>5), emoji bullets on every line, "Let that sink in", broetry (every sentence its own line for 40 lines). If found, rewrite that section — don't just delete the phrase.
6. **Build the pack** — add: visual direction (what image/carousel/document to attach and why, or "text-only" with reason), 3–5 hashtags (2 niche + 1–2 topical; never broad tags like #business), a first comment that adds a resource, source link, or extra example (links go here, not in the post), and a posting window (audience's timezone; B2B default Tue–Thu 8–10am; state the assumption).
7. **Deliver** — output the full template below as a draft. If a brand voice file exists, recommend a `brand-voice-guardian` pass before publishing.

## Output Template

```
# LinkedIn Pack: [topic]
**Audience:** [who] | **Goal:** [authority/discussion/traffic]

## Post (draft — do not auto-publish)
[hook line]

[body]

[close]

## Visual direction
[format + what it shows + why, or "text-only because ..."]

## Hashtags
#[niche] #[niche] #[topical]

## First comment
[value-add + any link]

## Posting window
[day/time + timezone + assumption stated]
```

## Pitfalls

- **Hook buried at paragraph three** — the draft warms up before it lands. Recovery: find the single most surprising line anywhere in the draft, promote it to line 1, rebuild downward from it.
- **Link in the post body** — external links in-post tank reach. Recovery: move every link to the first comment; in the post, reference it ("link in comments" at most once, or just let the comment carry it).
- **Engagement-bait relapse** — the close drifts into "Agree? ♻️ Repost if...". Recovery: rerun step 5's scan; replace the close with a specific question only someone who read the post could answer.
- **Multi-idea sprawl** — three lessons crammed into one post, none landing. Recovery: keep the strongest idea, park the others as "next post" notes at the bottom of the pack.

## Verification

- [ ] Hook ≤200 chars and body within limits — python3 counts actually run, numbers reported
- [ ] Zero banned patterns from the step 5 list present
- [ ] Exactly 3–5 hashtags, none generic
- [ ] Links live in the first comment, not the post body
- [ ] Pack delivered as a draft; no posting action taken or offered as automatic
