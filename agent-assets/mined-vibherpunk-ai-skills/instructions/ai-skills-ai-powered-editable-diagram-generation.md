# Copilot Instructions: Ai Powered Editable Diagram Generation
Description: Enables the AI agent to rapidly generate fully editable diagrams, charts, and floor plans using AI diagramming tools, moving beyond static images to functional, customizable files suitable for presentations, reports, and collaborative work.

## Overview
As an AI agent, you are often tasked with generating visual aids for various purposes, from strategic analyses to operational plans. This skill empowers you to rapidly create fully editable diagrams, charts, and floor plans using AI diagramming tools, moving beyond static image generation to produce functional, customizable files. Unlike general-purpose AI image generators that produce uneditable pictures, an AI diagram agent provides structured, editable outputs, saving significant time and enabling seamless integration into workflows. For a deeper dive into the fundamental differences, refer to [Core Concepts of AI Diagram Generation](references/core_concepts_of_ai_diagram_generation.md).

## Step-by-Step Workflow

Follow these steps to generate and refine editable diagrams efficiently:

### 1. Understand the Diagram Requirement
*   **Action**: Before interacting with any tool, clarify the exact type of diagram needed (e.g., SWOT, flowchart, floor plan, organizational chart, production schedule).
*   **Considerations**: Determine the diagram's purpose (e.g., leadership meeting, lecture, case study), target audience, and the key information it needs to convey.
*   **Example**: If a product manager needs a SWOT for an executive sync, the purpose is strategic communication, the audience is leadership, and the key info is strengths, weaknesses, opportunities, and threats for a specific product.

### 2. Access an AI Diagram Agent
*   **Action**: Utilize a dedicated AI diagramming tool that offers AI generation capabilities, such as EdrawMax.
*   **Best Practice**: Ensure the chosen tool explicitly supports AI-driven generation of *editable* diagrams, not just static image rendering. Tools like ChatGPT's image features or Midjourney produce screenshots, not working files.

### 3. Craft a Detailed Prompt
*   **Action**: Formulate a clear, specific, and contextualized prompt for the AI agent.
*   **Guidance**: Include the diagram type, the subject, key entities, relationships, and any specific constraints or nuances.
*   **Prompt Template**:
    ```
    "Generate a [DIAGRAM_TYPE] for [SUBJECT/CONTEXT].
    Include the following specific details:
    - [DETAIL 1]
    - [DETAIL 2]
    - [DETAIL N]
    Specify any particular structure or elements if necessary."
    ```
*   **Example (SWOT)**: "Generate a SWOT analysis for a project management platform launching AI task automation. Product Name: 'TaskFlow AI'. Customer Account: Enterprise clients. Context: This is a catch-up move, not a first-mover advantage. The output should be a four-quadrant diagram with actual content in each box, not lorem ipsum."
*   **Example (Floor Plan)**: "Generate a 2D floor plan for a small office. It should include six rooms, one open work area, a kitchenette, two meeting rooms, and a server closet."
*   **Reference**: For more detailed guidance on prompt engineering, refer to [Effective Prompting for Diagrams](references/effective_prompting_for_diagrams.md).

### 4. Generate the Initial Diagram
*   **Action**: Submit the crafted prompt to the AI diagram agent.
*   **Expectation**: The tool should rapidly produce a preliminary diagram with content in its respective nodes, typically within a minute.
*   **Pitfall**: If the output is a static image (e.g., a screenshot or a non-editable canvas), you are likely using the wrong type of tool or feature. The goal is a file that "behaves like Visio."

### 5. Refine and Customize the Diagram
*   **Action**: Review the generated diagram for accuracy, completeness, and visual appeal. Make necessary edits.
*   **Content Editing**: Click into any node or text box and rewrite or adjust the content. The tool should automatically resize elements as needed.
    *   **Example**: Change "We're playing the role of the follower, not the first mover" to "Second mover with a pricing edge." The text updates instantly, and the box resizes itself without shifting other elements.
*   **Styling Adjustments**: Modify colors, font sizes, and styles for better readability and branding.
    *   **Example**: Select SWOT headers with Shift held down, increase font size, and change their color to red for contrast, making the letters "pop as accent color on the slide."
