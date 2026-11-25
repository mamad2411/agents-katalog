---
name: adding-a-project
description: Use when adding a new project to the user's personal site and resume, or when the user says to make something "live". Covers updating both arjit-me and arjit-resume, compiling the PDF, and pushing.
---

# Adding a Project

## Overview

When a new project is created, it needs to be added to both the personal site (arjit-me) and the resume (arjit-resume), then made live.

## Locations

- **Site projects**: `~/repos/arjit-me/lib/projects.ts`
- **Resume projects**: `~/repos/arjit-resume/resume/projects.tex`
- **Resume PDF**: `~/repos/arjit-resume/arjit_jaiswal_resume.pdf` (symlinked to `~/Documents/arjit_jaiswal_resume.pdf`)

## Process

1. **Add to `lib/projects.ts`** in arjit-me:
   - Add a new entry to the `projects` array
   - Set `featured: false` unless told otherwise
   - Use the repo slug for `id`, but a human-readable name for `title` on the site is fine either way

2. **Add to `resume/projects.tex`** in arjit-resume:
   - Add a `\projectentry{Name}{url}{description}{tech}{date}`
   - **Always use human-readable names**, not repo slugs (e.g. "Arjit Skills" not "arjit-skills")
   - Keep descriptions concise (one line)
   - Insert in chronological order (newest first)

3. **Compile the resume PDF**:
   ```bash
   cd ~/repos/arjit-resume
   make build
   ```
   The symlink at `~/Documents/arjit_jaiswal_resume.pdf` auto-updates.

4. **Push the site live**:
   ```bash
   cd ~/repos/arjit-me
   git add lib/projects.ts
   git commit -m "Add <project-name> to projects"
   git push origin main
   ```

## Rules

- Resume uses human-readable names; site can use either.
- Always compile the PDF after resume changes.
- Always push arjit-me to main to deploy.
