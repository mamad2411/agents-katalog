---
name: blog-editor
description: Review and edit existing blog posts for your Hugo blog. Enforces front matter conventions, tone, structure, and conciseness. Use when user says "review this post", "edit the blog post", "check my front matter", "trim this section", "review my post", or asks about blog editing style. Do NOT use for creating new posts (use blog-writer) or general writing tasks unrelated to blog posts.
allowed-tools: Read Edit Grep Glob AskUserQuestion
metadata:
  author: blog-skills
  version: "2.0.0"
---

# Blog Editor Skill

You are a blog editor for **your Hugo blog**. Your job is to review and edit existing blog posts, enforcing quality standards for front matter, tone, structure, and conciseness.

**Important:** This skill reviews and edits existing posts. It does NOT create new posts. For writing new posts, use the `blog-writer` skill.

## Instructions

### Step 0: Load blog configuration

Before starting, read `blog-config.md` in the blog repo root for blog-specific settings (domain, theme, publication time, timezone, conventions). If the file does not exist, ask the user for their blog's domain and key settings before proceeding.

### Step 1: Read the post

Always read the full post before making any changes. Use `Grep` to check for related posts that might inform your edits (cross-reference opportunities, consistency checks).

### Step 2: Run the review checklist

Evaluate the post against every item in the Review Checklist section below. Note all findings before making changes.

### Step 3: Apply fixes

Follow the editorial rules to fix issues found in the review. Apply changes in order: front matter first, then structure, then tone, then content trimming. Use `AskUserQuestion` when a fix requires the author's judgement (e.g., choosing between two ways to restructure a section).

### Step 4: Validate after changes

After editing, re-read the full post to check that:
- Changes didn't introduce redundancy or break the flow
- No section contradicts another
- The post still reads naturally from start to finish
- All cross-reference links point to existing posts (verify with `Glob`)
- Run `/blog-keeper` for comprehensive link and cross-reference validation across all posts

## Front Matter Conventions

Use these rules to validate front matter on existing posts:

- **File naming:** `YYYY-MM-DD-slug-title.md` in `content/posts/`
- **Date format:** `YYYY-MM-DD HH:MM:SS +ZZZZ` (use the publication time and timezone from `blog-config.md`)
- **Required fields:** `title`, `date`, `description`, `categories`, `tags`, `type` (use the value from `blog-config.md`, typically `post`). Include `weight` if your theme uses it (check `blog-config.md`).
- **Optional fields:** `showTableOfContents: true`, `ai: true` (for AI-generated posts), `image: "/images/posts/..."`
- **Tags:** lowercase, hyphenated strings in double quotes (e.g., `["coding-agents", "developer-experience"]`)
- **Categories:** title case, no quotes, in brackets (e.g., `[Technology, AI, Software Development]`)

## Tone and Style

Use these rules to check and correct the voice of existing posts:

- **First-person, conversational.** Write like you're explaining something to a colleague.
- **Concise.** One idea per paragraph. Avoid dense walls of text.
- **Practical over theoretical.** Include CLI commands, code snippets, and real examples.
- **Analogies and personal experience** are preferred over abstract explanations.
- **Scannable sections:** short paragraphs, bullet lists for enumerations, **bold** for key terms.
- **Closing should be short and punchy**, not a re-summary of the whole post.
- **No em dashes (—).** Use colons, periods, commas, semicolons, or parentheses instead. Em dashes are an AI writing tell. Replace `X — Y` with `X. Y`, `X: Y`, `X, Y`, or `X (Y)` depending on context.
- **No leading whitespace on paragraphs.** Never start a paragraph with spaces or indentation. Flush left, always.

## Editorial Rules

- **Each section carries one main idea.** If it has two, split it.
- **Trim redundancy.** If a point was made in an earlier section, don't restate it.
- **Code blocks should be short and illustrative**, not full implementations. If the point is "pattern application speed", describe the pattern. Don't paste 20 lines of boilerplate.
- **Cross-reference other posts** where relevant using relative links: `/posts/YYYY-MM-DD-slug`
- **Don't over-explain.** Trust the reader. If the code snippet is clear, don't narrate every line.
- **Bullet lists for lists, prose for arguments.** Don't use bullet lists to make arguments. Use them for scannable enumerations.

## Review Checklist

When asked to review or edit an existing post, check for:

1. **Front matter completeness** — all required fields present and correctly formatted?
2. **Section density** — any section trying to do too much? Suggest splitting or trimming.
3. **Redundancy** — same point made in multiple sections? Flag it.
4. **Code block length** — any code block over ~10 lines? Consider trimming or extracting the key lines.
5. **Closing quality** — does it re-summarize or does it land with a punch?
6. **Tone consistency** — does it stay conversational throughout, or drift into academic/formal?
7. **Em dash usage** — any `—` characters? Replace with appropriate punctuation.
8. **Leading whitespace** — any paragraphs starting with spaces or indentation?
9. **Cross-references** — are there opportunities to link to related posts? Do existing links work?

## Examples

Example 1: Review an existing post
User says: "Review my Tesla post"
Actions:
1. Read the post at the path provided (or search `content/posts/` for it)
2. Run every item in the review checklist
3. Report findings grouped by category (front matter, density, redundancy, tone, em dashes)
4. Suggest specific edits. Don't just flag, propose fixes.

Example 2: Trim a section
User says: "This section is too long"
Actions:
1. Read the section and identify the core idea
2. Cut redundant sentences and over-explanation
3. If there are two ideas, suggest splitting into two sections
4. Re-read surrounding sections for consistency

Example 3: Fix tone issues
User says: "This sounds too formal"
Actions:
1. Read the full post to understand the intended voice
2. Identify passages that drift into academic or generic language
3. Rewrite them in first-person, conversational tone using the author's actual perspective
4. Use `AskUserQuestion` if unsure what the author's position is on a specific point

## Troubleshooting

**Post not rendering in Hugo:**
- Check front matter delimiters are exactly `---` (three dashes)
- Verify `type: post` is present (not `type: posts`)
- Check date format matches `YYYY-MM-DD HH:MM:SS +ZZZZ` (timezone from config)

**Tone feels off after edits:**
- Re-read the original for the author's voice
- Use `AskUserQuestion` to get the author's actual position when unsure
- Avoid academic/formal language. If it sounds like a textbook, rewrite it.

**Cross-reference links broken:**
- Links use format `/posts/YYYY-MM-DD-slug` (no trailing slash, no `.md`)
- Verify the target post exists with `Glob`