*   **Layout Adjustments**: Drag and drop elements, resize boxes, and adjust connections to optimize the layout.
*   **Reference**: For detailed editing instructions, consult [Diagram Refinement and Export](references/diagram_refinement_and_export.md).

### 6. Export the Final Diagram
*   **Action**: Once satisfied with the diagram, export it in the required format.
*   **Common Formats**:
    *   **PPTX (PowerPoint)**: Ideal for presentations, preserving editability within PowerPoint. "You don't rebuild the slide from scratch in PowerPoint. You just keep working with what you generated."
    *   **PDF**: For sharing static, high-quality documents.
    *   **PNG/JPG**: For image embedding in reports or web pages.
    *   **VSDX (Visio)**: Crucial for interoperability with Windows-based teams, preserving full editability, especially for Mac users.
*   **Best Practice**: Prioritize editable formats (PPTX, VSDX) if further modifications or collaboration are anticipated.

### 7. Leverage Advanced Features (Optional)
*   **Template Library**: Explore the tool's extensive library of pre-made templates for common diagram types (flowcharts, engineering drawings, production schedules). This can be faster than AI generation for standard layouts. "Hundreds, if not thousands, of ready-to-use layouts for any task."
*   **VSDX Import/Export**: If working on a Mac with Windows colleagues, use the VSDX import feature to open and edit Visio files, then export back to VSDX without loss of fidelity. "Every shape, every connection, every conditional label is preserved on import."
*   **AI Image Tools**: Utilize bundled features like background removal, object removal, or 4K image upscaling for quick image preparation within the same application. Understand these are convenience features, not professional replacements.
*   **Reference**: For more on these features and their limitations, see [Leveraging Advanced Features and Avoiding Pitfalls](references/leveraging_advanced_features_and_avoiding_pitfalls.md).

## Best Practices
*   **Be Specific in Prompts**: The more detail you provide (context, purpose, key elements), the better the initial output. This reduces post-generation editing time.
*   **Embrace Editability**: Don't treat the AI-generated diagram as final. Actively use the editing features to refine content, styling, and layout to meet exact requirements. This is the core advantage over static image generators.
*   **Utilize Templates**: For standard or repetitive diagrams, check the template library first. It can often provide a faster and more structured starting point than AI generation.
*   **Understand Tool Scope**: Recognize that AI diagramming tools are excellent for rapid, editable visual communication but may not replace specialized software for architectural-grade drawings or professional photo editing. They are "convenience features" for "fast and good enough."

## Common Pitfalls
*   **Using Image-Only AI Generators**: Relying on tools like ChatGPT or Midjourney for diagrams will result in static images that cannot be edited, recolored, or restructured, defeating the purpose of an editable diagram. This leads to burning "an extra hour building it by hand."
*   **Vague Prompts**: Prompts lacking specific details will lead to generic or irrelevant diagrams, requiring extensive manual correction or regeneration.
*   **Neglecting Post-Generation Editing**: Assuming the AI's first draft is perfect. Always review and refine the content, styling, and layout to ensure accuracy and alignment with your needs.
*   **Expecting Professional-Grade Output from Convenience Features**: While AI image tools (background removal, upscaling) are handy, they are not substitutes for professional graphic design software like Photoshop for high-stakes print or detailed image manipulation. Similarly, AI-generated floor plans are for conceptualization, not architectural blueprints; "It's clearly not architectural grade. You wouldn't hand this to a contractor."

## Validation Steps
1.  **Content Accuracy**: Verify that all text and data within the diagram nodes are correct and align with the prompt's intent.
2.  **Editability Check**: Attempt to modify text, colors, and drag elements around to confirm the diagram is fully editable and responsive.
3.  **Formatting and Readability**: Ensure fonts are legible, colors provide sufficient contrast, and the overall layout is clear and easy to understand.
4.  **Export Integrity**: Open the exported file (e.g., PPTX, VSDX, PDF) in its native application to confirm that all elements are preserved and functional as expected, without any loss of fidelity or editability (for relevant formats).

## Reference Guides

### Core Concepts Of Ai Diagram Generation

# Core Concepts of AI Diagram Generation

