---
name: scv-scan
description: Audits Solidity smart contracts for security vulnerabilities across 36 classes. Follows a structured four-phase workflow for comprehensive codebase analysis.
allowed-tools:
- Read
- Grep
- Glob
- Bash
- Write
- Task
metadata:
  version: 0.2.0
  category: security
---
# Smart Contract Vulnerability Auditor

## Quick Start
```bash
# Phase 1: Read the cheatsheet (mandatory)
read_file references/CHEATSHEET.md

# Phase 2: Sweep for grep-able keywords
grep -rnE "\.call\(|unchecked|selfdestruct" contracts/
```

## Workflow
1. **Load Cheatsheet**: Read `CHEATSHEET.md` to internalize patterns (grep and semantic).
2. **Codebase Sweep**: Run syntactic (grep) and structural (logic) scans to identify candidates.
3. **Deep Validation**: Validate candidates against full reference files and detection heuristics.
4. **Report**: Document confirmed findings with severity, description, and recommendations.

## Rules & Constraints
- **Cheatsheet Mandatory**: Always read the cheatsheet before touching Solidity files.
- **Reference Timing**: Read full references ONLY during validation (Phase 3), not sweep.
- **Semantic Analysis**: Prioritize reading logic over simple keyword matching.
- **False Positive Discipline**: Discard findings that match documented false positive conditions.
- **Trace Calls**: Follow state across contract boundaries and hidden hooks (ERC-721/1155).

## When to Use
- Auditing Solidity codebases for security vulnerabilities before deployment.
- Systematically validating a contract against common exploit patterns (reentrancy, access control).
- Performing a structured security scan of a new or modified contract.

## When NOT to Use
- Auditing non-Solidity contracts (Vyper, Rust, Move).
- Gas optimization or code style reviews only (this focuses on security).
- Formal verification of invariants (use Certora, Halmos, or Echidna instead).

## References
- [Skill Manual](references/scv-scan-manual.md)
- [Cheatsheet](references/CHEATSHEET.md)
- [Vulnerability Reference List](references/)
