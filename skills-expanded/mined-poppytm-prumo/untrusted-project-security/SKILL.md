---
name: untrusted-project-security
description: Zero-trust ingestion, no-execution static analysis, network egress quarantine, hidden hook scanning, and read-only container sandbox
---
# Untrusted Codebase & Repository Quarantine

## 1. Zero-Trust Ingestion Policy
Treat any foreign or newly cloned repository as potentially malicious untrusted data. Suspend automated task execution until formal quarantine inspection is complete.

## 2. No-Execution Static Analysis
Inspect untrusted repositories exclusively using static parsers, AST analyzers, and text scanners. Never run make, build scripts, test suites, or package install commands during initial triage.

## 3. Network Egress Quarantine
Isolate the analysis environment from all outbound internet connectivity. Prevent untrusted code from exfiltrating local environment data or downloading secondary malware stages.

## 4. Malicious Hook & Trigger Scanning
Scan the repository structure for hidden execution triggers: .git/hooks/, .vscode/tasks.json, .devcontainer/devcontainer.json, GitHub Actions workflows, and suspicious Makefile targets.

## 5. Obfuscation & Payload Detection
Detect high-entropy strings, long base64/hex encoded blobs, hidden Unicode zero-width spaces, and binary executables disguised with text file extensions.

## 6. Sandboxed Container Exploration
When dynamic execution or building is required, run the untrusted project inside an ephemeral, non-root Docker container or microVM (gVisor / Firecracker) with memory and CPU bounds.

## 7. Read-Only Root Filesystem
Mount the untrusted project directory with read-only permissions (ro). Provide only an isolated, ephemeral tmpfs scratchpad for temporary compilation artifacts.

## 8. Manual Human Authorization Barrier
Require explicit, human-confirmed consent before executing any build command or installing dependencies discovered in an untrusted project.

## 9. Safe Dependency Graph Inspection
Parse package manifests (go.mod, package.json, requirements.txt) statically. Never run package manager commands that automatically resolve or download remote packages.

## 10. Formal Clearance Certification
Emit a structured security assessment report (.prumo/history/quarantine-report.json) detailing findings, risk score, and clearance status before onboarding the repository to active development.
