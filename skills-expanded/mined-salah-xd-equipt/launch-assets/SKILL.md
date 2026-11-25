---
name: launch-assets
description: "Builds a complete product or service launch package with a structured checklist in Notion and coordinated visual assets in Canva, including social media graphics, announcement images, and email headers. Use when a user is preparing to launch a product, course, service, or campaign and needs both the planning checklist and the visual assets created together."
allowed-tools: Read Write Glob mcp__claude_ai_Notion__notion-create-pages mcp__claude_ai_Notion__notion-search mcp__claude_ai_Canva__generate-design mcp__claude_ai_Canva__generate-design-structured mcp__claude_ai_Canva__resize-design mcp__claude_ai_Canva__export-design mcp__claude_ai_Canva__get-export-formats mcp__claude_ai_Canva__list-brand-kits mcp__claude_ai_Canva__create-folder mcp__claude_ai_Canva__move-item-to-folder mcp__claude_ai_Canva__get-design-thumbnail
metadata:
  author: Salah-XD
  version: "1.0"
---

# Launch Assets

## When to Use This Skill

Use this skill when you need to:
- Prepare a full launch package for a product, course, service, or campaign
- Build a structured launch checklist in Notion with pre-launch, launch day, and post-launch tasks
- Generate coordinated visual assets (announcement graphic, social media set, email header) in Canva
- Ensure nothing falls through the cracks on launch day by combining planning and assets in one workflow

**DO NOT** use this skill for:
- Ongoing social media content creation (use social-media-graphics or content-repurpose instead)
- Building a CRM or client pipeline (use client-crm instead)
- Creating a content calendar without visual assets (use content-calendar instead)
- Designing logos, full brand identity, or print materials

---

## Quick Reference: Asset Dimensions

| Asset | Width | Height | Aspect Ratio | Purpose |
|-------|-------|--------|--------------|---------|
| Announcement Graphic | 1080 | 1080 | 1:1 | Hero image, Instagram post |
| Facebook Post | 1200 | 630 | 1.91:1 | Facebook feed announcement |
| X/Twitter Post | 1600 | 900 | 16:9 | X/Twitter timeline image |
| LinkedIn Post | 1200 | 627 | 1.91:1 | LinkedIn feed announcement |
| Email Header | 600 | 200 | 3:1 | Top banner for launch email |

## Quick Reference: Launch Checklist Sections

| Phase | Tasks | Timing |
|-------|-------|--------|
| Pre-Launch | 8 tasks | 7-14 days before launch |
| Launch Day | 6 tasks | Day of launch |
| Post-Launch | 5 tasks | 1-7 days after launch |

---

## Core Workflow

EVERY LAUNCH PACKAGE STARTS WITH A COMPLETE BRIEF BEFORE ANY NOTION PAGE OR CANVA DESIGN IS CREATED -- NEVER BUILD ASSETS WITHOUT KNOWING THE PRODUCT, AUDIENCE, AND KEY MESSAGE.

### Phase 1: Launch Brief

Gather all launch details from the user before building anything.

1. **Product/service name** -- what is being launched
2. **Launch date** -- when is it going live
3. **Target audience** -- who is this for (demographics, pain points, interests)
4. **Key message** -- the one headline or value proposition for the launch
5. **Call to action** -- what should the audience do (sign up, buy, join, enroll)
6. **Platforms** -- which social platforms to target (default: Instagram, Facebook, X/Twitter, LinkedIn)
7. **Brand kit** -- use existing Canva brand kit or specify colors/fonts
8. **Notion parent page** -- where to create the launch checklist

If the user provides items 1-5, proceed with defaults for items 6-8. Ask only about missing critical details.

**Brief template for vague requests:**

```
I'll build your complete launch package. Quick answers needed:

1. What are you launching? (product/service name)
2. When is launch day?
3. Who is it for? (target audience)
4. What's the key message or headline?
5. What should people do? (CTA: buy, sign up, enroll, etc.)
6. Which platforms? (default: Instagram, Facebook, X/Twitter, LinkedIn)
7. Use your Canva brand kit? (Y/N)
8. Which Notion page should the checklist live under?
```

**GATE: Do not proceed to Phase 2 until you have items 1-5 confirmed.** Items 6-8 can use defaults.

### Phase 2: Build Launch Checklist in Notion

Create a structured launch checklist page in Notion with to-do blocks organized by phase.

