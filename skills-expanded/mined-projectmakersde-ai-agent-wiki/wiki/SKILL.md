---
name: wiki
description: Read, search and maintain the wiki in docs/wiki, which holds the rules for AI agents and the knowledge about the projects they work on. Use it before a task that needs project knowledge, when the user asks you to document something or to update the wiki, when a decision was made that belongs in the wiki, and when a task changed facts that a wiki page states.
---

# Working with the wiki

The wiki in `docs/wiki/` holds the rules for AI agents and the knowledge about the projects they work on. The binding rules are in `docs/wiki/rules/agent-rules.md`. This skill does not repeat them. If this skill and the rules page disagree, the rules page wins.

Run every command from the root of the repository. If `AGENTS.md` points to a wiki in another folder, such as `../wiki/docs/wiki/`, put that folder in front of `tools/wiki.py` and `docs/wiki/` in every command and path of this skill, for example `python3 ../wiki/tools/wiki.py read INDEX.md`.

## When to use it

- Before a task that needs project knowledge.
- When the user asks you to document something or to update the wiki.
- When a decision was made that belongs in the wiki.
- When your task changed facts that a wiki page states, such as a command, a path or a dependency.

## Reading

Read the pages in the order that `AGENTS.md` gives:

1. `rules/agent-rules.md`
2. `INDEX.md`
3. `projects/README.md`
4. the `README.md` of the one project folder in `projects/` that matches the task

If `tools/wiki.py` exists, read every page with it. The tool logs each read. Do not open wiki files directly to read them.

```bash
python3 tools/wiki.py read rules/agent-rules.md
python3 tools/wiki.py read INDEX.md
python3 tools/wiki.py read projects/README.md
python3 tools/wiki.py read projects/<name>
```

Pages are relative to `docs/wiki/`. You can leave out `.md`. A folder name leads to its `README.md`. If `tools/wiki.py` does not exist, read the files in `docs/wiki/` directly.

Read further pages only when the task needs them. A link to another project is no reason to read its folder. Read reports in `docs/reports/` only when a human points you to them.

## Searching

```bash
python3 tools/wiki.py search <term>
```

All words after `search` form one term. The search ignores case and prints each matching line as `page:line: text`. It skips `docs/wiki/templates/`. Exit code 1 means no hits. Searches without hits are logged too, so a human can see which knowledge is missing. Without `tools/wiki.py`, search `docs/wiki/` with your own search tool.

## When the read gate is active

If `.claude/hooks/read_gate.py` exists, Claude Code blocks Edit, Write, NotebookEdit and shell commands until you have read the required pages. By default these are `rules/agent-rules.md`, `INDEX.md` and `projects/README.md`. The list is at the top of the hook script.

- Read the required pages before any other shell command.
- A page counts as read only with a command of exactly the form `python3 tools/wiki.py read <page>`. Use one page per command. Add no options, no pipes, no redirections and no `&&`. Do not run it in the background.
- A Read of the whole page file counts as well. Do not use `offset` or `limit`.
- A read counts only when it succeeded. If `wiki.py read` fails, read the page with the Read tool and tell the user what failed.
- Other plain calls of `tools/wiki.py` without options, such as `search`, are allowed before reading. They do not count as read. Calls with options such as `--wiki` or `--log` wait until the required pages are read.
- If the gate blocks a step, its message names the pages that are still missing.

## Writing

The section "Writing knowledge back" in `rules/agent-rules.md` is binding. In practice:

1. Search first. Extend an existing page before you create a new one.
2. Keep one topic per page. Rules go to `rules/`. Knowledge about a project goes to its folder in `projects/`.
3. Create a new page from `docs/wiki/templates/page.md` and replace every placeholder. The header needs three fields:

   ```yaml
   ---
   title: Short title
   verified: 2026-09-25
   source: Where the statements come from
   ---
   ```

   Set `verified` to the date on which you checked the content against reality. Name in `source` where the statements come from, such as a file in the code or an agreement with a person. Write only what you checked. When you change facts on an existing page, update both fields.
4. Use relative Markdown links such as `[Title](../folder/page.md)`. Do not use wikilinks in double square brackets or absolute paths.
5. Link every new page from its parent page. A new project also gets a row in `projects/README.md`.
6. Keep a page under 8000 characters. If it grows longer, move details to a page one level down and link to it.
7. Never write a secret. Name only where a secret lives, as `rules/secrets.md` describes.

Read a page before you change it. Then edit its file in `docs/wiki/`. If your edit tool has to open the file first, that is fine.

Dated documents, such as an analysis or an audit, do not go into the wiki. They go to `docs/reports/` with a file name like `2026-09-25-topic.md`. What stays valid from a report belongs in the wiki, and the report links to the wiki page.

A human reviews and approves every wiki change in a pull request. The rules page says which pull request it belongs in.

## After writing

If `tools/wiki.py` exists, run:

```bash
python3 tools/wiki.py check
```

The last line must say `0 errors`. The check reports missing header fields, broken or absolute links, wikilinks, pages over the budget and lines that look like a secret. Fix every error and run the check again. Without the tool, check the header and the links of each page you changed by hand.

## Maintenance

```bash
python3 tools/wiki.py stats
```

It shows how often each page was read, which pages were never read and which searches found nothing. A page that is never read is either superfluous or badly linked. A search term without hits points to knowledge that is missing. A page with an old `verified` date is a reason to check it. Suggest fixes in your report, such as a missing link or a new page. A human decides.
