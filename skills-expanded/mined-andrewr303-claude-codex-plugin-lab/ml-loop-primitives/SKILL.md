---
name: ml-loop-primitives
description: Internal Fusion-ML primitive references for watchdog, ml-iteration, autoresearch, and experiment handoff workflows.
---

# ML Loop Primitives

This directory contains shared primitive reference files used by the Fusion-ML
workflow skills. Do not invoke it as a standalone workflow unless another
Fusion-ML skill explicitly routes here for a specific reference.

When a workflow skill links to a file in this directory, read that referenced
file completely and apply it as local guidance for the current workflow only.
