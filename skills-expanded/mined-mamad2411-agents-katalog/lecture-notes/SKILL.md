---
name: lecture-notes
description: Transform lecture materials (slides, PDFs, text snippets, transcripts, audio, or video recordings) into comprehensive, exam-ready Markdown notes for Obsidian. Use when the user provides lecture content, study materials, or asks to take notes, summarize lectures, or create study guides. Outputs structured notes with key concepts, definitions, LaTeX math, and exam-important callouts.
license: MIT
metadata:
  author: emmsixx
  version: "1.3"
---

# Lecture Notes Skill

Transform lecture materials into structured, exam-ready Markdown notes for Obsidian.

## Audio and Video Inputs

When the source material is an audio or video file, always create a local transcript first and use that transcript as the primary input for note generation.

### Required Workflow
1. **If the input is audio**, transcribe it with OpenRouter using `openai/gpt-4o-audio-mini` and the `input_audio` format.
2. **If the input is video**, first extract a separate audio file with `ffmpeg`, then transcribe that extracted audio with OpenRouter.
3. **Save the transcript locally as a plain text file** and use that saved transcript for the rest of the lecture-notes workflow.
4. If useful, also save the raw JSON response locally, but the `.txt` transcript is the canonical note-generation source.

### OpenRouter Audio Transcription
Before using audio or video transcription, make sure `OPENROUTER_API_KEY` is defined in the environment.

Use OpenRouter's chat completions API with multimodal `input_audio`. The prompt should explicitly ask for a verbatim transcript with minimal cleanup.

```bash
AUDIO_BASE64=$(base64 < "Lecture 05.audio.wav" | tr -d '\n')

curl https://openrouter.ai/api/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -d "{\n    \"model\": \"openai/gpt-4o-audio-mini\",\n    \"messages\": [\n      {\n        \"role\": \"user\",\n        \"content\": [\n          {\n            \"type\": \"text\",\n            \"text\": \"Transcribe this lecture audio as plain text. Keep the wording faithful to the speaker, preserve important structure, and do not summarize.\"\n          },\n          {\n            \"type\": \"input_audio\",\n            \"input_audio\": {\n              \"data\": \"$AUDIO_BASE64\",\n              \"format\": \"wav\"\n            }\n          }\n        ]\n      }\n    ]\n  }"
```

For actual skill usage, save the JSON response first, then extract the transcript into a plain text file:

```bash
AUDIO_BASE64=$(base64 < "Lecture 05.audio.wav" | tr -d '\n')

curl https://openrouter.ai/api/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -d "{\n    \"model\": \"openai/gpt-4o-audio-mini\",\n    \"messages\": [\n      {\n        \"role\": \"user\",\n        \"content\": [\n          {\n            \"type\": \"text\",\n            \"text\": \"Transcribe this lecture audio as plain text. Keep the wording faithful to the speaker, preserve important structure, and do not summarize. Return only the transcript text.\"\n          },\n          {\n            \"type\": \"input_audio\",\n            \"input_audio\": {\n              \"data\": \"$AUDIO_BASE64\",\n              \"format\": \"wav\"\n            }\n          }\n        ]\n      }\n    ]\n  }" \
  > "Lecture 05.transcript.response.json"

jq -r '.choices[0].message.content // (.choices[0].message.content[]? | select(.type == "text") | .text)' \
  "Lecture 05.transcript.response.json" > "Lecture 05.transcript.txt"
```

### Recommended Local File Outputs
Given an input file like `Lecture 05.mp4` or `Lecture 05.m4a`, save derived files alongside it using predictable names:
- `Lecture 05.audio.wav` for audio extracted from video or normalized for upload
- `Lecture 05.transcript.response.json` for the OpenRouter API response
- `Lecture 05.transcript.txt` for the plain text transcript used to generate notes

### Video to Audio Extraction
Use `ffmpeg` to extract audio from video before transcription. A safe default is:

```bash
ffmpeg -i "Lecture 05.mp4" -vn -ac 1 -ar 16000 -c:a pcm_s16le "Lecture 05.audio.wav"
```

If the source is already audio but not in a convenient format, normalize it to `.wav` before base64 encoding and upload.

### Transcript Handling Rules
- Always generate notes from the saved local transcript file, not directly from the raw media file.
- If the user also provides slides, PDFs, or other lecture materials, combine them with the transcript when producing notes.
- Preserve important spoken structure such as section transitions, definitions, theorem statements, examples, and repeated exam hints.
- If the transcript is clearly noisy or incomplete, note uncertainty in the final notes rather than silently inventing missing content.
- If a transcript already exists locally for the same media file, reuse it unless the user explicitly asks for a fresh transcription.

## Output Format

Output all notes inside fenced codeblocks. When content spans multiple chapters or distinct topics, create separate files.

### File Naming
`Chapter X - Title.md` or `Unit X - Title.md`

### Document Structure
```markdown
---
course: [Course name if known]
lecture: [Lecture number/title]
date: [Date if provided]
tags: [relevant, topic, tags]
---

# Title
Brief overview connecting to previous material when applicable.

## Key Concepts
Bulleted summary of the most important takeaways.

## [Content Sections]
Organized by topic from the source material.

## Definitions
New terms introduced in this lecture.

## [Additional Sections as Needed]
Examples, proofs, diagrams, etc.
```

## Formatting Rules

### Headings
No empty lines after headings. Content begins immediately on the next line:
```markdown
## Section Title
Content starts here directly below the heading.
```

### Math and Equations
Use LaTeX inside `$...$` (inline) or `$$...$$` (block):
```markdown
The quadratic formula is $x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$.

$$
\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}
$$
```

### Footnotes
Use Markdown footnotes for supplementary information. Never use citations:
```markdown
This concept was introduced in 1905[^1].

[^1]: Additional context or clarification here.
```

### Callouts for Exam-Important Content
Use Obsidian callouts to flag critical information:
```markdown
> [!important] Exam Alert
> This formula is frequently tested.

> [!note] Remember
> Supplementary context or tips.

> [!example] Worked Example
> Step-by-step demonstration.

> [!warning] Common Mistake
> Students often confuse X with Y.

> [!definition] Term
> Formal definition here.
```

### Wiki-Links
Use `[[double brackets]]` to link related concepts:
```markdown
This relates to [[Chapter 2 - Thermodynamics#Entropy]].
```

## Content Guidelines

### Completeness
Capture all information from source material, especially:
- Formulas and equations
- Definitions and theorems
- Examples and worked problems
- Diagrams (describe or recreate in text/ASCII if needed)
- Any content emphasized as important by the lecturer

### Definitions Section
Always include a `## Definitions` section. Format each term:
```markdown
## Definitions
**Term**
Precise definition immediately below.

**Another Term**
Its definition here.
```

### Connections
When possible, reference previous lectures or related concepts:
```markdown
## Key Concepts
- Builds on [[Chapter 3 - Kinematics]] by introducing forces
- Extends the velocity equations to include acceleration
```

### Examples
Preserve all examples from source material. Format with the example callout:
```markdown
> [!example] Finding the Derivative
> Given $f(x) = x^3 + 2x$, find $f'(x)$.
>
> **Solution:**
> $$f'(x) = 3x^2 + 2$$
```

## Multiple Files

When source material covers multiple distinct chapters or units, output each as a separate codeblock with clear file naming:

````markdown
```markdown
<!-- Chapter 1 - Introduction.md -->
---
course: Physics 101
...
```
````

````markdown
```markdown
<!-- Chapter 2 - Mechanics.md -->
---
course: Physics 101
...
```
````
