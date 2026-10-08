---
name: f5-core
description: F5 Framework core workflow, quality gates, and behavioral modes
category: core
allowed-tools: Read, Write, Glob, Grep, Bash
user-invocable: true
context: inject
auto-load:
  - always
---

# F5 Framework Core Skills

This skill provides the foundational knowledge for F5 Framework:

## Contents

- [Workflow](./workflow.md) - F5 development workflow phases
- [Quality Gates](./quality-gates.md) - D1-D4 and G1-G4 gate definitions
- [Behavioral Modes](./behavioral-modes.md) - strict, standard, exploratory

## Auto-load

These skills are automatically loaded when F5 Framework is active.

## Quick Reference

### Workflow Phases
1. **D1**: Research Complete - Market/tech research, stakeholder interviews
2. **D2**: SRS Approved - Software Requirements Specification
3. **D3**: Basic Design Approved - System architecture, data model
4. **D4**: Detail Design Approved - Module design, API contracts
5. **G2**: Implementation Ready - Code complete, unit tests
6. **G2.5**: Verification Complete - Asset verification, visual QA
7. **G3**: Testing Complete - All tests pass, security scan
8. **G4**: Deployment Ready - Staging verified, UAT approved

### Behavioral Modes
- **coding**: Code-first, minimal explanations, production-ready
- **analytical**: Systematic analysis, data-driven decisions
- **security**: Paranoid mode, OWASP checks, defense in depth
- **debugging**: Root cause analysis, systematic diagnosis
- **review**: Constructive feedback, best practices check
- **planning**: Strategic thinking, phased approach
- **teaching**: Step-by-step explanations, examples
- **performance**: Metrics-driven optimization
- **creative**: Innovative approaches, exploration

### Gate Commands
```bash
/f5-gate check D1    # Check gate D1
/f5-gate check G2    # Check gate G2
/f5-gate status      # Show all gates status
```

$ARGUMENTS
