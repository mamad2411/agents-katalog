---
name: notebook-builder
description: Generate Jupyter notebooks (.ipynb) from detailed outlines using Python scripts that build notebook JSON. Triggers on "generate notebook", "build notebook from outline", "turn outline into notebook", or when a ready-to-generate outline exists.
---

# Notebook Builder

Mechanically generates .ipynb notebook files from detailed narrative outlines. This skill handles the **construction** — converting an approved outline into a valid, runnable Jupyter notebook with proper cell structure, engagement elements, and JSON formatting.

```
Approved outline (from outline-writer or lesson-generator)
    ↓
Python generation script (builds cells as dicts)
    ↓
.ipynb JSON file (valid, runnable notebook)
    ↓
Cleanup (remove script, verify structure)
```

**This skill does NOT**:
- Decide what content to include (that's the outline's job)
- Choose pedagogy or voice (that's lesson-generator's job)
- Retrofit existing notebooks (that's engagement-pass's job)

It **does**:
- Translate an outline into mechanically correct .ipynb JSON
- Ensure all engagement elements from the outline are present
- Produce notebooks that run top-to-bottom without import errors
- Handle cell metadata, IDs, and formatting correctly

---

## Trigger Detection

- "Generate the notebook from this outline"
- "Build the 0.3 notebook"
- "Turn the outline into a notebook"
- When a `module-N.M-outline.md` file exists and is marked "ready-to-generate"

---

## The Generation Script Pattern

### Why a Python Script?

Notebook JSON is finicky. Cell sources must be lists of strings with `\n` terminators. Metadata structures are rigid. Writing JSON by hand is error-prone. Instead:

1. Write a Python script that builds cells as dictionaries
2. Assemble them into a notebook structure
3. Dump to JSON
4. Delete the script

### Script Template

```python
#!/usr/bin/env python3
"""Generate Module N.M: [Title] notebook."""
import json

def md(source, cell_id=None):
    """Create a markdown cell."""
    cell = {
        "cell_type": "markdown",
        "metadata": {},
        "source": source.split("\n") if isinstance(source, str) else source
    }
    if cell_id:
        cell["id"] = cell_id
    lines = cell["source"]
    cell["source"] = [l + "\n" if i < len(lines) - 1 else l
                      for i, l in enumerate(lines)]
    return cell

def code(source, cell_id=None):
    """Create a code cell."""
    cell = {
        "cell_type": "code",
        "metadata": {},
        "source": source.split("\n") if isinstance(source, str) else source,
        "outputs": [],
        "execution_count": None
    }
    if cell_id:
        cell["id"] = cell_id
    lines = cell["source"]
    cell["source"] = [l + "\n" if i < len(lines) - 1 else l
                      for i, l in enumerate(lines)]
    return cell

cells = []

# --- BUILD CELLS HERE ---
# cells.append(md("""...""", "cell-id"))
# cells.append(code("""...""", "cell-id"))

notebook = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3 (ipykernel)",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.12.0"
        }
    },
    "cells": cells
}

output_path = "path/to/notebook.ipynb"
with open(output_path, 'w') as f:
    json.dump(notebook, f, indent=1)
print(f"Generated {len(cells)} cells: {output_path}")
```

---

## Cell Formatting Rules

### Source Lines

Cell source is a **list of strings**, each ending with `\n` except the last:

```python
# CORRECT
["line 1\n", "line 2\n", "line 3"]

# WRONG
["line 1", "line 2", "line 3"]      # Missing \n
"line 1\nline 2\nline 3"            # String, not list
["line 1\n", "line 2\n", "line 3\n"] # Last line has \n
```

The `md()` and `code()` helpers handle this automatically.

### Cell IDs

- **Engagement cells**: prefix with `engagement-` (e.g., `engagement-concept-map`, `engagement-video-beta`)
- **Content cells**: prefix with `cell-` (e.g., `cell-story-a`, `cell-pdf-formula`)
- IDs must be unique within the notebook
- IDs make it easy to reference cells in documentation and retrofit passes

### Markdown in Code Cells

Use triple-quoted strings with escaped inner quotes:

```python
cells.append(code('''def my_func():
    \"\"\"Docstring here.\"\"\"
    return 42''', "cell-my-func"))
```

Or use `\"\"\"` escaping inside the triple quotes.

---

## Standard Cell Sequence

Every Core notebook follows this order:

```
1. Metadata (markdown)         — Title, arc, prerequisites, time, objectives
2. Imports (code)              — All imports, helper functions from prior modules
3. Concept Map (code)          — arc_progress_map() — engagement-concept-map
4. Intro / Opening (markdown)  — War story or scenario
5-N. Content sections          — Alternating markdown + code, per outline
    Each section includes:
    - Section header (markdown)
    - Narrative (markdown)
    - Code demos (code)
    - Interactive elements (code) — Plotly, widgets, animations
    - Video embeds (code) — where specified in outline
    - Companion text callouts (markdown)
M. Exercises (markdown + code) — YOUR CODE / SOLUTION / TEST pattern
M+1. Outro (markdown)          — Summary, publication note, next module link
M+2. Resources (markdown)      — Books, videos, papers
```

