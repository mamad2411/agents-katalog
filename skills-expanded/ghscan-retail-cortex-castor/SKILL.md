---
name: bazel-modules
description: Elite Bazel 8/9 Bzlmod dependency management & SDLC. Covers hermetic toolchain setup, MODULE.bazel.lock security (CWE-829), HTTP 429 rate limit resilience, rules_hugo documentation on GitHub Pages, and troubleshooting.
license: Apache-2.0
metadata:
  author: Ryan McGuinness
  version: "1.0"
authors:
  - name: Retail Cortex Engineering
    url: https://github.com/retail-cortex/castor
category: bazel
tags:
  - bazel
  - bzlmod
  - monorepo
  - hermetic
trigger_phrases:
  - "configure Bazel bzlmod"
  - "setup Bazel build"
  - "hermetic Bazel TDD"
execution_hints:
  preferred_model: "gemini-3.1-pro"
  requires_human_approval: false
  environment_variables:
    - BAZEL_CXXOPTS
  timeout_seconds: 300
---
# Bazel Modules & Bzlmod Dependency SDLC Skill

This skill prescribes best practices for designing, managing, securing, and testing enterprise polyglot repositories using **Bazel 8/9** and the **Bzlmod** dependency system.

## Prerequisites & Pre-Flight Checklist

1. Bazel 8.0.0+ or Bazelisk installed.
2. `MODULE.bazel` file initialized in repository root.

## Security Checkpoints & CWE Invariants

- **CWE-829 (Unverified External Imports)**: Commit `MODULE.bazel.lock` to ensure all remote BCR dependencies match cryptographic checksums.
- **Hermetic Execution**: Build actions MUST NOT reach out to external networks during compilation.

## HTTP 429 Rate Limit & Quota Backoff Invariants

- Outbound remote cache actions and CI download tools must implement exponential backoff with jitter to handle HTTP 429 rate limits from remote artifact stores.

## 3-Phase Execution Protocol

### Phase 1: Declare Bzlmod Rulesets in MODULE.bazel
Import platform rules (`bazel_skylib`, `rules_go`, `rules_python`, `rules_java`, `aspect_rules_js`, `rules_proto_grpc`, `rules_hugo`).

### Phase 2: Hermetic TDD Testing & Coverage Collection
Execute unit tests across all languages within Bazel's sandboxed environment:
```bash
bazel test //... --test_output=errors
bazel coverage //... --combined_report=lcov
```

### Phase 3: Compile Hugo Docs for GitHub Pages
```bash
bazel build //docs:hugo_site
```

## Troubleshooting & Remediation Matrix

| Symptom / Error | Root Cause | Exact Remediation |
| :--- | :--- | :--- |
| `ERROR: The lockfile MODULE.bazel.lock is out of date` | Modified `MODULE.bazel` without regenerating lockfile | Run `bazel mod deps --lockfile_mode=update`. |
| `Gazelle: no Go packages found` | Missing `go_prefix` directive or incorrect directory path | Add `# gazelle:prefix github.com/org/repo` to root `BUILD.bazel`. |
| Build action fails due to missing internet access | Non-hermetic build rule reaching out to remote API | Pre-fetch remote assets via Bzlmod `http_archive` or Bazel download rules. |

## Progressive Disclosure References

- **Bzlmod Architecture Guide**: Read [`references/bzlmod_guide.md`](file:///Users/rmcguinness/Projects/skill-builder/skills/bazel-modules/references/bzlmod_guide.md).
- **CI/CD & Hugo Docs Guide**: Read [`references/ci_cd_hugo.md`](file:///Users/rmcguinness/Projects/skill-builder/skills/bazel-modules/references/ci_cd_hugo.md).
- **Reference Module File**: View [`examples/MODULE.bazel`](file:///Users/rmcguinness/Projects/skill-builder/skills/bazel-modules/examples/MODULE.bazel).
