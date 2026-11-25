---
name: frontend-design
description: Distinctive visual design for any UI: principles, a subject-first process, and a gallery of 216 directions to pick by category (67 style archetypes, 86 brand systems, 25 original web systems, 38 app references) plus a library map for charts, motion, 3D and UX. Use before building or restyling any page, app or demo.
requires: browser, services, playwright, ImageView
---
# Frontend Design

This skill has three parts. **Principles** (below) say how to design; the **gallery** gives you a
concrete direction to commit to, so two projects never come out looking alike; the **library map**
(`references/libraries.md`) names what to reach for when a page needs charts, motion, 3D or
interaction. Files are under this skill's directory (the Skill tool prints the absolute path);
read a gallery entry with `Read` before you build.

## Choosing a direction (do this first, every project)

1. **Name the subject, the audience and the job** of the thing you are designing. One sentence.
2. **Pick a category** from the gallery, then read two or three candidate entries and choose one.
   Choose by the subject, audience and job of step 1: a direction that fits this subject is what
   keeps one project from looking like the last. Reading the entry is mandatory: the index line is
   a scent, the file is the brief.
   - `styles/` are archetypes (brutalism, editorial, glassmorphism…): fastest way to a strong,
     coherent look for a new product.
   - `brands/` are analyses of real design systems (tokens, type, components, do/don't): use one
     as a *reference*, never as a copy of the brand; borrow the logic, change the identity.
   - `systems/` are complete original web systems with a demo page whose CSS you can read.
   - `apps/` describe product UIs (feeds, finance, messaging…): the reference for app screens,
     dashboards and mobile layouts rather than marketing pages.
3. **Write the brief** in the project (a `DESIGN.md`: palette, type scale, spacing, radius, motion,
   the one hero idea, what is forbidden). Everything you build must trace back to it.
4. **Make it live where it matters**: pick libraries from `references/libraries.md` for the parts
   that need data, motion or interaction. Purposeful, one orchestrated moment, reduced-motion
   respected. Not a carousel of effects.
5. **Verify with eyes**: serve it (`ServiceStart`), take screenshots at 390 and 1440 with a
   Playwright script run as `python3 shoot.py` (Playwright and its Chromium are installed for the
   shell's `python3`: never `uv add` or `playwright install` them; `Skill("webapp-testing")` has
   the patterns), and look at each with `ImageView`. Your own browser is loaded with this skill:
   `BrowserOpen` the service's address, `BrowserLogs` for console errors, `BrowserLook` for a
   question about the live page. Then the `no-ai-design-slop` gate. Fix what you see before you
   report.

Domain-specific guidance (product UI vs marketing pages, dashboards, admin panels):
`references/principles-by-domain.md`, `references/app-ui.md`, `references/marketing-pages.md`.
Motion-led cinematic sites: `references/motion-led-sites.md`. Dark glass: `references/glass-dark-ui.md`.

## Principles

Approach this as the design lead at a design studio known for giving every client a distinct visual identity that is not mistaken for anyone else's. This client has already rejected proposals that felt cliché or templated, and is paying for a distinctive point of view: make deliberate, opinionated choices about palette, typography, and layout that are specific to this brief, and take aesthetic risk if justified.

## Ground your designs in the subject matter

If the brief does not identify what the product or subject matter is, identify it yourself before designing, and confirm with the client. You can come up with one concrete subject, the design's audience, and the design's primary job, as a proposal. If there's any information in your memory about the client's preferences or context about what they're building, use that as a hint. The subject's industry, subject matter, materials, and vernacular are where distinctive visual choices come from — a design for a toy for girls aged 8–11 will be very aesthetically different from a dashboard for financial analysts. Build with the brief's real content and subject matter throughout.

## Design principles

For web designs, the hero is the first thing viewers will see. Open with the most characteristic thing in the subject's world, in the form that is most appropriate: a headline, an image, an animation, a live demo, an interactive moment, or other treatments. Be deliberate with your choice: a big number with a small label, supporting stats, and a gradient accent is the default treatment, so only use it if that's truly the best option.

Typography carries the personality of the page. You don't need a different typeface for display or headline text and body content: use one family or two, and if two, make them clearly distinct.

Choose your typefaces deliberately, not the default families you would reach for on any other project, and set a clear type scale following the default guidance of The Elements of Typographic Style with intentional weights, widths, and spacing. When type is used as a headline or visual element, use the type treatment itself as an active part of the design, not a neutral delivery vehicle for the content.

Default to line lengths of less than 80 characters. Serif typefaces can have slightly longer line lengths; give serif body text slightly more line-height than a sans-serif.

Avoid these default typographic treatments; they are the commonest tells of a generated page:
- Accenting just a single word or phrase in a headline, like putting one word in italic/bold or a different color.
- Using all caps for labels.
- Adding unnecessary typographic labels above content.

Visual structure is information. Structural devices like outlines, borders, numbering, eyebrows, dividers, labels, etc., encode useful information about the content rather than decorate it. Many generic designs use numbered markers (01 / 02 / 03), but that's only appropriate if the content actually is a sequence — like a stepped process or a timeline. Before adding numbered markers, check the content really is a sequence.

Use non-user-triggered motion sparingly and deliberately, only to draw attention. A single orchestrated moment — one page-load sequence or one reveal — lands better than scattered effects; fade-and-slide-up entrances on each section and hover transitions on every card are the generic default and read as AI-generated. Motion that answers a person's action (opening, expanding, confirming) is welcome when it shows what changed.

Consider written content carefully. Often a design brief may not contain real content, and it's up to you to come up with copy and placeholder content. Copy can make a design feel as templated as the design itself. See the below section on writing for more guidance.

## Process: plan, review against the brief, build, critique

For calibration, AI-generated design right now clusters around some traits:
1. a warm cream background (near #F4F1EA) with a high-contrast serif display and a terracotta or warm-clay accent (often near #D97757 — Anthropic's own Claude-interaction accent, so on a user's brief it reads as a tell);
2. a near-black background with a single bright acid-green or vermilion accent;
3. a broadsheet-style layout with hairline rules, zero border-radius, and dense newspaper-like columns;
4. the SaaS-card kit: content chopped into identical rounded cards, one border-radius on everything regardless of hierarchy, the same soft grey shadow (rgba(0,0,0,.1)) under each, and gradient washes as decoration;
5. template chrome that appears whatever the subject: a tracked-out ALL-CAPS eyebrow label above every heading; meta strings joined with middle dots ('A · B · C'); labels built as 'WORD — fragment' with a spaced em dash; tinted near-black (#0B0B0B, #111) standing in for black; a monospace face for small data labels; a '→' appended to link and button text.

All traits are legitimate for some briefs, but they are defaults rather than choices, and they appear regardless of subject. Where the brief pins down a visual direction, follow it exactly — the brief's own words always win, including when it asks for one of these looks. Where it leaves an axis free, don't spend that freedom on one of these defaults. As with a hired human designer, there's often a careful balance between doing what you're good at and taking each project as a chance to experiment and learn.

Work in two passes. First, brainstorm a short design plan based on the client's design brief: create a compact token system with color, type, layout, and principles.
- Color: describe the core base palette as 4–6 named hex values.
- Type: the typefaces and their roles.
- Layout: a layout concept, using one-sentence prose descriptions and ASCII wireframes to ideate and compare. Include alignment guidance; should the content be left aligned, center aligned, justified?
- Principles: the high-level guidance for what makes this page unique.

Then review that plan against the brief before building: if any part of it reads like the generic default you would produce for any similar page (work through a similar prompt to see if you arrive somewhere similar) rather than a choice made for this specific brief — revise that part, say what you changed and why. Only after you've confirmed the relative uniqueness of your design plan should you start to write the code, following the revised plan.

When writing the code, be careful of structuring your CSS selector specificities. It's easy to generate CSS classes that cancel each other out (especially with a type-based selector like .section and an element-based selector like .cta). This can happen often with padding/margin between sections.

## Restraint and self-critique

Spend your boldness in one place. Let one element be the memorable thing, keep everything around it quiet and disciplined, and cut any decoration that does not serve the brief. Build to a quality floor without announcing it: responsive down to mobile, visible keyboard focus, reduced motion respected, visually accessible, harmonious color palettes. Critique your own work as you build, taking screenshots to review if your environment supports it — a picture is worth 1000 tokens. Consider Chanel's advice: before leaving the house, take a look in the mirror and remove one accessory. Human creatives have memory and always try to do something new, so if you have a space to quickly jot down notes about what you've tried, it can help you in future passes.

## More on writing in design

Words appear in a design for one reason: to make it easier to understand and use. They are design content, not decoration. Bring the same intentionality and minimalism to copywriting that you would bring to spacing and color. Before writing anything, ask what the design needs to say, and how it can best be said to help the person navigate the experience.

Write from the end user's perspective. Name things by what users will understand in simple language, not by how the system is built. A user manages notifications, not webhook config. Describe what something is or does in plain terms rather than selling it. Being specific and legible to new users is always better than being clever.

Use active voice as default. A CTA says exactly what happens when it is used: "Save changes," not "Submit." An action keeps the same name through the whole flow, so the button that says "Publish" produces a toast that says "Published." The vocabulary of an interface is the signposting for someone navigating the product. Cohesion and consistency are how people learn their way around.

Treat failure and emptiness as moments for direction, not mood. Explain what went wrong and how to fix it, in the interface's voice rather than a person's. Errors don't apologize, and they are never vague about what happened. An empty screen is an invitation to act.

Keep the tone conversational: plain verbs, sentence case, no filler, with tone matched to the brand and the audience. Let each written element do exactly one job.

## Gallery

### Style archetypes (`styles/`, 67)

| entry | what it is |
|---|---|
| `styles/agentic.md` | Conversational AI-first interface with minimal controls, clear outcomes, and delegated task flows for agentic workflows. |
| `styles/ant.md` | Structured, enterprise-focused design system emphasizing clarity, consistency, and efficiency for data-dense web applications. |
| `styles/artistic.md` | High-contrast, expressive style with creative typography and bold color choices for visually striking interfaces. |
| `styles/basic.md` | Print-inspired visual language for books, magazines, and reports with editorial grids and expressive typography. |
| `styles/bento.md` | Modular grid layout with card-like blocks, clear hierarchy, soft spacing, and subtle visual contrast for organized, scannable interfaces. |
| `styles/bold.md` | Strong visual presence with heavyweight typography, high-contrast colors, and commanding layouts. |
| `styles/brutalism.md` | Raw, anti-design aesthetic inspired by concrete architecture with unadorned elements, jarring layouts, and functional minimalism. |
| `styles/cafe.md` | Cozy cafe-inspired interface with warm tones, soft typography, and clean layouts for a relaxed browsing experience. |
| `styles/claude.md` | A research-journal aesthetic printed on warm stone — authoritative, editorial, almost achromatic. Pages live on warm ivory parchment (never pure white), with near-black slate as the dominant ink. |
| `styles/claymorphism.md` | Soft, rounded 3D-like shapes mimicking malleable clay with playful, puffy elements and colorful surfaces. |
| `styles/clean.md` | Simplicity-focused design with ample whitespace, legible typography, and a limited color palette to reduce visual clutter. |
| `styles/codex.md` | A radically minimal, blank-canvas interface built as a pure edge-to-edge surface, with almost no color and typography carrying the visual weight. Black serves as the only filled color, the only divider, and the sole surface tone cards. |
| `styles/colorful.md` | Vibrant, high-contrast palettes and gradients for engaging, memorable, and modern user experiences. |
| `styles/contemporary.md` | Current-era minimalist design with bento grids, dark mode support, and high-performance accessible layouts. |
| `styles/corporate.md` | Professional, brand-aligned design with structured grids, minimalist layouts, and consistent enterprise patterns. |
| `styles/cosmic.md` | Futuristic sci-fi aesthetic with dark themes, vibrant neon accents, and immersive spatial elements. |
| `styles/creative.md` | Playful, character-driven design with expressive typography and bold graphics for landing pages and creative projects. |
| `styles/dithered.md` | Dot-pattern rendering technique that simulates shades with a limited palette for nostalgic, retro, high-contrast visuals. |
| `styles/doodle.md` | Hand-drawn, sketch-like style with doodles, handwritten fonts, and imperfect lines for a playful, informal feel. |
| `styles/dramatic.md` | High-contrast, theatrical design with bold layouts, immersive visuals, and unconventional compositions that command attention. |
| `styles/editorial.md` | Magazine-inspired editorial layout with refined serif typography, structured grids, and elegant reading experiences. |
| `styles/enterprise.md` | Dark-themed cloud-platform aesthetic with modular grids, glass-like panels, and strong data hierarchy for productivity dashboards. |
| `styles/expressive.md` | Vibrant, personality-driven design with bold colors, playful graphics, and dynamic layouts that balance creativity with structure. |
| `styles/fantasy.md` | Game-inspired fantasy aesthetic with bold, premium visuals, rich color palettes, and immersive thematic elements. |
| `styles/fiction.md` | A playful, energetic, cartoonesque interface inspired by friendly children's-book illustrations — warm cream backgrounds, big bold custom display typography, saturated brand color blocks, thick black outlines, generously rounded shapes |
| `styles/flat.md` | Two-dimensional minimalist style with vibrant colors, clean typography, and no 3D effects for fast, user-friendly interfaces. |
| `styles/friendly.md` | Approachable, intuitive design with rounded elements, ample whitespace, and soft pastel color palettes. |
| `styles/futuristic.md` | Forward-looking design with tech-inspired typography, modern layouts, and a sleek, innovation-driven aesthetic. |
| `styles/geometric.md` | Geometric, structured design with clean typography, neutral colors, precise shapes, and intuitive layouts that stay out of the way. |
| `styles/glassmorphism.md` | Frosted glass effect with translucent layers, subtle blur, and luminous borders for depth and modern elegance. |
| `styles/gradient.md` | Smooth color transitions and gradient-rich surfaces for modern, playful interfaces with visual depth. |
| `styles/immersive.md` | An immersive, interactive, exhibit-style interface that blends storytelling, animation, and gamified elements to create a playful, experience-driven journey. The entire app sits on a single continuous brand-colored canvas (deep green) |
| `styles/impeccable.md` | A modern, graphic, editorial-poster aesthetic — warm and confident — built on alternating cream and burnt orange sections, an amber brand color. |
| `styles/levels.md` | Conversion-focused design that removes friction and guides users toward action through clarity, trust, and speed. |
| `styles/lingo.md` | Playful, minimal design with bright colors, rounded shapes, tactile 3D borders, and friendly illustrations for approachable interfaces. |
| `styles/material.md` | Google's Material Design with layered surfaces, dynamic theming, built-in motion, and responsive cross-platform patterns. |
| `styles/matrix.md` | A cyber-slick, dark-only Matrix-inspired interface defined by minimalist fashion, high-tech digital elements |
| `styles/minimal.md` | Stripped-back design emphasizing whitespace, clean typography, and restrained color for maximum clarity and focus. |
| `styles/modern.md` | Contemporary editorial style with serif typography, minimal palettes, and clean layouts for polished digital products. |
| `styles/mono.md` | Monospace-driven, matrix-inspired design with high-contrast elements, compact density, and a hacker-chic aesthetic. |
| `styles/neobrutalism.md` | Modern take on brutalism with bold borders, vivid accent colors, and raw, high-contrast layouts on warm surfaces. |
| `styles/neon.md` | Electric neon glow effects with high-contrast color pairings for bold, attention-grabbing interfaces. |
| `styles/neumorphism.md` | Soft, extruded UI elements with inner and outer shadows on monochromatic surfaces for a tactile, embedded look. |
| `styles/pacman.md` | Retro arcade-inspired design with pixel fonts, dotted borders, playful high-contrast colors, and 8-bit game aesthetics. |
| `styles/paper.md` | Paper-textured, print-inspired design with minimal colors, clean serif/sans typography, and tactile surface qualities. |
| `styles/perspective.md` | Spatial depth design with isometric views, vanishing points, and layered elements that guide attention through 3D-like realism. |
| `styles/power.md` | High-end dark aesthetic with bold headings, monochromatic palette, and premium feel for premium brand experiences. |
| `styles/premium.md` | Apple-inspired premium aesthetic with precise spacing, modern typography, and a refined, polished visual language. |
| `styles/professional.md` | Polished, business-ready design with modern typography, structured layouts, and a trustworthy visual identity. |
| `styles/pulse.md` | Dynamic, vibrant style with thick borders, geometric shapes, high-contrast colors, and expressive typography conveying motion and vitality. |
| `styles/refined.md` | Carefully curated, modern minimal style with elegant serif typography and understated, sophisticated palettes. |
| `styles/retro.md` | Throwback design with vintage-inspired typography, high-contrast retro palettes, and nostalgic visual elements. |
| `styles/riso.md` | A playful, joyful, two-color risograph print aesthetic built on a single warm off-white paper surface running through every section |
| `styles/roku.md` | App dashboard with purple-themed aesthetic, top-bar navigation, card-based layouts, and developer-first workflows. |
| `styles/sega.md` | A playful, arcade-inspired interface for games — built on the VT323 pixel typeface, hard-edged 0px corners, chunky pill buttons that physically press into solid offset blocks |
| `styles/shadcn.md` | Shadcn/ui-inspired design with minimal, clean components, monochrome palette, and utility-first patterns. |
| `styles/sketch.md` | A friendly, hand-drawn sketch interface inspired by pencil illustrations on warm cream paper. Soft teal brand accents, hand-written display headings, rounded pill controls. |
| `styles/skeumorphism.md` | Real-world mimicry with textured surfaces, 3D effects, and familiar physical metaphors for intuitive digital interfaces. |
| `styles/sleek.md` | Modern minimalist aesthetic with clean lines, intentional color palette, subtle interactions, and consistent spacing. |
| `styles/spacious.md` | Generous whitespace, consistent padding, and grid-based layouts for clean, readable, and breathing interfaces. |
| `styles/square.md` | Graceful, refined aesthetic with delicate typography, minimal palettes, and polished layouts that exude sophistication. |
| `styles/stitch.md` | Clean, high-contrast enterprise design for data-driven workflows with intuitive drag-and-drop patterns and structured layouts. |
| `styles/storytelling.md` | Narrative-driven design using visuals, copy, and interaction to guide users through engaging, emotionally resonant journeys. |
| `styles/terracotta.md` | A sun-baked, clay-toned editorial interface built on warm cream surfaces, ink-brown headlines set in a display serif, and a single terracotta accent. |
| `styles/tetris.md` | Classic block-game inspired design with playful colors, bold display fonts, and compact, high-energy layouts. |
| `styles/vibrant.md` | Lively, colorful design with bold playful typography, warm accents, and dynamic visual energy. |
| `styles/vintage.md` | 1950s-1990s nostalgia with skeuomorphic touches, grainy textures, retro color palettes, and pixel-style typography. |

### Brand design systems (`brands/`, 86)

Analyses of real products, grouped by industry; keywords are the mood. Use as a reference for
tokens, hierarchy and component logic, then make the identity your own.

**AI**

| entry | keywords |
|---|---|
| `brands/claude.md` | warm, intellectual, editorial, literary, earthy, trustworthy |
| `brands/cohere.md` | confident, professional, restrained, enterprise, sophisticated |
| `brands/elevenlabs.md` | elegant, restrained, ethereal, premium, airy, audio |
| `brands/minimax.md` | clean, airy, approachable, colorful, product-forward |
| `brands/mistral.ai.md` | warm, bold, maximalist, golden, European, declarative |
| `brands/ollama.md` | minimal, grayscale, soft, approachable, rounded |
| `brands/opencode.ai.md` | terminal, warm, monospace, utilitarian, developer-focused |
| `brands/replicate.md` | bold, playful, energetic, high-contrast, community |
| `brands/runwayml.md` | cinematic, editorial, visual, dark, film |
| `brands/together.ai.md` | soft, airy, optimistic, pastel, light, gradient, pink |
| `brands/x.ai.md` | brutalist, dark, minimal, terminal, engineering, restrained |

**Automotive**

| entry | keywords |
|---|---|
| `brands/bmw.md` | precise, angular, industrial, authoritative, engineered |
| `brands/ferrari.md` | editorial, cinematic, restrained, luxurious, precise, red |
| `brands/lamborghini.md` | dark, theatrical, intimidating, nocturnal, luxurious, gold |
| `brands/renault.md` | vibrant, energized, bold, French, forward-leaning |
| `brands/tesla.md` | minimal, cinematic, restrained, product-forward, clean |

**Backend**

| entry | keywords |
|---|---|
| `brands/clickhouse.md` | aggressive, high-contrast, electrifying, powerful, fast, neon |
| `brands/composio.md` | dark, developer-focused, bioluminescent, minimal, authoritative |
| `brands/hashicorp.md` | enterprise, systematic, authoritative, token-driven, structured |
| `brands/mongodb.md` | dark, organic, editorial, bioluminescent, forest, electric, green |
| `brands/posthog.md` | irreverent, earthy, anti-corporate, playful, warm |
| `brands/sanity.md` | dark, precise, structured, achromatic, disciplined |
| `brands/sentry.md` | dark, vibrant, irreverent, technical, warm-purple |
| `brands/supabase.md` | dark, developer, open-source, sophisticated, terminal, green |
| `brands/voltagent.md` | dark, electric, focused, developer, cockpit, engineering |

**Consumer**

| entry | keywords |
|---|---|
| `brands/airbnb.md` | warm, inviting, tactile, approachable, cozy, marketplace |
| `brands/apple.md` | reductive, precise, cinematic, premium, confident, minimal |
| `brands/baemin.md` | playful, warm, irreverent, appetizing, friendly, cultural, korean, food-delivery |
| `brands/dcard.md` | social, forum, community, material-design, deep-navy, blue, taiwanese, anonymous, youth, magazine-like |
| `brands/ibm.md` | methodical, corporate, precise, engineered, systematic |
| `brands/kakao.md` | warm, friendly, functional, personal, sunshine, yellow, korean, messaging, super-app |
| `brands/karrot.md` | warm, approachable, trustworthy, local, energetic, orange, korean, marketplace |
| `brands/line.md` | green, pill-buttons, editorial, lifestyle, japanese, friendly, oversized-typography |
| `brands/mercari.md` | red, marketplace, japanese, semantic-tokens, dense, commerce, mature |
| `brands/nvidia.md` | industrial, engineering, high-contrast, disciplined, sharp |
| `brands/pinkoi.md` | dense, multi-cultural, marketplace, asian, handcrafted, coral, locale-aware, commerce, bold-headings |
| `brands/pinterest.md` | warm, cozy, craft-like, personal, inviting, handcrafted, red |
| `brands/spacex.md` | cinematic, minimal, aerospace, industrial, immersive |
| `brands/spotify.md` | dark, immersive, content-first, tactile, rounded, green |
| `brands/uber.md` | bold, confident, minimal, efficient, direct, black |
| `brands/naver.md` | pragmatic, neutral, factual, clinical, utility |
| `brands/ohouse.md` | warm, observational, sensory, spatial, aspirational, calm |
| `brands/qanda.md` | warm, encouraging, low-pressure, calm, reassuring, tutor-like |
| `brands/ridi.md` | calm, literate, editorial, low-pressure, bookish, respectful |
| `brands/binance.md` | A confident financial-platform interface anchored on a deep near-black canvas, where Binance's iconic yellow (#FCD535) carries every primary CTA,… |
| `brands/bmw-m.md` | A motorsport-engineering interface anchored on a near-black canvas with white BMW Type Next Latin display headlines in confident UPPERCASE. |
| `brands/bugatti.md` | An austere luxury-automotive interface that uses near-pure black canvas, white uppercase letterspaced display, and full-bleed automotive photography… |
| `brands/playstation.md` | A three-surface marketing system organized around alternating black, white, and PlayStation Blue chapters that scroll past the viewer like a console… |
| `brands/shopify.md` | An inspired interpretation of Shopifi's design language — a cinematic commerce platform that runs two parallel design tracks. |
| `brands/vodafone.md` | An inspired interpretation of Vodafone's design language — a telecom super-brand whose web surface alternates between editorial photography hero… |

**Design Tools**

| entry | keywords |
|---|---|
| `brands/airtable.md` | clean, sophisticated, precise, structured, enterprise |
| `brands/clay.md` | playful, artisanal, quirky, warm, delightful, craft |
| `brands/figma.md` | sophisticated, organic, precise, creative, black-white |
| `brands/framer.md` | cinematic, dark, seductive, precise, product-forward |
| `brands/miro.md` | clean, collaborative, pastel, geometric, visual |
| `brands/webflow.md` | clean, rich, confident, tool-forward, precise, blue |

**Developer**

| entry | keywords |
|---|---|
| `brands/cursor.md` | warm, crafted, typographically-rich, organic, editorial |
| `brands/expo.md` | luminous, airy, monochromatic, premium, friendly, approachable |
| `brands/lovable.md` | warm, approachable, analog, humanist, parchment |
| `brands/raycast.md` | dark, precise, macOS-native, trustworthy, fast, premium |
| `brands/superhuman.md` | luxurious, clean, confident, restrained, premium, lavender |
| `brands/vercel.md` | restrained, compressed, engineered, minimal, philosophical |
| `brands/warp.md` | warm, earthy, restrained, approachable, calm |

**E-commerce**

| entry | keywords |
|---|---|
| `brands/coupang.md` | direct, transactional, deal-driven, results-first, utility, dense |
| `brands/kurly.md` | calm, curated, operational, warm, restrained, editorial |
| `brands/musinsa.md` | editorial, compact, declarative, monochrome, magazine |

**Fintech**

| entry | keywords |
|---|---|
| `brands/coinbase.md` | clean, trustworthy, financial, professional, blue |
| `brands/kraken.md` | clean, professional, trustworthy, purple, confident, crypto |
| `brands/revolut.md` | confident, bold, restrained, premium, financial |
| `brands/stripe.md` | luxurious, precise, warm, premium, financial, refined, purple |
| `brands/toss.md` | calm, confident, simple, trustworthy, optimistic, korean, banking |
| `brands/wise.md` | bold, fresh, optimistic, nature-inspired, lime, green |
| `brands/kakaobank.md` | friendly, plain-spoken, warm, formal-when-needed, personal, trustworthy |

**Government**

| entry | keywords |
|---|---|
| `brands/krds.md` | polite, predictable, accessible, clear, neutral, civic |

**Productivity**

| entry | keywords |
|---|---|
| `brands/cal.md` | monochrome, bold, architectural, restrained, confident |
| `brands/freee.md` | enterprise, blue, structured, semantic-tokens, japanese, saas, accounting, calm |
| `brands/intercom.md` | warm, confident, editorial, industrial, customer-service |
| `brands/linear.app.md` | precise, dark, engineered, calibrated, minimal, purple |
| `brands/mintlify.md` | calm, confident, legible, fresh, airy, clean, docs, green |
| `brands/notion.md` | warm, approachable, tactile, analog, understated, minimal |
| `brands/resend.md` | cinematic, theatrical, premium, crystalline, precise, dark |
| `brands/zapier.md` | warm, approachable, professional, organic, energetic, orange |

**Retro web**

| entry | keywords |
|---|---|
| `brands/dell-1996.md` | An inspired interpretation of Dell.com's 1996 design language — a catalog-era enterprise web design built around a literal black page frame, vivid… |
| `brands/nintendo-2001.md` | An analysis of Nintendo.com's 2001 design language — a brushed-periwinkle "console chrome" interface where every panel is a beveled metal plate,… |

**Travel**

| entry | keywords |
|---|---|
| `brands/yanolja.md` | friendly, casual, energetic, playful, conversational, leisure |
| `brands/yeogiotte.md` | plain, polite, hospitable, confident, factual |

### Original web systems (`systems/`, 25)

Each has a full demo page beside it (`systems/<name>.demo.html`) with the real CSS and markup.

| entry | system |
|---|---|
| `systems/agency-grid-layout-minimal.md` | minimal agency design system with a disciplined editorial grid, oversized typography, quiet uppercase utility labels, restrained image blocks, and… |
| `systems/blue-cloudy-clean-modern.md` | clean modern design system with a luminous blue sky atmosphere, soft drifting cloud light, minimal white framing, and serene premium typography. |
| `systems/book-serif-index.md` | archival book-reader design system with serif-led pages, mono index navigation, aged paper surfaces, margin notes, and a premium catalog frame. |
| `systems/bright-green-tech-system-webgl.md` | bright-green technical design system with structured split layouts, hard-framed dark surfaces, mono utility labels, and a prominent WebGL… |
| `systems/clean-minimal-beige-light-mode.md` | clean minimal beige light-mode design system with warm neutral shells, quiet process grids, restrained accent color, and elegant low-contrast… |
| `systems/dark-blue-contrasting-clean.md` | dark-blue clean design system with strong contrast, cobalt gradient feature blocks, crisp framed structure, and restrained premium glow. |
| `systems/dither-laser-dark-mode.md` | dark premium design system that combines near-black surfaces, subtle ordered-dither texture, and a thin accent-colored laser atmosphere. |
| `systems/documentary-brutalist-agency.md` | creative agency, production studio, architecture, culture, and portfolio websites with billboard typography, hard black-and-white chapters, exposed… |
| `systems/editorial-portfolio-chapters.md` | creative-studio, agency, photographer, artist, and portfolio websites where project work leads the story. |
| `systems/editorial-service-booking.md` | appointment-based service websites for salons, barbers, spas, wellness studios, clinics, and hospitality brands. |
| `systems/editorial-tech.md` | Blend editorial magazine composition with precision product-tech detailing using asymmetrical grids, cinematic media bands, mono utility labels, and… |
| `systems/framed-tech-dark-border-gradient.md` | framed dark technical design system with border-gradient shells, asymmetrical grid panels, mono utility labeling, and restrained monochrome… |
| `systems/funky-purple-container-tech.md` | dark container-led technical design system with fuchsia-purple accents, layered rounded shells, crisp frame lines, and playful futuristic focal… |
| `systems/glass-dark-mode-clock.md` | dark glass design system with frosted shells, soft beam grids, circular clock-like calibration dials, and precise sci-fi instrument framing. |
| `systems/high-contrast-skeuomorphic-clean.md` | high-contrast clean skeuomorphic design system with molded dark surfaces, crisp light separation, tactile inset depth, and restrained signal accents. |
| `systems/image-first-grid-layout.md` | image-led grid design system with full-bleed photography, structural guide lines, anchored content blocks, and restrained technical overlays. |
| `systems/light-mode-paper-technical.md` | light-mode technical design system with warm paper surfaces, dark outer framing, subtle diagonal texture, precise bracketed geometry, and restrained… |
| `systems/mesh-gradient-dark-blue-clean.md` | futuristic, premium, clean dark-blue mesh-gradient design system across background rendering, hero shell, navigation, floating nodes, framed… |
| `systems/nested-container-clean-agency.md` | clean agency design system built from nested containers, with an outer editorial shell, inset dark feature blocks, rounded premium cards, and… |
| `systems/operational-enterprise-ai.md` | enterprise AI, automation, security, and operations product pages that explain system boundaries, approvals, auditability, exceptions, and rollback. |
| `systems/orange-clean-paper-saas.md` | clean paper-toned SaaS design system with warm neutrals, orange accent signals, rounded premium forms, and polished product illustration surfaces. |
| `systems/product-proof-saas.md` | SaaS and AI product landing pages where a real workflow, interface, or deterministic demo is the central proof. |
| `systems/split-layout-technical.md` | technical split-screen design system with dual panels, fine frame lines, mono metadata, quiet editorial typography, and premium inset surfaces. |
| `systems/tech-green-dark-mode-modern.md` | modern dark-mode technical design system with matte-black surfaces, emerald signal accents, mono system labeling, framed dashboard cards, and… |
| `systems/technical-wireframe-info-layout.md` | monochrome technical wireframe design system with exploded 3D structure, connector annotations, sparse information labels, and precise dark… |

### App references (`apps/`, 38)

Product UIs by category, described screen by screen (mobile-first, translate the logic to the web).

**dating**

| entry | the idea |
|---|---|
| `apps/dating-hinge.md` | Hinge's iOS app reads like a personal journal printed on warm uncoated paper. |
| `apps/dating-tinder.md` | Tinder's iOS app is built around a single, unforgettable gesture: the swipe. |
| `apps/dating-bumble.md` | Bumble's iOS app is unapologetically loud. |

**finance**

| entry | the idea |
|---|---|
| `apps/finance-robinhood.md` | Robinhood is a brokerage rendered as a clean tech consumer product. |
| `apps/finance-revolut.md` | Revolut's iOS app is a near-black financial cockpit where money looks engineered, not nostalgic. |
| `apps/finance-monzo.md` | Monzo's iOS app is built around one unforgettable object: the **Hot Coral debit card** (`#FF3464`). |
| `apps/finance-cash-app.md` | Cash App is a fintech rendered as a pop-art club flyer. |

**fitness**

| entry | the idea |
|---|---|
| `apps/fitness-calm.md` | Calm's iOS app is a night sky you can fall asleep inside. |
| `apps/fitness-headspace.md` | Headspace is a hand-drawn morning — warm, slow, and humanly imperfect. |
| `apps/fitness-alltrails.md` | AllTrails' iOS app is a clean, outdoorsy light space organized around two things: the **map** and the **trail card**. |
| `apps/fitness-strava.md` | Strava is a sweat-stained newspaper for athletes. |

**food**

| entry | the idea |
|---|---|
| `apps/food-doordash.md` | DoorDash's iOS app is warm, appetizing, and unapologetically commercial — a design optimized for one job: turning browsing into a placed order in… |
| `apps/food-deliveroo.md` | Deliveroo's iOS app is a single-brand-color food delivery experience. |
| `apps/food-chipotle.md` | Chipotle's iOS app is built like a foil-wrapped burrito: warm, hand-made, and stripped to the essentials. |

**messaging**

| entry | the idea |
|---|---|
| `apps/messaging-discord.md` | Discord's iOS app is a dark-first community UI built around one load-bearing color: Blurple (`#5865F2`). |
| `apps/messaging-signal.md` | Signal's iOS app is the calmest messaging surface on the platform, and the calm is the point. |
| `apps/messaging-telegram.md` | Telegram's iOS app is a messenger that lets the user's taste dominate the chrome. |

**misc**

| entry | the idea |
|---|---|
| `apps/misc-duolingo.md` | Duolingo's iOS app is a cartoon classroom in your pocket. |
| `apps/misc-chatgpt.md` | ChatGPT's iOS app is a master class in deliberate minimalism. |
| `apps/misc-claude.md` | Claude's iOS app feels like an AI assistant rendered on a piece of warm paper. |
| `apps/misc-amazon.md` | Amazon's iOS app is a relentlessly functional storefront — a design that has been A/B-tested down to the pixel, where every element is optimized to… |

**music**

| entry | the idea |
|---|---|
| `apps/music-spotify.md` | Spotify's iOS app is a dark canvas that treats album art as the sole source of color. |
| `apps/music-apple-music.md` | Apple Music's iOS app is the flagship showcase of Apple's own design language — a first-party experience that leans heavily into SF Pro, SF Symbols,… |
| `apps/music-bandcamp.md` | Bandcamp's iOS app is a paper-first, editorial music marketplace whose entire identity is built on one belief: the album artwork — uploaded by the… |

**productivity**

| entry | the idea |
|---|---|
| `apps/productivity-notion.md` | Notion's iOS app is an almost-invisible design system. |
| `apps/productivity-linear.md` | Linear's iOS app is a near-black command surface built for speed. |
| `apps/productivity-bear.md` | Bear's iOS app is a writer's instrument disguised as a design system. |
| `apps/productivity-craft.md` | Craft's iOS app is a *beautifully crafted document editor* — the antithesis of a spreadsheet-y productivity tool. |

**social**

| entry | the idea |
|---|---|
| `apps/social-instagram.md` | Instagram's iOS app is a study in chromatic restraint punctuated by one unforgettable gradient. |
| `apps/social-bluesky.md` | Bluesky's iOS app is a clean, friendly, sky-bright timeline that feels open and uncluttered. |
| `apps/social-bereal.md` | BeReal's iOS app is a deliberate rejection of the polished social-media aesthetic. |
| `apps/social-pinterest.md` | Pinterest's iOS app is a content-first, photo-driven canvas where the interface all but disappears so user-generated imagery can do the talking. |

**travel**

| entry | the idea |
|---|---|
| `apps/travel-airbnb.md` | Airbnb's iOS app is an editorial magazine for places to stay. |
| `apps/travel-flighty.md` | Flighty's iOS app is a deep, premium black canvas (`#0B0B0F`) that treats live flight data like an instrument panel. |
| `apps/travel-citymapper.md` | Citymapper's iOS app is a **transit nerd's instrument panel disguised as a friendly app**. |

**video**

| entry | the idea |
|---|---|
| `apps/video-netflix.md` | Netflix's iOS app is a cinematic dark canvas where poster art does all the heavy lifting. |
| `apps/video-crunchyroll.md` | Crunchyroll's iOS app is a cinema for anime. |
| `apps/video-youtube.md` | YouTube's iOS app is a content-forward canvas whose entire job is to surface a 16:9 thumbnail and let you tap it. |

## Libraries

`references/libraries.md`: charts and data, motion, 3D and effects, UX components, typography and
icons, layout and styling, feedback and quality. Each row says what the library is for, how to
load it (CDN with a pinned version, npm, or vendored when the host blocks external scripts) and
its usual trap.
