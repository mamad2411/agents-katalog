---
name: recipe-builder
description: "Make a new recipe when the user asks to create, save or build a recipe or template for a kind of visual answer they want again (a monthly review, a match report, a weekly plan)."
version: 0.1.0
platforms: [linux, macos, windows]
---
# Recipe builder

A recipe is a short instruction sheet that tells you how to lay out one kind of answer with blocks. Use this when the
user says "make a recipe for …", "save this layout", "next time show my … like this". Recipes can only combine the
block types `show_blocks` already knows; they can't add new kinds of component (that needs code).

## Steps

1. **Pin down the shape with the user** in one or two questions if it isn't clear: what goes in, what it should show
   first, what they want to click. If the user liked a board you just drew, start from that layout.
2. **Draft the recipe** as a full SKILL.md:
   - frontmatter: `name` (lowercase-with-dashes), `description` (one line saying *when* to use it, with the words a
     user would say), `version: 0.1.0`, `platforms: [linux, macos, windows]`;
   - "Use this when …";
   - numbered **Steps**: which tools to call (`market_history`, `find_photos`, web search, or the user's own numbers)
     and in what order;
   - one ```json **layout example**: a complete, valid board using only existing block types;
   - **Rules**: blocks only (never HTML or ::preview), numbers and photo URLs only from tools or the user, short words
     around the tag.
3. **Call `save_recipe`** with the name and the markdown. If it answers "Not saved", fix every listed problem and call
   again.
4. **Tell the user** Hermes will ask them to approve the new recipe, and that it works from their next new session.

## Layout example (for a "monthly investment review" recipe)

```json
[
  {"type": "heading", "text": "October investments"},
  {"type": "kpis", "items": [
    {"label": "Invested", "value": 25000, "unit": "₹"},
    {"label": "Portfolio", "value": 1240000, "unit": "₹", "change": 1.8, "change_unit": "%"}
  ]},
  {"type": "columns", "children": [
    {"type": "chart", "kind": "donut", "title": "Mix", "unit": "%", "x": ["Equity", "Debt", "Gold"],
     "series": [{"name": "Share", "data": [62, 28, 10]}]},
    {"type": "table", "caption": "Funds", "columns": ["Fund", "SIP", "1y"],
     "rows": [["Index fund", "₹15,000", "+12.4%"], ["Debt fund", "₹10,000", "+7.1%"]]}
  ]},
  {"type": "callout", "tone": "tip", "text": "Equity is 62% against a 60% target; next month's SIP can go to debt."},
  {"type": "actions", "items": [{"label": "Rebalance plan", "run": "Suggest a rebalance plan for my portfolio"}]}
]
```

## Rules

- Blocks only: a recipe never asks for HTML or ::preview.
- Never put real personal numbers in the recipe; the example shows the shape, the user's data comes each time.
- Don't copy or replace the recipes that ship with the plugin; pick a new name.
- Keep it under about 100 lines; one clear layout beats many options.
