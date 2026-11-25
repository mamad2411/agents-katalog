
START SPECIFICATION:
---
description: Generate high-level project overview documentation focusing on the core business logic and domain-specific implementations, particularly for text processing and speech synthesis pipelines
globs: *.py,*.md
alwaysApply: false
---


# main-overview

## Development Guidelines

- Only modify code directly relevant to the specific request. Avoid changing unrelated functionality.
- Never replace code with placeholders like `# ... rest of the processing ...`. Always include complete code.
- Break problems into smaller steps. Think through each step separately before implementing.
- Always provide a complete PLAN with REASONING based on evidence from code and logs before making changes.
- Explain your OBSERVATIONS clearly, then provide REASONING to identify the exact issue. Add console logs when needed to gather more information.


E11ocutionist is a specialized text-to-speech processing system with a multi-stage pipeline for optimizing literary content for speech synthesis.

Core Processing Pipeline:
1. Document Chunking
- Semantic analysis for intelligent document segmentation
- Hierarchical organization: doc -> chunks -> units -> items
- Language-aware chapter/scene boundary detection
- Business Importance: 95

2. Named Entity Processing
- Entity recognition with pronunciation mapping
- Multi-language entity detection and tagging
- Domain-specific classification (people, locations, organizations)
- Business Importance: 85

3. Speech Enhancement
- Sentence restructuring for natural flow
- Word/symbol normalization for speech
- Punctuation enhancement for pacing
- Emotional emphasis tagging
- Business Importance: 90

4. Tone Control
- Emphasis pattern optimization
- Pronunciation refinement
- Dialog formatting standardization
- Business Importance: 75

5. Speech Synthesis Integration
- ElevenLabs-specific markup conversion
- Personal voice profile management
- Multi-voice batch processing
- Business Importance: 80

Key Implementation Components:

1. Text Processing Orchestration (src/e11ocutionist/e11ocutionist.py)
- Manages complete processing pipeline
- Handles state preservation between stages
- Business Importance: 85

2. Dialog Processing System (src/e11ocutionist/elevenlabs_converter.py)
- Custom dialog transformation rules
- Quote standardization
- Speech timing markup
- Business Importance: 80

3. Entity Management (src/e11ocutionist/entitizer.py)
- Progressive entity processing
- Pronunciation dictionary maintenance
- Cross-document consistency
- Business Importance: 75

The system specializes in transforming literary content into enhanced speech synthesis markup through intelligent processing stages, maintaining semantic meaning while optimizing for natural speech output.

$END$
END SPECIFICATION