---
name: publish-checklist
description: Run a per-episode pre-publish checklist across video, notes, clips, newsletter, and guest assets, then report what's DONE, MISSING, or NEEDS-REVIEW.
metadata: { "openclaw": { "emoji": "✅" } }
---

# Publish Checklist

The last skill before you hit publish. It walks a single episode's assets, checks each item against a real launch checklist, verifies what it can, and reports back — so nothing ships with broken chapters, a missing thumbnail, or a guest who was never sent their clips.

## When to use (trigger phrases)

Use this skill when the user says:

- "am I ready to publish this episode?"
- "run the pre-publish checklist"
- "what's still missing before this goes live?"
- "check the episode folder / launch readiness"
- "did I forget anything for episode 42?"

## How it works

1. **Locate the episode's assets.** Ask for the episode folder or the files (master video/audio, `transcript.clean.md`, show notes, clip cut sheet, newsletter draft, thumbnail). Note the target publish date/time.
2. **Run each item through three states:** `DONE` (verified present/valid), `MISSING` (not found), or `NEEDS-REVIEW` (present but should be eyeballed — e.g. estimated timestamps, an unresolved `[find link]`).
3. **Verify what you actually can:**
   - File exists and is non-empty (master file, transcript, thumbnail).
   - **Chapters are valid** — first at `00:00`, ≥ 3 chapters, each ≥ 10s, ascending (delegate the rule to `show-notes` logic).
   - **Links resolve** — if a web-fetch skill is available, check each resource/CTA link for a live 200; otherwise flag them `NEEDS-REVIEW` for a manual click.
   - **Captions/SRT present** if the platform needs an upload.
   - Clip cut sheet has in/out points for each planned clip.
4. **Walk the standard checklist** (customize per the user's workflow — see `openclaw.json.example`):
   - **Video/audio:** master file rendered · title set · thumbnail ready · description has chapters + resource links · tags set · captions/SRT uploaded
   - **Show notes:** published to the episode page / podcast host
   - **Clips:** cut · captioned · scheduled (with dates/platforms)
   - **Newsletter:** drafted · scheduled/queued · one primary CTA links to the right episode
   - **Guest:** sent their clips + go-live time + suggested caption to reshare
   - **Cross-post:** X thread, LinkedIn, and any community posts scheduled
   - **Tracking:** UTM/campaign tags on the CTAs if the user uses them
5. **Report a scannable summary,** grouped by state, MISSING first, with the smallest next action for each gap. Don't just list problems — say what to do.

## Output

```markdown
## Publish readiness — Ep. 42 "The 90-Day Death Zone" (target: Thu 9:00am)

MISSING (3)
- [ ] Thumbnail — no image found in the episode folder. → design or generate one.
- [ ] Captions/SRT — not uploaded. → export from transcript.clean.md and attach.
- [ ] Guest handoff — Dr. Chen not sent clips + go-live time. → draft the email.

NEEDS-REVIEW (2)
- [ ] Chapters valid, but 44:30 label may exceed 40 chars — trim.
- [ ] Resource link "Amplitude cohorting" still marked [find link]. → resolve.

DONE (7)
- [x] Master file rendered (episode-42-final.mp4, 58:12)
- [x] Title set · description has chapters + links
- [x] Show notes published to the episode page
- [x] 6 clips cut with in/out points · scheduled Mon–Sat
- [x] Newsletter drafted + queued, CTA → 21:05 deep link
- [x] X thread + LinkedIn scheduled
- [x] UTM tags present on episode CTA

Next up: thumbnail → captions → guest email. Everything else is green.
```

## Notes

- **This skill reports and drafts — it does not upload, schedule, or send.** Uploading to YouTube, scheduling clips, or emailing the guest each require a channel/tool you configure (a YouTube skill, a scheduler, an email skill). Absent those, it tells you exactly what's left to do by hand.
- **Customize the checklist to your actual workflow.** A YouTube-first creator, an audio-only podcaster, and a LinkedIn-only operator need different lists — edit the items (or the `openclaw.json.example` config) so the report matches how *you* ship.
- **`NEEDS-REVIEW` is a feature, not a nag.** Estimated timestamps and unresolved links are exactly the things that embarrass you post-publish; surfacing them is the point.
- Keep the guest handoff on the list. Sending the guest their clips + go-live time is the single highest-leverage distribution step most creators forget.
- Re-run it after you fix the gaps — a clean green report is the go signal.
