---
name: thai-customer-service
description: Use this skill for any task drafting a Thai-language customer-service reply — apologies, status updates, refund/return scripts, or auto-replies for LINE OA, Facebook Page, Shopee, Lazada, Instagram DM, TikTok Shop, or similar channels. Trigger on "reply ลูกค้า", "ตอบแชท", "LINE OA", "Shopee ตอบลูกค้า", "ขอโทษลูกค้า", "refund script", "customer service Thai". If the message is internal (to a colleague, not a customer), this skill's apology-ladder register doesn't apply — use plain professional Thai instead.
---

# Thai Customer Service Replies

## Overview

Using the same apology intensity for a 1-day shipping delay and a wrong/damaged item both under- and over-shoots — Thai customer-service register has a graded apology ladder, and picking the wrong rung reads as either dismissive or oddly dramatic. This skill maps severity to the right phrase and gives channel-specific tone guidance, since a LINE OA reply and a Shopee platform-mediated reply don't read the same even for an identical situation.

## When to use

- Reply ลูกค้าที่ร้องเรียน/บ่น/ขอเงินคืน บน LINE OA, Facebook Page, Shopee, Lazada, IG DM, TikTok Shop
- เขียนข้อความแจ้งสถานะ (delay, order update, restock)
- ร่าง auto-reply / FAQ response ที่ยังต้องฟังดูเป็นมนุษย์ ไม่ใช่บอทแข็งๆ
- Choosing the right apology intensity for a given severity of complaint

## When NOT to use

- Internal communication to a colleague or vendor — that's a different register, not the customer-facing apology ladder
- Formal written complaint response requiring legal review (e.g. involving compensation liability) — draft here for tone, but have anything with real financial/legal exposure reviewed

## Core knowledge

**Apology ladder** — match intensity to severity, don't default to the strongest phrase every time (it reads as insincere when overused) or the mildest (reads as dismissive for a real failure):

| Phrase | Severity | Example trigger |
|---|---|---|
| ขออภัย(ค่ะ/ครับ)ในความไม่สะดวก | Mild | Minor delay, small inconvenience, a question that took a while to answer |
| ขออภัยเป็นอย่างยิ่ง | Moderate | Order delay beyond promised window, out-of-stock after order confirmed |
| ขอโทษอย่างสูง | High | Wrong item sent, damaged item, billing error, clearly the seller's fault |
| ขอแสดงความเสียใจอย่างยิ่ง | Severe | Major failure, safety/health concern, repeated failure after prior complaint |

Pair the apology with a concrete next step every time — an apology with no resolution offered reads as empty regardless of which rung is used.

**Channel tone differences**:

| Channel | Typical register |
|---|---|
| LINE OA | Most personal/warm of the group — emoji, stickers, first-name-adjacent tone common; closest to a 1:1 chat |
| Facebook Page / Messenger | Personal but slightly more public-facing (comments are visible) — keep resolution details in DM, acknowledge publicly |
| Shopee / Lazada / TikTok Shop (marketplace chat) | More procedural — platform policies constrain what can be promised (refund timing, dispute process); stick to what the seller can actually control and reference the platform's own return/refund flow rather than inventing terms |
| Instagram DM | Casual-personal, similar to LINE OA but often shorter messages |

**Structure for a complaint reply**: (1) acknowledge specifically what went wrong — not a generic "we're sorry for any inconvenience" that doesn't reference the actual issue, (2) apologize at the matched severity, (3) state the concrete resolution and timeline, (4) close with a way to follow up if unresolved.

## Common mistakes

1. Using ขอโทษอย่างสูง or ขอแสดงความเสียใจอย่างยิ่ง for a trivial delay — reads as performative rather than sincere.
2. Using only ขออภัยในความไม่สะดวก for a genuinely serious failure (wrong item, damaged goods) — reads as dismissive.
3. A generic apology with no acknowledgment of the specific problem the customer described.
4. Promising a resolution the seller can't actually deliver on a marketplace platform (e.g. an instant refund that has to go through the platform's dispute process).
5. Matching LINE OA's warm, emoji-heavy tone on a marketplace platform where the register expected is more procedural.
6. Public reply on Facebook/IG comments revealing personal order details that should move to DM.

## Known limitations

- Exact refund/return timelines and policies are platform- and seller-specific (Shopee, Lazada, and TikTok Shop each have their own dispute-resolution windows that change over time) — this skill supplies tone and structure, not current platform policy figures; verify those against the seller's own account/platform dashboard.
- Does not cover legal liability language for safety-related complaints — escalate those to a human/legal review rather than auto-generating a final response.
