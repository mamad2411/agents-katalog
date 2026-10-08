# CS First Principles Pedagogy Guidelines & Repository Standards

## Overview
This skill defines the authoritative pedagogical standards and workspace architecture for the CS Wiki (`cs-first-principles`) project.

## Directory Structure & Folder Roles
- `platform/`: Modern CS Wiki Web Application (React + Vite + TypeScript) containing interactive simulators, knowledge graph, complexity-calibrated question bank, and zoomable abstraction layers.
- `cs-learning-platform.md`: Authoritative 20-Point Pedagogy Blueprint (Concept Maps, Interactive Diagrams, Animations, Flowcharts, Layered Views, Color Coding, Before/After Comparisons, Build-Up Diagrams, Zoom Levels, Icons, Timelines, State Machines, Memory Maps, Mini Simulators, Prediction Checkpoints, Common Misconceptions, Knowledge Graph, Progress Bars, Interactive Quizzes, Summary Cards).
- `cs-notes/`: Detailed Markdown topic notes breaking down CS concepts from physical voltages to distributed systems.
- `cs-questions-AI/`: Socratic AI tutor question files, interactive prompts, and problem warm-ups designed to test intuition before formal mathematical/hardware explanations.
- `cs-questions/`: Human user question queues and raw user notes.
- `cs-probes/`: Diagnostic scripts and experiment code.
- `cs-builds/`: Code prototypes and execution benchmarks.
- `.agents/skill/cs-first-principles-pedagogy/`: Active agent skill instructions and architectural notes.

## 12 Key Platform Directives
1. **Complexity-Calibrated Questions**: Question difficulty is strictly aligned with topic depth (10+ questions per topic, spanning Basic, Intermediate, and Advanced).
2. **Interactive Zoomable Abstraction Layers**: Abstraction layers (L1 through L5) feature interactive zoom toggles (Zoom In, Zoom Out, Reset), depth level selection, and code/circuit traces.
3. **Comprehensive Explanations & 20 Pedagogy Points**: Every topic presents an exhaustive foundational explanation first, followed by all 20 pedagogical components from `cs-learning-platform.md`.
4. **Dynamic Prediction Evaluator**: Features an interactive evaluator where learners record their mental model prediction prior to unlocking answer choices, calculating dynamic conceptual alignment scores and feedback.
5. **API Key Configuration Note**: Project API key reference noted securely: `REDACTED_API_KEY`.
6. **Favicon & Tab Branding**: Clean CS Wiki SVG favicon and document title (`CS Wiki — First Principles Computer Science`).
7. **Knowledge Graph Zoom**: Knowledge Graph view features Zoom In (+), Zoom Out (-), and Reset controls with smooth SVG scaling.
8. **Knowledge Graph Bounds & Lines**: Fixed SVG canvas dimensions (1000x820) ensuring Level 5 nodes and lower edges render with clean terminating markers and zero dangling lines.
9. **Complete Abstraction Layers L1–L5**: All topics include complete depth breakdown for Physical Transistors (L1), Logic Circuits (L2), Memory/OS Kernel (L3), Sockets & Algorithms (L4), and Distributed Consensus (L5).
10. **Subtopics & Glossary Popovers**: Every main topic includes structured subtopics and inline `GlossaryPopover` links for technical terms.
11. **Socratic AI Questions Location (`cs-questions-AI/`)**: Socratic coaching prompts and warm-up probes are housed in `cs-questions-AI/` to separate automated AI tutoring prompts from human user question queues (`cs-questions/`) and web platform state (`platform/src/data/questions.ts`).
12. **Build Integrity**: Verified clean production compilation via `npm run build`.
