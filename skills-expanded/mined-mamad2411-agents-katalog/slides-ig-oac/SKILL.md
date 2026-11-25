---
name: slides-ig-oac
description: "Create high-converting 10-slide Instagram carousel posts for OAC Digital. Covers any digital marketing topic: websites, social media, customer service, lead generation, recurring customers, AI tools, and digital presence. Includes topic research, hook writing, slide copy generation, AI cover image creation using generate_image, and outputting a downloadable HTML slide deck with OAC branding."
risk: safe
---

# slides-ig-oac

## Overview

This skill creates a complete, ready-to-post Instagram carousel (10 slides, 1080x1080px) for **OAC Digital**. It handles everything from topic research to HTML output with a one-click download button — and **always ends with a high-converting Instagram caption including Miami-local hashtags**. Each carousel is designed to educate local business owners, drive saves/shares, and funnel toward OAC Digital services.

---

## Branding Specifications

| Token | Value |
|---|---|
| Primary font | `Playfair Display` (headings) |
| Body font | `Roboto` |
| Background dark | `#121212` (oac-black) |
| Accent gold | `hsl(40, 90%, 55%)` (oac-gold) |
| Background light | `#F8F9FA` (oac-lightGray) |
| Logo (ALL slides) | `./oac-logo-black.png` — ALWAYS this single file, on every slide |
| Logo background | None needed — the PNG has a transparent background, use it as-is |
| CTA | "Local Launch — Ready in 4 Hours 🚀 | $497 (One-Time Payment)" |

---

## When to Use This Skill

Use this skill when the user asks to:
- Create a new Instagram carousel post for OAC Digital
- Repurpose a topic into a slide format
- Generate a new piece of social content for local business owners
- Make a new Spanish or English educational carousel

---

## Step-by-Step Process

### Step 1 — Research Trending Topics

Use `search_web` to find what's trending in **digital marketing for small businesses** right now. Topics can include **any** of the following — do NOT limit to SEO or Google:
- Websites and digital presence
- Social media content and posting strategy
- Customer service and how businesses respond to clients
- Lead generation and why leads drop off
- Recurring customers and customer retention
- AI tools for marketing automation
- Email marketing and follow-ups
- Online reputation and reviews
- Paid ads (Meta, Google, TikTok)
- Pain points of small/local business owners

Search query example:
```
digital marketing tips small businesses 2026 leads customers social media website presence
```

### Step 2 — Recommend 3 Topic Options

Based on research, present the user with **3 topic options**, each including:
- **Topic title**
- **Hook** (the first-slide attention-grabbing headline)
- **Angle** (the educational thread through the carousel)
- **Why it works** (the psychology/reason it will perform)

> ⚠️ Always wait for user approval before moving to Step 3. Hook angles must create curiosity — use "what they don't want you to know", "why you're losing", "the secret behind", "what your competitors hide" style framing.

### Step 3 — Get Hook Approval

Once a topic is chosen:
1. Write **5 alternative hook variations** for the cover slide (Slide 1).
2. Each hook must be designed to stop the scroll in under 3 seconds.
3. Use these psychological triggers: **FOMO, curiosity gap, insider secret, direct challenge, painful truth**.
4. Wait for user to pick a hook before building slides.

**Hook formula examples:**
- `"The #1 [X] your competitors are using to [win outcome] — it's not what you think."`
- `"Why [competitor/top business] gets [X result] and you get [bad result]. (Hint: it's not [obvious answer])"`
- `"[Shocking stat/claim]. And fixing it takes [short time]."`

### Step 4 — Generate All AI Images (Nano Banana / generate_image)

Use the `generate_image` tool to generate **5 images in parallel** — all at the same time for speed.

**Images to generate:**
| File | Slide | Content |
|---|---|---|
| `carousel-cover.png` | 1 | Cinematic full-bleed hook image with text overlay |
| `carousel-slide3.png` | 3 | Dramatic image proving the data point visually |
| `carousel-slide5.png` | 5 | Real-world scene illustrating the "rule" |
| `carousel-slide7.png` | 7 | Abstract/tech visual for the deep-dive insight |
| `carousel-slide10.png` | 10 | Premium OAC Digital brand outro (logo + icons aesthetic) |

