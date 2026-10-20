---
name: scholarly-content-updater
description: This skill updates any specified file by comparing current content against a provided reference source (URL, document, or template), adding missing elements while maintaining MoxyWolf brand voice, and providing proper bibliographic citations.
---

# Scholarly Content Updater Skill

## Overview
This skill updates any specified file by comparing current content against a provided reference source (URL, document, or template), adding missing elements while maintaining MoxyWolf brand voice, and providing proper bibliographic citations.

## When to Use This Skill
- User specifies a file path and reference source for comparison
- User wants to add or strengthen content based on authoritative sources
- User needs updates delivered in a ready-to-paste markdown format
- User wants voice consistency maintained (MoxyWolf or other specified style)

## Required Inputs

The user must provide:
1. **Target file path** - Full path to the file being updated
2. **Reference source** - URL, document path, or citation to compare against
3. **Focus area** (optional) - Specific elements to add or strengthen
4. **Voice/style** (optional) - Defaults to MoxyWolf if not specified

## Core Process

### Step 1: Read Current Content

Ask user for the target file path, then use `view` tool to read it.

**Example invocation:**
```
Update file: /path/to/my/document.md
Using reference: https://example.com/authoritative-source
Focus: Add the framework for X and examples of Y
```

### Step 2: Load Reference Source

Based on what the user provides:
- **URL**: Use `web_fetch` to retrieve the reference content
- **File path**: Use `view` to read the reference document
- **Citation/concept**: Ask user to provide URL or key points to reference

### Step 3: Load Voice/Style Guidelines

- Default: Read `MoxyWolf Vault/_Shared Knowledge/Brand and Voice/dorian-cougias.md` for MoxyWolf voice
- If user specifies different style, adapt accordingly
- Preserve author's existing voice patterns from the target file

### Step 4: Analyze and Compare

Identify:
- Missing structural elements from reference source
- Gaps in examples or frameworks
- Areas where reference material could strengthen arguments
- Opportunities to add specific quotes, data points, or methodologies
- Contradictions or misalignments that need correction

### Step 4: Apply MoxyWolf Voice
Key principles from the MoxyWolf skill:

**Anchored Boldness**
- Open with clear, confident assertions
- Support with rigorous evidence
- Use construction: "This isn't X. This is Y."

**Recursive Precision**
- Define before using
- Layer from simple to complex
- Progressive disclosure pattern

**Strategic Emphasis**
- *Italics* for new concepts
- **Bold** for critical insights
- CAPS very rarely (only for genuine "Stop. Read that again.")

**Author's Personal Voice**
- Preserve Dorian's first-person stories
- Keep "P and I" references
- Maintain casual asides ("Seriously.", "Here's the thing:")

### Step 5: Generate Markdown Artifact

**ALWAYS** create artifact with this structure:

```markdown
# Updates for [Filename] - [Focus Area]

## Overview
[2-3 sentence summary of what's being added and why]

## Reference Source
[Citation or URL of source material used for comparison]

## New Content

### Addition 1: [Title]
**Location**: Insert after "[existing section name]"

[Complete markdown content ready to copy/paste]

---

### Addition 2: [Title]
**Location**: [Precise placement instruction]

[Content]

## Modifications to Existing Content

### In "[Section Name]" - [What's changing]
**Location**: [Specific paragraph identifier]

**Replace this:**
[Old text snippet for easy finding]

**With this:**
[New content]

---

## Bibliography Additions

Add to bibliography file:

- [Properly formatted citation with URL]
- [Properly formatted citation with URL]

## Integration Checklist
- [ ] Content matches specified voice/style
- [ ] Citations verified and formatted
- [ ] Placement instructions clear
- [ ] Ready to paste
- [ ] Natural flow with existing content
```

### Step 6: Bibliography Management

1. If bibliography file path is known (e.g., 99 Bibliography.md in same directory), read it
2. If not, ask user where bibliography should be documented
3. Check each new source cited
4. Format in requested citation style (default: Chicago 18th edition with URLs)
5. Note if reference source itself needs to be added to bibliography

## Flexible Invocation Patterns

### Pattern 1: Explicit File Path + URL Reference
```
Update: /Users/me/Documents/MyBook/Chapter3.md
Reference: https://example.com/authoritative-guide
Focus: Add the framework for risk management and compliance examples
```

### Pattern 2: Relative Path + Document Reference
```
Update: ./content/analysis.md
Reference: /Users/me/References/research-paper.pdf
Focus: Incorporate the statistical methodology from Section 4
```

### Pattern 3: Quick Update with Context
```
Update Section 2 (file: /path/to/section2.md) using the guidelines from 
https://source.com/guide to add the missing workflow diagrams
```

### Pattern 4: Multiple Files (Batch Mode)
```
Update these files based on https://newstandard.com:
- /path/to/file1.md (add methodology section)
- /path/to/file2.md (update examples)
- /path/to/file3.md (strengthen conclusions)
```

## Voice/Style Handling

