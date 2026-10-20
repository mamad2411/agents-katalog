# Antigravity & AI Assistant Rules for Obsidian Vault

This file defines the rules, requirements, and formatting guidelines for AI assistants (like Antigravity) working in this Obsidian workspace.

## 1. Vault Overview & Structure
This workspace is a personal Obsidian vault containing technical notes. The notes are organized into top-level topic directories. Always try to place new notes in their corresponding folder rather than the root directory:
- `Apache Zookeeper/`
- `Database Internals/`
- `Docker/`
- `Java 8/`
- `Java Collection Framework/`
- `Java Concurrency/`
- `Java Design Patterns/`
- `Java Fundamentals/`
- `Kafka/`
- `Low Level Design/`
- `Microservices/`
- `NGINX/`
- `Redis/`
- `Spring Framework/`
- `Spring JPA/`
- `System Design/`

---

## 2. Obsidian Compatibility Guidelines
All markdown files written or edited in this vault must strictly comply with Obsidian's formatting and rendering features:

### A. Internal Links (Wiki-links)
- Prefer Obsidian-style wiki-links `[[Note Name]]` or `[[Note Name|Display Text]]` when linking to other notes in the vault.
- Avoid raw file paths or standard Markdown links for internal notes unless explicitly requested.

### B. Callouts
- Use Obsidian's callout syntax to highlight key concepts, warnings, tips, or notes.
- Format:
  ```markdown
  > [!NOTE]
  > This is a standard note.
  
  > [!TIP]
  > Useful tips and best practices.
  
  > [!WARNING]
  > Critical warnings or pitfalls.
  
  > [!INFO]
  > Explanatory information.
  ```

### C. Fenced Code Blocks
- Always specify the language for syntax highlighting (e.g., ````java`, ````sql`, ````yaml`, ````bash`, ````json`).
- Ensure code block formatting is clean, readable, and properly indented.

### D. YAML Frontmatter
- If metadata is needed, use standard YAML frontmatter at the very top of the `.md` file, separated by `---`:
  ```yaml
  ---
  tags:
    - java
    - concurrency
  date_created: 2026-06-08
  last_modified: 2026-06-08
  ---
  ```

---

## 3. General Writing Style
- **Clarity and Depth**: Ensure technical notes are precise, accurate, and explain concepts clearly.
- **Hierarchy**: Use clear, semantic heading hierarchies (`#`, `##`, `###`, `####`).
- **Conciseness**: Keep explanations direct and avoid unnecessary filler text.

---

## 4. Git & Workflow Rules
- **No Auto-Commits**: **DO NOT** commit files or modifications to Git automatically.
- **Explicit Permission**: Only write, stage, or edit files. Always wait for the user to explicitly request a Git commit before running any `git commit` commands.
