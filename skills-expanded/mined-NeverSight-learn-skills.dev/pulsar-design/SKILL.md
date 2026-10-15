---
name: pulsar-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build components, pages, or applications regarding Pulsar. Generates creative, polished code that avoids generic AI aesthetics.
---

## Mission
This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

## Rules

### Do
- prefer semantic tokens over raw values
- preserve visual hierarchy
- keep interaction states explicit

### Don't
- VERY IMPORTANT: Don't use decorative colored dots as visual markers in lists or cards (e.g. colored circles next to vault names). Use the asset's real logo instead, or omit the marker entirely.
- VERY IMPORTANT: Don't use outlined pill badges with pulsing dots (e.g. "Coming Soon" badges with an animated green dot). If a badge is needed use a solid bg filled one with no dot.
- Don't use placeholder letter-circles for asset icons. Always use real logos (see "Asset Logos" section).
- Don't use full phone mockups/device frames. They compress too much info into a small space and look cheap at web scale. Use isolated feature widgets instead.

## Style Foundations
- Visual style: minimal, clean, white-first fintech aesthetic
- Art direction: performative lifestyle photography + realistic fintech 3D renders
- Typeface: DM Sans (single typeface for everything)

### Icons
- Library: **Lucide** (https://lucide.dev)

### Typography
- Heading 1: 72px / semibold (600) / tracking -2.88px
- Heading 2: 44px / semibold (600) / tracking -1.32px
- Heading 3: 27.68px / semibold (600) / tracking -0.5536px
- Body Large: 18px / regular (400)
- Body: 15px / regular (400)
- Label: 13px / medium (500)
- Caption: 11.2px / medium (500) / tracking 2.24px / uppercase

### Color palette (4 core colors):
- Ice Blue: #97C2EC (primary accent)
  - Scale: 50=#EFF6FC, 100=#D8EAFA, 200=#BFDAF5, 300=#AECDED, 400=#97C2EC, 500=#7AAED8, 600=#5C97C2, 700=#437FAB, 800=#2D6694, 900=#1B4E7A
- Carbon Black: #1F1F1F (backgrounds, dark surfaces)
  - Scale: 50=#F5F5F5, 100=#EBEBEB, 200=#D4D4D4, 300=#ABABAB, 400=#757575, 500=#525252, 600=#3D3D3D, 700=#2E2E2E, 800=#1F1F1F, 900=#141414
- White: #FFFFFF (light surfaces, text on dark)
  - Scale: 50=#FFFFFF, 100=#FAFAFA, 200=#F5F5F5, 300=#EEEEEE, 400=#E0E0E0, 500=#CDCDCD, 600=#B0B0B0, 700=#8E8E8E, 800=#6E6E6E, 900=#4E4E4E
- Frosted Mint: #E4FCD0 (secondary accent, success states)
  - Scale: 50=#F4FDF0, 100=#E9FBE0, 200=#E4FCD0, 300=#D0F5B5, 400=#B8EA91,500=#99D86A, 600=#78C24A, 700=#5CA636, 800=#458727, 900=#316B1C

### Spacing scale:
- Spacing scale: 8pt baseline grid
- Border radius: 24px (cards), 16px (containers), 14px (images), 10px (swatches/small elements)

### Asset Logos (crypto, fiat, stocks)
Never use placeholder circles with letters. Always use real logos:
- **Crypto tokens**: `https://coin-images.coingecko.com/coins/images/{id}/small/{filename}.png`. Common: Bitcoin `1/small/bitcoin.png`, Ethereum `279/small/ethereum.png`, USDC `6319/small/usdc.png`, USDT `325/small/Tether.png`, Cardano `975/small/cardano.png`, Solana `4128/small/solana.png`, DAI `9956/small/Badge_Dai.png`, Chainlink `877/small/chainlink-new-logo.png`.
- **Fiat currencies**: `https://flagcdn.com/w80/{country_code}.png`. Map: EUR=`eu`, USD=`us`, GBP=`gb`, JPY=`jp`, CHF=`ch`, RON=`ro`, CNY=`cn`, AUD=`au`, CAD=`ca`.
- **Stocks / companies**: `https://www.google.com/s2/favicons?domain={company_domain}&sz=64`. e.g. `apple.com`, `tesla.com`.
- Display in circular container (`border-radius: 50%`, `object-fit: cover`). 36px in lists, 48px in detail views.

### Brand Mark
- Wordmark: "Pulsar" set in DM Sans semibold (600), tracking −0.04em
- Icon mark: P glyph system — works on light (#F5F7FA), dark (#1F1F1F), and Ice Blue (#97C2EC) backgrounds -> both the logo-small.svg and logo.svg files are present in the ./assets folder
- App icon variants: Dark, Ice Blue, Light
- Full lockup: Icon mark + wordmark, horizontal arrangement

### Logo Usage Rules
1. **Clear Space**: minimum clear space equal to the height of the 'P' mark on all sides
2. **Minimum Size**: icon mark 24px, full wordmark 80px wide — never go below
3. **Color Integrity**: Carbon Black on light backgrounds, white on dark backgrounds, Ice Blue icon only on medium-tone surfaces
4. **No Distortion**: never stretch, rotate, recolor, or apply effects outside the approved palette

## Accessibility
WCAG 2.2 AA, keyboard-first interactions, visible focus states

## Writing Tone
concise, confident, helpful. Don't use emojis and don't use AI slop. Text should be straightforward and to the point without any fluff.

## When programming design systems
- don't use magic numbers / strings. Always define the brandguides in the code to be structured. If you use tailwind the colors should be defined in the tailwind.config file.