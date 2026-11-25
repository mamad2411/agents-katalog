---
name: comic-architect
description: Use when the user wants to generate AI image prompts for Comics, Cartoons, Infographics, or Icons based on the 'Cartoon Prompt' methodology.
---

# Comic Architect (v2.0 - The Multi-Layered Engine)

## Overview
This skill is a **Pro-Grade AI Art Director**. It transforms vague user ideas into highly structured, aesthetically sophisticated prompts for top-tier AI models (Flux, Ideogram, Midjourney v6). It uses a 4-layer architecture to ensure variety, professional design, and visual innovation.

## 📂 File Map (The Architecture)

**NOTE**: All paths below are relative to the skill root directory (`.trae/skills/comic-architect/`).

### Layer 1: Style DNA Vault (Aesthetics)
*   `styles/visual-styles.md`: Core art directions (Bauhaus, Pop Art, Cyberpunk, etc.).
*   `styles/rendering-techniques.md`: Execution methods (Watercolor, 3D Clay, Risograph, etc.).

### Layer 2: Layout & Typography Engine (Structure)
*   `layouts/grids.md`: Structural skeletons (Bento Grid, Comic Strip, Golden Spiral, etc.).
*   `layouts/typography.md`: Font strategies for models that render text.

### Layer 3: Innovation Mixer (Creativity)
*   `engine/recommender.md`: Logic to map "Content" -> "Style Options".
*   `engine/innovation-mixer.md`: Randomizers for Material, Lighting, and Color to ensure 365 days of uniqueness.

### Layer 4: Execution Templates (Assembler)
*   `templates/`: Pre-configured combinations of the above layers for specific common tasks (e.g., "Comic Strip", "Notion Icon"). Use these for specific requests, or use Dynamic Assembly for open-ended ones.

## The Workflow (Strict Execution Path)

1.  **Analyze & Recommend (The "Consultant" Phase)**:
    *   **Input**: User's vague idea (e.g., "Draw a day in the life of a coffee bean").
    *   **Action**: Consult `engine/recommender.md`.
    *   **Output**: Propose 3 distinct paths to the user (Safe, Bold, Twist).
        *   *Example: "Option A: 4-Panel Comic (Cute), Option B: Industrial Blueprint (Cool), Option C: Pixar 3D (Fun)."*

2.  **Select & Mix (The "Designer" Phase)**:
    *   **Selection**: User picks an option (or you pick best fit if user delegates).
    *   **Innovation**: Consult `engine/innovation-mixer.md`.
    *   **Roll the Dice**: Select 1 Material + 1 Lighting + 1 Color Strategy + 1 Composition Twist.
        *   *Example: "Pixar 3D" + "Velvet Texture" + "Neon Lighting" + "Fish-eye Lens".*
    *   **Translation**: **MANDATORY**: Translate the core subject and concept into **ENGLISH** for the final prompt, as top-tier models (Midjourney, Flux) perform best with English prompts.

3.  **Construct Prompt (The "Engineer" Phase)**:
    *   **Assemble**: Combine all layers into a structured prompt.
    *   **Typography**: Ensure text rendering instructions are explicit (from `layouts/typography.md`).
    *   **Layout**: Define the grid/structure explicitly (from `layouts/grids.md`).

## Output Format

Return the result in a code block. If you generated Options, present them first.

```markdown
**🎨 Comic Architect: Generated Design Strategy**

> **Concept**: [Brief Description]
> **Style DNA**: [Visual Style] + [Rendering Technique]
> **Layout**: [Grid Type]
> **Innovation Twist**: [Material] + [Lighting] + [Color]

```plaintext
[The Professional Prompt]
/imagine prompt: [Subject Description] in the style of [Visual Style], rendered as [Rendering Technique].
[Layout Details]: [Grid Description].
[Material/Lighting Details]: [Innovation Twist].
[Typography Details]: [Font Style] text "[Text Content]" placed [Location].
--ar [Aspect Ratio] --stylize [Value] --v [Model Version]
```
```

## Anti-Patterns
- **Do not** just default to "Notion Style". Explore the Vault.
- **Do not** forget the "Innovation Twist". Vague inputs need specific details to look good.
- **Do not** ignore text rendering. If the user implies text, specify the font and placement.
