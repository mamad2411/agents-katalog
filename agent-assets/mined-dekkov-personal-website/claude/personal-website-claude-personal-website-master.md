# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## AI Guidance

* Ignore GEMINI.md and GEMINI-*.md files
* To save main context space, for code searches, inspections, troubleshooting or analysis, use code-searcher subagent where appropriate - giving the subagent full context background for the task(s) you assign it.
* After receiving tool results, carefully reflect on their quality and determine optimal next steps before proceeding. Use your thinking to plan and iterate based on this new information, and then take the best next action.
* For maximum efficiency, whenever you need to perform multiple independent operations, invoke all relevant tools simultaneously rather than sequentially.
* Before you finish, please verify your solution
* Do what has been asked; nothing more, nothing less.
* NEVER create files unless they're absolutely necessary for achieving your goal.
* ALWAYS prefer editing an existing file to creating a new one.
* NEVER proactively create documentation files (*.md) or README files. Only create documentation files if explicitly requested by the User.
* When you update or modify core context files, also update markdown documentation and memory bank
* When asked to commit changes, exclude CLAUDE.md and CLAUDE-*.md referenced memory bank system files from any commits. Never delete these files.

## Memory Bank System

This project uses a structured memory bank system with specialized context files. Always check these files for relevant information before starting work:

### Core Context Files

* **CLAUDE-activeContext.md** - Current session state, goals, and progress (if exists)
* **CLAUDE-patterns.md** - Established code patterns and conventions (if exists)
* **CLAUDE-decisions.md** - Architecture decisions and rationale (if exists)
* **CLAUDE-troubleshooting.md** - Common issues and proven solutions (if exists)
* **CLAUDE-config-variables.md** - Configuration variables reference (if exists)
* **CLAUDE-temp.md** - Temporary scratch pad (only read when referenced)

**Important:** Always reference the active context file first to understand what's currently being worked on and maintain session continuity.

### Memory Bank System Backups

When asked to backup Memory Bank System files, you will copy the core context files above and @.claude settings directory to directory @/path/to/backup-directory. If files already exist in the backup directory, you will overwrite them.

## Project Overview

This repository contains two portfolio website projects:

### Main Project: `/portfolio/` (Next.js 16)
Active personal portfolio website built with Next.js App Router, TypeScript, and Tailwind CSS.

**Tech Stack:**
- Next.js 16 with App Router
- TypeScript
- Tailwind CSS
- React 19
- MDX for content (blog posts & projects)
- Radix UI components
- Resend (email service)
- Upstash Redis (rate limiting)
- Vercel Analytics

**Architecture:**
```
portfolio/
├── app/                    # Next.js App Router
│   ├── api/               # API routes (contact, track, download-resume)
│   ├── blog/              # Blog pages (dynamic routes)
│   ├── projects/          # Project pages (dynamic routes)
│   ├── about/             # About page
│   ├── contact/           # Contact page
│   ├── experience/        # Experience page
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page
├── components/            # React components (organized by feature)
│   ├── blog/
│   ├── contact/
│   ├── layout/
│   ├── mdx/
│   ├── projects/
│   └── ui/
├── content/              # Content files (file-based CMS)
│   ├── blog/*.mdx        # Blog posts (frontmatter + markdown)
│   ├── projects/*.mdx    # Project case studies
│   └── data/
│       ├── experience.json    # Work history
│       └── skills.json        # Skills by category
├── lib/                  # Utilities
│   ├── mdx.ts           # MDX processing & frontmatter parsing
│   ├── email.ts         # Email sending (Resend)
│   ├── validation.ts    # Zod schemas
│   └── utils.ts         # Helper functions
├── types/               # TypeScript types
│   ├── project.ts
│   ├── blog.ts
│   └── experience.ts
└── public/              # Static assets
    └── images/
        ├── projects/    # Project images
        ├── blog/        # Blog cover images
        └── companies/   # Company logos
```

**Content Management:**
- Blog posts and projects are MDX files with frontmatter
- Work experience and skills are JSON files
- Reading time is auto-calculated for blog posts
- Projects can be marked as `featured: true` to appear on homepage

**API Routes:**
- `POST /api/contact` - Contact form submission (sends email via Resend)
- `POST /api/track` - Custom analytics event tracking
- `GET /api/download-resume` - Resume download with tracking

### Secondary Project: `/Build Complete Portfolio App/` (Vite + React)
React portfolio built with Vite and shadcn/ui components. Appears to be an alternative/legacy version.

## Development Commands

### Portfolio (Main Project)
All commands must be run from the `/portfolio/` directory.

```bash
cd portfolio

# Development
npm run dev          # Start dev server at http://localhost:3000
npm run build        # Create production build
npm run start        # Start production server
npm run lint         # Run ESLint
npm run type-check   # Check TypeScript types without emitting files

# Adding Content
# 1. Blog post: Create /content/blog/my-post.mdx with frontmatter
# 2. Project: Create /content/projects/my-project.mdx with frontmatter
# 3. Experience: Edit /content/data/experience.json
# 4. Skills: Edit /content/data/skills.json
```

### Build Complete Portfolio App (Vite Project)
Run from `/Build Complete Portfolio App/` directory.

```bash
cd "Build Complete Portfolio App"

npm run dev          # Start Vite dev server
npm run build        # Build for production
```

