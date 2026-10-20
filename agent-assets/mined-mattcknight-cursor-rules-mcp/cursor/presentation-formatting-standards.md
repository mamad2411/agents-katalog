# Presentation Document Formatting Standards

**Rule for creating clean, modern, readable presentation documents that convert to HTML.**

---

## Core Principle

**Presentation documents MUST be clean, modern, and professional. No retro terminal styling. Maximum readability.**

---

## Section 1: Visual Styling Rules

### ❌ FORBIDDEN: Retro Terminal Styling

**NEVER use double-line borders:**

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SCOPE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Problem:** Looks like retro terminal/Tetris text, unprofessional, hard to read

### ✅ CORRECT: Modern Clean Headers

**ALWAYS use emoji-enhanced bold headers:**

```markdown
**🎯 Analysis Scope:**

**📋 Analysis Requirements:**

**📄 Expected Output:**

**💾 Save Location:**
```

**Why:** Clean, professional, visual hierarchy, easy to scan

### Standard Emoji Icons

| Icon | Usage |
|------|-------|
| 🎯 | Scope, Objectives, Goals |
| 📋 | Requirements, Methodology, Context |
| 📄 | Output, Deliverables, Results |
| 💾 | Save Location, File Path |
| ✅ | Correct, Recommended, Good Practice |
| ❌ | Wrong, Forbidden, Bad Practice |
| ⚠️ | Warning, Caution, Important |
| 🔴 | Critical, High Priority, Danger |
| 🟡 | Medium Priority, Warning |
| 🟢 | Low Priority, Success |

---

## Section 2: Code Block Rules

### Code Block Styling (Python Script)

**The HTML conversion script MUST style code blocks with:**

```css
pre {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: none;
    border-radius: 12px;
    padding: 24px;
    color: #ffffff;
    box-shadow: 0 10px 40px rgba(0,0,0,0.15);
}

pre code strong {
    color: #ffd700;  /* Gold for emoji headers */
    font-size: 1.1em;
    border-bottom: 2px solid rgba(255,255,255,0.2);
}
```

**Why:** Modern gradient look (VS Code dark theme style), not boring gray boxes

### ❌ FORBIDDEN: Nested Code Blocks

**NEVER nest code blocks:**

```markdown
```markdown
@persona-developer

**Code:**
```javascript
function example() {
  return true;
}
```
```
```

**Problem:** Breaks markdown parsing, renders as single line of text

### ✅ CORRECT: Separate Code Blocks

**ALWAYS separate code examples:**

```markdown
**Prompt:**

```markdown
@persona-developer
```

**Code Example:**

```javascript
function example() {
  return true;
}
```
```

**Why:** Clean rendering, proper syntax highlighting

### Language Identifiers

**ALWAYS include language identifiers:**

```markdown
```javascript
// Good - has language identifier
```

```
// Bad - no language identifier
```
```

**Supported languages:** `javascript`, `typescript`, `python`, `java`, `csharp`, `sql`, `bash`, `powershell`, `yaml`, `json`, `markdown`, `mermaid`

---

## Section 3: Visual Flow Diagrams

### ❌ FORBIDDEN: Plain Text Flows

**NEVER use plain text with arrows:**

```markdown
API Input → Validation → Service Layer → Database
```

**Problem:** Just plain text, no visual representation

### ✅ CORRECT: Mermaid Diagrams

**ALWAYS use mermaid diagrams for flows:**

```markdown
```mermaid
graph LR
    A[API Input] --> B[Validation]
    B --> C[Service Layer]
    C --> D[Database]
```
```

**Why:** Visual, interactive, professional

### Mermaid Diagram Direction

**Use left-to-right (LR) for sequential workflows:**

```mermaid
graph LR
    A[Start] --> B[Step 1]
    B --> C[Step 2]
    C --> D[End]
```

**Use top-down (TD) only for hierarchies or when space is limited:**

```mermaid
graph TD
    A[Parent]
    A --> B[Child 1]
    A --> C[Child 2]
```

---

## Section 4: Content Organization

### ❌ FORBIDDEN: Cramped Lists

**NEVER cram content into tight bullet points:**

```markdown
❌ "likely", "probably", "should", "might", "will be"
❌ "more effective", "better", "easier", "quicker"
❌ "ready to implement", "can start", "implementation ready"
```

**Problem:** Hard to read, no context, visually overwhelming

### ✅ CORRECT: Organized Tables

**ALWAYS use tables for comparisons and categorized content:**

```markdown
| Category | Forbidden Phrase | Why It's Wrong |
|----------|------------------|----------------|
| **Assumptions** | "likely", "probably", "should" | Makes assumptions without facts |
| **Comparisons** | "more effective", "better" | Unsolicited recommendations |
| **Status Claims** | "ready to implement" | Only humans can approve implementation |
```

**Why:** Clear categories, explanations, easy to scan

### Visual Hierarchy

**Use proper heading levels:**

