---
name: poster
description: |
  Generate a cinema-grade movie, event, podcast, or concert poster with
  proper typography in any language. One command, ~15 seconds, ~$0.12.
  Uses GPT Image 2 (multilingual text rendering!) via the BlockRun MCP
  plugin (x402 USDC on Base). Eight built-in genres: thriller, sci-fi,
  romcom, documentary, concert, horror, kids-animation, event.
triggers:
  - "movie poster"
  - "film poster"
  - "event poster"
  - "concert poster"
  - "podcast cover"
  - "key art"
  - "make a poster"
  - "电影海报"
  - "活动海报"
  - "founder documentary poster"
  - "launch poster"
user-invocable: true
allowed-tools: mcp__blockrun__blockrun_image, mcp__blockrun__blockrun_wallet, Bash(curl:*), Bash(mkdir:*), Bash(date:*), Read, Write
---

# `/poster` — Cinema-grade poster in one command

Generates a polished poster with **legible, accurate title typography in
any language** (gpt-image-2's killer feature). Use it for film festival
submissions, event banners, podcast cover art, concert posters, or pitch
deck mockups.

## What this skill does

Picks a genre block from the **Genre variants** section at the bottom of
this file, fills the master template with the user's title + tagline +
subject, and calls `mcp__blockrun__blockrun_image` with
`model="openai/gpt-image-2"`.

Default size is `1792x1024` (cinematic landscape). Add `--portrait` for
the traditional one-sheet `1024x1792`. Add `--square` for `1024x1024`
(podcast cover / Spotify Canvas friendly).

## Inputs

| Input | Required | Default | Notes |
|---|---|---|---|
| `title` | yes | — | The string that will be rendered as the title. CJK works. |
| `genre` | no | `documentary` | `thriller`, `sci-fi`, `romcom`, `documentary`, `concert`, `horror`, `kids-animation`, `event`. |
| `tagline` | no | `""` | A subtitle line. Empty omits the line. |
| `subject` | no | inferred from title | e.g., "a lone astronaut on a red planet". |
| `credits` | no | auto fake | A faux credit block, or pass real credits. |
| `accent_color` | no | per-genre default | Hex or color name. Useful for `event` genre. |
| Aspect flags | no | `--landscape` | One of `--landscape` (1792×1024, default), `--portrait` (1024×1792), `--square` (1024×1024). |
| `image` | no | — | Optional reference image for the lead subject (image-to-image edit). |

## Workflow (Claude executes strictly in order)

### Step 0 — Verify the BlockRun MCP server is registered

Before any tool call, confirm `mcp__blockrun__blockrun_image` and
`mcp__blockrun__blockrun_wallet` are available. If not, surface this
exact message and stop:

> "The BlockRun MCP server isn't registered with Claude Code yet, so
> `/poster` can't run. Please run **once**:
>
> ```
> claude mcp add blockrun -s user -- npx -y @blockrun/mcp@latest
> ```
>
> Then restart Claude Code and try `/poster` again. (Full install
> guide: `INSTALL.md` in the Claude Code-GPT-IMAGE2-SeeDance-BlockRun bundle.)"

Do not proceed to the wallet preflight or image call if the MCP tools
are missing.

### Step 1 — Wallet preflight

Call `mcp__blockrun__blockrun_wallet` with `{"action": "status"}`.

- Required: **≥ $0.20 USDC**.
- Too low? Show:
  > "Your BlockRun wallet balance is too low. /poster costs ~$0.12.
  > Run `blockrun_wallet action: setup` to top up Base USDC."
  Do not proceed.

### Step 2 — Resolve aspect

```
--landscape  → size = "1792x1024"
--portrait   → size = "1024x1792"
--square     → size = "1024x1024"
default      → "1792x1024"
```

### Step 3 — Prepare prompt

Use the master template from the **Genre variants** section at the bottom
of this file. Pick the genre block matching `--genre`. Fill the master
template with the user's `title`, `tagline`, `subject`, `credits`,
`accent_color`.

If `subject` is missing, infer it from the title and genre. For example,
`"Founders" + documentary` → `"a focused entrepreneur at a laptop, late
night, single desk lamp"`.

### Step 4 — Call BlockRun MCP

```
Tool: mcp__blockrun__blockrun_image
Arguments:
{
  "prompt": "<filled template from Step 3>",
  "action": "<generate or edit>",   // edit if user provided --image
  "model": "openai/gpt-image-2",
  "image": "<base64 data URI or URL>",  // only if --image was given
  "size": "<from Step 2>",
  "quality": "hd"
}
```

The tool returns synchronously in ~10–20 seconds.

### Step 5 — Download and save

1. Timestamp: `date -u +"%Y-%m-%dT%H%M%SZ"`.
2. Output dir: `${BLOCKRUN_OUT_DIR:-./blockrun-out}/{ts}-poster/`.
3. `mkdir -p` the dir.
4. Filename includes aspect: `poster-{aspect}.png`
   (e.g., `poster-1792x1024.png`).
5. `curl -sSL "<url>" -o <out_dir>/<filename>`.
6. Confirm file is non-empty.

### Step 6 — Verify title rendering (cheap quality gate)

Quickly check the response for content quality flags. If the user's title
contains CJK, Arabic, Cyrillic, or Hebrew characters, gently remind them
to verify the glyphs are correct in the output — gpt-image-2 is good but
not infallible with non-Latin scripts.

### Step 7 — Report to user

```
✅ Poster ready

  File:    {relative path}
  Title:   "{title}"
  Genre:   {genre}
  Aspect:  {size}
  Model:   openai/gpt-image-2 (HD)
  Cost:    ~$0.12 (settled on Base via x402)

Open it: open {relative path}
```

## Failure handling

| Error pattern | Action |
|---|---|
| `payment` / `balance` keywords | Show top-up message, do NOT retry. |
| Title text comes back as gibberish or wrong language | Apply the "Title text is gibberish" retry addendum from the **Common pitfalls** section below and retry once. |
| `content filter` / `safety` / `invalid` | Suggest rephrasing — common triggers are real-celebrity names or brand-protected IP. |
| Composition feels overstuffed | Apply the "no negative space" retry addendum from the **Common pitfalls** section below and retry once. |
| `No wallet found` | Walk through `blockrun_wallet action: setup`, then retry. |

## Cost

- Landscape / portrait / square: ~$0.12 each (gpt-image-2 HD)
- A retry counts as a second call (~$0.24 total for that command run)
- Settled on Base USDC via x402.

## Examples

```
/poster "Last Light" --genre thriller
/poster "Founders" --genre documentary --tagline "they bet everything"
/poster "BlockRun Live" --genre event --accent_color "#0066ff" --portrait
/poster "兵马俑：复活" --genre sci-fi
/poster "Coffee with the CEO" --genre documentary --square  # podcast cover
```

---

## Master template

```
A cinematic {format} poster for "{title}".

Genre: {genre}
Mood: {mood}
Lead subject(s): {subject_description}
Composition: {composition}
Lighting: {lighting}
Color palette: {palette}
Typography: render the title "{title}" prominently in {font_style} at
{title_position}. Below the title, a tagline line reading
"{tagline}" in a smaller complementary face. Include a faux credit block
at the bottom: "{credit_block}".

Aspect: {aspect_hint}
Texture: subtle film grain, deep blacks, professional color grade.

This is a marketing key art image — strong silhouette readability, hierarchy
flows from title → image → tagline → credits, no clutter, frame edges are
intentional negative space.
```

## Genre variants

### `thriller` (gritty, suspense, neo-noir)

```
{mood}: tense, paranoid, mysterious; viewer feels watched
{composition}: lone protagonist mid-frame, shoulders forward, half-shadowed
              face; vast empty negative space above their head
{lighting}: chiaroscuro, single hard key from off-frame, deep shadows
            swallowing background details
{palette}: charcoal, oxidized green, blood-rust accents; ~70% black
{font_style}: heavy sans-serif (think Helvetica Inserat) compressed;
              all caps; slight chromatic aberration on the title
{title_position}: lower-third, centered
```

### `sci-fi` (epic, cosmic, future-forward)

```
{mood}: vast, awe-inspiring, technologically sublime
{composition}: subject as small silhouette against an enormous structure
              (megastructure / planetary horizon / orbital ring)
{lighting}: rim light from a distant cosmic source (sun / portal / engine
            glow); subtle volumetric haze
{palette}: deep navy + cyan + warm signal-orange contrast accents
{font_style}: futuristic geometric sans (think Eurostile / Neue Haas Unica
              Condensed Bold); subtle monospace tracking
{title_position}: upper-third or lower-third — never center
```

### `romcom` (warm, playful, character-forward)

```
{mood}: hopeful, bright, romantically optimistic
{composition}: two protagonists in playful interaction (back-to-back / one
              looking away while the other smiles), shot at golden hour
{lighting}: warm golden-hour bounce, soft and forgiving
{palette}: cream + dusty pink + sunset gold
{font_style}: handwritten-meets-display script for the title; clean serif
              for the tagline (think Caslon italic)
{title_position}: top, slightly diagonal
```

### `documentary` (default — founder-story / true-events vibe)

```
{mood}: earnest, observational, fly-on-the-wall yet aspirational
{composition}: tight portrait of the protagonist at work — laptop / lab /
              workshop — slight motion blur from candid moment
{lighting}: practical naturalistic — desk lamps, monitor glow, window light
{palette}: muted denim, paper-white, warm tungsten accents; high realism
{font_style}: clean modern serif for title (Mercury Display / GT Sectra);
              compact grotesque for subtitle
{title_position}: bottom-third, left-justified, treated like a book cover
```

### `concert` (k-pop / festival / live event poster)

```
{mood}: high-energy, in-your-face, FOMO-inducing
{composition}: lead artist mid-pose taking up 60% of frame; secondary
              graphic motifs (lightning / bursts / typographic shapes)
              filling negative space
{lighting}: stage spotlight key + rim, lens flare on hits
{palette}: high-saturation duotone (e.g., hot pink + electric blue) OR
           single accent color over deep black
{font_style}: oversized display sans (think Druk Wide); title can break
              the bounding box
{title_position}: dominates upper half, can overlap subject
```

### `horror` (psychological, atmospheric)

```
{mood}: dread, unease, what-you-don't-see-is-worse
{composition}: extreme negative space; subject is a small silhouette OR a
              single uncanny detail (door ajar, eye in shadow); rule-of-thirds
              gives the viewer somewhere to escape to but keeps them stuck
{lighting}: minimal — one cold practical light, hint of sodium-vapor orange
            from a distant streetlamp
{palette}: ~85% black, sodium-orange accents, pale skin tones
{font_style}: distressed slab serif OR a fragile thin sans that "trembles"
{title_position}: bottom, small, almost a whisper
```

### `kids-animation` (family-friendly animated film vibe)

```
{mood}: warm, adventurous, hopeful, slight whimsy
{composition}: hero character + sidekick at lower-third, expansive sky /
              landscape filling the upper two-thirds, dynamic depth
{lighting}: full daylight, soft cloud shadows, characters slightly
            front-lit for clarity
{palette}: saturated primary triad (sky blue + grass green + warm yellow)
           with one accent character color
{font_style}: rounded display (think custom Disney / Pixar lockup);
              slight 3D bevel on the title
{title_position}: bottom, large, becomes part of the landscape
```

### `event` (conference / podcast / launch-day banner)

```
{mood}: clean, premium, "you should buy a ticket"
{composition}: bold typographic-led layout; subject (speaker portrait or
              product render) anchored to one third
{lighting}: studio flat-lit subject, contrasting graphic background
{palette}: brand-driven — derive from `--accent_color` or default to
           deep indigo + electric mint
{font_style}: contemporary geometric sans (Inter / Söhne) with a tight
              display headline; consistent grid
{title_position}: large headline + date + location stack on left; subject
                  on right
```

## Defaults the skill auto-fills if user doesn't specify

```
{format}        = "feature film one-sheet"
{aspect_hint}   = "landscape 1.85:1 cinematic crop"
{tagline}       = "" (omit the tagline line entirely if blank)
{credit_block}  = a fake but plausible "directed by / starring / studio"
                  line in tiny condensed caps. The skill's caller may pass
                  a real credit block via --credits.
```

## Common pitfalls + retry addenda

### "Title text is gibberish / wrong language"

Append:
```
The title MUST read exactly the characters: "{title}" — verify each glyph.
If rendering Chinese / Japanese / Korean, ensure correct CJK characters
and traditional vs simplified consistency. Do not invent letters.
```

### "Composition is too busy / no negative space"

Append:
```
Strip background detail by 60%. The hero subject + title + 30% empty
space is the goal. A movie poster is read in 0.5 seconds — hierarchy first,
detail second.
```

### "Looks like AI / overly painterly"

Append:
```
Render in a photorealistic key-art style with very subtle film grain. Avoid
illustrated brush strokes unless the genre is animation. Reference: think
"theatrical one-sheet shot on 70mm", not "Midjourney v3 fantasy splash".
```
