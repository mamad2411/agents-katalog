---
name: clean-notebook
description: "Cleans a Jupyter notebook: removes dead cells, fixes run order, moves reusable code into modules and checks it runs top to bottom."
disable-model-invocation: true
---

Clean up the notebook: $ARGUMENTS

1. Copy it to `<name>.backup.ipynb` before touching anything.
2. Read all cells with `jupyter nbconvert --to script` or by parsing the JSON. List cells that are empty, commented-out experiments, duplicated, or never referenced by later cells.
3. Find hidden state: variables used before they are defined in file order, cells that depend on a manual run order, and hard-coded absolute paths or credentials. Move paths to variables at the top.
4. Propose the cleanup list and ask for approval before deleting any cell.
5. Move functions used by more than one cell into `<name>_lib.py` beside the notebook with docstrings, and import them. Keep exploratory plotting in the notebook.
6. Order cells: imports, config, load, transform, analyze, plot. Add a short markdown heading before each section.
7. Clear outputs, then verify with `jupyter nbconvert --to notebook --execute --inplace` on a copy.

Report cells removed, code moved, and whether the notebook runs top to bottom.
