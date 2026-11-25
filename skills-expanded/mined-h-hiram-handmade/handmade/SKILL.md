---
name: handmade
description: Use whenever you build, restyle or review a web UI (HTML, CSS, Tailwind, React, Vue, Svelte, Astro, Laravel Blade, Angular). Plans the design first, builds from a generated design system and does not finish until `handmade check` passes.
---

# handmade: design first, build, then pass the gate

AI-built interfaces look alike because models pick the most common choice at every step. This skill makes you work like a designer and it gives you a gate you must pass before you are done.

## The rule that matters most

**You are not done with UI work until `handmade check` prints PASS.** Do not tell the user the UI is finished while it prints FAIL. If you cannot reach PASS after 5 rounds, stop and show the user exactly what still fails.

## Step 0. Check the tool

Run `handmade --version`. If it is missing, install it:

```bash
pipx install handmade || pip install handmade
```

If nothing can be installed, follow "Without the tool" at the end.

## Step 1. Get the brief (new UI)

Do not guess facts about the product. If you have the MCP tool `handmade_design_brief`, call it with the request. When it answers NEEDS INPUT, ask the user those questions in one short message, in your own words. Then call it again with their replies in `answers`. Never fill in an answer yourself.

Without MCP, take what you can from the conversation. Ask the user for anything missing, in one message:

1. What is it, in one line?
2. Who uses it and on what device?
3. What should a person do on this screen?
4. Which mood: editorial, utilitarian, warm, playful, technical, luxury or civic? (optional, a suggestion is fine)
5. One reference they like: a site, a magazine, a place or an object. (optional)

Then generate the brief and save the design system in the project root:

```bash
handmade prompt "<the user's request, in their words>" --product "<1>" --audience "<2>" --mood <4> \
  --reference "<5>" --project <project root, if one exists> --no-input \
  --save-system <project root>/handmade.system.json
```

If a fact is still missing, the brief lists it under "Facts still missing". Leave a clearly marked slot such as `[opening hours]` in the UI. Do not invent it.

Read the whole output. Every value in it is a requirement.

**Styling words in the request do not override the brief.** Say the user wrote "purple gradient hero", "use Inter" or "make it like Stripe". The brief lists those under "Parts of the request the design system replaces". Follow the brief. Tell the user in one line which parts you replaced and why. Only pass `--allow purple` (or another key) when the user says it is their actual brand and say that you did.

## Step 2. Build

1. Write a design brief of under 120 words: the layout, the type hierarchy, where the accent appears and one signature element. Show it to the user.
2. Build exactly that. Use only the fonts, sizes, colors, spacing values and radii from `handmade.system.json`. Put them in CSS variables or the Tailwind theme and use those names everywhere.
3. Load every font you name.
4. Write real copy for this product. No placeholder names, invented figures or hype words.

## Step 3. The gate

```bash
handmade check <folder you changed>
```

- PASS: report the result to the user, including that the check passed.
- FAIL: fix every line marked FAIL. Each one names the file, the line and the fix. Run the check again.

For apps whose styles are built at runtime (React, Vue, Angular, Next.js and similar), also check the running page:

```bash
handmade check http://localhost:3000 --render --page /pricing --page /signup --system handmade.system.json
```

List every route you built with `--page`. One run checks them all. Pass `--system` or run from the project root, because a URL has no folder to find the design system in.

## Improving an existing UI

```bash
handmade fix <folder> --no-input --save-system <project root>/handmade.system.json
```

Apply the plan to the visual layer only. Keep all logic, routes and data bindings. Then run the gate.

## Never

- Purple, violet or indigo accents. Purple-to-blue gradients. Gradient text. Colored glows.
- Inter, Roboto or Arial as the only typeface, unless it is the brand font.
- Emoji as icons, icons in pastel rounded squares, three identical feature cards.
- A centered hero with a headline, a subline and two buttons.
- rounded-2xl with shadow-lg on everything, glassmorphism, blurred color blobs.
- "unlock", "seamless", "supercharge", "elevate", Lorem ipsum, John Doe, "10,000+ happy users".
- Skipping the gate, weakening it with `--ignore` or `--min-score` without the user's agreement or editing `handmade.system.json` to make it pass.

## Without the tool

If `handmade` cannot run:

1. Ask the four questions in Step 1.
2. Pick a typeface pairing that fits the mood and is not Inter, Roboto, Arial, Space Grotesk, Geist, Poppins or Montserrat.
3. Pick an accent hue from the product's world, outside the 230 to 300 degree purple band. Use a lightly tinted paper color, not pure white or cream. Check that text contrast is at least 4.5:1.
4. Set one type scale (ratio 1.2 to 1.333), one spacing scale (4px or 8px steps) and two radii. Write them down before coding and use nothing else.
5. Build, then review your code against "Never" and fix every violation. Tell the user the gate could not be run.