As an AI agent, understanding the fundamental principles behind AI diagram generation is crucial for effectively utilizing these tools. This document outlines the core concepts, distinguishing features, and common applications of AI diagramming agents.

## AI Diagram Agents vs. Image Generators

The most critical distinction to grasp is between an AI diagram agent (like EdrawMax's AI feature) and a general-purpose AI image generator (like ChatGPT's image capabilities or Midjourney).
*   **AI Image Generators**: These tools take a text prompt and produce a static image (e.g., a PNG or JPG). While the image might *look* like a diagram, it is essentially a picture. You cannot click on individual boxes, change text, recolor elements, or drag components around. Any modification requires regenerating the entire image or using a separate image editing tool, which is inefficient and often leads to loss of fidelity. The transcript explicitly states, "ChatGPT canvas and claw artifacts give you something that looks like a diagram, but it behaves like a screenshot."
*   **AI Diagram Agents**: These tools generate structured, vector-based diagrams where each element (node, connector, text box) is an independent, editable object. This means you can interact with every part of the diagram post-generation. The output is a working file, not just a picture. The transcript highlights this: "Every node is editable. I can click any quadrant, retype the content, change the color, or drag the whole box around... This behaves like Visio."

## The Importance of Editability

Editability is the cornerstone of effective AI diagram generation. Without it, the time saved in initial generation is quickly lost in manual recreation or workarounds.
*   **Flexibility**: You can easily update content, correct errors, or refine messaging without starting from scratch. For example, changing "We're playing the role of the follower, not the first mover" to "Second mover with a pricing edge" is a simple text edit, not a complete redraw.
*   **Customization**: Tailor the visual style (colors, fonts, sizes) to match branding guidelines or presentation aesthetics. The ability to change SWOT letter colors to red for accent is a prime example.
*   **Collaboration**: Share editable files (like PPTX or VSDX) with human colleagues or other agents, allowing them to make their own modifications directly. This fosters a collaborative workflow, unlike sharing static screenshots.
*   **Adaptability**: Quickly adjust a diagram for different audiences or contexts. A single generated diagram can be repurposed multiple times with minor tweaks.

## Supported Diagram Types and Applications

AI diagram agents are versatile and can generate a wide array of diagram types, catering to various professional and academic needs.
*   **Business Analysis**: SWOT analyses, PESTEL analyses, business process models, organizational charts.
*   **Project Management**: Production schedules, Gantt charts, flowcharts for workflows.
*   **Architecture & Design**: 2D floor plans, basic network diagrams. The transcript demonstrates generating a floor plan with sensible proportions and door swings. While not "architectural grade," it's highly effective for stakeholder presentations.
*   **Education**: Concept maps, scientific diagrams, process flows for lectures or coursework.
*   **Technical Diagrams**: Basic flowcharts, network diagrams, and potentially more complex engineering drawings (often starting from templates).

## Key Features Beyond Basic Generation

Modern AI diagramming tools often bundle additional features that enhance productivity:
*   **Extensive Template Libraries**: Pre-designed templates for hundreds of common diagram types can serve as quick starting points, often faster than AI generation for very standard layouts.
*   **VSDX Compatibility**: The ability to import and export Microsoft Visio files (VSDX) is a significant advantage, especially for cross-platform collaboration (e.g., Mac users working with Windows teams). This preserves full editability and fidelity.
*   **Basic AI Image Tools**: Features like background removal, object removal, and 4K image upscaling are often integrated. These are convenience tools for quick image preparation within the diagramming environment, avoiding the need to "round-trip files between apps." However, it's crucial to understand their limitations; they are not replacements for professional image editing software.

By understanding these core concepts, you can effectively leverage AI diagram generation to produce high-quality, editable visual assets efficiently.


### Diagram Refinement And Export

# Diagram Refinement and Export

Generating a diagram with AI is often just the first step. The true power of AI diagramming tools lies in their ability to produce *editable* files, allowing for extensive refinement and customization. This document guides you through the process of post-generation editing and the critical steps for exporting your diagrams in various formats.

## Post-Generation Editing: Making it Your Own

Once the AI agent provides the initial diagram, your role shifts to that of a designer and editor. The goal is to ensure the diagram is accurate, clear, visually appealing, and perfectly aligned with its purpose.

### 1. Content Editing

