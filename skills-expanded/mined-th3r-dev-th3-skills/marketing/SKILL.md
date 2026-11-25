---
name: marketing
description: >-
  Marketing toolkit for selling a service, one skill with sub-skills. (1) strategy: who the service is for,
  what it promises and how buyers find it (STP, value proposition, persona, funnel, metrics); (2) pricing:
  measure the marketplace, then price packages from real costs (hourly target, living and business costs,
  equipment, platform fee) so no package loses money, with averages for anything unconfirmed; (3) listing:
  write the marketplace listing field by field (service name, description, packages, units, tags, media)
  and check it with offer.py. Use WHENEVER the user wants to sell a service, set up packages, price their
  work, write a Fastwork / Fiverr / Upwork listing, or asks "ตั้งราคายังไง", "ทำแพ็กเกจ", "คิดราคางาน",
  "ราคาต่อชั่วโมง", "ค่าใช้จ่ายต่อเดือน", "ลงขายงานบน Fastwork", "ดึงลูกค้า", "หาลูกค้า", "marketing",
  "pricing", "packages", "service listing". Read the sub-skill's SKILL.md before acting.
---

# marketing: sub-skills

| When the work is… | Read | Scripts |
|---|---|---|
| who to sell to, what to promise, how buyers find the service | [`strategy/SKILL.md`](strategy/SKILL.md) | none |
| what to charge, how many packages, whether a package loses money | [`pricing/SKILL.md`](pricing/SKILL.md) | `scripts/fastwork_market.py` (market sample), `scripts/offer.py price` |
| the listing itself: name, description, packages, units, tags, images | [`listing/SKILL.md`](listing/SKILL.md) | `scripts/offer.py check`, `../design/banner-design/scripts/banner.py` |

They run in order: strategy decides who and what, pricing turns costs and the market into package
prices, listing writes it in the platform's fields. The offer lives in one TOON file that both
`offer.py` commands read.

## Rules every sub-skill keeps

- **Measure before pricing.** Read the platform's own category (public pages only, stop at a bot
  check) and keep the sample's numbers as facts in the offer.
- **Ask for the user's own numbers first** (income target, living costs, equipment, fees they pay).
  For anything they don't know and can't be confirmed, use a published average and label it as an
  assumption with its source. Never invent a figure.
- **Every package must cover its hours at break-even;** `offer.py price` flags any that don't.
- **Buyers read outcomes, not tools.** The listing says what the client gets, where it runs (Cloud,
  self-host) and how it is supported, not the tech stack.
- **Plain characters in pasted fields:** no "·", "+" or dashes; write "และ" or a space.
- **Write the output in the platform's field layout** and save it where the user keeps their work.
  Ask for the folder once; don't hardcode a personal path in the skill.
- Thai prose goes through `kien-thai`, and every prose deliverable gets a `humanizer` pass.

The worked case is [th3r-web-service](examples/th3r-web-service/RESULTS.md).
