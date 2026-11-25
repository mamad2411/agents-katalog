---
name: devsecops-checker
description: Review CI or CD pipeline configuration for DevSecOps controls and help Claude explain maturity gaps, missing safeguards, and practical improvements.
---

# DevSecOps Checker

Use this skill when the user wants to assess a CI or CD pipeline for security controls, maturity, and coverage across the software delivery lifecycle.

## Goal

Help Claude evaluate pipeline configuration, identify missing DevSecOps safeguards, and explain what improvements would materially strengthen delivery security.

## Workflow

1. Review the pipeline or workflow configuration the user wants assessed.
2. Identify which security controls are present, such as scanning, signing, secret handling, approvals, or artifact protections.
3. Note missing or weak controls that reduce confidence in the pipeline.
4. Summarize the overall maturity level and the most important gaps to address first.
5. Present recommendations in a practical order that engineering teams can act on.

## Inputs

Expected inputs from the bundled tool metadata:
- config: Path to the CI or CD pipeline configuration file.
- output: Optional output format.

## Bundled Files

- main.py contains the executable pipeline assessment logic.
- README.md provides usage guidance and examples.
- skill.yaml captures the repo-native metadata for this skill.
- sample_input may contain example pipeline files.

## Guidance

Focus on material delivery risks such as missing security tests, weak secret handling, lack of gating, or absent artifact protections. Keep recommendations concrete and prioritized.
