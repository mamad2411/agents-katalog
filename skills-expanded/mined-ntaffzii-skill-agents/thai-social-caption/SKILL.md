---
name: thai-social-caption
description: Use this skill for any task writing Thai-language social media captions or short-form copy for Facebook, TikTok, Instagram, Threads, X, or Pantip. Trigger on "แคปชั่น", "แคปชั่นไอจี", "แคปชั่นติ๊กต๊อก", "โพสต์เฟส", "เขียนโพสต์ Pantip", "caption ภาษาไทย", "Thai social media caption". If the platform or tone isn't specified, ask or default to Facebook/Instagram conventions (the most common request) rather than guessing TikTok or Pantip's very different register.
---

# Thai Social Media Captions

## Overview

A literally-translated caption ("Get 20% off today!" → "รับส่วนลด 20% วันนี้!") is grammatically correct Thai but reads like a translated ad, not something a Thai creator would actually post — real Thai social copy code-switches with English, uses platform-specific slang (555 for laughter, จขกท on Pantip), and has a tone that varies sharply by platform. This skill supplies the per-platform conventions a literal translation misses.

## When to use

- เขียนแคปชั่น Facebook / Instagram / TikTok / Threads / X (Twitter) / Pantip
- ปรับ tone ของโพสต์ให้เข้ากับแพลตฟอร์ม (เช่น จากทางการเป็นกันเอง หรือกลับกัน)
- เลือกใช้ hashtag, คำเรียกร้องให้ทำ (CTA), หรือมุกตลกที่เข้ากับ platform culture

## When NOT to use

- Formal business copy (press release, official announcement) — that's closer to `thai-government-form`'s register, not casual social captions
- Customer-service replies to a specific complaint — use `thai-customer-service` for that register instead

## Core knowledge

**Platform tone differences**:

| Platform | Typical caption style |
|---|---|
| Facebook | Longer-form allowed — storytelling, personal voice, can carry a full narrative before the CTA. Older/broader audience skews slightly more formal than TikTok. |
| Instagram | Short-to-medium, aesthetic-led, heavy emoji use, hashtag block often placed at the end or in first comment |
| TikTok | Very short, hook-first (the first line has to stop the scroll), casual/playful, trend-aware slang, often incomplete sentences |
| Threads | Conversational, closer to a spoken reply than a polished post; short |
| X (Twitter) | Shortest, punchy, often opinion/reaction-driven; Thai X culture leans toward wit, sarcasm, or timely commentary |
| Pantip | Forum/narrative style, much longer than social captions, first-person storytelling; has its own jargon (จขกท = เจ้าของกระทู้ = the OP; ซี้ด = interesting/hype; มุ้งมิ้ง, อบายมุข used ironically) — writing a Pantip post like an Instagram caption reads as out of place |

**Common Thai internet conventions**:
- `555` (or `5555`) = laughter — "5" is ห้า, pronounced "ha", so repeated 5s read as "ha ha ha". Do not translate this literally as the number five.
- Code-switching (Thainglish) is normal and often expected in casual captions — mixing English words/phrases into Thai sentences reads as natural, not as a translation gap, especially on IG/TikTok.
- Emoji density is generally higher than English-language captions for the same platforms — sparse emoji can read as flat/corporate.
- Hashtags: Thai captions commonly mix Thai-language and English hashtags in the same post; over-stuffing (10+ hashtags) is more of an IG-era habit and reads dated on TikTok/Threads now.

## Common mistakes

1. Writing every platform's caption in the same register — a Facebook-length storytelling caption pasted into TikTok will underperform because it doesn't hook in the first line.
2. Translating "555" or "ha ha" literally instead of using the Thai internet convention.
3. Avoiding all English code-switching in an attempt to be "purely Thai" — this often reads as stiffer than natural Thai social writing.
4. Using Pantip forum jargon (จขกท, etc.) outside Pantip, where it doesn't belong.
5. Under-using emoji on IG/TikTok relative to what actually performs in that context, because English-language instincts default to sparser emoji use.
6. A CTA that's too soft/apologetic for the platform's norm — Thai TikTok/IG captions are often more direct about "กดตามด้วยนะคะ/ครับ" (follow, please) than an English-language equivalent would be.

## Known limitations

- Platform norms and trending slang shift fast — treat the specific slang terms listed here as illustrative, not exhaustive, and check current usage if the caption needs to sound current rather than merely correct.
- This skill doesn't know the brand's specific voice guidelines — if the user has an established brand tone, that overrides the general platform defaults above.
