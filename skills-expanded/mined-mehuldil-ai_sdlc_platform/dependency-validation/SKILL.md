---
name: dependency-validation
description: Validate bundle size budgets, analyze package dependencies, detect redundancy, flag security vulnerabilities
model: sonnet-4-6
token_budget: {input: 6000, output: 3000}
---

# Dependency Validation Skill

Analyzes frontend dependencies for size compliance, redundancy, and security vulnerabilities.

## Bundle Size Budgets

- Base Bundle: <= 10 MB (gzip)
- Vendor/Libraries: <= 20 MB (gzip)
- Assets: <= 20 MB
- Total: <= 50 MB (enforced)

## Package Analysis

### 1. Dependency Tree Inspection
- Direct dependencies count
- Transitive dependencies
- Duplicate packages (different versions)
- Unused dependencies

### 2. Package Size Analysis
- Gzip sizes for each dependency
- Compare to historical average
- Flag significant increases
- Check tree-shaking effectiveness

### 3. Redundant Package Detection
- Same functionality in multiple packages
- Multiple versions of same package
- Example: moment.js (68KB) + date-fns (13KB)

## Security Audits

### 1. Vulnerability Scanning
- npm audit for known vulnerabilities
- Severity levels: Critical, High, Moderate, Low
- Exploitability information
- Remediation paths

### 2. Dependency Security
- Malicious packages
- Abandoned packages (no updates 2+ years)
- Suspicious permissions
- Unusual OS/network requests

## Tree-Shaking Validation

- Build without tree-shaking (baseline)
- Build with tree-shaking (optimized)
- Compare reduction (should be 30-50%)
- Investigate if reduction insufficient

## Validation Process

1. Measure current state
2. Identify additions
3. Compare budgets
4. Analyze redundancy
5. Security check
6. Tree-shaking validation

## Guardrails

- Fail if: Total bundle > 50MB
- Fail if: Critical security vulnerabilities
- Warn if: Adding > 100KB single package
- Warn if: Total approaches 45MB
- Warn if: Redundant packages detected
- Warn if: Abandoned package found
- Require: >= 30% tree-shaking reduction

## Tools & Commands

```bash
npm ls --depth=0          # Analyze dependencies
npm audit                 # Security audit
npm pack                  # Bundle size
depcheck                  # Check for unused
webpack-bundle-analyzer  # Bundle visualization
size-limit                # Size constraints
```

## Triggers

Use when:
- PR adds/updates dependencies
- Bundle size review needed
- Security audit required
- Dependency optimization needed
- Architecture review includes dependencies

---
