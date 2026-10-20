---
description: Guidelines for Spatial RAG and Markdown parsing
globs: src/**/*.py
---

## Spatial RAG and Logseq markdown
- **Internal Primitives First:** For injecting properties, extracting frontmatter, or handling namespaces, use the robust internal utilities located in `src/graph/` (e.g., `page_properties.py`, `page_path.py`, `markdown_blocks.py`).
- **Code Block Immunity:** When scanning or modifying inline text, always use `global_fence_scanner.py` to identify protected lines. NEVER modify text inside Markdown code blocks (```), HTML comments, or Logseq queries.
- **External Parsing:** For complex spatial tree extraction (converting bullet outlines into LLM context), delegate to the external package `logseq_matryca_parser`. Do not reinvent AST tree-walking logic.