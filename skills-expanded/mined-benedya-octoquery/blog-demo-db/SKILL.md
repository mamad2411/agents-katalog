---
name: blog-demo-db
description: Query the blog database (authors, posts, comments) through the MCP SQL tool. Use whenever the user asks questions about authors, posts, comments, views, or blog activity — e.g. "how many posts are published?", "most viewed posts", "most commented post", "top authors by views".
---

# Blog database

The database is exposed as the MCP tool **`sql_blog_demo`**. Answer questions by sending a single SQL query string (MySQL dialect) to that tool. Results come back as JSON rows, truncated to the configured row limit (default 100) — use `LIMIT`, aggregation, or `ORDER BY` to keep result sets small and relevant.

## Schema

- **authors** — `id`, `email`, `full_name`, `joined_at`
- **posts** — `id`, `author_id` → authors, `title`, `category` (DevOps, Databases, Programming, Web), `status` (`draft`, `published`, `archived`), `views`, `published_at` (NULL for drafts)
- **comments** — `id`, `post_id` → posts, `commenter` (free-text name, not a registered author), `created_at`, `body`

## Relations

- One author has many posts (`posts.author_id` → `authors.id`).
- One post has many comments (`comments.post_id` → `posts.id`).
- Commenters are anonymous visitors — `comments.commenter` is just a name and does not reference the `authors` table.

## Conventions

- Only `published` posts are publicly visible; exclude `draft` and usually `archived` posts from reader-facing metrics unless asked otherwise.
- `views` is a lifetime counter per post; `published_at` is NULL until a post is published.
- Popularity questions can mean views (`posts.views`) or engagement (comment counts) — pick from context or show both.

## Guidelines

- Treat the database as read-only: stick to `SELECT` unless the user explicitly asks to modify data.
- Prefer one well-formed query over many small ones; use joins and aggregates server-side.
