---
name: viral-outliers
description: >
  Instagram Reels research. Finds the viral reels in the user niche (keeps only those with
  700k+ views AND 5x their follower count), downloads each one, watches it frame by frame,
  transcribes the audio, and turns it into a fill-in-the-blank script template adapted to the
  user own brand, plus the caption.
  Use when the user asks to find viral reels or viral videos, research Instagram, study what is
  working in their niche, get content ideas, hooks, video scripts, captions, a content calendar,
  "what should I post", or asks for viral outliers.
  Tambien en espanol: "reels virales", "buscar outliers", "hazme un guion", "que posteo esta
  semana", "ideas de contenido". Method credited to Ava Yuergens (@personalbrandlaunch).
---

# Viral Outliers

> **Rule number one: never write a script without WATCHING and LISTENING to the outlier.**
> The caption is not the script. Reading the caption and writing from it is the most expensive
> mistake you can make. See §3.

This skill implements the outlier research method taught by **Ava Yuergens
([@personalbrandlaunch](https://www.instagram.com/personalbrandlaunch/))**. All strategy credit is
hers. This is only an automation of her process.

---

## 0. BEFORE ANYTHING — read the brand profile

Everything in `references/brand-profile.md` decides what "your version" of a script sounds like.
**If that file is still a template, stop and fill it in with the user first.** Without it you will
write generic copy that could belong to anybody.

You need at minimum:

- **What they sell and to whom** — the buyer's job title or situation, not a market segment
- **Their words for the problem** — how the *customer* describes it, not how the industry does
- **Their real numbers** — prices, timeframes, results, with proof they can show on screen
- **Their voice** — vocabulary, register, things they would never say
- **What they must never claim** — the technical words their audience does not know

---

## 1. THE FILTER — two steps, in this order

**Step 1 (the one people skip).** Ava, on her own workflow:
> *"Day 1-2: pull **100+ reels with MILLIONS OF VIEWS**, apply the 5X rule, log the metrics."*

**Step 2.** Ava's definition:
> *"Outliers are videos from **small to mid-sized creators** that hugely outperform their average
> content. To make it measurable I use the 5X rule: **5 times more views than followers**."*

```
FILTER 1: absolute views >= 700,000     (below this it never met a cold audience)
FILTER 2: views >= 5x followers         (without this it is just a big account)
BOTH. ALWAYS.
```

⚠️ **A reel with 3,800 views from a 700-follower account is 5X and is useless.** It never reached
anyone new.

**Accounts above 500K followers:** almost none clear 5X. Use **5x their own median** instead. For
templates, prefer accounts between **1,000 and 100,000 followers** — small enough that the video
did the work, big enough that it reached cold traffic.

**Cross niches freely.** Ava: *"if you see a hook in another niche that you like, you can turn it
into a template and adjust it to yours."* The mold travels; the value does not.

---

## 2. FINDING THEM

This skill uses **[agent-reach](https://github.com/Panniantong/Agent-Reach)** for anything that
touches the internet. Run `agent-reach doctor --json` first and state which channel and backend
you are using.

Instagram runs through **OpenCLI**, which reuses the user's logged-in Chrome session.

```bash
opencli doctor      # must say "Extension: connected"
opencli browser <session> open "https://www.instagram.com/"   # required before any eval
```

⚠️ **Chrome closes often.** Check the output of every command. Never assume one worked.

### Discovery: the explore feed

```
/api/v1/discover/web/explore_grid/?is_prefetch=false&omit_cover_media=true
  &module=explore_popular&use_sectional_payload=true
  &cluster_id=explore_all%3A0&include_fixed_destinations=false
```
Paginate with `next_max_id`. Walk the response tree collecting any node with `code` and
`play_count`.

> ⛔ **The hashtag endpoint is capped.** `/api/v1/tags/web_info/` returns 24 items and its "top"
> section is personalised — for `#productivity` the highest was 279,000 views. **It will not find
> you millions.** Do not build a sweep on it.

### Follower counts, for the ratio

```
/api/v1/users/web_profile_info/?username=X   ->  data.user.edge_followed_by.count
```
Fails on some business accounts. Fallback:
```
/api/v1/web/search/topsearch/?context=blended&query=X   ->  users[].user.pk
/api/v1/users/<pk>/info/                                ->  user.follower_count
```

All calls need `x-ig-app-id: 936619743392459`, `credentials: "include"`, and **relative URLs**
while the tab is on instagram.com.

### ⛔ READ-ONLY. Always.

`profile`, `user`, `explore`, `search`, `download`, `followers`, `following` and GET requests only.
**Never** `follow`, `like`, `comment`, `post`, `save` or anything marked `[write]`. Those act on
the user's real account.

---

## 3. ⭐ WATCHING — the step you never skip

### ⛔ Screenshots do not work

`opencli browser screenshot` on a reel page **returns a black video**. Instagram serves it over
MSE and with the tab backgrounded the `<video>` element stays at `readyState 0`. Forcing
`play()/pause()` works only when the tab is in the foreground, so it is neither reliable nor
parallelisable.

### ✅ Download the MP4 and pull frames with ffmpeg

```bash
# shortcode -> pk : base64 over the alphabet A-Za-z0-9-_
#                   pk = sum(alphabet.indexOf(c) * 64^(len-1-i))
# /api/v1/media/<pk>/info/  ->  items[0].video_versions[0].url
#   also returns: play_count, like_count, comment_count, media_repost_count,
#                 video_duration, user.username, caption.text

curl -sL -A "<Chrome UA>" "<mp4 url>" -o reel.mp4
ffmpeg -nostdin -loglevel error -ss <t> -i reel.mp4 -frames:v 1 -vf scale=360:-2 f.jpg -y

# contact sheet, 3x2, so it can be read in one look
ffmpeg -i _t0.jpg -i _t1.jpg -i _t2.jpg -i _t3.jpg -i _t4.jpg -i _t5.jpg \
  -filter_complex "[0][1][2]hstack=3[a];[3][4][5]hstack=3[b];[a][b]vstack=2" \
  -q:v 3 SHEET.jpg -y
```

`scripts/getreel.sh` in this repo does all of it.

> **`media_repost_count` = shares.** It did not exist before 2025, so old reels report 3, 11, 17
> — not because nobody shared them, but because the counter was not there. Only compare within
> the same year.

**How many frames:** six minimum, spread across the whole video. Ten to twelve if it has fast cuts
or changing text. **One frame lies.**

### ⛔⛔ TRANSCRIBE THE AUDIO — without this you have not watched it

Frames are not enough. A reel can have a long, beautiful caption and be a guy silently moving his
fingers. **If you did not transcribe it, you did not watch it.**

```python
from faster_whisper import WhisperModel
m = WhisperModel("small", device="cpu", compute_type="int8")
segs, info = m.transcribe(
    "reel.wav",
    vad_filter=False,
    condition_on_previous_text=False,
    no_speech_threshold=1.0,           # never drop a segment as "no speech"
    log_prob_threshold=None,           # never drop on low confidence
    compression_ratio_threshold=None,  # never drop on repetition
    temperature=[0.0, 0.2, 0.4],
    beam_size=5,
)
for s in segs:
    print(f"[{s.start:6.1f}s] {s.text.strip()}")
```

### ⛔ Those parameters are not optional

With the defaults (`no_speech_threshold=0.6`, `log_prob_threshold=-1.0`) **Whisper silently drops
the opening seconds** when there is music over the speech or the speaker is fast. The transcript
starts at second 9 and looks complete.

**That is exactly where the hook lives.**

Real cases from this method's own logs:

| Started at | The hook that was missing |
|---|---|
| 11.6 s | *"China just crushed Claude's $800 billion business model."* |
| 9.1 s | The comparison was **four** images, not two, with a time jump in the middle |
| 5.9 s | *"Someone just built the most powerful Claude tool on the planet."* |
| 4.3 s | The dialogue opened on the *other* character, not the one who explains |

> **MANDATORY CHECK: the first line must read `[ 0.0s]`.**
> If it starts at 3, 5 or 11 seconds, **the transcript is truncated**. It does not mean the video
> opens without speech — it means the model ate it. Run it again.
> If there really is no speech at the start, confirm it **by looking at the frames**, never by
> assuming.

### The three sources are different. You need all three.

| Source | What it is | The mistake |
|---|---|---|
| **Caption** | What they wrote below | ⛔ **The most expensive and most repeated.** It often tells a story the video never tells |
| **On-screen text** | The cards and overlays | This is the real script of silent pieces |
| **Transcribed audio** | What is actually said | This is the real script of spoken pieces |

**Case:** a reel with **8,950,289 views**, caption full of paragraphs about a 90-day challenge.
Full audio, all 28 seconds: *"Challenge of the day for your brain."* One sentence. It was proposed
as a template for a "lesson" piece. There is no lesson anywhere in it.

---

## 4. ⛔ DISCARD BY FUNCTION, NOT BY METRICS

Before anything enters the library, two questions:

```
1. What does the video actually SAY?  (not the caption)
2. Does that fulfil the JOB of the piece you need?
```

If the answer to 2 is no, **discard it however many views it has.** Nine million views do not put
a lesson inside a video that has none.

### And discard what your user cannot film

| Discard | Why |
|---|---|
| 3D animation | Not reproducible without an animator |
| MrBeast-scale production | Too many shots, too many hours |
| Memes | No value and nothing to be proud of |
| Product reviews of other people's gear | Not their niche, and they do not own it |

**The filter:** *can they film it alone, in their room, in under an hour?* If not, it does not go in.

---

## 5. CLASSIFYING — what the structure is

Ava publishes eleven named structures. Label each outlier with the one it uses.

| Storytelling | Educational |
|---|---|
| Hero's Journey (6 steps) · About Me (5) · The Lesson (4) · The Big Goal/Dream (4) · Challenge to Victory (6) · The Breakthrough (3) | 3 Levels · 2 People · X vs X · Action-Result · Did You Know |

Plus eight piece templates: Tip/Hack · Myth · **Viral Video Reaction** · Step-By-Step · Common
Mistake · Authority · Selling.

**Three rules for labelling:**

1. **Prove the label in the transcript.** You must be able to point at the line where each step
   happens. If you cannot, leave it unclassified.
2. **"None of them" is a valid and frequent answer.** Do not force a label.
3. **Cap two per structure** in a batch of fifteen, or you hand over the same video fifteen times.

**Why it matters, beyond the label:** lessons drive **comments**, stories drive **shares**. An
outlier with many shares and few comments is the wrong template for a piece that has to generate
leads.

### The 7 hook types — one idea becomes seven videos

Shock · Comprehensive · Common Mistake · Comparison · Question · Negative · Tutorial

When a topic is good, do not write one script. **Write the seven hooks and pick.** The other six
are next month's content.

### The 5 visual hooks, by name

Clone · Prop · A bunch of jump cuts · Comparison · **Random mic**

---

## 6. THE OUTPUT — one card per outlier

One `.md` file per outlier, in a folder, **named after the CONCEPT of the video** — not the
account. So the folder can be opened and understood without opening anything.

```
YYYY-MM-DD - concept.md        worth trying
x YYYY-MM-DD - concept.md      rejected
```

Each card, in this order:

````markdown
# @account

*X views · Y followers · Zx · N s · niche*
*likes · comments · shares*
*link*

*Verbal hook: … Written hook: … Visual hook: …*

*Format: which structure it is and how it is shot*

---

## THE SCRIPT

```
[ 0.0s] …literal transcript, with timestamps…
```

*The formula: the skeleton with blanks — `Two guys have a different ___. The first uses ___…`*

---

## MY VERSION

**Verbal hook:** … **Written hook:** … **Visual hook:** …

```
…the user's script…
```

Why it works · what cannot change · production notes

---

## THE CAPTION

**Theirs, literal:** …

*The formula: how that caption is built*

**Yours:** …
````

Full template in `references/script-card.md`.

### Why the caption gets its own section

**The caption does a different job than the video.** Measured across sixteen outliers, not one of
them repeats what the video already said:

| What the caption does | Example |
|---|---|
| **Only the CTA**, 58 characters | AI tooling accounts |
| **Only the title**, 39 characters | A video-editing account |
| **The fine print** of the maths, plus a disclaimer | A personal-finance account |
| **The actual advert** — price, hours, address, phone | A local restaurant |
| **The series counters** (`DAY 68/90`) | A study-challenge account |
| The keyword **at the top and again at the bottom** | A skincare account |

---

## 7. WRITING "MY VERSION"

**This is where most of the value is, and where it goes wrong.**

### The template is literal

Only what is in parentheses changes. If the template says:
```
"Well all up until (insert life changing event)"
```
the line is **one sentence**. Not three.

> **The test:** count the sentences in the script, count the steps in the template.
> **More sentences than steps means there is filler.**

What does not fit is not cut information — **it is another video.**

### It carries the hook and the structure

If "my version" does not open with the adapted hook and does not follow the same steps, it is not
an adaptation. It is a different video wearing the outlier's name.

### Nothing technical the audience does not say

Write in the words the *customer* uses, from `references/brand-profile.md`. Every industry term
you keep is a viewer you lose.

### Never discredit them inside their own craft

Some molds ask for comic humility — *"everyone asks me how to change a tire, and I don't know"*.
That works because changing tires is **not her business**.

> **The test:** if the line of ignorance would cast doubt on what they are about to sell three
> seconds later, it is wrong. Move it to something outside their field.

### Never invent what they say

Every line of dialogue must be traceable to something the user actually told you. If it is not,
mark it `(TO CONFIRM)` and let them approve it. A script that sounds great and did not happen is
worse than no script.

### If the piece promises a number, the steps must reach that number

A five-step calculation whose title promises "how much this costs you" has to end **on that
figure**. Ava's own example: her five factors sum to exactly 1.

---

## 8. THE CTA LADDER

| Level | CTA |
|---|---|
| ❌ **Bad** | *"Follow me!"* · *"Come along"* · anything that promises nothing |
| ✅ **Good** | *"Follow for more education on X"* |
| 🏆 **Great** | *"Want to learn how (concrete result with a number) in (timeframe)? Follow and I'll show you exactly how"* **+ visual proof on screen** |

**Four types:** Follow · ManyChat · Engagement · None.

⛔ **Never "link in bio".** Ava: *"if you're sending people to a product, service or freebie,
please don't use 'link in bio'. Please use ManyChat."* Keyword under 5-7 letters.

The funnel:
```
comment with keyword -> auto-DM -> landing page loaded with PROOF -> VSL before the call
```

---

## 9. THE MISTAKES THIS METHOD ALREADY MADE

Every one of these is real. They are here so you do not repeat them.

| Mistake | What happened | How to avoid it |
|---|---|---|
| **Writing the script from the caption** | The real video was six women walking through Milan with two lines of text and no voice | Watch it. Always |
| **Applying 5X without the absolute-views filter** | Reels with 3,800 views proposed as outliers | Filter 1 before filter 2 |
| **Using the teacher as the template** | Ava's own posts are not outliers. She is the teacher, not the mold | Templates come from 1K-100K accounts |
| **Watching one frame** | Concluded a man was "reacting out loud" when he never spoke | Six frames minimum |
| **Watching frames but not listening** | 8.9M views proposed as a lesson template. Its full audio is one sentence | Transcribe. Always |
| **Accepting a truncated transcript** | Four cards written with the wrong hook | First line must read `[ 0.0s]` |
| **Padding the template** | 15 sentences where the template had 5 steps | One step, one sentence |
| **Inventing quotes for the user** | A line that sounded great and he had never said | Trace every line to source |
| **Confusing high metrics with fitness** | Nine million views on a video with no lesson in it | Discard by function |
| **Proposing what they cannot film** | 3D animation and a one-day shoot | Alone, their room, under an hour |
| **Assuming a command worked** | Printed "ok" while the browser extension was down | Verify every output |

---

## 10. WHAT CANNOT BE AUTOMATED

- **Deciding whether a piece is worth their name.** If it only chases views and they would not be
  proud of it, do not propose it.
- **The value inside the script.** Steal the mold — hook, structure, format, topic.
  **The value is always theirs.**

---

## CREDIT

The whole strategy — the 5X rule, the seven hooks, the eleven structures, the CTA ladder, the
caption discipline — is **Ava Yuergens'**, taught on
[@personalbrandlaunch](https://www.instagram.com/personalbrandlaunch/).

This skill only turns her process into something an agent can run. Go learn from her directly.
