---
name: data-inventory-mapper
description: Map personal and sensitive data across systems so Claude can explain data flows, classifications, transfers, and privacy-relevant handling risks clearly.
---

# Data Inventory Mapper

Use this skill when the user needs to map data assets, understand data movement across systems, or document where personal or special category data is stored and transferred.

## Goal

Help Claude turn inventory data into a clear picture of data flows, classifications, and privacy-relevant processing details that support audit or compliance work.

## Workflow

1. Confirm the inventory file and the output style the user wants.
2. Review the systems, data types, classifications, transfers, legal bases, and retention details in the inventory.
3. Identify important privacy signals such as special category data, unusual transfers, or unclear ownership.
4. Summarize the data landscape in a way that makes flows and processing relationships easy to understand.
5. Present the result as a concise narrative, diagram-ready view, or both.

## Inputs

Expected inputs from the bundled tool metadata:
- inventory: Path to the data inventory CSV file.
- output: Optional output format such as mermaid, markdown, or both.

## Bundled Files

- main.py contains the executable mapping logic.
- README.md provides examples and usage notes.
- skill.yaml captures the repo-native metadata for this skill.
- sample_input may contain representative inventory data.

## Guidance

Focus on clarity and traceability. Make it easy to see what data exists, where it moves, and which items are most privacy-sensitive.
