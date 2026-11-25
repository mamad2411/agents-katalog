---
name: publish-a-blog-post
domain: business
locale: [generic]
interface: web
difficulty: basic
est_time: 20min
risk: low
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Publish an approved blog post with correct formatting, metadata, links, and visibility.

## Preconditions

- The blog post text, images, author, and approvals are complete.
- You have access to the content management system.
- You know the intended publish date, category, and audience.

## Steps

1. **Create or open the post draft.** Open the CMS and start a new post or edit the approved draft. → *Expect:* the post editor is open.
2. **Add title and body.** Paste approved title, headings, body copy, and calls to action. → *Expect:* the post content is present and structured.
3. **Add media and alt text.** Upload approved images and add descriptive alt text. → *Expect:* images display correctly and are accessible.
4. **Set metadata.** Add slug, excerpt, category, tags, author, featured image, and SEO fields if used. → *Expect:* listing and search previews are complete.
5. **Check links.** Click or preview internal, external, download, and CTA links. → *Expect:* every link opens the intended destination.
6. **Preview the post.** Review desktop and mobile preview for formatting, media, and embedded content. → *Expect:* the post is readable and visually correct.
7. **Publish or schedule.** ⚠️ *Irreversible:* before publishing, confirm approvals, date, slug, claims, and links because the page may become public and indexed. → *Expect:* the post is live or scheduled.
8. **Record the URL.** Add the final URL to the editorial calendar or campaign tracker. → *Expect:* stakeholders can find the post.

## Decision points

- If approval is missing → leave as draft and request approval.
- If claims are time-sensitive or regulated → verify with the source owner before publishing.
- If the post is embargoed → schedule for the exact release time and time zone.

## Failure modes & recovery

- **F1 Broken formatting:** detect preview issues → fix headings, lists, embeds, or media before publishing.
- **F2 Wrong slug:** detect incorrect URL → update before launch or set redirect after correction.
- **F3 Missing image rights:** detect unapproved media → replace with licensed or owned media.

## Verification

The post is live or scheduled with approved content, correct URL, metadata, images, alt text, and working links.

## Variations

- News post: coordinate exact timing with PR and social teams.
- Technical post: verify code snippets and version references before publishing.
- Guest author: confirm author bio, permissions, and attribution.

## Safety & privacy

Low risk. Do not publish confidential data, unapproved claims, embargoed information, private customer stories, or unlicensed media.
