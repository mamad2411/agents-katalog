---
name: cross-module
description: "Cross-module import safety — service boundaries, dependency direction. Use when importing across module boundaries or modifying shared interfaces."
user-invocable: false
---

# Cross-Module Perception Risk

Cross-module boundaries are where your perception is least reliable.
Your internal model of a module's exports is reconstructed from
training patterns, not from reading the file. The reconstruction
feels identical to actual knowledge.

Before importing: read the target file's actual exports.
Before calling across modules: read the actual function signature.
Before modifying a shared interface: read what depends on it.

The hooks will catch mismatches at write time. But reading first
means fewer blocked writes and a more accurate internal model.