### Default: MoxyWolf Voice
If no style specified, apply MoxyWolf voice from `MoxyWolf Vault/_Shared Knowledge/Brand and Voice/dorian-cougias.md`:
- Anchored boldness with recursive precision
- Strategic emphasis (italics for concepts, bold for insights)
- Structured argumentation
- Casual-scholarly blend

### Preserve Existing Voice
Always analyze and maintain:
- Author's personal anecdotes and stories
- Existing terminology and phrases
- Tone consistency (formal, conversational, technical, etc.)
- Structural patterns (headers, lists, emphasis)

### Custom Style
If user specifies different style:
- Apply requested guidelines
- Maintain logical consistency with existing content
- Note any style conflicts in the artifact

## Voice Patterns to Preserve

From existing content, maintain:
- **Opening author's notes**: "Author's note: I like making up terms..."
- **Co-author references**: "P and I", "Coauthor P"
- **Personal stories**: UC/Amazon experiences, MoxyWolf founding
- **Emphasis patterns**: "Read that again. Seriously."
- **Casual-scholarly blend**: Mix of rigorous citations with conversational asides
- **Structural phrases**: "This isn't X. This is Y.", "The distinction matters because..."

## Quality Checks

Before delivering artifact, verify:
✓ MoxyWolf voice applied consistently
✓ Personal elements preserved
✓ All sources checked against existing bibliography
✓ New citations formatted correctly (Chicago 18th + URLs)
✓ Clear location instructions for each addition
✓ No broken markdown
✓ Content flows naturally with existing text
✓ Ready for direct copy/paste

## Example Interaction

**User**: "Update /Users/dorian/Documents/Thesis/Chapter2.md using the framework from https://research-methods.org/qualitative-analysis to add the coding methodology section"

**Assistant Process**:
1. Read `/Users/dorian/Documents/Thesis/Chapter2.md`
2. Fetch content from `https://research-methods.org/qualitative-analysis`
3. Check for MoxyWolf skill (or use specified style)
4. Analyze gaps between current content and reference framework
5. Generate artifact with:
   - New section on coding methodology
   - Examples from reference source adapted to thesis context
   - Integration instructions for Chapter 2
   - Bibliography entry for the reference source
6. Provide ready-to-paste markdown

**Output**: Single markdown artifact with clear sections, appropriate voice, placement instructions, and needed citations.

## Advanced Features

### Citation Style Options

User can specify:
```
Update: /path/to/file.md
Reference: https://source.com
Citation style: APA 7th edition
```

Defaults to Chicago 18th with URLs if not specified.

### Bibliography Auto-Detection

Skill attempts to find bibliography by:
1. Looking for `bibliography.md`, `references.md`, `99 Bibliography.md` in same directory
2. Checking for `\bibliography\` or `\references\` subdirectories
3. Asking user if not found

### Voice Preservation Analysis

Before generating updates, skill analyzes target file for:
- Consistent terminology (e.g., "user" vs "customer" vs "client")
- Emphasis patterns (bold, italics, CAPS usage)
- Section structure (numbered, named, nested depth)
- Personal pronouns (first-person, third-person, passive)
- Technical level (novice, intermediate, expert audience)

Maintains these patterns in all generated content.

## Prompt Template for User

### Minimal Invocation
```
Update [file path] using [reference source]
```

### Detailed Invocation
```
Update: [full file path]
Reference: [URL or file path]
Focus: [specific elements to add/strengthen]
Style: [voice/style to use, default: MoxyWolf]
Citations: [format preference, default: Chicago 18th with URLs]
```

### Natural Language Invocation
```
I need to update [filename] in [directory] to include [specific content] 
from [reference]. Make sure to use [style] voice and add any new citations 
to [bibliography location].
```

## Error Handling

If information is missing, skill will ask:
- **No file path**: "Which file would you like me to update? Please provide the full path."
- **No reference**: "What reference source should I compare against? Please provide a URL or file path."
- **File not found**: "I couldn't find that file. Could you verify the path?"
- **Reference inaccessible**: "I couldn't access that reference. Could you provide the URL or key points to include?"
- **Bibliography unclear**: "Where should I document new citations? Please provide the bibliography file path."

## Quick Start Examples

### Academic Paper Update
```
Update: ~/Dissertation/Chapter3.md
Reference: https://academic-journal.org/methodology-paper
Focus: Integrate the revised statistical framework
```

### Business Document Update  
```
Update: /Company/Strategy/Q4-Plan.md
Reference: https://industry-best-practices.com/2025-guide
Focus: Add competitive analysis framework and market sizing approach
```

### Technical Documentation Update
```
Update: ./docs/api-guide.md
Reference: https://api-standards.org/rest-spec
Focus: Update authentication section with OAuth 2.0 examples
```

The assistant will automatically:
- Read your file
- Fetch/read the reference
- Apply appropriate voice (MoxyWolf by default)
- Generate markdown artifact
- Handle bibliography
- Provide clear integration instructions