*   **Action**: Click directly into any text box, node, or label to modify its content.
*   **Best Practice**: Review every piece of AI-generated text for accuracy, tone, and conciseness. The AI provides a "real starting point, not lorem ipsum," but it's rarely perfect.
*   **Example from Transcript**: The weakness "We're playing the role of the follower, not the first mover" was softened to "Second mover with a pricing edge." This demonstrates how easy it is to refine messaging. The tool should automatically resize the text box to accommodate changes, ensuring nothing shifts out of place.

### 2. Styling Adjustments

*   **Action**: Select individual elements or groups of elements (e.g., all headers, specific connectors) to change their visual properties.
*   **Font Management**: Adjust font size, type, and weight for readability.
    *   **Example**: The transcript mentions selecting headers with Shift held down and bumping up the font size because "Your eye loses them." This improves visual hierarchy.
*   **Color Schemes**: Modify fill colors, line colors, and text colors to match corporate branding, presentation themes, or simply to add visual contrast.
    *   **Example**: Changing the default blue SWOT letters to red to make them "pop as accent color on the slide."
*   **Line Styles**: Adjust line thickness, style (solid, dashed), and arrowheads for connectors.

### 3. Layout and Structure Refinement

*   **Action**: Drag and drop nodes, resize boxes, and adjust the spacing between elements.
*   **Alignment**: Use built-in alignment tools (often found in top panels) to ensure elements are neatly arranged on a grid.
*   **Connections**: Verify that all connectors accurately represent relationships and adjust their paths if they overlap or appear messy.
*   **Proportions**: For diagrams like floor plans, check if the proportions are sensible. The transcript notes that the AI-generated floor plan had "sensible proportions" and "doors swing into the rooms the right way," which is a significant advantage over generic tools.

## Exporting Your Diagram: Choosing the Right Format

The final step is to export the refined diagram in a format suitable for its intended use. The choice of format is crucial, especially if further editing or collaboration is required.

### 1. PowerPoint (PPTX)

*   **Use Case**: Ideal for presentations.
*   **Benefit**: Exports as a fully editable slide within PowerPoint. You don't get a static image; you get a slide where you can still move elements, change text, and recolor. The transcript emphasizes this: "You don't rebuild the slide from scratch in PowerPoint. You just keep working with what you generated."
*   **Recommendation**: Always choose PPTX if the diagram is destined for a presentation deck and might need last-minute tweaks.

### 2. PDF

*   **Use Case**: For sharing static, high-quality documents where content should not be altered.
*   **Benefit**: Preserves layout and formatting across different devices and software.
*   **Limitation**: Not editable once exported.

### 3. Image Formats (PNG, JPG)

*   **Use Case**: For embedding in reports, web pages, or other documents where the diagram acts as a static visual.
*   **Benefit**: Widely compatible, easy to share.
*   **Limitation**: Not editable. PNG supports transparency, which can be useful.

### 4. Visio (VSDX)

*   **Use Case**: Essential for interoperability with Microsoft Visio users, especially in corporate environments.
*   **Benefit**: Preserves full editability and fidelity, allowing Windows users to open and continue working on the diagram as if it was created in Visio. This is particularly valuable for Mac users who historically faced challenges with VSDX files. The transcript highlights this: "This app lets you import VSDX without any hassle. Every shape, every connection, every conditional label is preserved on import... export it back to VSDX, and your colleague on Windows won't even know you were working on a Mac."
*   **Recommendation**: Use VSDX when collaborating with teams that rely on Visio.

By diligently refining your AI-generated diagrams and selecting the appropriate export format, you ensure that your visual communications are not only fast to produce but also professional, accurate, and adaptable.


### Effective Prompting For Diagrams

# Effective Prompting for AI Diagram Generation

As an AI agent, your ability to craft precise and comprehensive prompts is paramount to generating accurate and useful diagrams. Vague or incomplete prompts will lead to generic outputs, requiring extensive manual correction. This guide outlines the principles and provides examples for effective prompt engineering when using AI diagramming tools.

## Principles of Effective Prompt Engineering

