# Team Collection - Writing Guide

## Voice & Tone

**Voice**: Professional yet personable bio that showcases expertise
**Tone**: Confident without being arrogant, approachable and authentic
**Style**: Clear professional narrative with personality

### Writing Principles
- Balance professional credentials with personal touch
- Show expertise through specifics, not generalities
- Include what makes you unique as a developer
- Be honest about your journey and interests
- Make it memorable and human

## Content Structure

Team member profiles should include:
1. **Header** - Name, title, contact info
2. **Professional Summary** - Your value proposition in 2-3 sentences
3. **Key Competencies** - Core skills and expertise areas
4. **Professional Experience** - Relevant work history
5. **Personal Touch** - Interests, philosophy, or what drives you (optional)

## Creating a New Team Member

### 1. English Version (`src/content/team/en/{id}-{name}.md`)

```markdown
---
draft: false
name: "Jane Smith"
alias: "Jane"
selfHealing: "000002"  # 6 chars, use 0000xx pattern for team members
title: "Senior Full-Stack Developer"
avatar: { src: "jane-smith-photo", alt: "Jane Smith profile photo" }
classes: "bg-clip-text text-transparent bg-gradient-to-r from-emerald-400 to-cyan-600"
resume: "Full-stack developer passionate about building accessible, performant web applications"
pathToTranslate: "/team/jane-smith"
publishDate: "2025-01-15 10:00"
---

# Jane Smith

**Senior Full-Stack Developer | Accessibility Advocate**
📍 Portland, Oregon, USA
📧 jane@example.com | 📞 +1 503 555 0100
[LinkedIn](https://linkedin.com/in/janesmith) | [Website](https://janesmith.dev) | [GitHub](https://github.com/janesmith)

---

## 🧠 Professional Summary

Senior Full-Stack Developer with 8+ years of experience building accessible, high-performance web applications. Specialized in React ecosystems and Node.js, with a proven track record of leading teams to deliver quality software on time. Passionate about web accessibility (WCAG 2.1 AA+) and mentoring junior developers.

---

## 🛠️ Key Competencies

**Frontend**
React, Next.js, TypeScript, Vue.js, Web Components, Tailwind CSS, CSS-in-JS

**Backend**
Node.js, Express, NestJS, GraphQL, REST APIs, PostgreSQL, MongoDB

**DevOps & Tools**
Docker, AWS (S3, Lambda, CloudFront), CI/CD (GitHub Actions), Vercel, Testing (Jest, Playwright)

**Specializations**
Web Accessibility (WCAG 2.1), Performance Optimization, Micro-frontends, Design Systems

---

## 💼 Professional Experience

### Senior Full-Stack Developer | TechCorp Inc.
**Jan 2021 – Present | Portland, OR**

- Lead development of accessible component library used by 15+ product teams
- Reduced page load times by 60% through lazy loading and code splitting strategies
- Mentor team of 4 junior developers, conducting code reviews and pair programming sessions
- Implemented automated accessibility testing reducing WCAG violations by 85%

### Full-Stack Developer | StartupXYZ
**Mar 2018 – Dec 2020 | Remote**

- Built real-time collaboration features serving 50K+ daily active users
- Migrated legacy jQuery application to React, improving developer velocity by 40%
- Designed and implemented GraphQL API serving 500+ requests/second

### Frontend Developer | WebAgency Co.
**Jun 2016 – Feb 2018 | Seattle, WA**

- Developed responsive websites for 30+ clients using modern frontend frameworks
- Established component-driven development workflow reducing development time by 25%
- Introduced automated testing practices improving code quality and reducing bugs

---

## 🎓 Education & Certifications

**B.S. Computer Science** | University of Washington | 2016
**IAAP Web Accessibility Specialist (WAS)** | 2022
**AWS Certified Developer – Associate** | 2021

---

## 🌟 What Drives Me

I believe the web should be accessible to everyone, regardless of ability or device. That's why accessibility isn't just a checkbox for me—it's fundamental to how I build software. When I'm not coding, you'll find me contributing to open-source accessibility tools, speaking at local meetups about inclusive design, or hiking the Pacific Northwest trails.

I love working with teams that value quality, collaboration, and continuous learning. There's nothing better than solving complex problems together and seeing the impact of our work on real users.

---

## 📝 Recent Speaking & Writing

- **"Beyond Alt Text: Advanced Web Accessibility Patterns"** | React Summit 2024
- **"Building Performant Micro-frontends"** | CSS-Tricks | 2023
- **"Testing Accessibility: Automated and Manual Approaches"** | Portland Dev Meetup | 2023

---

## 🔗 Links

- Personal blog: [janesmith.dev/blog](https://janesmith.dev/blog)
- Open source: [github.com/janesmith](https://github.com/janesmith)
- Speaking: [sessionize.com/janesmith](https://sessionize.com/janesmith)
```

### 2. Spanish Version (`src/content/team/es/{id}-{name}.md`)

Translate while maintaining professional tone and personal authenticity.

## Self-Healing Pattern for Team

Team members use the `0000xx` pattern:
- Start with `000000` or `000001`
- Increment for each new member: `000002`, `000003`, etc.
- Keeps team members distinct from other content types

## Resume Field Guidelines

The `resume` field is a one-line summary:
- Keep under 100 characters
- Focus on specialization or passion
- Make it memorable and unique

Examples:
✅ "Full-stack developer passionate about web accessibility and performance"
✅ "Solutions architect specializing in micro-frontend architectures"
✅ "Frontend engineer who loves building delightful user experiences"

❌ "Developer" (too vague)
❌ "Experienced professional with many skills in various technologies" (too generic)

## Avatar Guidelines

- Use professional but approachable photo
- Square aspect ratio (1:1)
- High quality (at least 800x800px)
- Descriptive alt text including name

## Writing Style Tips

### Professional Section
- Be specific about years of experience
- Quantify achievements when possible
- Include relevant certifications
- List concrete technologies, not "proficient in modern frameworks"

### Personal Section
- Show what makes you unique
- Include non-work interests that relate to your work
- Share your development philosophy
- Make it memorable—give people something to connect with

### Avoid
❌ Generic buzzwords: "team player", "self-starter", "passionate professional"
❌ Listing every technology you've touched once
❌ Vague claims: "expert in everything", "best developer"
❌ All work, no personality—make it human

## Gradient Classes

Choose gradient classes for visual variety:

**Emerald to Cyan** (default):
```yaml
classes: "bg-clip-text text-transparent bg-gradient-to-r from-emerald-400 to-cyan-600"
```

**Purple to Pink**:
```yaml
classes: "bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-600"
```

**Blue to Indigo**:
```yaml
classes: "bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-indigo-600"
```

**Orange to Red**:
```yaml
classes: "bg-clip-text text-transparent bg-gradient-to-r from-orange-400 to-red-600"
```

## Content Sections to Include

**Must Have:**
- Name and title
- Professional summary
- Key competencies
- Contact information

**Should Have:**
- Professional experience
- Education
- Links to GitHub, LinkedIn, portfolio

**Nice to Have:**
- Personal philosophy or "what drives me"
- Speaking engagements
- Writing/blog posts
- Open source contributions
- Hobbies/interests that relate to work

## Publishing Checklist

Before setting `draft: false`:
- [ ] Professional photo uploaded and optimized
- [ ] Contact information is current
- [ ] Spanish translation is complete
- [ ] Links are working and correct
- [ ] Self-healing code follows 0000xx pattern
- [ ] Resume field is concise and compelling
- [ ] Content feels authentic, not like a generic resume
- [ ] Quantifiable achievements where possible
