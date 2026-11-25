---
name: cv-resume
description: Generate professional, ATS-optimized CVs and resumes as polished HTML files. Use this skill whenever the user asks to create, write, build, update, or improve a CV, resume, curriculum vitae, or job application document — even if they just say "make me a resume" or "help with my CV". Also trigger when the user provides career info, work history, or asks to format their experience for job applications. This skill produces visually stunning, eye-catching HTML that is simultaneously ATS-friendly — the best of both worlds.
---

# CV / Resume Generator

Produce a **visually stunning, eye-catching** and ATS-optimized resume as a single self-contained HTML file. Generic-looking output is a failure. Every resume must feel like it was designed by a professional designer — bold, memorable, and uniquely crafted.

---

## Step 1: Gather Information

Ask for (or extract from context):
1. **Full name** and contact info (email, phone, LinkedIn, location, portfolio/GitHub)
2. **Target role / industry** — critical for ATS keywords and visual tone
3. **Career Objective** — their goal statement or aspirations (1–3 sentences, or generate from context)
4. **Work experience** (company, title, dates, responsibilities, achievements)
5. **Education** (institution, degree, year, GPA if strong)
6. **Skills** (technical + soft)
7. **Optional**: Certifications, projects, publications, languages, awards, volunteer work

Never stall waiting for complete info. Work with what's given and note what's missing.

---

## Step 2: Career Objective Section (REQUIRED)

Every resume MUST include a **Career Objective** section, placed immediately after the header and before Work Experience.

**What makes a great Career Objective:**
- 2–4 sentences, highly personalized to the target role
- Formula: [Who you are] + [Core strengths/experience] + [What you bring to the role] + [What you want to achieve]
- Avoids clichés like "hardworking", "team player", "passionate"
- Uses concrete language and industry-relevant keywords
- Feels aspirational yet grounded

**Examples by level:**

*Entry-level*:
> "Computer Science graduate from UC Berkeley with hands-on experience in full-stack development through internships at two early-stage startups. Skilled in React, Node.js, and PostgreSQL, with a strong foundation in system design and agile collaboration. Seeking a junior software engineering role where I can contribute to scalable product development while growing within a high-performance engineering team."

*Mid-career*:
> "Senior Product Manager with 7 years of experience leading cross-functional teams to ship B2B SaaS products that drive measurable revenue growth. Passionate about translating complex user needs into elegant product solutions through rigorous data analysis and iterative experimentation. Looking to bring strategic roadmap leadership and a builder's mindset to a growth-stage company scaling its core platform."

*Career changer*:
> "Former secondary school teacher transitioning into UX design, bringing 6 years of experience understanding learner psychology, communicating complex ideas clearly, and designing curricula centered on user needs. Completed a Google UX Design Certificate and built 4 end-to-end case study projects. Eager to apply a people-first design approach at a company creating meaningful digital experiences."

**ATS note**: The Career Objective is a great place to front-load role-specific keywords naturally.

---

## Step 3: ATS Optimization Rules

**HTML Structure** (non-negotiable):
- `<h1>` for the person's name
- `<h2>` for all section headings (Career Objective, Work Experience, Education, Skills, etc.)
- `<h3>` for job titles
- `<ul>/<li>` for all bullet points
- Section order: Career Objective → Work Experience → Education → Skills

**Content rules**:
- Start every bullet with a strong action verb: Led, Built, Designed, Launched, Reduced, Generated, Optimized, Architected, Coached, Negotiated...
- Quantify at least one achievement per role: numbers, %, $, time saved
- Mirror keywords from target job description if provided
- Spell out acronyms once: "Machine Learning (ML)"
- Use past tense for previous roles, present tense for current

**ATS killers to avoid**:
- No HTML `<table>` for layout (use CSS flexbox/grid)
- No critical text inside `background-image`, `content:`, or decorative SVGs
- No multi-column layouts that fragment linear text flow for ATS parsers
- Skills must appear as plain readable text, not just as visual bars/charts