1.  **Clarity**: Be unambiguous about what you want. Avoid jargon where simpler terms suffice, but use precise technical terms when necessary.
2.  **Specificity**: Provide as much detail as possible. General requests yield general results.
3.  **Context**: Explain the purpose, audience, and background information relevant to the diagram. This helps the AI understand the nuances and generate appropriate content.
4.  **Structure**: Indicate the desired diagram type explicitly. If there are specific sections or elements, list them.
5.  **Constraints/Nuances**: Mention any particular requirements, limitations, or specific angles the diagram should take.

## Components of a Good Prompt

An effective prompt typically includes:
*   **Diagram Type**: Clearly state what kind of diagram you need (e.g., "SWOT analysis," "2D floor plan," "flowchart," "organizational chart").
*   **Subject/Topic**: What is the diagram about? (e.g., "a project management platform," "a small office," "a customer onboarding process").
*   **Key Elements/Content**: List the specific information, entities, or data points that must be included. For a SWOT, this means the product name, customer, and strategic context. For a floor plan, it means the rooms and areas.
*   **Relationships/Flow (for flowcharts/process diagrams)**: Describe how elements connect or the sequence of steps.
*   **Purpose/Audience**: Briefly explain why the diagram is being created and for whom. This helps the AI tailor the tone and level of detail.
*   **Specific Instructions**: Any particular styling, layout preferences, or admissions (e.g., "acknowledge this is a catch-up move").

## Prompt Examples from the Transcript

Let's break down successful prompts used in the source material:

### Example 1: SWOT Analysis

**Scenario**: A product manager needs a SWOT slide for an executive sync for a project management platform launching AI task automation, which is catching up to competitors.

**Effective Prompt**:
```
"Generate a SWOT analysis for a project management platform launching AI task automation.
Product Name: 'TaskFlow AI'.
Customer Account: Enterprise clients.
Context: This is a catch-up move, not a first-mover advantage.
The output should be a four-quadrant diagram with actual content in each box, not lorem ipsum."
```
**Analysis**:
*   **Diagram Type**: "SWOT analysis"
*   **Subject**: "project management platform launching AI task automation"
*   **Key Elements**: "Product Name: 'TaskFlow AI'", "Customer Account: Enterprise clients"
*   **Context/Nuance**: "This is a catch-up move, not a first-mover advantage." This crucial detail ensures the AI generates realistic weaknesses and threats.
*   **Specific Instruction**: "actual content in each box, not lorem ipsum" – prevents generic placeholders.

### Example 2: 2D Floor Plan

**Scenario**: An office manager needs a 2D floor plan for a small office.

**Effective Prompt**:
```
"Generate a 2D floor plan for a small office.
It should include the following areas:
- Six individual rooms
- One open work area
- A kitchenette
- Two meeting rooms
- A server closet (ensure it's not in an inappropriate location like a bathroom)."
```
**Analysis**:
*   **Diagram Type**: "2D floor plan"
*   **Subject**: "a small office"
*   **Key Elements**: Explicitly lists all required rooms and areas.
*   **Constraint/Nuance**: "(ensure it's not in an inappropriate location like a bathroom)" – a subtle but important detail for practical utility.

## Iterative Prompting

Sometimes, the first generated diagram might not be perfect. This is where iterative prompting comes in.
1.  **Review Initial Output**: Analyze what worked and what didn't.
2.  **Identify Gaps/Errors**: Pinpoint missing information, incorrect relationships, or stylistic issues.
3.  **Refine Prompt**: Add more specific instructions or constraints based on your review. For instance, if the initial SWOT was too generic, you might add, "Focus on competitive landscape and market positioning."
4.  **Regenerate (or Edit Manually)**: Depending on the extent of changes, you can either regenerate with the refined prompt or make manual edits to the existing diagram. For minor tweaks, manual editing is often faster.

By mastering these prompting techniques, you can significantly reduce the time spent on diagram creation and ensure the AI delivers highly relevant and actionable visual content.


### Leveraging Advanced Features And Avoiding Pitfalls

# Leveraging Advanced Features and Avoiding Pitfalls in AI Diagram Generation

Beyond basic AI diagram generation, modern tools often offer a suite of advanced features that can further enhance your productivity. However, it's equally important to be aware of common pitfalls and the limitations of these tools to ensure you use them effectively and avoid missteps.

