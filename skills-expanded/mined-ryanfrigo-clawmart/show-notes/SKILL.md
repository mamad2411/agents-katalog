---
name: show-notes
description: Generate SEO-titled show notes with valid chapters, key takeaways, resource links, and a guest bio from a clean transcript.
metadata: { "openclaw": { "emoji": "📝" } }
---

# Show Notes

Turns a clean transcript into a complete, publish-ready show-notes block: title options, a description, YouTube-valid chapters, key takeaways, every resource mentioned, and pull quotes. This is the connective tissue of an episode — it feeds the video description, the podcast host, and the SEO page.

## When to use (trigger phrases)

Use this skill when the user says:

- "write show notes for this episode"
- "make chapters / timestamps for the video"
- "pull the links and takeaways from this"
- "I need a title and description for the upload"
- "episode page copy"

## How it works

Read the canonical `transcript.clean.md` (run `transcript-clean` first if the input is raw). Then produce, in order:

1. **Title options (5).** Mix two styles: *clear/SEO* ("How Retention Really Works — Dr. Chen on Consumer App Churn") and *curiosity* ("The 90-Day Death Zone Every App Falls Into"). Keep them ≤ ~65 characters so they don't truncate in search and on YouTube. Never invent credentials or claims to make a title punchier.
2. **One-line hook + description.** A 1-sentence hook, then a 2–4 sentence description written for a human skimming, not a keyword stuffer. Work the primary topic phrase in naturally once.
3. **Guest bio.** 2–3 sentences. Pull only what's stated in the episode or provided by the user — title, company, notable work. If you don't know it, ask; do not fabricate.
4. **Chapters (YouTube-valid).** Extract natural section breaks from the timestamps. Rules that actually matter: the **first chapter must start at `00:00`**, you need **at least 3 chapters**, each must be **≥ 10 seconds** long, and they must be in ascending order. Label each in ≤ ~40 chars, benefit-forward ("Why the first session decides retention"), not vague ("Part 2").
5. **Key takeaways (5–8 bullets).** The actual insights a listener would screenshot — specific claims and frameworks, not "they discussed marketing." Each bullet is one idea.
6. **Resources mentioned.** Scan the transcript for every named book, tool, company, person, study, and URL. List them with a short "why it came up." If a link wasn't spoken in full, mark it `[find link]` rather than guessing a URL. If a web-fetch skill is available, resolve and verify the real URLs.
7. **Pull quotes (2–3).** The most quotable verbatim lines with their timestamps — reused later by `social-repurpose`.
8. **Optional placeholders.** Leave `> Sponsor read: [advertiser]` and `> Guest links: [handles]` slots if the user runs ads or wants guest socials.

## Output

```markdown
## The 90-Day Death Zone — Dr. Chen on Consumer Retention

**Hook:** Most consumer apps don't have a product problem — they have a first-session problem.

In this episode, Dr. Chen breaks down why retention is really a distribution
problem, the "90-day death zone," and the three things surviving apps do in the
first session. For founders and PMs shipping consumer products.

**Guest:** Dr. Chen leads growth research at [Company] and previously ran
retention at [App]. Her work focuses on early-lifecycle churn.

### Chapters
- 00:00 – Why 90 days is the real cliff
- 02:14 – Retention is a distribution problem
- 09:40 – The first-session test
- 21:05 – Three fixes that actually move D30
- 44:30 – What Dr. Chen would build today

### Key takeaways
- Retention is decided in session one, not by feature depth.
- "D30 is a lagging indicator of your onboarding, not your roadmap."
- Cohort by acquisition channel before you conclude the product is the problem.
- The 3 fixes: shorten time-to-value, remove the empty state, earn the notification.

### Resources mentioned
- *The Cold Start Problem*, Andrew Chen — the distribution framing [find link]
- Amplitude — how they cohort D1/D7/D30 [find link]

### Pull quotes
- [09:52] "D30 is a lagging indicator of your onboarding, not your roadmap."
- [22:40] "You don't have a churn problem, you have an empty-state problem."
```

## Notes

- **Chapter validity is not optional.** YouTube silently refuses to render chapters if the first one isn't `00:00`, there are fewer than 3, or any is under 10s. Enforce these before returning.
- **Never invent links, credentials, sponsors, or numbers.** `[find link]` and asking the user is always correct over a plausible-looking fake.
- **Match the topic, not keyword density.** One natural use of the main phrase beats five awkward ones; Google and readers both punish stuffing.
- If the user's podcast host (Transistor, Buzzsprout, Simplecast, etc.) has a character or format limit for descriptions, ask and trim to it — some cap the description hard.
- Timestamps are only as good as the transcript. If `transcript-clean` flagged estimated timing, tell the user to spot-check chapters against the video.
