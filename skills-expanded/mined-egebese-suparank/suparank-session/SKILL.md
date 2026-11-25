---
name: suparank/session
description: Manage saved articles and workflow sessions. Save, load, list, and remove content.
user_invocable: true
---

# Suparank Session Management

You manage the user's content session - saved articles, workflow state, and content storage.

## File Locations

- **Session state:** `.claude/suparank-session.json` (in project root)
- **Saved content:** `.claude/suparank-content/` (in project root)
- **Project config:** `.claude/suparank.json` (in project root)

## Commands

Detect what the user wants and execute the appropriate action:

---

### Show Session Status

**Triggers:** "show session", "session status", "what's in my session", "show my articles"

1. Read `.claude/suparank-session.json`
2. If it doesn't exist, say: "No active session. Create content with `/suparank` to start."
3. If it exists, display:

```
Session Status
══════════════
Workflow: [workflow_id]
Request: [original request]
Phase: [current_phase]
Articles: [saved count] / [total expected]

Articles:
  1. [title] - [word_count] words - [status] - Saved [date]
  2. [title] - [word_count] words - [status] - Saved [date]
  ...

Research: [Available / Not done]
```

---

### List Saved Content

**Triggers:** "list articles", "list saved content", "show past articles", "what articles do I have"

1. Check if `.claude/suparank-content/` directory exists
2. If not, say: "No saved content yet. Create content with `/suparank` to start."
3. If it exists, list all subdirectories (each is a saved article)
4. For each, read `metadata.json` to get title, date, word count

Display:

```
Saved Articles
══════════════
1. 2026-02-23-how-ai-is-changing/
   Title: How AI is Changing Content Marketing
   Words: 2,800 | Keywords: AI content marketing
   Saved: 2026-02-23 10:30

2. 2026-02-23-seo-best-practices/
   Title: SEO Best Practices for 2026
   Words: 3,100 | Keywords: SEO best practices
   Saved: 2026-02-23 11:45
```

---

### Save Article

**Triggers:** "save this article", "save content", "save my article"

This is typically called automatically by the pipeline/create skills, but can be invoked manually.

1. The user should provide or have just written:
   - **title**: Article title
   - **content**: Full article markdown
   - **keywords**: Target keywords (array)
   - **meta_description**: SEO meta description

2. Generate a folder name: `YYYY-MM-DD-slug-from-title`
3. Create the directory: `.claude/suparank-content/[folder-name]/`
4. Write the article to `article.md`
5. Write metadata to `metadata.json`:

```json
{
  "title": "Article Title",
  "slug": "article-title",
  "version": 1,
  "keywords": ["keyword1", "keyword2"],
  "meta_description": "SEO description...",
  "word_count": 2800,
  "saved_at": "2026-02-23T10:30:00Z",
  "updated_at": "2026-02-23T10:30:00Z",
  "published_to": [
    {
      "platform": "wordpress",
      "post_id": "12345",
      "url": "https://myblog.com/article-title",
      "published_at": "2026-02-23T11:00:00Z",
      "status": "draft"
    }
  ],
  "image_urls": [
    {
      "url": "https://fal.ai/...",
      "alt_text": "Article hero image",
      "type": "cover"
    }
  ]
}
```

When updating an existing article, increment `version` and update `updated_at`.

6. Update `.claude/suparank-session.json` to add this article to the articles array:

```json
{
  "workflow_id": "wf_[timestamp]",
  "articles": [
    {
      "id": "article-1",
      "title": "Article Title",
      "folder": ".claude/suparank-content/2026-02-23-article-title/",
      "keywords": ["keyword1"],
      "meta_description": "...",
      "word_count": 2800,
      "status": "saved",
      "published_to": [],
      "image_urls": [],
      "saved_at": "2026-02-23T10:30:00Z"
    }
  ],
  "saved_at": "2026-02-23T10:30:00Z"
}
```

7. Confirm: "Article saved! [title] ([word_count] words) → .claude/suparank-content/[folder]/"

---

### Load Article

**Triggers:** "load article", "open article", "bring back article", "edit my article about..."

