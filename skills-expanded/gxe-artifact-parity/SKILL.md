---
name: gxe-artifact-parity
description: Compare gx-engine and SDK generated artifact trees, investigate missing or extra output, or validate an artifact-parity claim. Read-only comparison of explicit offline roots; not a runtime or full-SDK parity test.
---

# Generated artifact parity

1. Resolve the repository root (`../../..` from this skill directory). Read
   `src/gx-engine/scripts/artifact_diff.py --help` with Python from that root.
   Confirm the comparator and both explicit input directories exist.
2. Establish provenance: record source snapshot, object closure, SDK/generator,
   generation options and generation outcome for each tree. Use disposable
   `C:/KBs/*teste*` offline outputs or synthetic fixtures. Stale/unequal workloads
   may be inspected, but cannot certify parity. This skill does not generate
   output, open a KB or authorize an SDK call.
3. Run `python src/gx-engine/scripts/artifact_diff.py --engine <engine-out>
   --sdk <sdk-out> --out <report-outside-both-trees>` from the repository root.
   Keep reports outside Git. Compare all extensions for an inventory claim;
   an explicit extension filter limits the claim to that selection.
4. Read the JSON inventory and process exit status together. Exit 0 means a
   nonempty selected file set matched by size and SHA-256; 1 means differences;
   2 means invalid input or incomplete comparison. Account for engine-only,
   SDK-only and excluded files. Directory-only differences, runnable behavior,
   SDK metadata and generated applications are separate validation gates.
5. Report provenance, selected denominator, exclusions, differences and a
   verified/not-verified/blocked conclusion for this exact artifact comparison.
   Matching artifacts alone never establishes full SDK replacement or speed.

For comparator changes, run `python -m unittest discover -s
src/gx-engine/scripts -p test_artifact_diff.py`; mutations must detect unequal
content and writes through an output alias before restoring passing tests.