**Slide 1 cover prompt template:**
```
A stunning, ultra high-impact 1:1 square Instagram carousel cover (1080x1080px).
Dark premium background (near-black #0a0a0a) with electric gold (#F5A623) accents.
[Thematic visual — e.g. city at night with Google Maps pins, smartphone battle, data streams].
Large bold white text overlaid: "[HOOK]" with the power word in electric gold.
Bottom left: subtle OAC DIGITAL logo. Cinematic, premium — like a movie poster.
Font: bold sans-serif. Colors: near-black, electric gold, white.
```

**Middle slides (3, 5, 7) prompt style:** Real-world or abstract visuals, NO text overlaid — the text is added in HTML. Dark/cinematic tone. Must feel editorial and high-end.

**Slide 10 prompt style:** Clean black background, OAC DIGITAL wordmark in gold neon glow, three icons (bookmark, share, person+). Premium luxury brand aesthetic.

**After generation, copy ALL images at once:**
```bash
cp "/path/to/slide1.png" "/Users/othmarcasilla/oac-digital-website/public/images/carousel-cover.png"
cp "/path/to/slide3.png" "/Users/othmarcasilla/oac-digital-website/public/images/carousel-slide3.png"
cp "/path/to/slide5.png" "/Users/othmarcasilla/oac-digital-website/public/images/carousel-slide5.png"
cp "/path/to/slide7.png" "/Users/othmarcasilla/oac-digital-website/public/images/carousel-slide7.png"
cp "/path/to/slide10.png" "/Users/othmarcasilla/oac-digital-website/public/images/carousel-slide10.png"
```

### Step 5 — Write 10-Slide Content

**Standard carousel structure (Hybrid: Text + AI Image slides):**

| Slide | Format | Type | Purpose |
|---|---|---|---|
| 1 | 🖼️ AI Image | **Cover Hook** | Full-bleed cinematic image — stop the scroll in 3 seconds |
| 2 | 📄 Text | **Concept Reveal** | Subvert expectations, introduce the real insight |
| 3 | 🖼️ AI Image Overlay | **Data/Proof** | Striking image + bold text: the visual "wow" that proves the problem |
| 4 | 📄 Text | **Gold Explainer** | WHY this works (psychology or mechanism). Gold gradient bg. |
| 5 | 🖼️ AI Image Overlay | **The Rule** | Memorable named rule on top of a real-world image |
| 6 | 📄 Text | **Dark List** | 3 actionable tactics (numbered gold circles on dark bg) |
| 7 | 🖼️ AI Image Overlay | **Deep Dive** | Visual reinforcement of one specific tactic with overlay text |
| 8 | 📄 Text | **Gold Secret Reveal** | "Your competitors don't have a bigger budget — they have a system." |
| 9 | 📄 Text | **Dark Motivator** | Quote + emotional push. "Consistency is the unfair advantage." |
| 10 | 🖼️ AI Image | **Follow CTA** | Generic branded outro — Follow / Save / Share. NO price. |

> ⚠️ **Slide 10 is NEVER a sales/price slide.** It is always a brand awareness + engagement CTA: follow, save, share. The offer can live in Slide 8 or 9 at most as a soft mention.

**Text slide background rotation:**
- Dark slides (2, 6, 9): `bg-oac-black` with `text-oac-white`
- Light slides: `bg-oac-white` with `text-oac-black`
- Special: `bg-gold-gradient` for Slide 4 and 8

### Step 6 — Build the HTML File

Output the completed carousel to:
```
/Users/othmarcasilla/oac-digital-website/carousel-preview.html
```

**Key HTML requirements:**
- Slides are `1080px × 1080px` divs
- Scaled down with `.slide-view-wrapper { transform: scale(0.5); margin-bottom: -540px; }`
- **Image slides** use inline `style="background-image: url('./public/images/[filename].png'); background-size: cover;"` on the slide div
- **Text slides** use Tailwind bg classes (`bg-oac-black`, `bg-oac-white`, `bg-gold-gradient`)
- All slides show OAC logo (light logo on dark slides, dark logo on light slides)
- Include `html2canvas` + `FileSaver.js` CDN links

