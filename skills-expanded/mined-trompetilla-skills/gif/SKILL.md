---
name: GIF
description: Find, search, and create GIFs with proper optimization and accessibility.
metadata: {"clawdbot":{"emoji":"🎞️","requires":{},"os":["linux","darwin","win32"]}}
---

## Where to Find GIFs

| Site | Best for | API |
|------|----------|-----|
| **Giphy** | General, trending | Yes |
| **Tenor** | Messaging apps (WhatsApp, Slack, Discord) | Yes |
| **Imgur** | Viral/community content | Yes |
| **Reddit r/gifs** | Niche, unique | No |
| **Reaction GIFs** | Emotions | No |

## Giphy API

```bash
# Search
curl "https://api.giphy.com/v1/gifs/search?api_key=KEY&q=thumbs+up&limit=10"

# Trending
curl "https://api.giphy.com/v1/gifs/trending?api_key=KEY&limit=10"
```

Response sizes: `original`, `downsized`, `fixed_width`, `preview`—use `downsized` for chat.

## Tenor API

```bash
curl "https://tenor.googleapis.com/v2/search?key=KEY&q=thumbs+up&limit=10"
```

Returns: `gif`, `mediumgif`, `tinygif`, `mp4`, `webm`—use `tinygif` or `mp4` for performance.

## Creating GIFs with FFmpeg

**Always use palettegen (without it, colors look washed out):**
```bash
ffmpeg -ss 0 -t 5 -i input.mp4 \
  -filter_complex "fps=10,scale=480:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse" \
  output.gif
```

| Setting | Value | Why |
|---------|-------|-----|
| fps | 8-12 | Higher = much larger file |
| scale | 320-480 | 1080p GIFs are massive |
| lanczos | Always | Best scaling quality |

## Post-Optimization

```bash
gifsicle -O3 --lossy=80 --colors 128 input.gif -o output.gif
```

Reduces size 30-50% with minimal quality loss.

## Video Alternative

For web, use video instead of large GIFs (80-90% smaller):

```html
<video autoplay muted loop playsinline>
  <source src="animation.webm" type="video/webm">
  <source src="animation.mp4" type="video/mp4">
</video>
```

## Accessibility

- **WCAG 2.2.2:** Loops >5s need pause control
- **prefers-reduced-motion:** Show static image instead
- **Alt text:** Describe the action ("Cat jumping off table"), not "GIF"
- **Three flashes:** Nothing >3 flashes/second (seizure risk)

## Common Mistakes

- No `palettegen` in FFmpeg—colors look terrible
- FPS >15—file size explodes for no visual benefit
- No lazy loading on web—blocks page load
- Using huge GIF where video would work—10x larger
