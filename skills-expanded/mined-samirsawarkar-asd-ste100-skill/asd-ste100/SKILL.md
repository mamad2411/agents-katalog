---
name: asd-ste100
description: >
  Comprehensive ASD-STE100 Simplified Technical English (STE) skill and prompt compiler
  for Claude Code, OpenAI Codex, and LLMs. Repurposes aerospace maintenance controlled
  English to eliminate ambiguity in agent communications and human comprehension.
  Implements Andrej Karpathy's Ladder of Understanding: 80% ASD-STE100 prose,
  structural diagrams (Mermaid/SVG), interactive single-file HTML micro-simulators,
  and bespoke 3Blue1Brown-style explainer video scripts with synced TTS narration.
  Use when asked for "ASD-STE100", "STE-100", "simplify English", "controlled language",
  "karpathy style", "high-bandwidth output", "interactive explainer", or "3b1b video".
argument-hint: "[ste100|80-ste100|diagram|html|video|all] [topic or prompt]"
license: MIT
---

# ASD-STE100 Skill: Simplified Technical English & The Karpathy Ladder

> *"We'll be spending a lot more time trying to understand the outputs of language models... As LLMs get better, they will do more and more of the legwork autonomously, and a lot more of our work will rise up the abstractions into oversight and understanding."*  
> — **Andrej Karpathy**

Default LLM outputs are linear, verbose, and cognitively expensive. This skill implements the international ASD-STE100 standard and Karpathy's hierarchy of high-bandwidth comprehension artifacts to replace walls of conversational AI text with unambiguous, discardable, high-leverage cognitive aids.

---

## The Four Rungs of the Ladder

```
 ▲ Rung 4: Bespoke Explainer Videos (3b1b / Manim + Synced TTS)
 │   └── Vector animation script + timestamped audio narration.
 │
 ▲ Rung 3: Interactive Web Artifacts (Single-File HTML / Canvas / JS)
 │   └── Hands-on state simulation: step controls, sliders, reactive boards.
 │
 ▲ Rung 2: Visual Structural Diagrams (Mermaid.js / Standalone SVG)
 │   └── Spatial cognition: message exchanges, state lifecycles, data flows.
 │
 █ Rung 1: Controlled Technical English (ASD-STE100 / 80% Softened STE)
     └── Linguistic density: <=25 words/sentence, active voice, zero fluff.
```

---

## Operating Modes

This skill operates in two distinct modes depending on user intent:

### Mode 1: Prompt Converter (When the user wants a prompt to use elsewhere)
Triggered by: *"Convert this prompt to Karpathy style"*, *"Make a prompt for Claude/Codex to explain X"*, or when given a raw prompt without asking for the explanation directly.
- Read or accept the user's base prompt.
- Select the appropriate rung (or full ladder package).
- Output the engineered, high-octane prompt formatted with strict constraint blocks and output specifications.
- You can also run the local compiler helper:
  ```bash
  python3 /Volumes/SamirDrive/Development/karpathy-explainer/scripts/compile_prompt.py --tier all "Your prompt here"
  ```

### Mode 2: Autonomous Execution (When the user wants the explanation directly)
Triggered by: *"Explain X using Karpathy ladder"*, *"Teach me X in ASD-STE100"*, *"/karpathy-explainer [rung] [topic]"*.
- Directly generate the high-bandwidth artifacts according to the requested rung (or default to the multi-tier package).

---

## Detailed Rules per Rung

### Rung 1: Controlled Technical Writing (ASD-STE100 & 80% Softened STE)

ASD-STE100 is an aerospace maintenance specification designed to eliminate ambiguity and prevent human error.

#### Hard Quantitative Limits
- **Procedural sentences**: Max **20 words**.
- **Descriptive sentences**: Max **25 words**.
- **Paragraphs**: Max **6 sentences**. Exactly **one topic** per paragraph.
- **Noun clusters**: Max **3 words** (e.g. `memory buffer pool`).
- **Instructions per sentence**: Max **1 instruction** (unless actions are strictly simultaneous).

#### Verb Rules
- **Approved Verb Forms**:
  - Command / Imperative: `Run the validation check.`
  - Simple Present: `The worker thread polls the queue.`
  - Simple Past: `The leader node dropped the socket.`
  - Simple Future: `The replica will catch up.`
  - Infinitive: `Call the cleanup routine to free memory.`
  - Past Participle as adjective: `The closed connection.`
- **Banned Verb Forms**:
  - Progressive (`-ing`): Ban `is processing`, `are running`. Use simple present instead.
  - Perfect Tenses: Ban `has committed`, `had written`. Use simple past.
  - Passive Voice in procedures: Ban `The log must be flushed`. Use active imperative: `Flush the log.`

