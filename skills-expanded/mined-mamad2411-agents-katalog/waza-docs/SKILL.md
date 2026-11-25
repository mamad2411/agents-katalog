---
description: 'Reference and links to the official Microsoft/waza documentation. You MUST load this skill when you need detailed guides, best practices, or reference documentation for the Waza tool.'
license: MIT
name: waza-docs
---
# Waza Docs

<!-- markdownlint-disable MD013 MD024 MD033 -->

## WHEN TO USE

- When configuring or troubleshooting Waza implementations.
- When creating SKILL assessments and evaluating agents using Waza.
- When you need reference material such as Graders, CI/CD integration, or telemetry documentation.

## References

To fully utilize this skill, you MUST read at least one of the links relevant to the current context:

- [CI/CD Integration Guide](https://raw.githubusercontent.com/microsoft/waza/refs/tags/v0.33.0/docs/CI-CD-GUIDE.md)
  This guide explains how to integrate waza evaluations into your CI/CD pipelines using GitHub Actions, Azure DevOps, and other platforms.

- [Waza Demo Guide](https://raw.githubusercontent.com/microsoft/waza/refs/tags/v0.33.0/docs/DEMO-GUIDE.md)
  Comprehensive walk-through for demonstrating waza's capabilities. Provides step-by-step instructions for 9 practical demonstrations.

- [Getting Started with Waza](https://raw.githubusercontent.com/microsoft/waza/refs/tags/v0.33.0/docs/GETTING-STARTED.md)
  A complete walkthrough for creating, testing, and validating AI agent skills.

- [Waza User Guide](https://raw.githubusercontent.com/microsoft/waza/refs/tags/v0.33.0/docs/GUIDE.md)
  A CLI tool for evaluating AI agent skills, including installation, creating evaluations, running benchmarks, and reviewing results.

- [Integration Testing with Copilot SDK](https://raw.githubusercontent.com/microsoft/waza/refs/tags/v0.33.0/docs/INTEGRATION-TESTING.md)
  This guide explains how to run real integration tests using the GitHub Copilot SDK.

- [Waza Skills Development Platform - PRD](https://raw.githubusercontent.com/microsoft/waza/refs/tags/v0.33.0/docs/PRD.md)
  Product Requirements Document for the Waza Skills Development Platform.

- [Release Process](https://raw.githubusercontent.com/microsoft/waza/refs/tags/v0.33.0/docs/RELEASE.md)
  This document describes how the Waza release process works.

- [Skill Development Best Practices](https://raw.githubusercontent.com/microsoft/waza/refs/tags/v0.33.0/docs/SKILL-BEST-PRACTICES.md)
  Guidance for creating high-quality SKILL.md files that integrate well with waza evaluations and follow industry best practices.

- [Waza Integration for microsoft/skills](https://raw.githubusercontent.com/microsoft/waza/refs/tags/v0.33.0/docs/SKILLS_CI_INTEGRATION.md)
  This guide explains how to use waza for evaluating skills in the microsoft/skills repository.

- [Runtime Telemetry](https://raw.githubusercontent.com/microsoft/waza/refs/tags/v0.33.0/docs/TELEMETRY.md)
  Capture and analyze metrics from skills running in production.

- [Token Limits Configuration](https://raw.githubusercontent.com/microsoft/waza/refs/tags/v0.33.0/docs/TOKEN-LIMITS.md)
  Reference for resolving token limits in configuration, such as `.waza.yaml`.

- [Waza Project Configuration Schema](https://raw.githubusercontent.com/microsoft/waza/refs/tags/v0.33.0/schemas/config.schema.json)
  JSON Schema for validating `.waza.yaml` project configuration files.

- [Advisory Checks](https://github.com/microsoft/waza/blob/v0.33.0/internal/checks/advisory_checks.go)
  Logic for advisory Waza checks and compliance patterns for `SKILL.md` files.

- [Writing Skill Evals - Tutorial](https://raw.githubusercontent.com/microsoft/waza/refs/tags/v0.33.0/docs/TUTORIAL.md)
  This tutorial walks you through creating evaluations for your Agent Skills.

### Design

- [A/B Baseline Skill Impact Measurement](https://raw.githubusercontent.com/microsoft/waza/refs/tags/v0.33.0/docs/design/194-baseline-skill-impact.md)
  Design document for A/B Skill Impact Measurement.

### Grader Reference

Complete reference for all available grader types in waza.

- [Grader Reference Overview](https://raw.githubusercontent.com/microsoft/waza/refs/tags/v0.33.0/docs/graders/README.md)
  Complete reference for all available grader types in waza.

- [`action_sequence`](https://raw.githubusercontent.com/microsoft/waza/refs/tags/v0.33.0/docs/graders/action_sequence.md)
  Tool Call Sequence Validation. Validates that the agent's tool calls match an expected action sequence.

- [`behavior`](https://raw.githubusercontent.com/microsoft/waza/refs/tags/v0.33.0/docs/graders/behavior.md)
  Agent Behavior Validation. Validates agent behavior patterns like tool call counts, token usage, and execution duration.

- [`code`](https://raw.githubusercontent.com/microsoft/waza/refs/tags/v0.33.0/docs/graders/code.md)
  Assertion-Based Grader. Evaluates expressions against the execution context using an inline script runner.

- [`diff`](https://raw.githubusercontent.com/microsoft/waza/refs/tags/v0.33.0/docs/graders/diff.md)
  Workspace File Comparison. Compares post-execution workspace files against expected snapshots and/or line fragments.

- [`file`](https://raw.githubusercontent.com/microsoft/waza/refs/tags/v0.33.0/docs/graders/file.md)
  File Existence & Content Grader. Validates file existence, absence, and content patterns in the post-execution workspace.

- [`human_calibration`](https://raw.githubusercontent.com/microsoft/waza/refs/tags/v0.33.0/docs/graders/human_calibration.md)
  Calibration Grader. Collects human labels to calibrate LLM graders.

- [`human`](https://raw.githubusercontent.com/microsoft/waza/refs/tags/v0.33.0/docs/graders/human.md)
  Manual Review Grader. Marks tasks for human review.

- [`json_schema`](https://raw.githubusercontent.com/microsoft/waza/refs/tags/v0.33.0/docs/graders/json_schema.md)
  JSON Schema Validation Grader. Validates that the agent output is valid JSON conforming to a given JSON schema.

- [`llm_comparison`](https://raw.githubusercontent.com/microsoft/waza/refs/tags/v0.33.0/docs/graders/llm_comparison.md)
  Reference Comparison Grader. Compares output against a reference using LLM.

- [`llm`](https://raw.githubusercontent.com/microsoft/waza/refs/tags/v0.33.0/docs/graders/llm.md)
  LLM-as-Judge Grader. Uses an AI model to evaluate quality.

- [`program`](https://raw.githubusercontent.com/microsoft/waza/refs/tags/v0.33.0/docs/graders/program.md)
  External Program Grader. Runs an external program or script to grade agent output.

- [`prompt`](https://raw.githubusercontent.com/microsoft/waza/refs/tags/v0.33.0/docs/graders/prompt.md)
  LLM-Based Evaluation. Uses a language model to evaluate skill execution quality via an explicit grader prompt.

- [`script`](https://raw.githubusercontent.com/microsoft/waza/refs/tags/v0.33.0/docs/graders/script.md)
  External Script Grader. Runs a custom Python script for complex validation.

- [`skill_invocation`](https://raw.githubusercontent.com/microsoft/waza/refs/tags/v0.33.0/docs/graders/skill_invocation.md)
  Skill Invocation Sequence Validation. Validates that dependent skills were invoked in the correct sequence during orchestration.

- [`text`](https://raw.githubusercontent.com/microsoft/waza/refs/tags/v0.33.0/docs/graders/text.md)
  Text Matching Grader. Validates output using substring matching and regex patterns.

- [`tool_calls`](https://raw.githubusercontent.com/microsoft/waza/refs/tags/v0.33.0/docs/graders/tool_calls.md)
  Tool Usage Grader. Validates which tools were called and how.

- [`tool_constraint`](https://raw.githubusercontent.com/microsoft/waza/refs/tags/v0.33.0/docs/graders/tool_constraint.md)
  Tool Usage Constraint Grader. Validates which tools an agent used (or avoided).

- [`trigger`](https://raw.githubusercontent.com/microsoft/waza/refs/tags/v0.33.0/docs/graders/trigger.md)
  Heuristic grader for validating whether a prompt should activate a skill.

### Plans

- [MCP Server Design Document](https://raw.githubusercontent.com/microsoft/waza/refs/tags/v0.33.0/docs/plans/2026-02-21-mcp-server-design.md)
  Design document for the MCP Server implementation.