---

## Step 4: Visual Design (CRITICAL — Generic = Failure)

This is a designed artifact. It must be **visually exceptional**. Think: design portfolio piece, not Word template.

### Mandatory Visual Standards

**Typography** — pick a pairing that feels intentional and distinctive:
- Display options: Playfair Display, Cormorant Garamond, DM Serif Display, Fraunces, Libre Baskerville, Yeseva One, Abril Fatface
- Body options: DM Sans, Outfit, Plus Jakarta Sans, Nunito Sans, Lato, Karla, Mulish
- NEVER use: Arial, Roboto, Inter, Times New Roman, system-ui generics
- Name: 36–48px display font. Section headers: spaced capitals, 10–12px. Body: 13–14px.

**Color** — pick ONE cohesive palette per resume, vary across generations:

| Theme | Background | Text | Accent | Header BG |
|-------|-----------|------|--------|-----------|
| Midnight Navy | #F5F7FA | #1A1A2E | #4361EE | #1A1A2E |
| Warm Burgundy | #FDFAF6 | #2D1B1B | #8B2635 | #2D1B1B |
| Forest Executive | #F4F6F0 | #1C2B1E | #2D6A4F | #1C2B1E |
| Slate & Copper | #F7F8FA | #1E2433 | #C87941 | #1E2433 |
| Rose Editorial | #FFF8F8 | #2B1B1B | #C0414F | #2B1B1B |
| Deep Teal | #F2F8F8 | #0D2B2B | #0D7377 | #0D2B2B |
| Charcoal & Gold | #FAFAF7 | #1A1A1A | #C9A84C | #1A1A1A |
| Custom | Invent something tasteful and industry-appropriate | | | |

**Layout Patterns** — choose one and execute it boldly:

*Option A: Bold Side Panel* — Dark sidebar (240–260px) with name, contact, skills, education on a rich accent-colored column; main content (Career Objective, Experience) on right with clean white background.

*Option B: Dramatic Full-Width Header* — Full-bleed dark header with name large (centered or left), target role subtitle, contact row in light text; geometric accent or diagonal clip-path at bottom edge; clean content area below.

*Option C: Left Accent Column* — Subtle 6–8px thick colored left border running full height; name massive at top-left; elegant single-column flow with strong typographic contrast between section labels and body.

*Option D: Editorial Card* — Whole resume in a centered card with drop shadow; name in extra-large serif (48px+); section headings as thin all-caps ruled lines; generous padding; feels like a high-end magazine layout.

*Option E: Diagonal/Geometric Header* — Header area uses CSS clip-path or skewed pseudo-element to create a dynamic angled boundary between the dark header and white content area.

**Eye-catching details that elevate the design:**
- Skill tags as styled pill badges (colored background, rounded corners, small font)
- Section headings with a decorative rule, or character like ▪ ◆ ● — before the label
- Job title + company on same line, dates right-aligned in muted badge or italics
- Accent-colored bullet markers (▸ • ◦ ➤)
- Thin colored horizontal rules between major sections
- Name initials as a decorative monogram or avatar placeholder in the header
- Subtle CSS gradient or geometric pattern behind the header area
- Timeline dot-and-line treatment on the left of experience entries
- Hover effects: subtle left border reveals or background tints on job cards

**Skill badge pattern** (ATS-safe: plain text in `<li>`, styled visually):
```html
<ul class="skill-tags">
  <li>React</li>
  <li>Node.js</li>
  <li>PostgreSQL</li>
</ul>
```
```css
.skill-tags { display: flex; flex-wrap: wrap; gap: 8px; list-style: none; padding: 0; margin: 0; }
.skill-tags li { background: var(--accent-light); color: var(--accent-dark);
  padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 500; }
```

### Print & PDF Optimization
Always include:
```css
@media print {
  * { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  body { background: var(--bg); color: var(--text); }
  .resume { box-shadow: none; margin: 0; border: none; max-width: 100%; }
}
@page { margin: 0; size: A4; }
```

