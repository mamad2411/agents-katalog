---
name: dev-docstring
description: Use when adding or updating docstrings, file headers, or inline documentation in `.c/.h` (Basilisk literate-c) or `.py` files destined for the pandoc + `generate_docs.py` docs site.
---

# Literate Programming Documentation Style

Write documentation that renders beautifully as web pages while remaining readable in source code. This style is used with Basilisk's `literate-c` tool and this repo's docs generator (`.github/scripts/generate_docs.py`).

## Basilisk Tooling Hygiene

- qcc-lsp may generate a `.comphy-basilisk` file when a local `basilisk/` folder exists in the workspace.
- Add `.comphy-basilisk` to `.gitignore`; it is generated and should not be committed.

## Basilisk Source Grounding

Before documenting or changing any Basilisk source, API, or numerics behaviour,
Skip Basilisk-specific steps when that skill is unavailable. Use a local Basilisk source index if available in
the mandatory order `symbol` (known identifier) → `search --scope source`
(behaviour) → `read` (surrounding implementation). Archiver may supply the user's
notes and project context, but it is not evidence for Basilisk implementation
claims.

## Core Principle

Documentation blocks are **Markdown** embedded in comments/docstrings. They become prose on web pages while code stays as syntax-highlighted blocks.

## File Type Reference

### C/H Files: Use `/** */` Blocks

Documentation uses double-asterisk opening. Single-asterisk is for inline comments.

**File Header Pattern:**
```c
/**
# File Title

Brief description of what this file does and its purpose in the project.

## Author
Name
Email: email@domain.org
Lab/Organization
Last updated: Mon DD, YYYY
*/
```

**Section Documentation:**
```c
/**
## Section Name

Explanation of what this section does. Use Markdown formatting:
- Bullet points for lists
- `backticks` for code references
- $LaTeX$ for math expressions
*/
```

**Function Documentation:**
```c
/**
### function_name()

Brief description of what the function does.

#### Parameters
- `param1`: Description of first parameter
- `param2`: Description of second parameter

#### Returns
Description of return value or behavior.

#### Example
```c
result = function_name(arg1, arg2);
```
*/
int function_name(int param1, double param2) {
```

**Inline Explanations:**
```c
/**
For the boundary conditions, we set: */
u.t[top] = dirichlet(1.0);  // Lid velocity
u.t[bottom] = dirichlet(0); // No-slip
```

### Python Files: Use Triple-Quote Docstrings (Markdown)

`generate_docs.py` extracts **standalone string-literal statements** (module/class/function docstrings and standalone `""" ... """` blocks) as Markdown prose. Everything else is wrapped into fenced Python code blocks.

Implications:
- You *can* use standalone `""" ... """` blocks between code sections as “Markdown comment blocks”.
- A multiline string literal only shows up in docs if it is a standalone statement. If you need a multiline runtime string, **assign it to a variable** so it is not extracted.

#### Pandoc Formatting Rules (Critical)

The docs site uses `pandoc` to convert Markdown → HTML. To guarantee correct rendering:
- Use Markdown headings like `#### Args`, `#### Returns`, `#### Raises`, `#### Example` (recommended).
- If you prefer `Args:`/`Returns:` lines, add a **blank line** before starting a list. Otherwise Pandoc will collapse list items into a single paragraph.
- Always put a blank line between paragraphs and lists.

#### Critical: Module Docstring Must Come First

**The module docstring MUST be the first statement** in your Python file (after any shebang/encoding). This is not just style—`generate_docs.py` uses AST extraction that processes docstrings in line order.

**Why this matters:**
The generator walks through your file and emits everything between docstrings as code blocks. If imports come before the module docstring, they appear as code BEFORE your module description.

**Anti-pattern (breaks documentation flow):**
```python
import numpy as np          # ← This becomes a code block
import matplotlib.pyplot as plt

"""
# My Module
Description here.           # ← This appears AFTER the imports!
"""
```

**Correct pattern:**
```python
"""
# My Module
Description appears first, as intended.
"""

import numpy as np
import matplotlib.pyplot as plt
```

