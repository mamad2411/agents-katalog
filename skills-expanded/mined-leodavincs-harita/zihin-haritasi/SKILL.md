---
name: zihin-haritasi
description: Turn any content into an interactive mind map (one HTML file). Use for "mind map", "map this", "zihin haritası", "haritala", "harita çiz", or a long answer the user wants at a glance.
license: MIT
---

# Zihin haritası (mind map)

You turn content into an interactive mind map. You write the structure as JSON, the bundled script turns it into a single self-contained HTML page (no internet needed). The user sees the whole thing at a glance and opens details only when they want.

Paths below are relative to the folder that holds this SKILL.md.

## 1. Gather the content

- Default source: what is in this conversation (the topic, a long answer you gave, notes the user pasted, uploaded files).
- If the user asks to map things from earlier chats or "what you know about me", use whatever memory or past-chat search tools you have. If you have none, say so in one sentence and ask them to paste the material.
- Do not invent facts to fill branches. A short honest map beats a full fake one.

## 2. Pick a layout

| `duzen` | Use for |
| --- | --- |
| `harita` | default: report, research, plan, topic overview |
| `mantik` | step-by-step process, decision tree |
| `agac` | team, system parts, folder structure |
| `zaman` | week plan, roadmap, timeline (main branches in order) |
| `kilcik` | "why did this break": root = problem, main branches = causes |
| `matris` | comparison: main branch = row, children = cells |

## 3. Write the JSON

Read `references/bicim.md` once before your first map; it has the full format and a complete example. The keys are Turkish (`kok` = root, `alt` = children, `ad` = name, `not` = note); keep them exactly as written there.

Rules that make a good map:
- Write node text in the user's language.
- Node names are short: at most ~6 words. Everything longer goes into `not` (a string or a list of bullet strings), which opens when the node is clicked.
- 3-7 main branches. Depth 2-4. If a branch has more than ~8 children, group them.
- Root `not`: the one-sentence answer or conclusion, so the map is useful even without clicking.
- Use `isaret` markers sparingly: `karar` (a decision for the user), `kanit` (evidence), `fikir`, `uyari`, `soru`, `tamam`, `oncelik-1`…`oncelik-9`.
- Add `iliskiler` (arrows between distant nodes) only when the link is the point.
- Theme: leave `tema` out (default `beyaz`, clean white) unless the user asks for a look: `pastel` (soft, friendly), `kagit` (warm paper), `koyu` (dark), `gece` / `fosfor` / `amber` (terminal style). The viewer can also switch theme on the page; their choice is remembered.

## 4. Build the page

```
python3 scripts/kur.py <data.json> -o <output.html>
```

- The script checks the data first. If it prints `Veri hatalı:` followed by problems (duplicate id, unknown id, bad range, unknown layout), fix the JSON and run it again.
- Python 3.8+ standard library only; nothing to install.

## 5. Deliver

- **Claude app (claude.ai, desktop):** write the HTML into the outputs folder (`/mnt/user-data/outputs/` when it exists) so the user gets the file to open or download. If you can also show HTML as an artifact, you may show it there.
- **Local agents (Codex, Claude Code):** save next to the user's work (or the current folder) and add `--ac` to open it in the browser. Tell the user the file path.
- Never paste the generated HTML into the chat; it is large. Reply with one or two sentences: what the map shows and where it is.

## PDF

The page has a **PDF** button: page 1 is the map fitted to landscape A4, the following pages list every node with all its details. When the user asks for a PDF:
- Local agents: add `--pdf` to the build command; it writes `<output>.pdf` next to the HTML using Chrome, Chromium or Edge if installed. If none is found the script says so; then tell the user to open the page and press PDF.
- Claude app: try `--pdf` too; if the sandbox has no browser, deliver the HTML and tell the user to press the PDF button and choose "Save as PDF".

## 6. Changes

When the user asks for a change ("merge these two branches", "add a branch for X", "switch to timeline"), edit the same JSON and rebuild to the same output file. Keep `id`s stable so arrows and groups survive.

## When not to use a map

A short answer, a single fact, or text the user will copy and paste (a message, an email, code). Say so and answer normally.
