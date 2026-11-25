---
description: Search for posts and content on X, LinkedIn, or Reddit; open YouTube search results via browser URL
user-invocable: true
---

# Search Social Media

Search for posts, topics, and conversations across platforms.

## Workflow

1. **Check connection**
   ```
   socials_check_access
   ```

2. **Get search parameters**
   - Platform: X, LinkedIn, Reddit, or YouTube?
   - Keywords or search query
   - Type: Latest, Top, or People (X only)

3. **Open the platform**
   ```
   socials_open_tab({ url: "[platform URL]" })
   ```

4. **Execute search**

   **On X:**
   ```
   socials_x_search({
     query: "[keywords]",
     type: "Latest" | "Top" | "People"
   })
   ```

   **On LinkedIn:**
   ```
   socials_linkedin_posts_search({ query: "[keywords]" })
   ```
   Or for people:
   ```
   socials_linkedin_people_search({ keywords: "[name or title]" })
   ```

   **On Reddit:**
   Navigate to the subreddit and use:
   ```
   socials_get_feed({ platform: "reddit" })
   ```

   **On YouTube (search in the browser):**
   There is no separate MCP search tool. Build a results URL and open it (URL-encode the query, same idea as `encodeURIComponent`):
   ```
   socials_open_tab({
     url: "https://www.youtube.com/results?search_query=hello+kitty"
   })
   ```
   Use **`socials_navigate`** on the agent tab to change the search. Apply search filters with:
   ```
   socials_apply_search_filters({
     platform: "youtube",
     filters: ["Videos", "This week", "HD"]
   })
   ```
  For a specific video page (`/watch?v=...`), use `socials_get_page_content` to extract video metadata plus comments.

5. **Show results**
   For X, LinkedIn, or Reddit:
   ```
   socials_get_feed({ platform: "[platform]" })
   ```
  For YouTube search results, call **`socials_get_page_content`** (optional **`limit`**, 1–80, default 40) to read **video cards** from the results page.
  For YouTube watch pages, call **`socials_get_page_content`** with optional `comment_sort` (`top` or `newest`) and `comments_limit` to read fresh comments in that order.
   Call **`socials_fetch_image`** for thumbnail URLs only when visual inspection materially improves the answer (comparison/detail checks). If text/URLs are enough, keep image URLs as text to reduce token usage.

6. **Offer next actions**
   - Get more details on a specific post
   - Engage with a post
   - Search with different terms

## Arguments

Provide the search query after the command.

Examples:
- `/socials:search AI startups on X`
- `/socials:search product managers on LinkedIn`
- `/socials:search r/entrepreneur`
