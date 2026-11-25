---
name: doc-language-conversion
description: De-bilingualize markdown docs or merge EN/CN READMEs.
metadata:
  source_frontmatter:
    tags:
    - docs
    - chinese
    - translation
    - markdown
    - bilingual
    - readme
  imported_from: hermes
---

# Doc Language Conversion (去双语化 / 文档语言统一)

Convert markdown docs between languages for this user: strip duplicate English from bilingual docs (中文正文 + 英文重复段), translate remaining English prose/tables, merge separate EN/CN README files into one with anchor links. The user's projects routinely carry 中英对照 content (docs/, README, reports) and periodically ask to unify to one language.

## When to Use

- User says "docs里面的所有文档用中文写" / "translate X to Chinese" / "这些文档呢（还有英文吗）"
- User asks to merge `README.md` + `README.zh-CN.md` into one file with click-to-jump links
- Any repo doc pass where bilingual duplicate paragraphs must be collapsed to one language

## Workflow: De-bilingualize a Markdown Doc

1. **Inventory first** — list all `*.md` under the target dir; check each file's first lines. Many docs LOOK Chinese (Chinese H1) but the body is bilingual: every Chinese paragraph is followed by a full English translation. Don't assume from the title.
2. **Scan for English prose** (see `scripts/scan_english_prose.py`) — find lines that are mostly Latin letters outside code fences/tables/lists. Also catch blockquote lines (`>`-prefixed).
3. **Delete English duplicate paragraphs** that follow a Chinese translation. Keep: code blocks, JSON examples, field names, technical identifiers (`VLMOutput`, `HeteroData`, IoU), and English titles in parens `(Ground Truth Format Analysis)` — these are references, not prose.
4. **Translate the rest** — table Description columns, blockquote notes, section intros that have no Chinese counterpart. Keep the doc's established bilingual-title style: `## 标题 (English Title)`.
5. **Verify** — re-run the scan; expect zero prose hits. Check code-fence pairing (`grep -c '```'` must be even) and that `## ` heading count didn't change.

## Pitfall: silent `str.replace` no-op (this cost a session)

Batch `s.replace(old, new)` **fails silently** when `old` doesn't match — no error, file unchanged, and you only notice later. This bit us twice: (1) blockquote replacements written with a `|>` prefix instead of `>` never matched; (2) a too-short `old` snippet missed. **Always assert before replacing:**

```python
def apply(p, old, new):
    s = open(p, encoding='utf-8').read()
    assert old in s, f"NOT FOUND in {p}: {old[:60]!r}"   # fail loudly, not silently
    open(p, 'w', encoding='utf-8').write(s.replace(old, new))
```

Also verify with the scanner after all edits — the scanner caught the two silent misses that the assert in the NEXT batch caught.

## Workflow: Merge EN/CN READMEs into One File

User request: "合并为上下两部分，通过url点击跳转". Result: single `README.md`, English on top, Chinese below, anchor links between.

- Top of file: `**English** | [简体中文](#简体中文)` — link to the Chinese section.
- Chinese section header: `## 简体中文` (GitHub anchor = `#简体中文`); inside it `**简体中文** | [English](#bipartite-gnn-gui)` — anchor back to the H1 (`# Bipartite-GNN-GUI` → `#bipartite-gnn-gui`).
- Strip the old cross-file links (`[English](README.md)`) from both halves.
- Delete `README.zh-CN.md` after merging; grep the repo for references to the deleted file first.
- Watch for duplicated subtitle lines when splicing (saw the zh subtitle twice after the merge — dedupe).

## Rules for This User

- **Official submission materials stay in the source language** — e.g. `docs/ai-acknowledgement.md` (VeriGuide/academic honesty declaration) stays English; ask if in doubt.
- Keep technical terms and identifiers in English inside Chinese prose; the user's style is 中文正文 + 英文术语 + 英文标题括号.
- Commit per doc batch (`docs: ...`), push immediately after (user's git rule: add specific paths, never `add .`).

## Support Files

- `scripts/scan_english_prose.py` — residual-English scanner (letter-density heuristic, skips code fences/tables/lists; flags `>`-blockquotes too).
