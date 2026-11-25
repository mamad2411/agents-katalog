---
name: new-brand
description: Set up a new brand (product, app, side project) in brands/<slug>/ so videos can be made for it - facts and their sources, look (colours, fonts, logo, mascot), voice, compliance and default engines. Done as a short conversation with the person, reading their website and files first. Use before the first video for a brand, or when asked to add a brand.
---

# Adding a brand

The person is usually a marketer or founder. Treat this as getting to know their product, not filling in a form.
Plain words, 2–3 questions per message, no file paths or jargon (see `make-video`, *How to talk*).

## The conversation

1. **Ask for what you can read**: "What's the product called, and is there a website, app store page or folder
   with your logo and past ads I can look at?" Then read all of it before asking anything else.
2. **Play back what you found**, short: "So it's X for Y, the colours look like these, the font is Z. Right?"
   Show a quick brand still (logo, colours, a headline in each font) instead of listing hex codes.
3. **Ask only what you couldn't find**, a few at a time:
   - Who is it for, in their customer's words? What does that customer struggle with?
   - Facts you're allowed to say (numbers, prices, ratings): "Only what's on your site, or are there others I can
     use? Where do they come from?"
   - Words or claims to never use (legal, sector rules, things the team hates).
   - Is there a mascot, character or a person who'd be happy to appear and talk? (Reels with a voice and a face
     reach further: worth asking now.)
   - A few accounts or ads they love, and ones they don't want to look like.
4. **Show the brand in 2–3 different looks** (each look's starter with their colours, fonts and a real line) and ask
   which feel like them and which don't. Their answer fills the *Look range*.

## Writing it down (quiet work)

1. `cp -R brands/_template brands/<slug>` (lowercase-kebab).
2. **Facts from sources, never from memory.** Record each source in *Fact sources*; anything the person told you is
   a source too ("told by <name>, <date>").
3. `README.md`: who it is, audience, positioning, identity (colours, fonts, logo, mascot or presenter), voice, *Look
   range* (fits, ask first, never). Identity and art direction stay apart: the brand never fixes one layout for
   every piece. Logo, fonts, references → `assets/` (`scripts/svg-to-png.sh` for SVG logos).
4. `tokens.css`: real colours and fonts (plus optional look tokens, `looks/README.md`). Render the check still and
   look at it.
5. `compliance.md`: keep *Always*, add the brand's own rules.
6. Style frames from step 4 → `assets/reference/looks/`.
7. `STATUS.md` (*Brands*) with open questions; the brand table in `README.md`.

A brand is ready when no ❓ or placeholder is left and the check still looks right. Then: "Ready. Want to start on
the first video? Tell me what it's for."
