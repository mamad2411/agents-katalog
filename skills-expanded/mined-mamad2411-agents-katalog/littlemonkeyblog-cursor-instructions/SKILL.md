# LittleMonkeyBlog Workflow

This document describes how to work with this blog using Cursor.

## Creating a New Blog Post

### Method 1: Using the Script (Recommended)
```bash
python3 new_post.py "Your Post Title"
```

With options:
```bash
python3 new_post.py "Your Post Title" --categories "Data Science,Tutorial" --description "A great post"
```

### Method 2: Using Cursor Tasks
1. Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
2. Type "Tasks: Run Task"
3. Select "Create New Blog Post"
4. Enter your post title when prompted

### Method 3: Manual Creation
1. Create a new folder in `posts/` with a URL-friendly name (kebab-case)
2. Create `index.qmd` inside that folder
3. Use the template structure from `posts/example-post/index.qmd`

## Previewing Your Blog

### Using Cursor Tasks
1. Press `Cmd+Shift+P` / `Ctrl+Shift+P`
2. Select "Tasks: Run Task"
3. Choose "Preview Blog (Local)"
4. Your blog will open in your browser at `http://localhost:4200`

### Using Command Line
```bash
quarto preview
```

## Publishing Your Blog

### Quick Publish (Recommended)
1. Press `Cmd+Shift+P` / `Ctrl+Shift+P`
2. Select "Tasks: Run Task"
3. Choose "Quick Publish (Render + Push)"
4. This will render, commit, and push to GitHub
5. GitHub Actions will automatically deploy to GitHub Pages

### Step-by-Step Publish
1. Render: Run "Render Blog" task or `quarto render`
2. Commit: Stage and commit your changes
3. Push: Run "Publish Blog (Git Push)" task or `git push origin main`

## Post Structure

Each post should be in `posts/[slug]/index.qmd` with:

```yaml
---
title: "Your Post Title"
date: "YYYY-MM-DD"
categories: [Category1, Category2]
description: "A brief description"
image: optional-image.png
---
```

## Tips

- Use the example post (`posts/example-post/index.qmd`) as a reference
- Preview locally before pushing
- The blog auto-deploys on push to `main` branch
- Check `.github/workflows/publish.yml` for deployment details

