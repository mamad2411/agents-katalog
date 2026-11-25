# elf

Static GitHub repo safety scanner meant to sit between an agent and “go use this repo.” You give it a GitHub URL and it runs 136 checks across multiple threat categories, returning a simple verdict (SAFE / WARN / NOT SAFE). Design goal is safe scanning of potentially hostile repos: it never clones, never executes code, never fetches URLs found in repo contents, and only uses the GitHub REST API + string analysis. It aims to produce human-readable explanations per finding (plus a machine-readable check code), with a “gatekeeper” posture for agentic code-install workflows.

## Triggers
- "scan github repo"
- "elf safety check"
- "github repo security"
- "safe to use repo"
- "security scan repo"
- "vet github repository"

## Description
ELF is a static safety scanner for GitHub repositories designed to be used by AI agents before installing or using code from unknown repositories. It performs 136 security checks across multiple threat categories without cloning the repo or executing any code, making it safe to scan potentially hostile repositories.

## Features
- 136 security checks across threat categories
- Uses only GitHub REST API + string analysis (no cloning/execution)
- Returns SAFE/WARN/NOT SAFE verdict
- Human-readable explanations for each finding
- Machine-readable check codes
- Gatekeeper posture for agentic code-install workflows
- Safe scanning of potentially hostile repositories

## Usage
Use when you need to vet a GitHub repository for security risks before allowing an agent to install or use its code.

## Example
```
/elf scan https://github.com/unknown/mysterious-repo
/elf safety-check git@github.com:company/suspicious-package.git
/elf is-this-repo-safe-to-install https://github.com/vendor/critical-library
```
