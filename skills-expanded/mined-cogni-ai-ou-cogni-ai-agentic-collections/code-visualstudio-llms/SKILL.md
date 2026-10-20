---
name: code-visualstudio-llms
description: >-
  Reference and APIs for retrieving Visual Studio Code documentation programmatically for LLMs.
  USE FOR: vscode, visual studio code, code.visualstudio.com, vs code, code editor, ide, copilot in vscode, github copilot chat, extension marketplace, dev containers.
  DO NOT USE FOR: visual studio (full IDE), intellij, rider, eclipse, webstorm.
  You MUST load this skill when asked to search or retrieve Visual Studio Code documentation.
license: MIT
---

# Skill: code-visualstudio-llms

<!-- markdownlint-disable MD013 MD023 MD031 MD032 -->

## WHEN TO USE

- **Documentation Search**: Locating specific Visual Studio Code documentation articles, setup guides, or configuration references.
- **Article Retrieval**: Fetching the full rendered markdown of a specific VS Code docs page via its `llms.txt` or related context.

## WHEN NOT TO USE

- **Other IDEs/Editors**: When the user explicitly asks for Visual Studio (the full IDE), IntelliJ IDEA, Eclipse, WebStorm, or other non-VS Code editors.

## Core Process

1. **Identify the Need**: Determine whether you need to search for a topic or fetch a specific known documentation path.
2. **Execute the Query**: Fetch the data from the llms.txt reference or relevant URLs.
3. **Process Content**: Extract the relevant information to answer the user's query or inform the ongoing task.

## Common Pitfalls

- **Confusing VS Code with Visual Studio**: Ensure the context refers to "Visual Studio Code" or "VS Code", not the full "Visual Studio" IDE.
- **Using this skill for non-VS Code editors**: Route IntelliJ or other IDE documentation requests to the appropriate skill instead of relying on VS Code references.

## References

To fully utilize this skill, you MUST read at least one of the links relevant to the current context:

- [Visual Studio Code Documentation Index](https://code.visualstudio.com/llms.txt)
  USE FOR: Index of documentation, Setup, Get Started, GitHub Copilot, Configure, Edit Code, Build, Debug, Test, Source Control, Terminal, Enterprise,
  Languages, Node.js / JavaScript, TypeScript, Python, Java, C++, C#, Container Tools, Data Science, Intelligent Apps, Azure, Remote.
