---
name: supply-chain-mapper
description: Map vendor dependencies and supply chain relationships so Claude can explain concentration risk, critical dependencies, and possible circular relationships clearly.
---

# Supply Chain Mapper

Use this skill when the user wants to understand vendor relationships, visualize third-party dependencies, or identify concentration and dependency risks in the supply chain.

## Goal

Help Claude turn vendor dependency data into a clear picture of supply chain structure, critical relationships, and the most important third-party risk signals.

## Workflow

1. Confirm the vendor inventory file and the preferred output style.
2. Review the listed vendors, dependency relationships, criticality, data access, and tiering details.
3. Identify notable structural risks such as critical dependencies, concentration, or circular relationships.
4. Summarize the supply chain in a way that makes the dependency model easy to understand.
5. Present the result as a concise narrative, diagram-ready view, or both.

## Inputs

Expected inputs from the bundled tool metadata:
- vendors: Path to the vendor dependency CSV.
- output: Optional output format such as mermaid, markdown, or both.

## Bundled Files

- main.py contains the executable mapping logic.
- README.md provides examples and usage notes.
- skill.yaml captures the repo-native metadata for this skill.
- sample_input may contain representative vendor dependency data.

## Guidance

Prioritize structural understanding. Make it easy to see which vendors are critical, where dependency chains are concentrated, and which relationships may need deeper review.