---

## Engagement Element Templates

### Concept Map (Cell 3 — Required)

```python
cells.append(code("""# Arc 0 Progress Map — Where are we?
import networkx as nx

ARC_0_MODULES = [
    "Taste Demo", "Probability & Counting", "Distributions & Beta Priors",
    "Bayesian Updating", "Hypothesis Testing", "Bootstrap CIs",
    "Thompson Sampling", "Ship It"
]

def arc_progress_map(arc_number, total_modules, current_module, module_titles):
    # ... [full function from interactive-templates.md]
    pass

arc_progress_map(0, 8, CURRENT_MODULE, ARC_0_MODULES)""", "engagement-concept-map"))
```

### Video Embed

```python
cells.append(code("""embed_video(
    "VIDEO_ID",
    "Title — Creator",
    "1-2 sentence context explaining why this video is relevant here."
)""", "engagement-video-TOPIC"))
```

### Widget

```python
cells.append(code("""# Widget description
slider = FloatSlider(value=X, min=Y, max=Z, ...)
out = widgets.Output()

def update(change):
    with out:
        from IPython.display import clear_output
        clear_output(wait=True)
        # ... compute and plot ...

slider.observe(update, names='value')
display(widgets.VBox([slider, out]))
update(None)  # Initial render""", "engagement-widget-NAME"))
```

### FuncAnimation

```python
cells.append(code("""# Animation: [description]
fig_anim, ax_anim = plt.subplots(figsize=(10, 5))
# ... setup ...

def update(frame):
    # ... update plot ...
    return line, title

anim = FuncAnimation(fig_anim, update, frames=N, interval=200, blit=False)
plt.close(fig_anim)
HTML(anim.to_jshtml())""", "engagement-anim-NAME"))
```

---

## Exercise Cell Pattern

Three separate cells per exercise:

```python
# 1. Problem description (markdown)
cells.append(md("""## Exercise N: Title
Description...
- Step 1
- Step 2""", "cell-exN"))

# 2. Student code (code)
cells.append(code("""# --- YOUR CODE BELOW ---
def solve():
    # TODO: Implement
    pass""", "cell-exN-code"))

# 3. Solution (code)
cells.append(code("""# --- SOLUTION ---
def solve():
    return 42

# Test
assert solve() == 42
print("Tests pass.")""", "cell-exN-solution"))
```

### Build-a-Toy Exercise

Same pattern but the solution includes widgets:

```python
cells.append(md("""## Exercise N [BUILD-A-TOY]: Title
**Scenario**: ...
**Components given**: ...
**Your task**: ...
**Success criteria**: ...
**Extensions**: ...""", "cell-exN-build-a-toy"))
```

---

## Post-Generation Checklist

After running the script:

- [ ] Valid JSON (Python can parse it)
- [ ] Cell count matches outline expectation
- [ ] All engagement elements present:
  - [ ] 1 concept map (cell 3)
  - [ ] N videos (from outline)
  - [ ] N Plotly plots (from outline)
  - [ ] N widgets (from outline)
  - [ ] N animations (from outline)
  - [ ] 1+ build-a-toy exercise
- [ ] All cells have unique IDs
- [ ] Engagement cells prefixed with `engagement-`
- [ ] Imports cell includes all needed packages
- [ ] No orphaned references (every function/variable used is defined earlier)
- [ ] `embed_video()` helper defined in imports or inline
- [ ] Exercise cells follow YOUR CODE / SOLUTION / TEST pattern
- [ ] Outro links to next module
- [ ] Generator script deleted after successful generation

---

## Verification Command

```python
python -c "
import json
with open('path/to/notebook.ipynb') as f:
    nb = json.load(f)
print(f'Cells: {len(nb[\"cells\"])}')
md = sum(1 for c in nb['cells'] if c['cell_type'] == 'markdown')
code = sum(1 for c in nb['cells'] if c['cell_type'] == 'code')
print(f'Markdown: {md}, Code: {code}')
ids = [c.get('id') for c in nb['cells'] if c.get('id')]
engagement = [i for i in ids if i.startswith('engagement-')]
print(f'Engagement elements: {len(engagement)}')
for e in engagement:
    print(f'  {e}')
"
```

---

## Common Pitfalls

1. **Forgetting `\n` on source lines**: The `md()` and `code()` helpers handle this. Don't manually build source lists.

2. **Quotes inside triple-quoted strings**: Use `\"\"\"` to escape docstrings inside code cells, or use `'''` as the outer quote.

3. **Index shifts when inserting cells**: When retrofitting (not generating fresh), track index offsets from prior insertions. The notebook-builder skill generates fresh, so this doesn't apply.

4. **Large notebooks timing out**: For 50+ cell notebooks, the generation script runs fast (< 1s). The notebook *execution* is what's slow — that's a separate concern.

5. **Missing `from IPython.display import clear_output`**: Widget update functions often need this. Include it inside the function, not at top level, to avoid import-before-use issues in cell ordering.
