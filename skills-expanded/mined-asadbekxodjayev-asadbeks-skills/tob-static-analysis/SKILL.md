# Static Analysis Toolkit

This comprehensive security toolkit integrates three complementary analysis approaches: CodeQL, Semgrep, and SARIF parsing.

## Core Components

**CodeQL** supports multiple languages including Python, JavaScript, Go, and Java, enabling database creation and taint tracking queries with structured output formats.

**Semgrep** provides "quick security scans using built-in rulesets" covering OWASP and CWE categories, plus custom YAML rule authoring and taint mode analysis.

The SARIF parsing component handles result aggregation from multiple security tools, supporting both CLI queries and Python-based processing.

## Practical Application

Two agents are included: a bash-based scanner for parallel language-specific scans and a triager agent that classifies findings through source code inspection. This workflow supports both standalone analysis and CI/CD pipeline integration.

## Use Cases

Designed for scenarios where you need to "perform security vulnerability detection on codebases."

The toolkit draws methodology from the Trail of Bits Testing Handbook, providing battle-tested approaches for vulnerability detection across diverse development environments.

## Source

Trail of Bits skills repository: https://github.com/trailofbits/skills
