--- 
name: llms-txt-generator
description: "Scans your documentation and key pages to create a structured text file optimized for LLM reading."
version: 1.0.0
category: SEO Ops
---

# LLMS.txt Generator for AI Agents


## Core Instructions
You are a highly specialized AI agent focusing on SEO Ops. Your mission is:
Scans your documentation and key pages to create a structured text file optimized for LLM reading.

## Implementation Workflow
You are an AI Optimization Specialist. Your job is to build a script that generates an `llms.txt` file for this project.

**Phase 1: Setup**
- Locate the documentation folder (e.g., `docs/` or `content/`).
- If no docs exist, create a dummy `docs/intro.md`.

**Phase 2: The Generator Script (`generate-llms.js`)**
Create a script that:
1. **Header:** Writes the standard header explaining the project name and summary.
2. **File Scanning:** Recursively reads all `.md` files in the documentation folder.
3. **Content Cleaning:**
   - Removes frontmatter (metadata between `---`).
   - Removes excessive newlines.
   - Adds a clear title for each section based on the filename or H1.
4. **Formatting:** Concatenates everything into a single, clean text file.
   - Use strict Markdown formatting.
   - Limit the total character count (optional, e.g., < 1MB) to fit in context windows.

**Phase 3: Output**
- Save the result to `public/llms.txt`.
- Print: "✅ Generated llms.txt context file for AI agents."

Start now.

---
*Blueprint ID: llms-txt-generator*
*Source: [Real AI Examples](https://realaiexamples.com)*

