# Architectural Decision Record: Repository Triage Skill — IMPULSE

**Status:** Accepted  
**Date:** 2026-09-26  
**Decision Makers:** IMPULSE Architecture Team  
**Consulted Documents:**
- [PLAN.md](file:///e:/Projects/Impulse/PLAN.md) (Section 19, Stage 17)
- [HARNESS_README.md](file:///e:/Projects/Impulse/data/competition/HARNESS_README.md) (Sections 2.2, 2.3, 2.4)
- [IMPULSE.md](file:///e:/Projects/Impulse/IMPULSE.md) (Sections 34, 58)
- [testing_skill.md](file:///e:/Projects/Impulse/docs/decisions/testing_skill.md)
- [hybrid_localization.md](file:///e:/Projects/Impulse/docs/decisions/hybrid_localization.md)

---

## 1. Context & Problem Statement

Prior candidates established:
- **E6**: Hybrid localization policy orchestrating exact, semantic, neighbor, and subgraph search.
- **E7**: Systematic testing strategy skill (`test_strategy`) for framework discovery, reproduction, targeted verification, and intelligent broadening.

However, when an autonomous agent is dropped into an unfamiliar repository without global context, it often wastes initial tool calls on **unstructured, blind exploration**:
1. Guessing primary language, framework, or packaging tools from isolated file names.
2. Incurring repeated directory listings and searching arbitrarily across deep folder structures.
3. Reading massive generated or vendored directories (`node_modules/`, `vendor/`, `dist/`).
4. Re-inspecting build configurations repeatedly across turns because baseline architectural facts were never systematically recorded in task state.

Candidate E8 resolves this by introducing the **Systematic Repository Triage Skill**:
$$\text{E8} = \text{E7} + \text{Systematic Repository Triage Skill}$$

---

## 2. Distinction & Relationship to `test_strategy`

The two skills address orthogonal, complementary stages of the software engineering lifecycle:

| Skill | Primary Question | Scope | Phase of Execution |
| :--- | :--- | :--- | :--- |
| **`repo_triage`** (Stage 17) | *"What is this repository, how is it organized, and how do developers build, run, and test it?"* | Global repository architecture, tooling, entry points, layout, build/CI conventions. | Initial reconnaissance (Step 2 of root workflow). |
| **`test_strategy`** (Stage 16) | *"How should I reproduce and verify this specific bug fix?"* | Detailed verification lifecycle, reproduction, test execution flags, result interpretation, regression bounds. | Defect reproduction and post-edit verification (Step 7 of root workflow). |

`repo_triage` establishes the repository topology early; `test_strategy` executes targeted defect verification later. Neither skill duplicates the other.

---

## 3. Seven Triage Dimensions & Compact Summary

The skill instructs the agent to rapidly investigate 7 core dimensions:
1. **Language & Polyglot Boundaries**: Primary and secondary languages corroborated by root manifests and source trees.
2. **Framework & Ecosystem**: Application framework or library ecosystem identified via dependency manifests and entry-point imports.
3. **Package & Build Manager**: Build tools, packaging managers, and local invocation wrappers (e.g., `make`, `tox`, `poetry`, `npm`, `cargo`).
4. **Entry Points**: Executable scripts, CLI console scripts, `__main__` entry points, or service startup modules.
5. **Test Topology**: Test directory layout, runner configurations, and naming conventions (leaving execution details to `test_strategy`).
6. **CI & Build Conventions**: Key build and test commands extracted from `.github/workflows/`, `.gitlab-ci.yml`, or `Makefile`.
7. **Repository Layout**: Concise structural mapping of root configs, source directories, test locations, and documentation.

### Compact Summary Output
Triage findings are synthesized into a bounded summary:
```text
=== Repository Triage Summary ===
Language(s):          <primary language> (secondary: <if polyglot>)
Framework:            <framework name or "None / Library">
Package Manager:      <detected package/build tool>
Entry Point(s):       <key executable modules, CLI commands, or factory functions>
Source Layout:        <main source directory structure>
Test Layout:          <test directory, runner, and naming conventions>
CI / Build Command:   <canonical test/build command from CI or Makefile>
Key Configurations:   <primary manifest files>
Unknowns / Ambiguity: <explicit list of unresolved questions or "None">
=================================
```

---

## 4. Evidence, Anti-Fabrication & Bounded Reconnaissance Rules

1. **Evidence-Driven Conclusions**:
   - Facts must be corroborated by repository files. If evidence is ambiguous, record `"Unknown"` rather than guessing.
2. **Bounded Reconnaissance Order**:
   - High-value inspection first: root listing $\to$ root manifests $\to$ build tooling $\to$ test topology $\to$ CI conventions $\to$ source entry points.
   - Deeper directory inspection occurs only if root evidence is inconclusive.
3. **Anti-Dumping Invariant**:
   - Never recursively dump whole trees or traverse generated/vendor directories (`node_modules/`, `vendor/`, `target/`, `.git/`).
4. **Strict Secrets Exclusion**:
   - Credentials, API tokens, private keys, and passwords must never be copied from `.env` or config files into task state or triage notes.
5. **Zero Hard-Coded Benchmark Knowledge**:
   - Contains no repository-specific answers, task shortcuts, or paths for FastAPI, Requests, Rich, HTTPX, or SWE-bench tasks.

---

## 5. TaskState Integration

Verified triage facts are recorded directly into `TaskState.repository_facts` via standard categories:
- `category="environment"`: Language, framework, and packaging tooling.
- `category="layout"`: Source directory and test directory paths.
- `category="architecture"`: Discovered entry points and interfaces.
- `category="conventions"`: Canonical build and test commands.
- `category="uncertainty"`: Explicitly recorded unknowns.

This preserves facts across turns, preventing redundant manifest re-reading and tool budget depletion.

---

## 6. Skill Packaging & Declarative Schema

Per `HARNESS_README.md` Section 2.2 and Section 2.3:
- Canonical location: `agent/skills/repo_triage/SKILL.md`
- Packaged in Candidate E8: `experiments/candidates/E8/skills/repo_triage/SKILL.md`
- Declared in `experiments/candidates/E8/agent.yaml`:
  ```yaml
  skills:
    - skills/test_strategy
    - skills/repo_triage
  ```
- Referenced in `experiments/candidates/E8/prompts/root.md` in Operational Workflow and Step 2.

---

## 7. Experimental Hypothesis & Future Metrics

### 7.1. Hypothesis (Stage 17)
> An agent equipped with a generic repository triage skill that front-loads high-value reconnaissance will reduce redundant exploratory commands and shorten the path to relevant source and test files without degrading localization quality.

### 7.2. Proposed Future Metrics (For Live Inference)
- `triage_command_count`: Number of tool calls spent in initial reconnaissance.
- `redundant_exploration_command_count`: Repeated directory or manifest searches across turns.
- `time_to_first_relevant_source_seconds`: Latency from task start to reading the defect source file.
- `patch_resolution_rate`: Fraction of benchmark issues successfully resolved.

### 7.3. Anti-Fabrication Notice
Candidate E8 has **not** been executed against live Gemma 4 inference on this workstation. All empirical metrics remain `null`. No performance claims are asserted without official benchmark evaluation.

---

## 8. Hard Stage 18 Boundary

Candidate E8 implements **Stage 17 only**. It does **NOT** implement:
- Stage 18 Failure Classification (`FailureClassifier`, taxonomy);
- Stage 19 No-Progress Detector;
- Stage 20 Recovery Paths;
- Sub-agents (Scout, Debugger, Reviewer) or LoRA adapters.