#### Step 1: Locate the Notion Parent Page

1. Call `notion-search` with the page name or keywords the user provided
2. Identify the correct parent page from the search results
3. Confirm the page ID with the user if multiple matches exist

```
Found Notion page: "Marketing Hub"
Page ID: abc12345-def6-7890-ghij-klmnopqrstuv

I'll create the launch checklist under this page. Correct?
```

**IF THE PAGE IS NOT FOUND:**
- Ask the user for the exact page title
- Try `notion-search` again with a shorter keyword
- **After 3 failed searches:** "I cannot find that page. Please verify it exists and that the Notion integration has access. Check Settings > Connections in Notion."

#### Step 2: Create the Launch Checklist Page

Call `notion-create-pages` to create a page under the parent with the following structure. Use the product/service name and launch date in the title.

**Page title:** `{Product Name} Launch Checklist — {Launch Date}`

**Page content (to-do blocks organized by section):**

```
# {Product Name} Launch Checklist

Launch Date: {date}
Target Audience: {audience}
Key Message: {headline}
CTA: {call to action}

---

## Pre-Launch (7-14 Days Before)

- [ ] Finalize product/service page or sales page copy
- [ ] Write and schedule launch announcement email
- [ ] Create and schedule social media posts for all platforms
- [ ] Prepare FAQ or objection-handling document
- [ ] Set up payment/checkout flow and test it end-to-end
- [ ] Brief any team members, partners, or affiliates
- [ ] Schedule launch day posts in social media scheduler
- [ ] Review all visual assets for brand consistency

## Launch Day

- [ ] Publish product/service page or make it live
- [ ] Send launch announcement email
- [ ] Post announcement on all social platforms
- [ ] Notify partners, affiliates, and collaborators
- [ ] Monitor comments, DMs, and email replies — respond within 1 hour
- [ ] Track early metrics (page views, sign-ups, sales)

## Post-Launch (1-7 Days After)

- [ ] Send follow-up email to non-openers (48 hours after launch)
- [ ] Share social proof (testimonials, early results, milestones)
- [ ] Engage with comments and questions on all platforms
- [ ] Compile launch metrics report (traffic, conversions, revenue)
- [ ] Document lessons learned for the next launch
```

Present the completed checklist to the user:

```
Launch checklist created in Notion:

  Page: "{Product Name} Launch Checklist — {Launch Date}"
  Location: Under "{Parent Page Name}"
  Sections: Pre-Launch (8 tasks), Launch Day (6 tasks), Post-Launch (5 tasks)
  Total: 19 actionable tasks with checkboxes

Ready to generate your visual assets next.
```

**GATE: Confirm the checklist was created successfully before proceeding to Phase 3.** If Notion creation fails, resolve it before moving to Canva.

### Phase 3: Generate Visual Assets in Canva

Create all launch visuals from a single hero design, then resize and generate platform-specific variants.

#### Step 1: Load Brand Kit

1. Call `list-brand-kits` to retrieve available brand kits
2. Present brand kit names to the user if multiple exist
3. Note brand colors, fonts, and logo references for generation prompts

```
Brand kit loaded: "My Brand"
- Primary: #2D5BFF
- Secondary: #FF6B35
- Font: Montserrat Bold / Open Sans Regular
- Logo: Available
```

**IF NO BRAND KIT EXISTS:**
- Ask the user for primary color, secondary color, and font preference
- Proceed without brand kit — embed color hex codes and font style directly in generation prompts
- Inform the user: "You can create a brand kit in Canva for future consistency."

#### Step 2: Generate the Announcement Graphic (Hero Design)

The announcement graphic is the hero design. **Default: Instagram Post (1080x1080)** because square crops cleanly to other formats.

1. Build the generation prompt incorporating:
   - Product/service name and key message as headline text
   - CTA text as subheading
   - Brand colors, fonts, and style from the brand kit
   - Launch-appropriate visual tone (exciting, professional, bold)
   - Square (1:1) composition with text and focal elements centered

2. Call `generate-design` with the composed prompt

3. Call `get-design-thumbnail` to preview the hero design

4. Present to the user:

```
Announcement graphic generated: "{Product Name} Launch"
Design ID: dsg_hero123
Preview: [thumbnail displayed]

Does this look good, or would you like adjustments before I create the rest of the set?
```

5. **Wait for user approval before proceeding**