## Environment Variables

The portfolio project requires these environment variables (in `/portfolio/.env` or `.env.local`):

```bash
# Required for contact form
RESEND_API_KEY=re_xxxxxxxxxxxxx
CONTACT_EMAIL=your-email@example.com

# Optional
NEXT_PUBLIC_SITE_URL=http://localhost:3000
UPSTASH_REDIS_REST_URL=https://...
UPSTASH_REDIS_REST_TOKEN=...
```

## Code Patterns & Conventions

### MDX Content Structure
Blog posts and projects use frontmatter for metadata:

```yaml
---
# Blog Post
slug: "post-slug"
title: "Post Title"
excerpt: "Summary (160 chars)"
publishedAt: "2024-10-27"
tags: ["React", "TypeScript"]
category: "Tutorial"
featured: true

# Project
slug: "project-slug"
title: "Project Name"
description: "One-line impact statement"
tldr: ["Key outcome 1", "Key outcome 2"]
role: "Developer"
teamSize: 1
duration: "2 months"
timeline:
  start: "2024-08-01"
  end: "2024-10-01"
tags: ["Next.js"]
domain: ["Web Development"]
featured: true
publishedAt: "2024-10-27"
---
```

### Component Organization
- UI components in `/components/ui/` (Radix UI based)
- Feature components in `/components/[feature]/`
- Shared components in `/components/shared/`
- Page-specific components in `/components/pages/`

### Type Definitions
TypeScript types are organized in `/types/` directory by domain (project, blog, experience).

### Styling
- Tailwind CSS with custom configuration in `tailwind.config.ts`
- Global styles in `app/globals.css`
- Use `cn()` utility from `/lib/utils.ts` for conditional classes

### MDX Processing
- MDX files are processed server-side using `next-mdx-remote`
- Syntax highlighting via `rehype-pretty-code` with Shiki
- Reading time calculated automatically with `reading-time` package
- Frontmatter parsed with `gray-matter`

## Documentation References

For detailed content management instructions, refer to:
- `/portfolio/CONTENT_MANAGEMENT.md` - Complete guide for adding/modifying content
- `/portfolio/README.md` - Project setup and deployment guide



## ALWAYS START WITH THESE COMMANDS FOR COMMON TASKS

**Task: "List/summarize all files and directories"**

```bash
fd . -t f           # Lists ALL files recursively (FASTEST)
# OR
rg --files          # Lists files (respects .gitignore)
```

**Task: "Search for content in files"**

```bash
rg "search_term"    # Search everywhere (FASTEST)
```

**Task: "Find files by name"**

```bash
fd "filename"       # Find by name pattern (FASTEST)
```

### Directory/File Exploration

```bash
# FIRST CHOICE - List all files/dirs recursively:
fd . -t f           # All files (fastest)
fd . -t d           # All directories
rg --files          # All files (respects .gitignore)

# For current directory only:
ls -la              # OK for single directory view
```

### BANNED - Never Use These Slow Tools

* ❌ `tree` - NOT INSTALLED, use `fd` instead
* ❌ `find` - use `fd` or `rg --files`
* ❌ `grep` or `grep -r` - use `rg` instead
* ❌ `ls -R` - use `rg --files` or `fd`
* ❌ `cat file | grep` - use `rg pattern file`

### Use These Faster Tools Instead

```bash
# ripgrep (rg) - content search 
rg "search_term"                # Search in all files
rg -i "case_insensitive"        # Case-insensitive
rg "pattern" -t py              # Only Python files
rg "pattern" -g "*.md"          # Only Markdown
rg -1 "pattern"                 # Filenames with matches
rg -c "pattern"                 # Count matches per file
rg -n "pattern"                 # Show line numbers 
rg -A 3 -B 3 "error"            # Context lines
rg " (TODO| FIXME | HACK)"      # Multiple patterns

# ripgrep (rg) - file listing 
rg --files                      # List files (respects •gitignore)
rg --files | rg "pattern"       # Find files by name 
rg --files -t md                # Only Markdown files 

# fd - file finding 
fd -e js                        # All •js files (fast find) 
fd -x command {}                # Exec per-file 
fd -e md -x ls -la {}           # Example with ls 

# jq - JSON processing 
jq. data.json                   # Pretty-print 
jq -r .name file.json           # Extract field 
jq '.id = 0' x.json             # Modify field
```

### Search Strategy

1. Start broad, then narrow: `rg "partial" | rg "specific"`
2. Filter by type early: `rg -t python "def function_name"`
3. Batch patterns: `rg "(pattern1|pattern2|pattern3)"`
4. Limit scope: `rg "pattern" src/`

### INSTANT DECISION TREE

```
User asks to "list/show/summarize/explore files"?
  → USE: fd . -t f  (fastest, shows all files)
  → OR: rg --files  (respects .gitignore)

User asks to "search/grep/find text content"?
  → USE: rg "pattern"  (NOT grep!)

User asks to "find file/directory by name"?
  → USE: fd "name"  (NOT find!)

User asks for "directory structure/tree"?
  → USE: fd . -t d  (directories) + fd . -t f  (files)
  → NEVER: tree (not installed!)

Need just current directory?
  → USE: ls -la  (OK for single dir)
```