- `#` - Document title only
- `##` - Major sections (1. Introduction, 2. Core Concepts)
- `###` - Subsections (2.1 Persona Types)
- `####` - Sub-subsections (specific rules within subsections)

**Add separators between major sections:**

```markdown
---
```

---

## Section 5: Tool Design Principles

### ❌ FORBIDDEN: Multiple Conversion Scripts

**NEVER create separate formatting/conversion scripts:**

```
scripts/
├── convert_md_to_html.py
├── convert_retro_to_modern.py  ❌ BAD
├── fix_formatting.py            ❌ BAD
└── cleanup_styles.py            ❌ BAD
```

**Problem:** Tool bloat, maintenance nightmare, confusing workflow

### ✅ CORRECT: Single Comprehensive Script

**ALWAYS build functionality into one main script:**

```
scripts/
└── convert_md_to_html_for_presentation.py  ✅ GOOD
    - Reads markdown
    - Applies modern styling
    - Converts to HTML
    - Generates mermaid diagrams
    - One command does everything
```

**Why:** Simple, maintainable, clear workflow

---

## Section 6: Readability Principles

### Always Provide Context

**When showing wrong vs. right examples:**

1. ✅ Show the wrong way with ❌
2. ✅ Explain WHY it's wrong
3. ✅ Show the correct way with ✅
4. ✅ Explain WHY it's better
5. ✅ Add a summary reminder

### Example Structure

```markdown
#### ❌ Wrong Approach

[Show bad example]

**Problem:** [Why it's wrong]

#### ✅ Correct Approach

[Show good example]

**Why:** [Benefits of correct approach]

**Remember:** [Key takeaway]
```

### Breathing Room

- ✅ Add blank lines between sections
- ✅ Use horizontal rules (`---`) to separate major sections
- ✅ Don't cram content together
- ✅ Use tables to naturally space content
- ✅ Add margins in CSS styling

---

## Section 7: HTML Conversion Requirements

### CSS Requirements

**The HTML conversion script MUST include:**

1. **Modern code block styling** - Gradient backgrounds, not gray boxes
2. **Emoji support** - Headers styled with gold color
3. **Table styling** - Clean borders, alternating row colors
4. **Responsive design** - Works on mobile and desktop
5. **Print-friendly** - Page breaks, clean printing
6. **Mermaid support** - Load mermaid.js for diagram rendering

### Font Requirements

**Code blocks MUST use modern monospace fonts:**

```css
font-family: "SF Mono", "Monaco", "Inconsolata", "Fira Code", 
             "Droid Sans Mono", "Source Code Pro", monospace;
```

### Color Scheme

**Code blocks:**
- Background: Purple gradient (`#667eea` to `#764ba2`)
- Text: White (`#ffffff`)
- Headers: Gold (`#ffd700`)
- Comments: Light gray (`#e0e0e0`)

**Tables:**
- Header: Blue (`#3498db`)
- Alternating rows: Light gray (`#f9f9f9`)

---

## Section 8: Common Mistakes to Avoid

### Mistake 1: Nested Code Blocks

```markdown
❌ WRONG:
```markdown
```javascript
code here
```
```

✅ CORRECT:
Separate the markdown prompt from the code example
```

### Mistake 2: Plain Text Flows

```markdown
❌ WRONG:
A → B → C → D

✅ CORRECT:
```mermaid
graph LR
    A --> B --> C --> D
```
```

### Mistake 3: No Language Identifiers

```markdown
❌ WRONG:
```
function test() {}
```

✅ CORRECT:
```javascript
function test() {}
```
```

### Mistake 4: Cramped Content

```markdown
❌ WRONG:
List with no spacing or organization

✅ CORRECT:
| Category | Item | Description |
|----------|------|-------------|
| ... | ... | ... |
```

---

## Verification Checklist

Before publishing a presentation document, verify:

- [ ] No double-line borders (━━━━) anywhere
- [ ] All code blocks have language identifiers
- [ ] No nested code blocks
- [ ] Flows use mermaid diagrams (not plain text)
- [ ] Tables used for comparisons and categorized lists
- [ ] Proper heading hierarchy (h1, h2, h3, h4)
- [ ] Emoji icons used consistently
- [ ] Horizontal rules separate major sections
- [ ] Content has breathing room (not cramped)
- [ ] HTML renders with gradient code blocks
- [ ] Mermaid diagrams render correctly

---

## Integration with Conversion Script

**File:** `scripts/convert_md_to_html_for_presentation.py`

**Must include:**
1. Modern gradient CSS for code blocks
2. Gold styling for emoji headers in code blocks
3. Mermaid.js integration
4. Responsive table styling
5. Print-friendly CSS

**Must NOT include:**
- Gray box code blocks
- Plain text rendering
- Retro terminal styling

---

**Last Updated:** 2025-01-18  
**Version:** 1.0.0  
**Rule Type:** CRITICAL - Presentation Formatting  
**Priority:** HIGH  
**Always Apply:** YES - For all `.presentation.md` files