**IF THE HERO DESIGN MISSES THE MARK:**
- Ask what specific element needs changing (layout, colors, text placement, imagery)
- Regenerate with an adjusted prompt
- If 2 regenerations still miss, ask the user to describe what they envision or provide a reference image
- **If 3 attempts fail:** "Let me try a different approach with `generate-design-structured` for more layout control."

#### Step 3: Generate the Social Media Set

Once the hero is approved, create platform-specific variants.

1. **Resize for Facebook (1200x630):**
   - Call `resize-design` with hero design ID and target dimensions
   - Call `get-design-thumbnail` to verify headline and CTA are visible
   - Wide crop — ensure text is not cut off at edges

2. **Resize for X/Twitter (1600x900):**
   - Call `resize-design` with hero design ID and target dimensions
   - Call `get-design-thumbnail` to verify
   - Wide format — check text stays centered

3. **Resize for LinkedIn (1200x627):**
   - Call `resize-design` with hero design ID and target dimensions
   - Call `get-design-thumbnail` to verify
   - Nearly identical to Facebook — confirm clean layout

**IF A RESIZE CROPS TEXT OR KEY ELEMENTS:**
- Do not deliver the cropped version
- Call `generate-design` for that specific platform dimension using the same creative brief
- Adjust the prompt: "Center text horizontally, keep in middle third vertically"
- Verify the regenerated variant with `get-design-thumbnail`

#### Step 4: Generate the Email Header

The email header has a unique aspect ratio (600x200) that does not resize well from the square hero. **Generate this as a separate design.**

1. Call `generate-design` with a prompt tailored for email header:
   - 600x200 dimensions, 3:1 aspect ratio
   - Product name and key message in concise form
   - Brand colors and fonts matching the announcement graphic
   - Minimal layout — text must be readable at small size
   - No fine details that get lost at 200px height

2. Call `get-design-thumbnail` to verify readability

```
Email header generated: "{Product Name} - Email Banner"
Design ID: dsg_email456
Preview: [thumbnail displayed]

Text readable at email width. Brand colors match the announcement set.
```

#### Step 5: Export All Assets

1. Call `get-export-formats` to confirm available formats

2. Export each design as PNG (default):
   - Announcement graphic (1080x1080)
   - Facebook post (1200x630)
   - X/Twitter post (1600x900)
   - LinkedIn post (1200x627)
   - Email header (600x200)

3. Collect all export download URLs

**FILE NAMING CONVENTION:** `{product-name}-{asset-type}.png`
- All lowercase, hyphens only, no spaces
- Examples: `email-mastery-announcement.png`, `email-mastery-facebook.png`, `email-mastery-email-header.png`

#### Step 6: Organize in Canva Folder

1. Call `create-folder` with name: `{Product Name} — Launch Assets`

2. Call `move-item-to-folder` for each design to place it in the folder

3. Confirm organization:

```
All designs organized in Canva folder: "{Product Name} — Launch Assets"

Contents:
  - Announcement Graphic (1080x1080)
  - Facebook Post (1200x630)
  - X/Twitter Post (1600x900)
  - LinkedIn Post (1200x627)
  - Email Header (600x200)
```

### Phase 4: Deliver the Complete Package

Present the full launch package with both the Notion checklist and all Canva assets in a single summary.

```
LAUNCH PACKAGE COMPLETE: {Product Name}

Notion: "{Product Name} Launch Checklist — {Launch Date}" under "{Parent Page}"
        19 tasks (8 pre-launch, 6 launch day, 5 post-launch)

Canva:  "{Product Name} — Launch Assets" (PNG, {brand kit or colors})
  Announcement (1080x1080)  — [export URL]
  Facebook (1200x630)       — [export URL]
  X/Twitter (1600x900)      — [export URL]
  LinkedIn (1200x627)       — [export URL]
  Email Header (600x200)    — [export URL]

Next Steps:
1. Review checklist in Notion — adjust dates/owners
2. Download assets or access them in your Canva folder
3. Upload graphics to your social media scheduler
4. Add email header to your launch email template
5. Start working through pre-launch tasks
```

---

## Example 1: Online Course Launch

**User request:** "I'm launching an online course called 'Freelance Mastery' on March 15. It's for freelancers who want to land higher-paying clients. Key message: 'Stop Undercharging. Start Earning What You're Worth.' CTA is 'Enroll now.' My Notion page is 'Course Launches' and I have a Canva brand kit."