1. If the user specifies a folder name or title, find it in `.claude/suparank-content/`
2. If not specified, run "List Saved Content" first and ask them to choose
3. Read `article.md` and `metadata.json` from the folder
4. Load the article into the session by updating `.claude/suparank-session.json`
5. Display the article title and first few lines
6. Say: "Article loaded into session. You can now optimize or publish it."

---

### Remove Article from Session

**Triggers:** "remove article", "delete from session", "remove article 2"

1. Read `.claude/suparank-session.json`
2. If the user specifies a number, remove that article from the session's articles array
3. This does NOT delete the files from `.claude/suparank-content/` - just removes from active session
4. Update the session file
5. Confirm: "Article [title] removed from session. Files still saved in .claude/suparank-content/[folder]/"

---

### Clear Session

**Triggers:** "clear session", "start fresh", "reset session"

1. Ask for confirmation: "This will clear your active session (all article references). Saved files in .claude/suparank-content/ will NOT be deleted. Continue?"
2. If confirmed, delete or reset `.claude/suparank-session.json` to:

```json
{
  "workflow_id": null,
  "articles": [],
  "research_results": {},
  "saved_at": null
}
```

3. Confirm: "Session cleared. Saved content files are still in .claude/suparank-content/"

---

### Delete Saved Content

**Triggers:** "delete article files", "permanently delete", "remove saved files"

1. This PERMANENTLY deletes files from disk
2. Ask for confirmation with the specific folder name
3. If confirmed, delete the folder from `.claude/suparank-content/`
4. Also remove from session if present
5. Confirm: "Permanently deleted [folder]. This cannot be undone."

---

## Session File Schema

The session file `.claude/suparank-session.json` tracks the current workflow:

```json
{
  "workflow_id": "wf_1709234567890",
  "request": "Write 3 articles about AI content tools",
  "current_phase": "creation",
  "total_articles": 3,
  "articles": [
    {
      "id": "article-1",
      "title": "How AI is Changing Content Marketing",
      "folder": ".claude/suparank-content/2026-02-23-how-ai-is-changing/",
      "keywords": ["AI content marketing"],
      "meta_description": "...",
      "word_count": 2800,
      "status": "saved",
      "published_to": [],
      "image_urls": [],
      "saved_at": "2026-02-23T10:30:00Z"
    }
  ],
  "research_results": {
    "keywords": {
      "primary": [
        { "keyword": "AI content tools", "volume": "2.4K", "difficulty": 35, "intent": "commercial" }
      ],
      "longtail": [
        { "keyword": "best AI tools for blog writing", "volume": "720", "difficulty": 18, "content_type": "listicle" }
      ],
      "questions": [
        { "question": "What are the best AI content tools?", "volume": "590", "snippet_opportunity": true }
      ],
      "selected_primary": "AI content tools",
      "selected_secondary": ["AI writing software", "content automation"]
    },
    "seo_strategy": {
      "search_intent": "commercial",
      "content_type": "listicle",
      "recommended_title": "10 Best AI Content Tools in 2026",
      "outline": ["Introduction", "Tool 1...", "Conclusion", "FAQ"]
    },
    "topical_map": {
      "pillar": "AI Content Tools Guide",
      "clusters": ["AI writing tools", "AI SEO tools", "AI image tools"]
    },
    "content_calendar": {
      "articles": [
        { "order": 1, "title": "...", "keyword": "...", "type": "guide" }
      ]
    }
  },
  "saved_at": "2026-02-23T10:30:00Z"
}
```

## Directory Initialization

Before writing ANY files, ALWAYS run:
```bash
mkdir -p .claude/suparank-content
```

This ensures both `.claude/` and `.claude/suparank-content/` exist.

## Important Notes

- Always run directory initialization before any file write operation
- Session is project-scoped (different projects have independent sessions)
- Content folder names use format: `YYYY-MM-DD-slug-from-title`
- Never delete files without explicit user confirmation
- Article status can be: "saved", "published", "draft"
- When updating an article, increment `version` in metadata.json and update `updated_at`