**Module Header (top of file):**
```python
"""
# Module Title

Description of the module's purpose and functionality.

## Dependencies
- numpy: Array operations
- matplotlib: Plotting

## Author
Name (email@domain.org)
"""
```

**Section Block (standalone “Markdown comment” between code):**
```python
"""
## Matplotlib Configuration

Configure matplotlib with LaTeX rendering if available, with serif font fallback.
"""
```

**Function Docstring (recommended):**
```python
def function_name(param1, param2):
    """
    Brief description of function purpose.

    Detailed explanation if needed, describing the algorithm
    or approach used.

    #### Args
    - `param1`: Description of first parameter.
    - `param2`: Description of second parameter.

    #### Returns
    - `float`: Description of return value.

    #### Example
    ```python
    result = function_name(1, 2)
    print(result)
    ```
    """
```

**Class Docstring:**
```python
class ClassName:
    """
    Brief class description.

    #### Attributes
    - `attr1`: Description.
    - `attr2`: Description.

    #### Methods
    - `method1()`: What it does.
    - `method2()`: What it does.
    """
```

## Markdown Formatting Rules

### Headings Hierarchy
- `#` — File/module title (one per file; typically module docstring only)
- `##` — Major sections (Dependencies, Physical Setup, Algorithm)
- `###` — Subsections
- `####` — API blocks (Args/Returns/Raises/Example) and parameter lists

### Code References
Always use backticks for:
- Variable names: `velocity`, `pressure`
- Function names: `calculate_velocity()`
- File names: `simulation.c`
- Parameters: `tmax`, `LEVEL`

### Mathematical Expressions
Use LaTeX within `$...$` (MathJax is enabled in the docs site):
- Inline: `$Re = \\frac{\\rho U L}{\\mu}$`
- Display:
  `$$\\nabla \\cdot \\mathbf{u} = 0$$`

### Lists
```markdown
## Parameters
- `We`: Weber number, $We = \\frac{\\rho U^2 L}{\\sigma}$
- `Oh`: Ohnesorge number
- `LEVEL`: Grid refinement level (default: 9)

## Algorithm Steps
1. Initialize velocity field
2. Solve pressure Poisson equation
3. Update velocity with pressure gradient
4. Repeat until convergence
```

### Links to Other Files
Reference other documented files:
```c
/**
See [velocity.h](velocity.h) for the velocity solver implementation.
*/
```


## Gotchas

1. **Module docstring not first -> docs break** -- in Python, any import before the triple-quote docstring becomes an orphaned code block that renders before your module description. Move the module docstring to line 1.
2. **No blank line before list -> Pandoc collapses items** -- Pandoc renders `Args:\n- item` as a single paragraph, not a list. Always insert a blank line between a label and its bullet list.
3. **Asterisks inside `/** */` break Markdown** -- `/** * This line */` renders the leading `*` as literal text, not Markdown. Use clean Markdown with no per-line asterisks.
4. **Assigned string literals are invisible to the extractor** -- `docs = '...'` is NOT a standalone statement and will NOT be extracted by `generate_docs.py`. Only true standalone string-literal statements (function/class/module docstrings or bare string expressions) are extracted.

## What NOT to Do

1. **Don't use `*` on every line** inside documentation blocks:
   ```c
   /* BAD - asterisks on each line */
   /**
    * This style breaks
    * the Markdown rendering
    */

   /* GOOD - clean Markdown */
   /**
   This renders correctly
   as prose documentation.
   */
   ```

2. **Don't mix documentation styles**:
   ```c
   /* BAD - mixing // with /** */
   // # Title  <-- won't be extracted

   /* GOOD */
   /**
   # Title
   */
   ```

3. **Don't forget backticks for code**:
   ```c
   /* BAD */
   The velocity variable stores...

   /* GOOD */
   The `velocity` variable stores...
   ```

4. **Don't put imports before the module docstring** (Python):
   ```python
   # BAD - imports before docstring
   import sys
   """Module docstring appears after imports in docs!"""

   # GOOD - docstring first
   """Module docstring appears first."""
   import sys
   ```

