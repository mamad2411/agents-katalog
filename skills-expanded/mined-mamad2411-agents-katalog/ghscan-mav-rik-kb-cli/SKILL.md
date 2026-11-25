# kb — Agent Instructions

You have access to a persistent wiki via the `kb` CLI.

## What the wiki is

The wiki is a **graph of interlinked markdown notes**, synthesized and cross-referenced by prior conversations. Pages are connected because some earlier session recognized them as related — those links are pre-computed reasoning you can follow.

- To **answer a question**: don't read one page. Find seed pages via search, then traverse the link graph (follow `--links`, run `kb related`) until you have enough context. Context comes from the network, not the node.
- To **add knowledge**: don't just store text. Decompose it into atomic pages and connect them to existing ones — both outgoing links AND incoming links from related pages. A page with no incoming links is invisible.

The wiki compounds: every good synthesis filed back becomes a new seed for future questions.

## When to use

- User asks to **remember/store** something → use ingest workflow
- User asks to **recall/find** something → use search workflow
- User provides **new information** → use ingest workflow
- User asks to **organize/clean up** memory → use lint workflow

## Quick reference

Square brackets `[...]` mark optional flags. Pipes `a|b|c` mark exclusive choices. Short aliases shown after the long form, e.g. `--limit, -n`.

### Global flag

Most commands accept:

- `--wiki, -w <name>` — target a specific wiki. If omitted, uses the project default (from `kb.config.json`) or the global default.

### Search & retrieval

```bash
kb search "<query>" [--limit, -n N] [--mode, -m hybrid|fts|vec] [--format json] [--wiki, -w <name>]
    # Default: limit 10, mode hybrid (semantic + keyword via Reciprocal Rank Fusion).
    # --mode fts: keyword only — fast, no embedding model load. Use for exact terms / identifiers.
    # --mode vec: semantic only. Use for conceptual questions.
    # --format json: machine-parseable output.

kb related <id> [--limit, -n N] [--format json] [--wiki, -w <name>]
    # Semantically nearest neighbors to <id>. Default limit 10.
```

### Reading

```bash
kb read <filename>                          # full document (alias: kb get)
kb read <filename> --lines, -l 1-80         # chunked reading by line range
kb read <filename> --meta, -m               # frontmatter only, as JSON
kb read <filename> --links                  # list outgoing links from this doc
kb read <filename> --follow, -f ./other.md  # follow a link and return the linked doc
kb read <filename> --raw                    # literal file bytes — pipe-safe (no header, no line numbers)

kb resolve <arg> [--format json]            # any handle form → canonical id + filename
    # Returns: id, filename, exists, title?, category?, suggestions[] (fuzzy matches if no exact hit).
    # Use when `kb read`/`kb update`/etc. say "not found" — the suggestions tell you the real id.
```

**Doc handles accept any form.** `read`, `update`, `delete`, `rename`, `related`, `reindex`, `resolve` all accept: bare id (`foo`), filename (`foo.md`), markdown-link form (`./foo.md`), full path, or any case. Internally all forms collapse to the canonical lowercase id — same effect on every call.

### Writing

```bash
kb add --title, -t "<title>" --category, -c <cat> [--tags <t1,t2>] \
       (--content "<body>" | --body "<body>" | --text "<body>" | --file <path> | --stdin) \
       [--dry-run] [--format json] [--wiki, -w <name>]
    # --content has aliases --body and --text (same thing).
    # Exactly one of --content / --file / --stdin is required.
    # Always surfaces per-doc lint warnings in the response.
    # --dry-run: lint only — no write, no index touch. Use to iterate on
    #   content shape before the doc enters retrieval.

kb update <id> [--title, -t "<new>"] [--category, -c <c>] [--tags "<t1,t2>"] \
               (--content "<full replacement>" | --append "<more>") \
               [--section "<heading>"] \
               [--set <key=value>] [--add-to <key=value>] \
               [--dry-run] [--format json] [--wiki, -w <name>]
    # --append vs --content: append adds; content replaces.
    # --section "<heading>" scopes --content/--append/--stdin to a single H1-H6 section
    #   (case-insensitive heading match). The heading line stays; only the section body
    #   changes. Errors on missing or ambiguous heading. Mutually exclusive with --file
    #   and with --set/--add-to.
    # --set sets one frontmatter field; --add-to appends to an array field (idempotent).
    #   Valid keys: title, category, tags, important_sections, suppress_merge_warn, suppress_lint.
    #   Value is JSON-parsed when possible, else literal string. One key per invocation.
    # With NO content flags at all, kb re-reads the file from disk and re-indexes that doc.
    # Always surfaces per-doc lint warnings in the response.
    # --dry-run: lint only — preview the merged doc without writing.

kb delete <id> [--wiki, -w <name>]
kb rename <old-id> <new-id> [--wiki, -w <name>]    # auto-updates all links pointing to <old-id>
```

