---
name: bilingual-readme-merge
description: Use when merging bilingual EN/ZH READMEs into one file.
metadata:
  source_frontmatter:
    tags:
    - readme
    - bilingual
    - documentation
    - markdown
    - anchors
    - github
  imported_from: hermes
---

# Bilingual README Merge (single file, anchor navigation)

Merge `README.md` (EN) + `README.zh-CN.md` (ZH) into ONE `README.md` with the English part on top and the Chinese part below, linked by in-page anchor jumps instead of cross-file links. Learned merging the bipartite-gnn-gui README (2026-08-10). This is the reverse of the split recipe (see `repo-documentation` skill for the two-file split direction).

## Recipe

1. **Read both files fully first** (zh-CN file may read as "binary" via read_file — fall back to `python3 -c "print(open(p, encoding='utf-8').read())"`; it is still plain UTF-8).
2. **English part stays as-is** except the language-switch line becomes an anchor link:
   `**English** | [简体中文](README.zh-CN.md)` → `**English** | [简体中文](#简体中文)`
3. **Chinese part**: strip its `# Bipartite-GNN-GUI` H1, its subtitle line, and its language-switch line; open with `## 简体中文` (this is the anchor target). Its switch line points back to the file's H1 anchor: `**简体中文** | [English](#bipartite-gnn-gui)`.
4. Join: `EN body + "\n\n---\n\n" + "## 简体中文\n\n<subtitle>\n\n" + ZH body`.
5. Delete `README.zh-CN.md` (`git rm`), but FIRST grep the repo for references to it (`grep -rn "README.zh-CN" --include="*.md" --include="*.py" .`) — fix or drop any other pointers.
6. Commit as one change: `docs: merge EN and zh-CN README into one file with anchor links`.

## GitHub anchor rules (verified)

- `# Bipartite-GNN-GUI` → anchor `#bipartite-gnn-gui` (lowercase, spaces→hyphens, punctuation stripped).
- `## 简体中文` → anchor `#简体中文` — **CJK characters are kept verbatim** in GitHub's anchor IDs; no URL-encoding, no pinyin. Use the raw Chinese text in the link.
- The merge keeps GitHub's repo-page rendering (README.md remains the canonical top file); the ZH section is a jump target, not a separate file.

## Pitfalls

- **Duplicate subtitle after merge:** if the ZH part's original subtitle line survives inside the body AND you add it in the section header, the file has the line twice. Dedupe (keep one).
- **Extra blank lines:** the stripped ZH header often leaves 2–3 consecutive blank lines before the switch line — collapse to one.
- **Anchor case sensitivity:** GitHub anchors are case-sensitive to the heading text; `#简体中文` must match `## 简体中文` exactly.
- **Mermaid blocks:** each language keeps its own localized mermaid (node labels in that language) — do not merge them, just stack EN then ZH.
- **Verify after merge:** grep the section map (`grep -n "^## "`), confirm EN section count == ZH section count, and eyeball the two switch lines resolve to the right anchors.

## Verification checklist

- [ ] `grep -n "^# \|^## 简体中文" README.md` → exactly one H1 (file title) and one `## 简体中文`
- [ ] EN sections (N) and ZH sections (N) match in count
- [ ] No leftover `README.zh-CN.md` references anywhere in the repo
- [ ] `git log` shows the delete of README.zh-CN.md in the same commit
