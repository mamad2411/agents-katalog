---
name: literature-reading
description: Guide an agent through professional interpretation of a locally parsed scholarly paper using MinerU Markdown and image assets. Default to a complete reading, narrow the scope only when the user asks, and write Markdown only when requested or when the result is too long for chat.
license: MIT
---

# Literature interpretation

Use this Skill after `paper-reading` has produced a local MinerU publication. Work from the parsed Markdown, `metadata.json`, and linked assets with the host's local file, search, and image-viewing capabilities. Do not invent a separate reading or analysis MCP tool.

## Defaults

- Unless the user asks about a specific question, section, figure, table, or equation, perform a complete professional interpretation of the paper.
- Return the interpretation in the conversation by default. Write a Markdown file only when the user requests one or the result is too long to remain useful in chat.
- Follow the user's language and desired depth. Preserve titles, identifiers, formulas, units, sample names, and technical terms when translation could change their meaning.

## Workflow

1. Confirm the paper from the Markdown frontmatter and `metadata.json`, including title, Zotero key, DOI when present, and selected attachment. If no readable parsed publication is available, return to `paper-reading` instead of reconstructing the paper from metadata or memory.
2. Map the document structure first: headings, captions, tables, equations, and image links. Then read progressively so long papers do not overflow the working context.
3. For a complete interpretation, cover every substantive section, normally including the abstract, background, research question, methods or argument, results, discussion, limitations, and conclusion. Do not treat the abstract and conclusion as a substitute for the full paper.
4. Explain the paper's problem, approach, critical conditions or assumptions, main evidence, quantitative results, reasoning, contribution, limitations, applicability, and unresolved questions. Adapt these dimensions to the paper rather than forcing a fixed report template.
5. Attach reproducible source locators to important claims: relative Markdown filename, section heading, stable line range or identifying phrase, and figure/table/equation identifier when relevant. Keep conditions, units, comparison direction, and reported uncertainty with numerical results.
6. Distinguish paper evidence, the authors' own interpretation, the Agent's interpretation, and uncertainty. Mark missing information as unreported or unavailable; do not fill it from general knowledge.

## Figures, tables, and equations

- A figure interpretation must combine three sources: direct visual inspection of the MinerU image asset, its caption, and the surrounding passages where the authors discuss it.
- State visual observations separately from the authors' statements and from the Agent's scientific interpretation. If the image cannot be inspected or is unclear, say so and do not infer visual details from the caption alone.
- For tables, retain row/column meaning, units, conditions, baselines, and statistical notation. For equations, preserve the expression and explain symbols or assumptions only when supported by nearby text.

## Optional Markdown output

When a file is needed, save it in the paper's publication directory unless the user chooses another location. Use a concise non-colliding filename, never alter the MinerU source or assets, and do not overwrite an existing note without confirmation.

Keep all source and asset links relative to the output file. Embed each interpreted MinerU image as a linked preview so the reader can both see it and open the original asset:

```markdown
[![Figure 2](assets/ZOTEROKEY-image-2.png)](assets/ZOTEROKEY-image-2.png)
```

Use the asset's actual filename and path; never fabricate an image name. Place the caption, relevant author context, visual observations, and interpretation near the preview rather than compressing long analysis into a Markdown table.

Before finishing, reopen any saved file and verify that its Markdown, image previews, links, formulas, and source locators work. Report the saved path in the conversation, but do not write private absolute paths, credentials, or signed URLs into the document.

Zotero notes and PDF annotations may provide personal reading context, but they are not independent evidence from the paper.
