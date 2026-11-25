---
name: engagement-pass
description: Retrofit existing notebooks with interactive engagement elements — Plotly plots, video embeds, ipywidgets, animations, concept maps, and "build a toy" exercises. Triggers on "add engagement to", "make interactive", "retrofit", "engagement pass on", or when upgrading static notebooks with interactive elements.
---

# Engagement Pass

A retrofit skill that analyzes existing Jupyter notebooks and adds interactive engagement elements without changing the narrative flow or learning sequence.

**When to use**: On notebooks that are already written and working but are purely static (matplotlib only, no widgets, no videos, no interactive plots).

**When NOT to use**: During initial notebook generation — the `lesson-generator` skill now includes engagement patterns (sections 13-18) and should generate with them from the start.

---

## Trigger Detection

Activate on:
- "Add engagement to [notebook]"
- "Make [notebook] interactive"
- "Retrofit [notebook]"
- "Engagement pass on [notebook]"
- "Add interactive elements to [notebook]"
- "This notebook needs more dopamine"

---

## Process

### Step 1: Analyze

Read the target notebook and identify enhancement opportunities:

**Scan for**:
| What to Find | Enhancement Type | Priority |
|-------------|-----------------|----------|
| Static matplotlib scatter plots with meaningful per-point data | Plotly conversion | High |
| 3D matplotlib surface plots | Plotly 3D conversion | High |
| Missing concept map after imports | Arc progress map | High |
| Concept introductions (interludes, theory sections) | Video embed opportunity | High |
| Parameter explorations ("try changing X") | Widget (ipywidgets) | Medium |
| Simulations or Monte Carlo sections | Button-triggered widget | Medium |
| Time-series / convergence / updating sections | FuncAnimation | Medium |
| Static bar charts comparing categories | Plotly bar with hover | Medium |
| Exercise sections without a "build" component | "Build a toy" candidate | High |
| Every single matplotlib plot | NOT a conversion candidate | N/A |

**Output**: A concrete enhancement list with cell numbers and descriptions.

### Step 2: Prioritize

Not everything should be converted. Apply the engagement budget:

**High priority** (do first):
1. Arc progress concept map (after imports) — every notebook needs one
2. 1-2 key Plotly conversions where hover/interaction genuinely helps
3. 1 strategic video embed at a concept introduction point

**Medium priority** (do if budget allows):
4. Widget for parameter exploration
5. Animation for a dynamic concept
6. Additional Plotly conversions

**Low priority** (skip unless specifically requested):
7. Converting every matplotlib plot to Plotly
8. Adding widgets to sections where the static version is clear enough
9. Multiple animations (expensive to render)

**Budget limits per notebook**:
- Max 1 concept map
- Max 3 video embeds
- Max 4 Plotly conversions
- Max 3 widgets
- Max 2 animations
- At least 1 "build a toy" exercise

### Step 3: Apply

Insert enhancements using templates from `lesson-generator/interactive-templates.md`.

**For each enhancement**:

#### Concept Map
1. Add engagement imports to the imports cell (Cell 2)
2. Insert `arc_progress_map()` call as a new cell after imports
3. Use `ARC_0_MODULES` list and set `current_module` appropriately

#### Video Embed
1. Identify the target section from `lesson-generator/video-index.md`
2. Create a new markdown cell with contextual intro (1-2 sentences)
3. Add code cell with `embed_video(video_id, title, context)`
4. Place AFTER the reader has worked through the concept, not before

#### Plotly Conversion
1. Read the existing matplotlib cell
2. Determine what hover data would be useful
3. Replace with equivalent Plotly code using templates
4. Keep the same color palette and visual style
5. Remove the old matplotlib cell (don't leave both)

#### Widget Addition
1. Identify the parameter(s) the reader should explore
2. Choose widget type: `@interact` for simple sweeps, button for stochastic processes
3. Add the widget cell after the static version
4. Include a "What to notice" comment guiding exploration

#### Animation
1. Show the static/final result first (existing cell)
2. Add animation cell after with `FuncAnimation` → `HTML(anim.to_jshtml())`
3. Include frame counter and running metrics in the animation

#### "Build a Toy" Exercise
1. Place in the Exercises section
2. Provide scenario, components, task, success criteria, extensions
3. Include starter code and a working solution in a separate cell
4. The toy must be interactive (widgets + plotly/matplotlib)

### Step 4: Validate

After applying enhancements:

- [ ] All cells run sequentially without error
- [ ] Story flow is unchanged — enhancements clarify, don't distract
- [ ] No widget overload (check budget limits)
- [ ] Imports cell includes all needed engagement imports
- [ ] Videos reference correct IDs from video-index.md
- [ ] Plotly plots use consistent color palette and `plotly_white` template
- [ ] Concept map correctly identifies current module

---

## Quality Checklist

Run this checklist after every engagement pass:

- [ ] **Concept map** present after imports
- [ ] **1-3 strategic video embeds** at concept introductions (not more)
- [ ] **Key plots converted to Plotly** (hover data is useful, not just pretty)
- [ ] **At least 1 widget** for parameter exploration
- [ ] **0-1 animations** for dynamic concepts
- [ ] **At least 1 "build a toy" exercise** in the exercises section
- [ ] **Story flow preserved** — if you removed the enhancements, the notebook still makes sense
- [ ] **All cells run sequentially** without error
- [ ] **No engagement bloat** — every interactive element has a reason to be interactive

---

## Reference Files

| File | Location | Purpose |
|------|----------|---------|
| `engagement-patterns.md` | `.claude/skills/lesson-generator/` | When/how to use each pattern type |
| `interactive-templates.md` | `.claude/skills/lesson-generator/` | Copy-paste code templates |
| `video-index.md` | `.claude/skills/lesson-generator/` | YouTube video IDs per module/section |
| `SKILL.md` (lesson-generator) | `.claude/skills/lesson-generator/` | Sections 13-18 define generation-time patterns |

---

## What This Skill Does NOT Do

- **Rewrite narrative**: The story, voice, and flow are sacred. Enhancements slot in alongside, never replace.
- **Restructure exercises**: Exercise order and structure remain unchanged. "Build a toy" is *added*, not substituted.
- **Add theory content**: No new concepts, formulas, or explanations. Only interactive wrappers around existing content.
- **Fix bugs**: If the notebook has code errors, fix those first before running an engagement pass.
- **Change the belt level**: A Core notebook stays Core. A Depth notebook stays Depth. Engagement elements don't change the target audience.

---

## Example: Before/After

### Before (static matplotlib scatter)
```python
fig, ax = plt.subplots(figsize=(10, 5))
ax.scatter(salience_scores, intuitive, c='#2196F3')
ax.set_xlabel('Salience Score')
ax.set_ylabel('Intuitive Rating')
ax.set_title('Scorer vs. Intuition')
plt.show()
```

### After (Plotly with hover context)
```python
plotly_scatter_with_context(
    x=salience_scores, y=intuitive_ratings,
    labels=[f"Entry {i}" for i in range(len(ENTRIES))],
    descriptions=[e.task[:60] for e in ENTRIES],
    title="SalienceScorer vs. Intuitive Ratings",
    xaxis_title="Salience Score", yaxis_title="Intuitive Rating"
)
```

The Plotly version lets the reader hover over each point and see which entry it is, what the task was, and both score values. The matplotlib version just shows dots.