5. **Don't forget blank lines before lists** (Python/Pandoc):
   ```python
   # BAD - Pandoc collapses this into one paragraph
   """
   Args:
   - param1: First parameter
   - param2: Second parameter
   """

   # GOOD - blank line before list
   """
   Args:

   - param1: First parameter
   - param2: Second parameter
   """
   ```

## Complete Example: C File

```c
/**
# Lid-Driven Cavity Flow

Simulation of incompressible Newtonian fluid in a square cavity
with a moving lid.

## Physical Setup
- Square domain: $[0,1] \\times [0,1]$
- Top lid moves at $U = 1$
- Reynolds number: $Re = \\frac{UL}{\\nu} = 100$

## Author
${AUTHOR_NAME:-Your Name}
${AUTHOR_EMAIL:-you@example.com}
*/

#include "navier-stokes/centered.h"

/**
## Parameters
*/
#define LEVEL 8
double Re = 100.;

/**
## Boundary Conditions

No-slip on all walls except top (moving lid):
*/
u.t[top] = dirichlet(1.);
u.t[bottom] = dirichlet(0.);
u.t[left] = dirichlet(0.);
u.t[right] = dirichlet(0.);

/**
## Initialization
*/
event init(t = 0) {
  /**
  Start from rest with uniform pressure. */
  foreach() {
    u.x[] = 0.;
    u.y[] = 0.;
  }
}

/**
### log_progress()

Logs simulation time and maximum velocity for monitoring convergence.
*/
event log_progress(i += 100) {
  fprintf(stderr, "t = %g, max(u) = %g\\n", t, normf(u.x).max);
}
```

## Complete Example: Python File

```python
#!/usr/bin/env python3
"""
# Post-Processing for Cavity Flow

Extract and visualize velocity fields from simulation snapshots.

## Dependencies

- numpy: Array manipulation
- matplotlib: Visualization

## Author

${AUTHOR_NAME:-Your Name} (${AUTHOR_EMAIL:-you@example.com})
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

"""
## Configuration

Set up matplotlib with publication-quality defaults.
"""

plt.rcParams.update({'font.size': 12, 'figure.dpi': 150})

"""
## Data Extraction
"""

def extract_field(filename, grid_size):
    """
    Extract velocity field from simulation snapshot.

    Reads binary data and reshapes into a 2D grid for visualization.

    #### Args

    - `filename`: Path to snapshot file.
    - `grid_size`: Number of grid points per dimension.

    #### Returns

    - `tuple[np.ndarray, ...]`: `(X, Y, U, V)` coordinate and velocity arrays.

    #### Raises

    - `FileNotFoundError`: If snapshot file doesn't exist.
    - `ValueError`: If grid_size doesn't match data dimensions.

    #### Example

    ```python
    X, Y, U, V = extract_field("snapshot-0.1", 256)
    plt.quiver(X, Y, U, V)
    ```
    """
    path = Path(filename)
    if not path.exists():
        raise FileNotFoundError(f"Snapshot not found: {filename}")

    data = np.fromfile(path, dtype=np.float64)
    # ... implementation ...
    return X, Y, U, V


class VelocityField:
    """
    Container for velocity field data with visualization methods.

    #### Attributes

    - `X`, `Y`: Coordinate meshgrids.
    - `U`, `V`: Velocity components.
    - `magnitude`: Speed at each point.

    #### Methods

    - `plot_streamlines()`: Generate streamline plot.
    - `plot_contour()`: Generate contour plot of speed.
    """

    def __init__(self, X, Y, U, V):
        """Initialize with coordinate and velocity arrays."""
        self.X, self.Y = X, Y
        self.U, self.V = U, V
        self.magnitude = np.sqrt(U**2 + V**2)
```

## Reference Templates

For copy-paste starting points, see the `references/` folder in this skill directory:

| Template | Use Case |
|----------|----------|
| `template_utility.c` | Data extraction, post-processing utilities |
| `template_simulation.c` | Physics simulations with Basilisk |
| `template_module.py` | Python modules and scripts |
| `template_header.h` | C/C++ header files |

Each template demonstrates all patterns from this guide in a minimal, working example. See `references/README.md` for detailed usage instructions.
