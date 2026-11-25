# Attribution

**Buchbinder** builds upon and substantially expands the work of multiple antecedent projects spanning both agentic and non-agentic AI writing tools. This document records the full chain of attribution.

---

## Direct Lineage

### Primary Source

**novel-writer-english** by JeroTan
- **Repository**: https://github.com/JeroTan/novel-writer-english
- **License**: MIT
- **Role**: Provided the initial English-language translation, platform-agnostic re-architecture, and the eight-step methodology structure that Buchbinder uses as its fiction track foundation. The command-based workflow, constitution/specify/clarify/plan/write/edit/review loop, pre-write checklist system, genre knowledge bases, and writing technique skills all derive from this project.

### Secondary Source

**novel-writer-skills** by wordflowlab (wutongci)
- **Repository**: https://github.com/wordflowlab/novel-writer-skills
- **License**: MIT
- **Role**: Original Chinese-language methodology, skill architecture, auto-detection patterns, and quality assurance framework that novel-writer-english itself built upon.

---

## Prior Work by the Author

### Fiction Fabricator

**Fiction Fabricator** by Thomas Highbaugh (the author of Buchbinder)
- **Repository**: https://github.com/Thomashighbaugh/fiction-fabricator
- **License**: MIT
- **Role**: The author's earlier non-agentic AI novel generation system — a Python CLI that produced full-length novels via LLM APIs through multi-phase content synthesis, interactive editing, and an XML-based state management system. Buchbinder inherits several concepts from Fiction Fabricator, refined and re-architected for an agentic context:

| Concept | Fiction Fabricator | Buchbinder |
|---------|-------------------|------------------|
| **Multi-phase generation** | Outline → draft → refine pipeline | 25-subcommand workflow with quality gates between phases |
| **XML state persistence** | XML files for project state and patch logs | XML-structured drafting with internal verification tags, JSON checkpoints for resume |
| **Lorebook system** | Auto-generated world-building entries with SillyTavern compatibility | Series lorebook infrastructure with cross-book inheritance + external import (SillyTavern/JanitorAI/CharacterAI) |
| **Export options** | EPUB, HTML, Markdown, PDF, TXT | Pandoc-integrated export with post-export verification |
| **Interactive editing** | Chapter management and AI-powered rewrites | Three-pass editing (line-edit → copy-edit → proofread) + 8 critique modes |
| **Resume** | XML patch replay to reconstruct state | JSON checkpoint with content hashing and file diffing |

Fiction Fabricator itself was inspired by and built upon ideas from several other projects in the AI novel generation space:

#### Projects That Influenced Fiction Fabricator

**pulpgen** by pulpgen-dev
- **Repository**: https://github.com/pulpgen-dev/pulpgen
- **License**: MIT
- **Role**: AI novel drafting agent using Google Gemini with a three-phase assembly line (outline generation → content drafting → interactive revision). Inspired Fiction Fabricator's multi-phase generation approach and XML-based patch system for tracking narrative evolution. Buchbinder carries forward the concept of structured phase progression but replaces the patch-replay model with JSON checkpoints and adds hard-block quality gates between phases.

The broader ecosystem of AI-assisted creative writing tools — including character card formats from the SillyTavern community, lorebook structures from the AI roleplay community, and the general methodology of multi-phase novel generation — all contributed ideas that flowed through Fiction Fabricator into Buchbinder's design.

---

## Platform Attribution

### OpenCode

**OpenCode** by the OpenCode team
- **Repository**: https://github.com/sst/opencode
- **Role**: The agentic coding platform that Buchbinder is built for. OpenCode's hub-and-skill architecture, slash command system, per-project `.opencode/` configuration, TypeScript tool JIT compilation, and `hubMenu` routing pattern are the foundation Buchbinder runs on. The entire 26-spec, 32-library, 34-skill structure is designed to install into and operate within OpenCode's per-project configuration model. Buchbinder would not exist without OpenCode's architecture for agent-orchestrated workflows.

### Claude Code

