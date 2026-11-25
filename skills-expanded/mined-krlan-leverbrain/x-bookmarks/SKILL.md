---
name: X bookmarks
tagline: Local self-custody bookmarks syncing and long-form article extractor.
description: Archive and enrich your bookmarked X posts and long-form articles. Resolves scrambled images and missing text by extracting from the GraphQL API directly with active cookies and mapping Draft.js blocks.
author: santa
creatorWallet: Fd983Npa5kCh1WohgZ4xJj95EUefGxwyBEfXHbBYhBZh
price: "$9.99"
priceUsdc: 9.99
category: skill
tags:
  - archival
  - indexing
  - scraper
  - knowledge
whenToUse: Use this skill when compiling or indexing long-form X posts, media attachments, and articles into a local markdown library.
---

# X Bookmarks - Knowledge Archival & Article Enrichment

End-to-end local knowledge archiving workflow for X (Twitter) bookmarks and articles. Resolves limitations of the standard Field Theory CLI, particularly the link-only constraint bug and missing/scrambled images, by querying the X GraphQL API directly with active cookies and mapping Draft.js blocks to download and embed local media files in the correct positions.

## When to Apply

This Skill should be used when the task involves **syncing, indexing, searching, or archiving X bookmarks, especially when extracting long-form X Articles with images**.

### Must Use

This Skill must be invoked in the following situations:
- Setting up a local, private knowledge base of bookmarked X/Twitter posts.
- Resolving the "scrambled images" or "missing text" issues on X Article syncs.
- Extracting long-form X Articles (`/i/article/...`) that have user commentary on X (which bypasses standard Field Theory enrichment).
- Rebuilding or formatting the local markdown glossary, monthly statistics, or search indexes.

### Skip

This Skill is not needed in the following situations:
- Bookmarks from non-X sources (e.g. browser bookmarks, pocket, instapaper).
- Fetching single public tweets without media or long-form articles.

---

## Prerequisites

Ensure the following tools are installed on the local system:

1. **Node.js** (for running the Field Theory CLI)
2. **SQLite3** (for querying the local database)
3. **Python 3** (for running custom GraphQL enrichment and library compiler scripts)

---

## How to Use This Skill

### Step 1: Install Field Theory CLI

To install the self-custody bookmarks CLI tool globally:

```bash
npm install -g fieldtheory
```

---

### Step 2: Authenticated Bookmarks Sync

Because sandboxed/headless terminal sessions cannot access browser keychains to retrieve session tokens, you must manually supply your active X session cookies. 

#### 1. Retrieve Cookies from Browser (e.g., Brave or Chrome)
1. Open your browser and go to `https://x.com` (ensure you are logged in).
2. Open Developer Tools (`F12` or `Cmd + Option + I`).
3. Go to the **Application** (or **Storage**) tab, select **Cookies**, and click on `https://x.com`.
4. Copy the values of the following two cookies:
   - `ct0` (CSRF token, a long hex string)
   - `auth_token` (active authentication token, a long hex string)

#### 2. Run the Sync Command
Execute the sync using the raw values (do not prefix them with names like `ct0=`; pass only the raw values separated by a space):

```bash
npx fieldtheory sync --rebuild --yes --cookies <csrfToken> <authToken>
```

> [!CAUTION]
> **Positional Trap:** Field Theory parses cookie arguments positionally. Do not pass labels like `ct0=value`. Only supply the raw token values: `--cookies csrfTokenValue authTokenValue`.

---

### Step 3: Direct GraphQL Article Enrichment (The Hybrid Scraper)

Standard Field Theory sync has a known bug: it only enrich X Articles if a bookmark is "link-only" (contains less than 80 characters of text commentary). If you wrote an introductory summary, it skips it. Furthermore, it only pulls plain text and completely ignores inline and cover images.

To solve this, run a custom enrichment script that connects directly to the authenticated GraphQL endpoint:

```bash
python3 -u scripts/enrich_all_articles.py
```

This custom script performs the following actions:
1. Queries `/Users/shark/.fieldtheory/bookmarks/bookmarks.db` for bookmarks containing `/i/article/` in `links_json`.
2. Resolves status IDs to X's internal GraphQL endpoint: `https://x.com/i/api/graphql/fHLDP3qFEjnTqhWBVvsREg/TweetResultByRestId`.
3. Parses the returned Draft.js `content_state` blocks (unstyled, header-one, blockquote, atomic) and inline formatting styles.
4. Detects media entities, downloads images locally to `bookmarks_library/images/<tweet_id>-<mediaId>.jpg`, and maps them to their exact visual layout locations.
5. Updates both the SQLite `bookmarks` table and the `bookmarks.jsonl` cache file.

---

### Step 4: Compile the Local Wiki & Glossary

Once articles are enriched, compile the central index and generate the individual markdown wiki files:

```bash
python3 scripts/build_library.py
```

This generates:
- Individual markdown files for each bookmark under `bookmarks_library/bookmarks/` with formatted headers, text, and correctly aligned inline local images (`![Image](../images/<filename>.jpg)`).
- A central `README.md` containing an indexed Glossary Table of all bookmarks and a monthly ASCII bar chart of your bookmarking activity.

---

## Pre-Delivery Checklist

Before finalizing any bookmarks library updates, verify these items:

- [ ] `.gitignore` contains `/bookmarks_library/` and `/Users/shark/.fieldtheory/` to keep all synced data 100% local.
- [ ] Every article has its cover image and inline images downloaded to `/bookmarks_library/images/`.
- [ ] Image paths in the exported markdown files are relative (e.g. `../images/<filename>.jpg`).
- [ ] Run `npx fieldtheory index` to rebuild the FTS5 search index, enabling fast keyword searches.