---

## Step 5: Section Template Reference

Full HTML skeleton with Career Objective:
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Name] – Resume</title>
  <link href="https://fonts.googleapis.com/css2?family=[DisplayFont]&family=[BodyFont]&display=swap" rel="stylesheet">
  <style>/* All CSS here */</style>
</head>
<body>
<div class="resume">
  <header>
    <h1>[Full Name]</h1>
    <p class="headline">[Target Job Title]</p>
    <div class="contact-info">
      <span>[email]</span> · <span>[phone]</span> · <span>[location]</span>
    </div>
  </header>

  <main>
    <!-- CAREER OBJECTIVE — REQUIRED -->
    <section class="objective">
      <h2>Career Objective</h2>
      <p>[2–4 sentence tailored objective with role-specific keywords]</p>
    </section>

    <!-- WORK EXPERIENCE -->
    <section class="experience">
      <h2>Work Experience</h2>
      <div class="job">
        <div class="job-header">
          <div>
            <h3>[Job Title]</h3>
            <span class="company">[Company]</span> · <span class="location">[City]</span>
          </div>
          <span class="dates">[Month Year] – [Month Year]</span>
        </div>
        <ul>
          <li>[Action verb] + [task] + [measurable result]</li>
        </ul>
      </div>
    </section>

    <!-- EDUCATION -->
    <section class="education">
      <h2>Education</h2>
      <div class="edu-item">
        <div>
          <h3>[Degree, Field]</h3>
          <span class="school">[Institution]</span>
        </div>
        <span class="dates">[Year]</span>
      </div>
    </section>

    <!-- SKILLS — plain text li for ATS, styled as badges -->
    <section class="skills">
      <h2>Skills</h2>
      <ul class="skill-tags">
        <li>Skill One</li><li>Skill Two</li><li>Skill Three</li>
      </ul>
    </section>
  </main>
</div>
</body>
</html>
```

---

## Step 6: Industry-Specific Guidance

| Industry | Visual tone | Emphasize | Notes |
|----------|------------|-----------|-------|
| Tech/Engineering | Clean, modern | GitHub, tech stack, OSS | Skills section near top |
| Finance/Consulting | Conservative, navy/burgundy | ROI metrics, deal sizes | Education prominent |
| Creative/Design | Bold, expressive | Portfolio URL, visual projects | Add Projects section |
| Healthcare | Trustworthy, blue/green | Licenses, certifications | Certs after Education |
| Academia | Traditional, serif-heavy | Publications, grants, teaching | Full CV format (longer) |
| Executive/C-Suite | Premium, restrained | P&L, board, M&A, revenue scale | Board/Advisor section |
| Startups | Modern, energetic | Growth metrics, multiple roles | Projects/Side work |

---

## Quality Checklist

**ATS**:
- [ ] `<h1>` name, `<h2>` sections, `<h3>` job titles
- [ ] Career Objective present, personalized, keyword-rich
- [ ] Skills in plain `<li>` text
- [ ] Action verbs start every bullet
- [ ] At least one metric per role
- [ ] No `<table>` for layout

**Visual**:
- [ ] Google Fonts loaded — distinctive pairing, never generic
- [ ] Cohesive color palette — one accent color used consistently
- [ ] Header is visually impactful (not a plain white box)
- [ ] Section headings have typographic flair (spacing, color, decorative rules)
- [ ] Skill tags styled as pill badges
- [ ] Print CSS with `print-color-adjust: exact`
- [ ] Looks like a real designer made it

**Content**:
- [ ] Career Objective is personalized and uses target-role keywords
- [ ] Contact info includes email + at least one other method
- [ ] No placeholder text in output
- [ ] Valid, complete HTML

---

## Output

A HTML file of CV/resume

Follow with a brief note on: (1) Career Objective angle chosen and why, (2) what ATS optimizations were applied, (3) 1-2 suggestion to strengthen it further.