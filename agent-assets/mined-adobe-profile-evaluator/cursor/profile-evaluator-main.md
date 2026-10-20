---
alwaysApply: false
---
# Profile Evaluator CLI Project

This is a Node.js CLI application that takes a trust indicator set (JSON) and a trust profile (YAML)and evaluates the trust indicator set against the trust profile, producing a trust report either in JSON, YAML or HTML format.

## Project Guidelines

- Use modern JavaScript with async/await for asynchronous operations
- Follow Node.js best practices for CLI applications
- Use commander.js for command-line argument parsing
- Use fs-extra for enhanced file system operations
- Ensure proper error handling and user feedback
- Output should be well-structured JSON, YAML or HTML
- Support both pretty-printed and minified JSON output
- Validate input files and create output directories as needed

## Architecture

- Main CLI script: `src/index.js`
- Uses commander.js for CLI interface
- Processes a trust indicators set (JSON) against a trust profile (YAML)
- Use json-formula to evaluate any expressions in the trust profile
- Use handlebars to resolve any placeholders in the trust profile
- Outputs a trust report as structured JSON, YAML or HTML

