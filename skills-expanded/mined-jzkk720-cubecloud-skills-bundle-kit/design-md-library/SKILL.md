---
name: design-md-library
description: Curated library of 74 real-world DESIGN.md files (Google Stitch spec) extracted from sites like Apple, Stripe, Linear, Vercel, Notion, Airbnb. USE WHEN the user wants a design system to ground UI generation, says "make it look like [brand]", "use the [brand] design system", wants to build a page matching a known site's visual language, asks for design tokens/colors/typography for a named brand, or references DESIGN.md / Stitch / VoltAgent awesome-design-md. Returns the path to the matching DESIGN.md so the agent can read and apply it. Not a generator itself — it's an index into the fork mirror at ~/dev/forks/JZKK720/awesome-design-md/design-md/.
---

# design-md-library

Index into the **awesome-design-md** collection (VoltAgent/awesome-design-md, MIT).
74 `DESIGN.md` files extracted from real websites, each following the Google Stitch
DESIGN.md spec (9 sections: visual theme, color palette, typography, components,
layout, depth, do/don'ts, responsive, agent prompt guide).

## Where the files live

The fork mirror is at:

```
~/dev/forks/JZKK720/awesome-design-md/design-md/<site>/DESIGN.md
```

Each `<site>/` dir also has a `README.md` with a one-line description. Read the
`DESIGN.md` for the full design system; the README is just a label.

## How to use

1. Identify the brand/site the user wants to emulate (e.g. "make it look like Stripe",
   "use the Linear design system", "build a page in the Vercel style").
2. Check if that site is in the index below. If yes, `read_file` the DESIGN.md at the
   path shown and apply it verbatim — it already contains the agent prompt guide.
3. If the user names a brand NOT in the index, tell them it's not in the library and
   either (a) fall back to the closest match by category, or (b) ask if they want a
   generic design system instead. Do not fabricate a DESIGN.md.
4. Do NOT copy the DESIGN.md into the project unless the user asks. Just read it and
   follow its rules when generating UI.

## Categories (for fallback matching)

- **AI & LLM Platforms:** claude, cohere, elevenlabs, minimax, mistral.ai, ollama,
  opencode.ai, replicate, runway, together.ai, voltagent, x.ai
- **Developer Tools & IDEs:** cursor, expo, lovable, raycast, superhuman, vercel, warp
- **Backend, Database & DevOps:** clickhouse, composio, hashicorp, mongodb, posthog,
  sanity, sentry, supabase
- **Productivity & SaaS:** cal, intercom, linear, mintlify, notion, resend, zapier
- **Design & Creative Tools:** airtable, clay, figma, framer, miro, webflow
- **Fintech & Crypto:** binance, coinbase, kraken, mastercard, revolut, stripe, wise
- **E-commerce & Retail:** airbnb, meta, nike, shopify, starbucks
- **Media & Consumer Tech:** apple, hp, ibm, nvidia, pinterest, playstation, spacex,
  spotify, theverge, uber, vodafone, wired
- **Automotive:** bmw, bmw-m, bugatti, ferrari, lamborghini, renault, tesla
- **Retro Web:** dell-1996, nintendo-2001

## Full index (site → path)

For any `<site>` below, the DESIGN.md is at
`~/dev/forks/JZKK720/awesome-design-md/design-md/<site>/DESIGN.md`.

ai-&-llm-platforms: claude, cohere, elevenlabs, minimax, mistral.ai, ollama,
opencode.ai, replicate, runway, together.ai, voltagent, x.ai
developer-tools: cursor, expo, lovable, raycast, superhuman, vercel, warp
backend-devops: clickhouse, composio, hashicorp, mongodb, posthog, sanity, sentry,
supabase
productivity-saas: cal, intercom, linear, mintlify, notion, resend, zapier
design-creative: airtable, clay, figma, framer, miro, webflow
fintech-crypto: binance, coinbase, kraken, mastercard, revolut, stripe, wise
ecommerce-retail: airbnb, meta, nike, shopify, starbucks
media-consumer: apple, hp, ibm, nvidia, pinterest, playstation, spacex, spotify,
theverge, uber, vodafone, wired
automotive: bmw, bmw-m, bugatti, ferrari, lamborghini, renault, tesla
retro-web: dell-1996, nintendo-2001

## Notes

- The DESIGN.md files are extracted from public CSS values of public websites. The
  repo's LICENSE (MIT) explicitly states these are provided "as is" and do not claim
  ownership of any site's visual identity.
- The library is a fork mirror, not a dependency. Updating means `git pull` in the
  fork dir; the index above is a snapshot of what was present at install time.
- If a site the user names is missing, the upstream repo accepts requests at
  https://getdesign.md/request — but do not make requests on the user's behalf.