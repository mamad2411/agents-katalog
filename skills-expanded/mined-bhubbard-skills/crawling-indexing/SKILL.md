---
name: crawling-indexing
description: Guidelines for managing how Google crawls and indexes a website, including sitemaps, robots.txt, and JavaScript SEO.
---

# Crawling and Indexing

Use this skill when the user needs help managing how search engines crawl and index their website, or when debugging indexing issues.

## Key Guidelines

- **Sitemaps**: Provide a sitemap (XML or text) to help Google discover all relevant pages on your site, especially for large sites or sites with isolated pages.
- **robots.txt**: Use a `robots.txt` file to prevent Google from crawling specific pages or directories, but do not use it to hide pages from search results (use `noindex` instead).
- **Meta Tags**: Use `<meta name="robots" content="...">` to control indexing at the page level (e.g., `noindex`, `nofollow`).
- **Canonicalization**: Use `rel="canonical"` link tags to specify the preferred version of a page when duplicate content exists.
- **Redirects**: Implement server-side 301 redirects when permanently moving a page to a new URL.
- **JavaScript SEO**: Ensure that Googlebot can render JavaScript-heavy sites by either using server-side rendering, dynamic rendering, or ensuring client-side rendered content is accessible to crawlers.