## Leveraging Advanced Features

### 1. Extensive Template Library

*   **Feature**: Most AI diagramming tools come with a vast library of pre-designed templates for various diagram types, including flowcharts, engineering drawings, education diagrams, business reports, and production schedules.
*   **Benefit**: For standard or common diagram types, using a template can often be faster than generating from scratch with AI. You simply select a template and swap in your specific content. The transcript notes, "We're talking hundreds, if not thousands, of ready-to-use layouts for any task." This saves time on building grids or structures from scratch.
*   **Best Practice**: Before prompting the AI, quickly browse the template library. If a suitable template exists, it might be the most efficient starting point.

### 2. VSDX Import and Export (Visio Compatibility)

*   **Feature**: The ability to open, edit, and save files in Microsoft Visio's native VSDX format.
*   **Benefit**: This is a game-changer for cross-platform collaboration, particularly for Mac users who need to work with Windows-based teams. It eliminates the need for workarounds like Parallels, paid converters, or requesting screenshots. All shapes, connections, and labels are preserved, allowing seamless editing and round-tripping of files.
*   **Use Case**: If you receive a VSDX file from a colleague, you can import it, make edits, and export it back to VSDX, maintaining full compatibility and editability for the original sender.

### 3. Integrated AI Image Tools

*   **Feature**: Many diagramming applications now bundle basic AI-powered image editing capabilities, such as background removal, object removal (generative fill), and 4K image upscaling.
*   **Benefit**: These are "convenience features" designed to save you the trip to a second, dedicated image editing app. They allow for quick, "good enough" image preparation directly within your diagramming workflow.
    *   **Background Removal**: Quickly isolate a subject from its background for clean integration into diagrams.
    *   **Object Removal**: Erase unwanted elements from an image, filling the area with plausible background.
    *   **4K Upscaling**: Enhance the resolution of low-quality images for better clarity in presentations or reports.
*   **Best Practice**: Use these tools for quick fixes and general-purpose visuals.

## Avoiding Common Pitfalls

### 1. Misunderstanding the Scope of AI Image Tools

*   **Pitfall**: Expecting professional-grade results from integrated AI image features.
*   **Clarification**: The transcript explicitly states, "Not perfect on fine detail," for background removal, and "Not the level you'd hand off for a professional print publication" for 4K upscaling. These tools are for "fast and good enough," not replacements for professional software like Photoshop or a dedicated graphic designer.
*   **Recommendation**: For critical, high-stakes image manipulation or print-quality output, always use specialized image editing software.

### 2. Expecting Architectural-Grade Precision from AI Floor Plans

*   **Pitfall**: Assuming AI-generated floor plans are suitable for construction or detailed architectural work.
*   **Clarification**: While AI can generate "sensible proportions" and "doors swing into the rooms the right way," the transcript clearly states, "It's clearly not architectural grade. You wouldn't hand this to a contractor."
*   **Recommendation**: Use AI-generated floor plans for conceptualization, stakeholder presentations, or internal planning where a visual representation of space is needed, but not for precise engineering or construction blueprints.

### 3. Over-Reliance on AI Without Human Review

*   **Pitfall**: Trusting the AI's initial output implicitly without thorough review and refinement.
*   **Clarification**: While AI provides a "real starting point," it's crucial to remember that the content "isn't world-changing strategy." AI can generate plausible text, but it lacks true understanding or strategic insight.
*   **Recommendation**: Always validate the content, accuracy, and strategic relevance of AI-generated text and diagrams. Use the editing features to inject your own expertise and ensure the final product meets your specific requirements.

### 4. Ignoring the Template Library

*   **Pitfall**: Always defaulting to AI generation even when a perfect template already exists.
*   **Clarification**: The template library can often be a faster and more reliable starting point for common diagram types, as it provides a pre-vetted structure.
*   **Recommendation**: Develop a habit of checking the template library before crafting a prompt for AI generation.

By understanding these advanced features and being mindful of these common pitfalls, you can maximize your efficiency and produce high-quality diagrams that truly serve their purpose.


### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[FREE AI Diagram Tool — How to Create Any Diagram Using AI (Visio Alternative)](https://www.youtube.com/watch?v=Vn-2b4SZCDs)** by AI Master