---
name: copyright-notice
description: "Creates copyright notices and policies for digital content with DMCA procedures and fair use guidelines. Use when protecting original content and establishing copyright policies."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Copyright Notice

## When to Use This Skill

Use this skill when you need to:
- Create copyright notices for websites, digital products, or content
- Draft a DMCA takedown policy for your platform
- Establish fair use guidelines for your content
- Write copyright policies for courses, templates, or digital downloads

**DO NOT** use this skill for trademark applications (use trademark-application), patent filings, or legal disputes. This is for creating copyright notices and policies. Consult an attorney for enforcement or litigation.

---

## Core Principle

COPYRIGHT PROTECTION EXISTS AUTOMATICALLY WHEN YOU CREATE ORIGINAL WORK — BUT A CLEAR NOTICE AND POLICY DETERS INFRINGEMENT AND STRENGTHENS YOUR LEGAL POSITION.

---

## Phase 1: Content Inventory

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Content types** | "What content do you need to protect? (website, courses, templates, ebooks, software)" | Website + digital products |
| **Business name** | "What is the legal name or business name that owns the content?" | No default — must be provided |
| **Year of first publication** | "When was the content first published?" | Current year |
| **User-generated content** | "Does your platform allow users to submit content?" | No |
| **Content licensing** | "Do you license or sell content for others to use?" | No |
| **DMCA agent needed** | "Do you host user-uploaded content that needs DMCA compliance?" | No |

**GATE: Do not proceed without business name and content types.**

---

## Phase 2: Copyright Notices

### Standard Copyright Notice

```
## Copyright Notices

### Website Footer Notice
Copyright [Year] [Business Name]. All rights reserved.

### Extended Notice (for legal page or terms)
Copyright [Year]-[Current Year] [Business Name]. All rights reserved.

All content on this website, including text, graphics, logos, images,
audio, video, software, and digital downloads, is the property of
[Business Name] and is protected by United States and international
copyright laws. No part of this content may be reproduced, distributed,
transmitted, displayed, or otherwise used without the prior written
permission of [Business Name].

### Digital Product Notice (for courses, ebooks, templates)
Copyright [Year] [Business Name]. All rights reserved.

This [product type] is licensed for personal use only. You may not
reproduce, distribute, modify, create derivative works from, publicly
display, or commercially exploit any part of this material without
prior written permission from [Business Name].

Unauthorized copying, sharing, or distribution of this material is
strictly prohibited and may result in legal action.

### Code/Software Notice
Copyright [Year] [Business Name]. All rights reserved.

Licensed under [License Type]. See LICENSE file for details.
```

---

## Phase 3: Policies

### DMCA Takedown Policy

```
## DMCA Policy

### Digital Millennium Copyright Act Notice

[Business Name] respects the intellectual property rights of others
and expects our users to do the same.

### Reporting Copyright Infringement

If you believe your copyrighted work has been used on our platform
in a way that constitutes infringement, please send a written notice
to our designated DMCA agent containing:

1. Your physical or electronic signature
2. Identification of the copyrighted work claimed to have been infringed
3. Identification of the material that is claimed to be infringing,
   including its URL or location on our site
4. Your contact information (name, address, phone, email)
5. A statement that you have a good faith belief that the use is not
   authorized by the copyright owner, its agent, or the law
6. A statement, under penalty of perjury, that the information in the
   notice is accurate and that you are the copyright owner or authorized
   to act on behalf of the owner

### DMCA Agent
Name: [Name]
Email: [email]
Address: [Address]

### Counter-Notification
If you believe your content was removed in error, you may submit a
counter-notification containing the required information under 17
U.S.C. Section 512(g).

### Repeat Infringers
[Business Name] will terminate the accounts of users who are repeat
infringers in appropriate circumstances.
```

### Fair Use Guidelines

```
## Content Usage Guidelines

### What You CAN Do (Fair Use / Permitted Uses)
- Quote short excerpts (under 100 words) with proper attribution
- Link to our content from your website or social media
- Share our content via the share buttons provided
- Reference our work in educational or commentary contexts
- Use purchased templates/tools for your own business

### What You CANNOT Do
- Copy and republish articles, courses, or downloads in full
- Redistribute purchased digital products to others
- Remove copyright notices or author attribution
- Use our content in competing products or services
- Claim our content as your own original work
- Upload our digital products to file-sharing sites

### Attribution Format
When quoting or referencing, use:
"[Quote]" — [Author Name], [Business Name] ([URL])
```

---

## Phase 4: Implementation

### Implementation Checklist

```
## Copyright Implementation Checklist

### Website
- [ ] Copyright notice in website footer (updated year)
- [ ] Copyright policy page published
- [ ] DMCA policy page published (if hosting user content)
- [ ] DMCA agent registered with US Copyright Office (if applicable)

### Digital Products
- [ ] Copyright notice on first page/slide of every product
- [ ] License terms included with every digital download
- [ ] Purchase confirmation email references usage terms

### Content
- [ ] Watermarks on preview images (optional)
- [ ] Right-click protection on images (optional, limited effectiveness)
- [ ] Content usage guidelines published

### Registration (Optional but Recommended)
- [ ] Register key works with US Copyright Office ($65/work online)
- [ ] Registration enables statutory damages and attorney fees in infringement cases
```

---

## Example: Course Creator

**Footer:** Copyright 2024-2026 LearnFast LLC. All rights reserved.
**Course files:** "Copyright 2025 LearnFast LLC. This course is licensed for the individual purchaser's personal and professional use only. Sharing login credentials, distributing course materials, or reproducing content without written permission is prohibited."
**DMCA:** Not needed (no user-uploaded content). Fair use policy allows quoting under 100 words with attribution.

---

## Anti-Patterns

- **No copyright notice at all** — while copyright exists automatically, a notice deters infringement and eliminates "innocent infringer" defenses
- **Outdated year** — update the copyright year annually or use a range (2023-2026)
- **Overly restrictive fair use language** — banning all quotes and references is unenforceable and alienates your audience
- **No DMCA agent for UGC platforms** — if users can upload content to your platform, you need a registered DMCA agent for safe harbor protection
- **Assuming copyright = trademark** — copyright protects the content itself. Your brand name needs trademark protection (separate filing).

---

## Recovery

- **Content already being copied:** Send a cease and desist (use cease-and-desist skill). File DMCA takedowns with hosting providers. Consider copyright registration for statutory damages.
- **Forgot to register copyright:** You can register at any time, but registration within 3 months of publication or before infringement enables statutory damages.
- **International infringement:** Copyright is territorial. The Berne Convention provides baseline protection in 180+ countries, but enforcement varies.
- **Employee or contractor created the content:** Ensure contracts include work-for-hire or IP assignment clauses. Without them, the creator may own the copyright.