### Browsing

```bash
kb list [--category, -c <c>] [--tag <t>] [--format json] [--wiki, -w <name>]
kb categories [--wiki, -w <name>]            # all categories in use
kb toc [--wiki, -w <name>]                   # table of contents grouped by category
```

### Maintenance

```bash
kb lint [--fix] [--format json] [--wiki, -w <name>]
    # Reports: broken links, orphans, missing frontmatter, drift,
    #          long-paragraph, doc-too-short, doc-too-long, chunk-merge (retrievability).
    # --fix: auto-repair broken links + drift (orphans need manual handling).
    # --format json: machine-parseable output (issues + fixed count).

kb reindex [--wiki, -w <name>]               # drop and rebuild index, FTS, embeddings from MD files
kb schema [--wiki, -w <name>]                # show wiki schema (structure, conventions, categories)
kb schema update [--wiki, -w <name>]         # regenerate schema (run after structural changes)
```

### Activity log

```bash
kb log [--limit, -n N] [--wiki, -w <name>]   # recent activity (default 20 entries)

kb log add --op, -o <type> [--doc, -d <id>] [--details, -m "<text>"] [--wiki, -w <name>]
    # <type> is one of: ingest | query | lint | note
    # Use after completing an agent session to record what was done and why.
```

### Wikis

```bash
kb wiki list                       # all wikis (local + attached remote), default marked
kb wiki create <name>              # create a new local wiki
kb wiki use <name>                 # set as default
kb wiki info <name>                # show counts, paths, recent activity
kb wiki delete <name> [--force, -f]   # --force required to delete the default wiki
```

### Config

```bash
kb config list
kb config get <key>
kb config set <key> <value>
```

### Remote wikis (HTTP-backed)

```bash
kb remote list
kb remote add <name> --url <http://host:port> [--secret <shared-secret>]
kb remote remove <name>                          # unregister (remote data preserved)
kb remote connect <name>                         # health check
kb remote wikis <name>                           # list wikis on the remote
kb remote attach <kb> <wiki> [--alias, -a <local-name>]
kb remote detach <name>
kb remote create-wiki <kb> <wiki> [--alias, -a <local-name>]
kb remote delete-wiki <kb> <wiki> --force        # destructive — --force required
```

Once attached, remote wikis are addressed by name (or alias) like local ones — every command above accepts `--wiki <name>` against them transparently.

### Server (to share this KB with remotes)

```bash
kb serve [--port, -p 4141] [--secret <shared-secret>]
    # Default port 4141. --secret enables Bearer-token access control (clients pass --secret on `kb remote add`).
```

### Skill / instructions

```bash
kb skill                          # this document (full agent instructions)
kb skill ingest                   # detailed ingest workflow
kb skill search                   # detailed search workflow
kb skill update                   # detailed update workflow
kb skill lint                     # detailed lint/maintenance workflow
```

## Key principles

1. **Search before adding** — avoid duplicates
2. **Cross-link aggressively** — use `[text](./other-doc.md)` format
3. **After every mutation, check related docs** — fix contradictions/outdated info
4. **One concept per doc, ~200-1500 words** — atomic, searchable units. Below 200 the centroid embedding is noisy; above 1500 split into linked sub-docs.
5. **Write for chunked retrieval** — docs are split by H2/H3 heading and each chunk is searched independently. Trivial sections (under ~160 chars, or >50% link syntax) auto-merge into the previous chunk. See `kb skill update` for chunking-aware authoring and frontmatter opt-outs (`important_sections`, `suppress_merge_warn`, `suppress_lint`).
6. **Categories are free-form** — run `kb categories` to discover existing ones
7. **Update schema after changes** — `kb schema update`

## Workflows

Run `kb skill ingest`, `kb skill search`, `kb skill update`, or `kb skill lint` for detailed workflow instructions.
