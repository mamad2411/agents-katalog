---
name: readme-showcase
description: >-
  Design or refresh GitHub README.md as a centered, badge-rich, professional
  showcase (shields.io, emoji section headers, judge-first layout, collapsible
  references). Use when the user asks to beautify README, add badges/icons,
  center layout, hackathon submission polish, or "README ấn tượng/chuyên nghiệp".
---

# README Showcase — GitHub professional layout

Design README files that read well on GitHub: **centered hero**, **shields.io badges**, **emoji section anchors**, **scannable tables**, **collapsible long references**. Canonical example in this repo: [`README.md`](../../../README.md).

## When to apply

- User wants README "đẹp hơn", badges, icons, emoji, căn giữa, chuyên nghiệp
- Hackathon / judge-facing repos needing clear verify path above the fold
- Refactoring a wall-of-text README without dropping technical links

## Design rules

1. **Hero (centered)** — `<div align="center">` wrapping title, italic tagline, middle-dot subtitle, badge rows, one ASCII or quote block, then close `</div>`.
2. **Badge tiers**
   - Row 1: `style=for-the-badge` — track/event (hackathon, submission status)
   - Row 2: `for-the-badge` — primary CTAs (live demo, doc hub, judge guide, GitHub)
   - Row 3: `style=flat-square` — stack (TypeScript, Node, pnpm, license)
3. **Emoji in headings** — one emoji per `##` section for scanability; **do not** put emoji inside Mermaid `subgraph` labels (breaks GitHub render).
4. **Judge-first** — verify commands + link table within first ~120 lines when repo has judges.
5. **Tables over prose** — resources, scripts, docs index as two-column tables with emoji column labels (`🔗`, `📍`).
6. **Collapsible references** — long external link lists go in `<details><summary>…</summary>` blocks.
7. **Footer (centered)** — project name, tagline, star badge, license, one-line acknowledgement.
8. **Preserve content** — never drop verify commands, mainnet IDs, or doc paths when restyling; consolidate duplicates instead.

## Standard section order

```
[Centered hero + badges]
---
## 📑 Contents (anchor table)
---
## ⚖️ For judges (centered subhead + bash block + link table)
## 🎬 Demo / Doc Hub (if applicable)
## 🔌 MCP / SDK (if applicable)
## 🏗️ Overview (layers table + mermaid + narrative)
## ⚡ Quick start (judge / dev / optional live)
## ⛓️ On-chain (badges + ID table)
## 📜 Scripts
## 📚 Documentation (compact index)
## 🔗 References (<details> groups)
## ✅ Checklist
## 🔒 Security
[Centered footer]
```

## Badge URL patterns

```markdown
[![Label](https://img.shields.io/badge/Label-Value-COLOR?style=for-the-badge)](https://link)
[![Stack](https://img.shields.io/badge/TypeScript-5.7-3178C6?style=flat-square&logo=typescript&logoColor=white)](https://typescriptlang.org/)
[![GitHub stars](https://img.shields.io/github/stars/ORG/REPO?style=social)](https://github.com/ORG/REPO/stargazers)
```

Use `_` for spaces in badge label text (shields.io convention). Link badges to real destinations (not `#`).

## HTML GitHub allows

- `<div align="center">` … `</div>`
- `<br />` for vertical spacing in hero
- `<details>` / `<summary>` for collapsible sections
- Blockquote `>` for one-line callouts under hero

Avoid: raw HTML for entire body, custom CSS, JavaScript.

## Workflow

1. Read existing README; list sections that must stay (judge path, IDs, scripts).
2. Draft centered hero with project name, tagline, 3 badge rows.
3. Add Contents table with emoji + anchor links (GitHub slugifies emoji headers).
4. Restructure body per section order; move duplicate reference tables into `<details>`.
5. Verify all relative links still resolve; mermaid renders without emoji in subgraph IDs.
6. Keep length reasonable (~400–500 lines max); prefer collapsible over deletion.

## Anti-patterns

- Broken badge rows (plain URLs without `![...](shields.io/...)`)
- Nesting entire README in one center div ( hurts left-aligned code blocks )
- Emoji overload in every bullet (one per section header is enough)
- Removing judge verify block to "look cleaner"
- `MemWal++` vs official name inconsistency — use repo display name + legacy alias once in hero

## Reference

- Full skeleton: [template.md](template.md)
- Live example: [README.md](../../../README.md)
