# Notebook Module

This directory owns the `notebook` capability pack — Jupyter notebook creation and cell editing.

- The `notebook` tool creates or extends `.ipynb` files with code and markdown cells.
- Supports `python3` and `javascript` kernels.
- Classified as `moderate` risk in guardrails.

## Boundaries

- Does not own code execution or REPL capabilities (those belong in `execution/`).
- Does not own general file read/write (those belong in `filesystem/`).