**Claude Code** by Anthropic
- **Role**: Claude Code's terminal-based agentic coding approach — where an AI agent directly manipulates files, runs commands, and iterates on work within a project — was a major inspiration for the shift from Fiction Fabricator's non-agentic Python CLI model to Buchbinder's agentic workflow design. The idea that a writing pipeline could be driven by an AI agent making decisions about which phase to run, what context to load, and how to verify quality — rather than a fixed Python script executing predetermined steps — came from seeing what Claude Code and similar agentic tools made possible.

---

## What Buchbinder Adds

While the DNA of the eight-step fiction methodology originates from the projects above, Buchbinder introduces substantial new architecture, binding, and tooling:

| Area | Novelty |
|------|---------|
| **Non-fiction track** | Full non-fiction workflow with thesis/argument structuring, citation management (APA, Chicago, MLA, IEEE), source evaluation, and bibliography generation — no antecedent exists in either source project. |
| **Research phase** | Active research ingestion: web search integration, source extraction and annotation, interview methods, field notes, and literature review workflows. The original treated research as passive genre knowledge only. |
| **Critique workflow** | 8 structured critique modes (alpha, beta, peer, sensitivity, cold-read, comprehensive, adversarial two-agent dialectic, personas with 3-5 reader types) as a distinct phase with feedback categorization and prioritization matrices. The original had only self-editing. |
| **Revision cycle** | Dedicated revision planning between critique and edit with a revision-verify gate, plus `--depth full` multi-pass revision (structural→language→pacing). The original looped directly from review back to edit. |
| **Three-pass editing** | Line-edit (craft) → copy-edit (mechanics) → proofread (typos) as distinct passes, each with a different focus. |
| **Publish pipeline** | Pandoc-integrated multi-format export with post-export verification, replacing Fiction Fabricator's direct Python generators. |
| **25 hard-block quality gates** | Evidence-based pass/fail gates across 7 categories (outline, pre-draft, post-draft, revision, structural, linguistic, experience). No soft warnings — gates block progression on failure. No antecedent had programmatic quality gates. |
| **Fine-grained outline with gate** | Scene beats (min 2/chapter), setup/payoff bidirectionality, continuity anchors, pacing distribution — with a quality gate that blocks drafting if the outline is too coarse, plus 3 revision cycles. |
| **Awareness maps** | Each chapter loads only its outline slice (scene beats, payoff-from, sets-up, continuity anchors, adjacent summaries) instead of the whole book. Post-draft gate verifies the awareness map was honored. |
| **Phase 2 structural analyses** | 14 dedicated analysis libraries: reverse outline, character arc, Q/A accounting, promise audit, escalation curve, subtext, rhythm, purple prose, immersion, trust, cognitive load, knowledge state, opening/closing, cliché detection. |
| **Voice fingerprinting** | Per-character AND per-narration voice profiles with independent fingerprints. |
| **Modular style sheets** | 5 separate modules (prose, dialogue, description, pacing, POV) instead of a monolithic style document. |
| **Series lorebook** | Cross-book knowledge base with inheritance, sync, audit, and external import (SillyTavern/JanitorAI/CharacterAI). |
| **Premise stress-test** | 6-criteria hard block before specification begins. |
| **Thematic statement** | Required, testable argument (not just a topic) in the constitution, referenced by outline and critique. |
| **TypeScript tooling** | All internal tools written in TypeScript — 26 spec files, 32 library files, compiled via OpenCode's JIT tool loading. The original used Python only. |
| **Per-project plugin** | Designed specifically for per-book `.opencode/` installation as an npm-installable plugin, not a global resource. |
| **Command architecture** | `/buchbinder` hub with 25 subcommands via `hubMenu` routing rather than flat top-level commands. Full project state machine with phase detection, drift analysis, and contextual navigation. |
| **Batch-first defaults** | All pipeline phases default to batch processing (up to 6 chapters) with shared context loaded once per batch. Single-chapter is an explicit override. |
| **Serious tone** | Professional register throughout — no emoji in command output, no tutorial-style cheerful framing. |

---

## License

Buchbinder is released under the MIT license, consistent with all antecedent projects.

The original copyrights remain with their respective authors:
- wordflowlab / wutongci — novel-writer-skills
- JeroTan — novel-writer-english
- Thomas Highbaugh — Fiction Fabricator
- pulpgen-dev — pulpgen

All new work in Buchbinder is:
- Copyright (c) 2026 Buchbinder contributors
- Licensed under MIT