#### AI Image Overlay Slide Template
```html
<div id="slide-3" class="slide" style="background-image: url('./public/images/carousel-slide3.png'); background-size: cover; background-position: center;">
    <!-- Dark gradient: transparent top → dark bottom for text readability -->
    <div class="absolute inset-0" style="background: linear-gradient(to top, rgba(0,0,0,0.92) 45%, rgba(0,0,0,0.1) 100%);"></div>
    <!-- OAC Logo top left -->
    <div class="absolute top-12 left-24 z-10">
        <img src="./public/images/logo-light.png" alt="OAC Digital" class="h-10 opacity-80">
    </div>
    <!-- Bold text at the bottom (like the Instagram examples shown) -->
    <div class="absolute bottom-0 left-0 right-0 p-20 z-10">
        <!-- Optional gold pill label -->
        <div class="inline-block mb-6" style="background: hsl(40,90%,55%); padding: 6px 24px; border-radius: 999px;">
            <span class="font-sans font-black text-black text-3xl uppercase tracking-widest">Label Here</span>
        </div>
        <h2 class="font-sans text-6xl font-black text-white leading-tight uppercase">
            BOLD STATEMENT HERE IN CAPS.
        </h2>
        <p class="font-sans text-3xl text-white/80 mt-4 font-medium">Supporting detail or stat.</p>
    </div>
</div>
```

#### Slide 10 — Follow CTA Template (ALWAYS use this, never a price slide)
```html
<div id="slide-10" class="slide" style="background-image: url('./public/images/carousel-slide10.png'); background-size: cover; background-position: center;">
    <div class="absolute inset-0" style="background: rgba(0,0,0,0.45);"></div>
    <div class="absolute inset-0 flex flex-col items-center justify-end pb-24 px-20 z-10">
        <h2 class="font-sans text-6xl font-black text-white text-center leading-tight uppercase mb-8">
            If You Found This Valuable,<br>You'll Love What Comes Next.
        </h2>
        <p class="font-sans text-4xl text-white/85 text-center leading-relaxed max-w-3xl mb-12">
            Follow <span style="color: hsl(40,90%,55%); font-weight: 800;">@oacdigital</span> for weekly tips on SEO, Google, and digital marketing.
        </p>
        <!-- Save / Share / Follow icons -->
        <div class="flex gap-10 items-center">... SVG icons ...</div>
    </div>
</div>
```

**Download function — CRITICAL: re-apply background-image on clones for image slides:**
```javascript
async function downloadAllSlides() {
    const status = document.getElementById('statusIndicator');
    const btn = document.getElementById('downloadBtn');
    btn.disabled = true;
    status.style.opacity = '1';
    await document.fonts.ready;
    await new Promise(r => setTimeout(r, 500));
    const offScreen = document.createElement('div');
    offScreen.style.cssText = 'position:absolute;top:-9999px;left:-9999px;';
    document.body.appendChild(offScreen);
    // Image slide numbers — must re-apply bg-image inline on clone
    const imageSlideBgs = {
        1: "url('./public/images/carousel-cover.png')",
        3: "url('./public/images/carousel-slide3.png')",
        5: "url('./public/images/carousel-slide5.png')",
        7: "url('./public/images/carousel-slide7.png')",
        10: "url('./public/images/carousel-slide10.png')"
    };
    for (let i = 1; i <= 10; i++) {
        const clone = document.getElementById('slide-' + i).cloneNode(true);
        if (imageSlideBgs[i]) {
            clone.style.backgroundImage = imageSlideBgs[i];
            clone.style.backgroundSize = 'cover';
            clone.style.backgroundPosition = 'center';
        }
        offScreen.appendChild(clone);
        await new Promise(r => setTimeout(r, 200));
        const canvas = await html2canvas(clone, { scale: 1, useCORS: true, allowTaint: true, backgroundColor: null });
        offScreen.removeChild(clone);
        canvas.toBlob(blob => saveAs(blob, `OAC-Slide-${i}.png`), 'image/png');
    }
    document.body.removeChild(offScreen);
}
```

**Image files naming convention:**
```
public/images/carousel-cover.png    ← Slide 1
public/images/carousel-slide3.png   ← Slide 3
public/images/carousel-slide5.png   ← Slide 5
public/images/carousel-slide7.png   ← Slide 7
public/images/carousel-slide10.png  ← Slide 10
```

### Step 7 — Verify and Deliver