**Execution:**

1. **Brief:** Product: Freelance Mastery. Launch: March 15. Audience: freelancers. Message: "Stop Undercharging. Start Earning What You're Worth." CTA: "Enroll now." Brand kit: yes. Notion parent: "Course Launches."

2. **Notion checklist:** `notion-search` finds "Course Launches" (`pg_courses789`). Created "Freelance Mastery Launch Checklist — March 15" with 19 tasks (8 pre-launch, 6 launch day, 5 post-launch).

3. **Brand kit:** `list-brand-kits` returns "Freelance Pro" — navy (#1A3A5C), gold (#E8A838), Poppins Bold / Inter Regular.

4. **Hero design:** `generate-design` with prompt including headline, brand colors, and "professional, aspirational" style at 1080x1080. Thumbnail previewed. User approves.

5. **Social set:** Resized hero to Facebook (1200x630), X/Twitter (1600x900), LinkedIn (1200x627). All thumbnails verified — text visible, no cropping.

6. **Email header:** Generated separately at 600x200 with condensed headline. Verified readable.

7. **Exported** all 5 as PNG: `freelance-mastery-announcement.png`, `freelance-mastery-facebook.png`, `freelance-mastery-twitter.png`, `freelance-mastery-linkedin.png`, `freelance-mastery-email-header.png`

8. **Organized** in Canva folder: "Freelance Mastery — Launch Assets"

**Delivered:**

```
LAUNCH PACKAGE COMPLETE: Freelance Mastery

Notion: "Freelance Mastery Launch Checklist — March 15" (19 tasks)
Canva:  "Freelance Mastery — Launch Assets" (5 designs, PNG, "Freelance Pro" brand kit)

  Announcement (1080x1080) | Facebook (1200x630) | X/Twitter (1600x900)
  LinkedIn (1200x627)      | Email Header (600x200)

Next: Review checklist, download assets, schedule posts for March 15.
```

---

## Example 2: New Service Offering Launch

**User request:** "I'm a business coach adding a new VIP Day offering. Launching it next Friday. Audience is established entrepreneurs who want intensive 1-on-1 strategy sessions. Message: 'One Day. Total Clarity.' CTA: 'Book your VIP Day.' Notion page is 'Services'. No brand kit but my colors are coral and charcoal."

**Execution:**

1. **Brief:** Product: VIP Day (coaching service). Launch: next Friday. Audience: established entrepreneurs. Message: "One Day. Total Clarity." CTA: "Book your VIP Day." No brand kit — coral (#FF6F61) + charcoal (#36454F). Notion parent: "Services."

2. **Notion checklist:** `notion-search` finds "Services" (`pg_services456`). Created "VIP Day Launch Checklist — {date}" with 19 tasks.

3. **No brand kit:** `list-brand-kits` returns empty. Using manual colors: coral (#FF6F61), charcoal (#36454F). Font defaulted to Playfair Display Bold / Lato Regular. User informed about creating a brand kit for future use.

4. **Hero design:** Generated at 1080x1080 with elegant, minimal style. User requested "more coral" — regenerated with coral background and charcoal text. Approved on second attempt.

5. **Social set:** Facebook and LinkedIn resized cleanly. X/Twitter resize cropped headline — regenerated natively at 1600x900 with text in middle third. All verified.

6. **Email header:** Generated separately at 600x200. Verified readable.

7. **Exported** all 5 as PNG: `vip-day-announcement.png`, `vip-day-facebook.png`, `vip-day-twitter.png`, `vip-day-linkedin.png`, `vip-day-email-header.png`

8. **Organized** in Canva folder: "VIP Day — Launch Assets"

**Delivered:**

```
LAUNCH PACKAGE COMPLETE: VIP Day

Notion: "VIP Day Launch Checklist — {date}" (19 tasks)
Canva:  "VIP Day — Launch Assets" (5 designs, PNG, coral + charcoal)

  Announcement (1080x1080) | Facebook (1200x630) | X/Twitter (1600x900)*
  LinkedIn (1200x627)      | Email Header (600x200)
  * X/Twitter regenerated natively due to crop issue

Next: Review checklist, download assets, schedule posts for launch day.
```

---

## Pre-Delivery Checklist

Run this before delivering. **DO NOT SKIP ANY ITEM.**

```
Pre-Delivery Checklist:
  [ ] Notion checklist created under correct parent page
  [ ] All 3 sections present (pre-launch, launch day, post-launch)
  [ ] 19 tasks with checkboxes
  [ ] Launch date in page title
  [ ] Hero design approved by user before resizing
  [ ] All 5 visual assets generated (announcement, FB, X, LinkedIn, email header)
  [ ] Brand colors match kit or user-specified values
  [ ] Text readable on all assets at mobile size
  [ ] No cut-off text on any resized variant
  [ ] Visual style consistent across all 5 assets
  [ ] File naming follows {product-name}-{asset-type}.png convention
  [ ] All designs organized in one Canva folder
  [ ] Export format confirmed (PNG default)
```

---

## Recovery and Troubleshooting

### Notion Page Not Found

1. Ask the user for the exact page title
2. Try `notion-search` with a shorter keyword (e.g., "Marketing" instead of "Marketing Hub Dashboard")
3. Ask the user to confirm the page is shared with the Notion integration
4. **After 3 failed searches:** "I cannot locate that page. Check Settings > Connections in Notion and verify the integration has access."

### Notion Page Creation Fails

1. Verify the parent page ID by searching again
2. Retry once with the same parameters
3. **If it fails again:** "Page creation failed. Please check that the Notion integration has 'Can edit' access. Go to the page > three-dot menu > Connections."
4. **Fallback:** Provide the full checklist as formatted markdown text that the user can paste into Notion manually

### Brand Kit Not Found

1. Inform the user: "No brand kits found in your Canva account."
2. Ask for primary color (hex code or name), secondary color, and font preference
3. Proceed with manual values embedded in the generation prompt
4. Suggest: "You can create a brand kit in Canva to speed up future launches."

### Resize Crops Text or Key Elements

1. Do not deliver the cropped version
2. Call `generate-design` for that specific platform dimension using the same creative brief
3. Adjust the prompt for the target aspect ratio:
   - Wide formats (Facebook, X/Twitter, LinkedIn): "Center text horizontally, keep in middle third vertically"
   - Email header: "Condense text to fit 3:1 ratio, prioritize readability"
4. Verify the regenerated variant with `get-design-thumbnail`

### Design Generation Fails

1. Simplify the prompt — remove complex layout instructions, keep to headline + colors + style
2. Retry once with the simplified prompt
3. If it fails again, try `generate-design-structured` as an alternative
4. **If 3 attempts fail:** "Canva design generation is unavailable right now. Here are the specs for each asset so you can create them manually: [provide dimensions, colors, text for all 5 assets]."

### Export Fails

1. Verify the design ID by calling `get-design-thumbnail`
2. Try exporting as JPG instead of PNG
3. **If both fail:** provide the design IDs and Canva folder name so the user can export manually from their Canva account

### Partial Failure (Notion Works, Canva Fails — or Vice Versa)

1. **Notion works, Canva fails:** Deliver the Notion checklist and provide complete design specs (dimensions, colors, text, layout notes) for all 5 assets so the user can create them manually in Canva
2. **Canva works, Notion fails:** Deliver the Canva assets and provide the full checklist as formatted markdown for the user to paste into Notion manually
3. **NEVER skip one half of the package without informing the user** — always deliver what succeeded and provide a clear path for the part that failed

---

## Anti-Patterns

- **DO NOT** skip the launch brief — generating assets without a confirmed product name, key message, and audience produces generic, off-brand results
- **DO NOT** create Canva assets before the Notion checklist is confirmed — the checklist grounds the entire launch plan and may surface details that affect the visuals
- **DO NOT** generate each social platform variant from scratch — start with the hero announcement graphic and resize, only regenerating natively when resize crops badly
- **DO NOT** skip the brand kit check — guessing brand colors produces inconsistent assets that the user will have to redo
- **DO NOT** export before the user approves the hero design — resizing and exporting 5 assets from an unapproved hero wastes time
- **DO NOT** leave designs scattered in Canva — always organize all launch assets into a single labeled folder
- **DO NOT** deliver the Canva assets without the Notion checklist (or vice versa) — this skill produces a complete launch package, not one piece of it
- **DO NOT** use JPG as the default export — always default to PNG for launch graphics
- **DO NOT** overcrowd any design with text — launch graphics need a clear visual hierarchy with one headline and one CTA maximum
