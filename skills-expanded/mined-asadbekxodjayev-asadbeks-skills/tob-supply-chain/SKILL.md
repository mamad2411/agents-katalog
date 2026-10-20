# Supply Chain Risk Auditor

## Purpose

This skill analyzes the supply-chain threat landscape by evaluating a project's direct dependencies. It examines factors including popularity, maintainer count, CVE history, and update frequency to identify high-risk components.

## Key Capabilities

The tool "enumerates all of the direct dependencies of a target project, then uses the `gh` command line tool to query a variety of information about each dependency" such as maintainer details, commit history, and security contacts.

## Important Limitation

The skill "does NOT scan source code for CVEs or credentials," so it focuses on external risk factors rather than internal code analysis.

## Use Cases

Deploy this skill when stakeholders need to understand supply-chain vulnerability exposure and want guidance on replacing risky dependencies with more secure alternatives.

## Installation

```
/plugin install trailofbits/skills/plugins/supply-chain-risk-auditor
```

**Author:** Spencer Michaels

## Source

Trail of Bits skills repository: https://github.com/trailofbits/skills
