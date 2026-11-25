---
name: tavily-text
description: Use when the user asks for Tavily Text, or wants a headline or key phrase set with letters alternating between a pixel font and a serif italic inside each word.
---

# Tavily Text

Display type where the letters of a word swap between a chunky pixel face and a flowing serif italic: A*t* t*h*e / *Ta*bl*e* / V*eg*as. The clash between bitmap and calligraphy does the emphasising, so it needs no colour, weight or size tricks. Named after the event invitation that inspired it.

## Fonts

Use exactly these two; near misses look sloppy.

| Role | Font | Get it |
| --- | --- | --- |
| Pixel | Geist Pixel Square (OFL) | `npm pack geist`, copy `package/dist/fonts/geist-pixel/GeistPixel-Square.woff2` and the OFL licence into the site, load with `@font-face` |
| Italic | Newsreader Italic, optical size 72 (OFL) | Google Fonts stylesheet: `family=Newsreader:ital,opsz@1,72` (the page needs a network connection) |

Geist Pixel is lighter than the look needs: thicken it with `-webkit-text-stroke: 0.03em currentColor`. Do not substitute Pixelify Sans, Silkscreen, Tiny5, Departure Mono or any other pixel font, and do not use a low-contrast italic such as Charter or Georgia.

## Choosing what to set

- **Headline on its own** (poster, card, hero title): set every word.
- **Inside a sentence**: set only the two or three phrases that carry the message (who it is for, what it is). The rest stays in the page's normal sans, at the same colour. Never set a whole paragraph.
- Use it sparingly: one headline, one key line, or the two together. It is display type: at least 28px, ideally 40px or more.

## Choosing which letters go italic

- Swap inside words, never whole words: every set word has both faces.
- Italic runs are 1–2 letters. Across a phrase, roughly a third of the letters go italic; judge by eye, not by count.
- Prefer letters whose italic form is very different from the pixel form: a, e, g, d, n, u, h, t, T, A. When a word has few of these, any letter other than i, l and r will do.
- Keep each word readable: leave at least two pixel letters in a row somewhere in every word of four or more letters.
- Mark italic letters with brackets: `st[a]rt[u]ps`, `[e]ngin[ee]ring t[ea]ms`, `co[d]ing [a]ge[n]ts`, `A[t] t[h]e`, `[Ta]bl[e]`, `V[eg]as`.

## Sizing and spacing

Relative to the surrounding text size: pixel letters at `1.1em`, italic letters at `1.2em`, both `line-height: 1`, `letter-spacing: normal`. These sizes put the two x-heights level. Give the surrounding line its own line height: about 1.1 for a headline, 1.35 for a sentence. Spaces between set words stay in the surrounding font: the pixel font's space is far too wide. Lines may break between words but never inside one (`white-space: nowrap` on each word).

## Colour

Set letters are always the full text colour (white on dark, black on light), and never an accent colour.

- **Headline on its own:** one colour throughout.
- **Inside a sentence:** the rest of the sentence drops to a soft grey, about 65% opacity of the text colour. Next to full-strength plain text the mixed letters blur into it and the line becomes hard to read; much below 60% the sentence looks washed out.

## Implementation (React, plain CSS)

```tsx
// "st[a]rt[u]ps": bracketed letters render italic, the rest pixel.
export function TavilyText({ text }: { text: string }) {
  return (
    <span className="tavily-text">
      {text.split(' ').map((word, w) => (
        <span key={w}>
          {w > 0 && ' '}
          <span className="tavily-word">
            {word.split(/(\[[^\]]+\])/).filter(Boolean).map((part, i) =>
              part.startsWith('[')
                ? <span key={i} className="tavily-italic">{part.slice(1, -1)}</span>
                : <span key={i} className="tavily-pixel">{part}</span>
            )}
          </span>
        </span>
      ))}
    </span>
  );
}
```

```css
@font-face { font-family: "Geist Pixel Square"; src: url("/fonts/GeistPixel-Square.woff2") format("woff2"); font-display: swap; }
.tavily-text { letter-spacing: normal; color: #fff; }
.tavily-word { white-space: nowrap; }
.tavily-pixel { font-family: "Geist Pixel Square", monospace; font-weight: 400; font-size: 1.1em; line-height: 1; -webkit-text-stroke: 0.03em currentColor; }
.tavily-italic { font-family: Newsreader, Georgia, serif; font-style: italic; font-weight: 400; font-size: 1.2em; line-height: 1; }
```

Usage, inside a sentence whose colour is `rgb(255 255 255 / 0.65)`: `I help <TavilyText text="st[a]rt[u]ps" /> and <TavilyText text="[e]ngin[ee]ring t[ea]ms" /> work smarter with <TavilyText text="co[d]ing [a]ge[n]ts" />.` Set `.tavily-text`'s colour to the full text colour of your theme. Outside React, write the same spans by hand.

## Check by looking

Screenshot at 2x device scale on desktop and at 390px wide. Confirm the pixel letters are crisp and as tall as the italic x-height, no gap opens between set words, and every set word still reads at a glance.

## Common mistakes

| Mistake | Fix |
| --- | --- |
| Whole words in one face ("*coding* agents") | Swap inside each word |
| Pixel letters look thin or tiny next to the italic | Use the stroke and the 1.1em / 1.2em sizes; set the line at 28px or more |
| Wide gap between set words | Put spaces outside the pixel spans |
| Accent colour on the set words | Full text colour only |
| Sentence hard to read, set words lost | Drop the rest of the sentence to about 65% |
| Substitute pixel font or soft italic | Geist Pixel Square and Newsreader Italic only |
