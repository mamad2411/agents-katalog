---
name: readme-crafter
description: Use this skill when you need to write, refactor, or improve a project's README.md file. Trigger this anytime the user wants to create documentation, project overviews, or profile pages following best practices and modern aesthetics.
---

# README Crafter

This skill equips the agent with best practices, architectural templates, and modular components to generate modern, high-quality `README.md` files.

## Core Principles
When crafting a README, always adhere to the fundamental rules of clear positioning, cognitive funneling, visual appeal, and practical usage.
See **[Core Principles](references/core_principles.md)**.

## Structure & Architecture
A standard modern README is composed of modular sections: Header, Overview, Features, Getting Started, and Community Support.
See **[README Structure](references/structure.md)**.

## Reference Projects
Different projects require different README styles (e.g., comprehensive, visual-driven, architecture-heavy, or personal profile).
See **[Reference Projects](references/reference_projects.md)** to understand which style fits the user's needs.

## Workflow / Instructions

1. **Analyze the Request & Project**:
   - Determine the project type (CLI, Frontend, Library, Personal Profile, Backend Service).
   - Identify the target audience (contributors, end-users, recruiters).
2. **Select Components**:
   - Choose the appropriate template components from the `assets/` directory based on the project type.
   - For a full out-of-the-box solution, use the `complete_modern_template.md`.
   - You can mix and match snippet components to assemble the perfect README.
3. **Draft the README**:
   - Write the content. Ensure a strong "Hero Section" (Golden First 3 Seconds).
   - Keep paragraphs concise (Cognitive Funneling).
   - Use proper markdown headings, badges, and code blocks.
4. **Refine and Polish**:
   - Add placeholders for screenshots, architecture diagrams, or GIFs if applicable.
   - Include a Table of Contents for longer documents.

## Bundled Resources (Assets)

Modular template components to assemble a README. Use these to construct the final output based on user requirements:

### Complete Templates
- **[Complete Modern Template](assets/complete_modern_template.md)**: A beautiful, comprehensive out-of-the-box README template.
- **[Profile](assets/profile.md)**: Template for personal GitHub profile READMEs.

### Snippets & Fragments (Plug-and-play)
- **[Header: Standard](assets/header_standard.md)**: A clean, text-and-badge focused header.
- **[Header: Visual](assets/header_visual.md)**: A banner/GIF focused header for visual projects.
- **[Navigation & Features](assets/navigation_and_features.md)**: Table of contents and feature highlights.
- **[Getting Started](assets/getting_started.md)**: Prerequisites, Installation, and Usage examples.
- **[Support & Community](assets/support_and_community.md)**: Contributing, License, and Acknowledgments.
- **[Badges Collection](assets/badges_collection.md)**: A collection of various markdown badges.
- **[Architecture Diagram](assets/architecture_diagram.md)**: Examples of using Mermaid for architecture diagrams.
- **[Contributors & Sponsors](assets/contributors_and_sponsors.md)**: Snippets for showing contributors, backers, and sponsors.