1. Confirm the local server is running:
   ```bash
   curl -s -o /dev/null -w "%{http_code}" http://localhost:8081/carousel-preview.html
   ```
   If not running, start it:
   ```bash
   python3 -m http.server 8081
   ```
   (run from `/Users/othmarcasilla/oac-digital-website`)

2. Tell the user to open: **http://localhost:8081/carousel-preview.html**
3. Confirm the gold **"Download All 10 Slides"** button works.

### Step 8 — Write the Caption (MANDATORY — Always Do This)

**The caption is NOT optional.** Every carousel must be delivered with a complete, high-converting, SEO-optimized Instagram caption. Do not wait for the user to ask.

#### Caption Structure

```
[LINE 1 — THE HOOK]
Mirror the Slide 1 hook word-for-word. This is the only line visible before "More".
Must create immediate curiosity or FOMO. Maximum 1 sentence. No hashtags here.

[BODY — THE STORY / VALUE]
Deliver the 3 core insights from the carousel in plain, punchy language.
Use emojis as bullet markers (❌ for pain, ✅ for solution, 🔑 for key insight).
Each point should be 1-2 lines max. No fluff. Speak directly to the local business owner.

[THE BRIDGE — OAC POSITION]
1 short paragraph that:
- Validates the problem ("Most agencies charge $2K+ for this...")
- Introduces OAC as the fast, affordable solution
- Highlights the 4-hour delivery and $497 one-time price

[CTA — CALL TO ACTION]
Always use TWO CTAs for maximum conversion:
1. Micro-CTA: "Comment 'LAUNCH' below" (drives comments → boosts algorithm reach)
2. Macro-CTA: "Click the link in our bio" (drives traffic → drives sales)

[HASHTAGS — SEO BLOCK]
Always include the full hashtag block at the bottom (see below).
```

#### Permanent Hashtag Bank (Always Include)

Use **20–30 hashtags** mixing:
- **OAC brand:** `#OACDigital #OACDigitalInnovations`
- **Core topic:** `#LocalSEO #GoogleBusiness #GoogleMaps #DigitalMarketing #SEO2026`
- **Audience:** `#SmallBusiness #SmallBusinessOwner #BusinessGrowth #LocalBusiness #Entrepreneur`
- **Miami-specific (ALWAYS include at least 5):** `#Miami #MiamiSmallBusiness #MiamiEntrepreneur #SouthFlorida #MiamiBusiness #305 #MiamiMarketing #MiamiBusiness`
- **Topic-specific:** Swap 3–5 based on the carousel topic (e.g. `#GooglePhotos #MapPack #ReviewMarketing #LocalMarketing`)

**Example full hashtag block:**
```
#OACDigital #LocalSEO #GoogleBusiness #GoogleMaps #SmallBusiness #SmallBusinessOwner
#DigitalMarketing #BusinessGrowth #LocalBusiness #Entrepreneur #SEO2026
#Miami #MiamiSmallBusiness #MiamiEntrepreneur #SouthFlorida #MiamiBusiness #305
#MiamiMarketing #OnlinePresence #MarketingTips #LocalMarketing #GoogleMyBusiness
```

#### Caption Quality Rules
- **First line must hook** in under 3 seconds — test it by reading it out loud.
- **Use short paragraphs.** Never more than 3 lines per block before a line break.
- **Avoid agency jargon.** Write like you're texting a friendly business owner.
- **Always mention Miami** at least once in the body text (builds geo-relevance for local discovery).
- **Save-worthy content**: End the body with a line like "Save this post — you'll need it."

---

## Language Support

- **English:** Default. Use direct, punchy language. American business tone.
- **Spanish:** When user requests. Use neutral Latin American Spanish. Keep all metrics/prices in English numerals.

---

## Files & Paths Reference

| Item | Path |
|---|---|
| Carousel HTML | `/Users/othmarcasilla/oac-digital-website/carousel-preview.html` |
| Cover image (generated) | `/Users/othmarcasilla/oac-digital-website/public/images/carousel-cover.png` |
| Light logo | `/Users/othmarcasilla/oac-digital-website/public/images/logo-light.png` |
| Dark logo | `/Users/othmarcasilla/oac-digital-website/oac-logo-black.png` |
| Local preview server | `http://localhost:8081/carousel-preview.html` |
