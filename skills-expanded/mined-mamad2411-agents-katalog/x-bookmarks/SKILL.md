---
name: x-bookmarks
description: Capture, organize, and digest X bookmarks — list and filter saved posts, file them into folders, build reading digests, and prune stale saves. Use when the user mentions their X bookmarks or saved posts.
---

# X Bookmarks

Workflows for the bookmark tools of X's official MCP server. Requires the X
plugin's MCP server to be connected (see the `x` skill, Step 0).

## The one constraint that shapes everything

**X has no bookmark-search endpoint.** There is no server-side way to search
inside bookmarks. To find anything: list bookmarks (paginated), then filter
and rank model-side. Never claim you "searched bookmarks" — you listed and
filtered them. For large collections, say how many pages you scanned.

## Workflows

### Find in bookmarks ("that post I saved about ...")
1. List bookmarks page by page (newest first).
2. Filter model-side against the user's description (topic, author, rough
   date). Stop as soon as confident matches appear.
3. Return matches with `https://x.com/i/status/<post_id>` links. If nothing
   surfaced after a few pages, say how far back you looked and offer to
   continue.

### Capture ("bookmark this / save the best posts about ...")
1. For a URL or post id: bookmark it directly.
2. For "the best posts about X": run a search first (see the `x` skill), show
   the candidates, and bookmark the ones the user confirms — don't mass-save
   unprompted.
3. When a folder for the theme exists, file the bookmark into it; offer to
   create one when a clear new theme emerges.

### Organize ("clean up my bookmarks")
1. List everything, cluster into themes.
2. Propose a folder scheme (5-8 folders beats 30) and show which bookmarks
   land where. Apply on confirmation using the folder tools.
3. Flag duplicates and dead saves for removal — remove only on explicit
   confirmation; bookmark removal has no undo.

### Reading digest ("what's in my bookmarks this week")
1. List recent bookmarks (last 1-2 weeks or the most recent 25-50).
2. Group by theme; summarize each saved post in a line with its link.
3. End with two lists: worth reading in full, and safe to skim or remove.

## Practices

- Bookmarks are private account data — never include them in anything shared
  or published without explicit confirmation.
- Additions and removals are account mutations: confirm before bulk changes;
  single explicit requests need no re-confirmation.
- Cite metrics only from tool output, never from memory.