#### Mandatory Plain Replacements
- `ensure` -> **MAKE SURE**
- `prior to` -> **BEFORE**
- `replenish` -> **FILL**
- `utilize` -> **USE**
- `commence` -> **START**
- `approximately` -> **ABOUT**
- `in order to` -> **TO**
- `terminate` -> **STOP / END**
- `modify` -> **CHANGE**
- `obtain` -> **GET**

#### The "80% ASD-STE100" Softening
For computer science and software systems:
- Keep all structural constraints (word caps, active voice, simple tenses, plain verbs, zero AI buzzwords).
- Permit necessary domain technical nouns (*idempotency*, *backpressure*, *quorums*, *mutex*).
- **Zero AI Buzzwords**: Strictly ban *delve, leverage, tapestry, seamless, revolutionize, testament, beacon, holistic, game-changer, blazing-fast*.
- **No Semicolons (Rule 8.1)**: STE strictly bans semicolons. Split compound statements into two sentences.
- **No Nominalizations (Rule 3.7)**: Use direct verbs ('analyze', not 'perform an analysis of').
- **No Soft Phrasal Verbs (Rule 9.3)**: Use single plain verbs ('start', not 'spin up'; 'contact', not 'reach out').
- **Preserve Modality & Hedges**: Never upgrade hedges (*may, could, might, is likely to*) to false certainties. Preserving probabilistic nuance is essential for technical accuracy.
- **Output Discipline**: Deliver clean, unpadded results. Do not add chatty preamble or self-referential summaries.

---

### Rung 2: Visual Structural Diagrams (Mermaid & SVG)

Never rely solely on prose to describe topologies, state machines, or network protocols.
- **Protocol / Message Passing**: Always generate a `sequenceDiagram` with explicit actor names, arrows (`->>`, `-->>`), and payload labels.
- **Architecture / Topology**: Generate a `flowchart TD` or `flowchart LR` with grouped `subgraph` clusters.
- **State Machines**: Generate a `stateDiagram-v2` with clear transitions (`[*] --> Idle --> Active --> [*]`).
- **Data Flow / Schema**: Include an invariants summary table below the diagram.

---

### Rung 3: Discardable Interactive Web Artifacts (Single-File HTML)

LLMs excel at writing self-contained frontend code. Deliver discardable micro-simulators:
- **Zero Build / Single File**: Put all HTML, CSS, and JavaScript into a single `.html` file. It must open directly via `open explainer.html`.
- **Interactive State Stepper**: Provide `[Step Back]`, `[Play / Pause]`, `[Step Forward]`, `[Reset]` controls.
- **Visual State Canvas / SVG**: Graphically render the system state (e.g., node rings, queue buffers, tree nodes, memory blocks) that update reactively as steps advance.
- **State Inspector Pane**: Display current variables, active step description in 80% ASD-STE100, and invariants verified.
- **Dark Mode Aesthetics**: Use crisp engineering dark mode (`#0d1117` background, `#58a6ff` primary accent, `#3fb950` success, monospace font tokens).

---

### Rung 4: Bespoke Explainer Videos (3b1b / Manim + Synced TTS)

For deep mathematical, algorithmic, or conceptual subjects:
- **Manim Script (`scene.py`)**:
  - Valid Manim Community Edition code (`manim -pql scene.py MainScene`).
  - High-contrast 3b1b aesthetic (dark slate background, vibrant colored vectors, smooth camera movements, `TransformMatchingShapes`).
- **Timed Narration Transcript (`voiceover.md`)**:
  - Script broken into numbered scenes with visual timestamp markers: `[00:00 - FadeIn Title]`, `[00:08 - Split Node]`.
  - Written in 80% ASD-STE100 cadence matching the exact animation duration.
- **Audio Pipeline (`narrate.sh`)**:
  - Provide a one-liner using free local compute (`edge-tts` or macOS `say`):
    ```bash
    # Free local compute via Microsoft Neural TTS (zero API key)
    edge-tts --voice en-US-ChristopherNeural --file voiceover.txt --write-media narration.mp3
    # Or macOS native
    say -v Samantha -f voiceover.txt -o narration.aiff && ffmpeg -i narration.aiff narration.mp3
    # Mux video + audio
    ffmpeg -i MainScene.mp4 -i narration.mp3 -c:v copy -c:a aac final_explainer.mp4
    ```
  - Also provide optional ElevenLabs API snippet for studio-grade voice.

---

## Quick Reference Commands

| User Request | Action | Target Rung |
| :--- | :--- | :--- |
| `explain <topic>` (default) | Provide 80% STE-100 summary + Mermaid diagram | Rungs 1 & 2 |
| `make interactive app for <topic>` | Write standalone `explainer.html` | Rung 3 |
| `make 3b1b video for <topic>` | Write `scene.py` + `voiceover.md` + `narrate.sh` | Rung 4 |
| `convert prompt: <prompt>` | Output compiled multi-tier prompt | Prompt Compiler |
| `check text in STE-100` | Run `compile_prompt.py --lint` on target text | STE-100 Linter |
