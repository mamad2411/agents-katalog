---
name: quality-repair
description: |
  Diagnose, fix, review, secure, optimize, and harden code or delivery pipelines.
  Use when debugging, fixing issues, reviewing code, auditing security, checking dependencies, diagnosing CI/CD, or optimizing performance.
---

<skill name="quality-repair" version="3.0.0">
  <metadata>
    <keywords>
      <keyword>debug</keyword>
      <keyword>fix</keyword>
      <keyword>review</keyword>
      <keyword>security</keyword>
      <keyword>performance</keyword>
      <keyword>ci</keyword>
      <keyword>dependency</keyword>
      <keyword>quality</keyword>
    </keywords>
  </metadata>

  <goal>Diagnose, fix, review, secure, optimize, and harden code or delivery pipelines.</goal>

  <core_principles>
    <principle name="Progressive Disclosure">
      <rule>Keep this skill as a compact router and load detailed lane references only on demand.</rule>
    </principle>
    <principle name="Intent Routing">
      <rule>Choose the narrowest matching route before reading references or using scripts.</rule>
    </principle>
    <principle name="Compatibility Preservation">
      <rule>Use consolidated lane references to preserve former skill and workflow behavior without reinstalling alias skills.</rule>
    </principle>
  </core_principles>
  <routing>
    <route intent="Root-cause diagnosis" reference="references/analyze.md">Read when the problem is unclear or needs investigation before changes.</route>
    <route intent="Issue fixing" reference="references/fix-issue.md">Read when assigned a GitHub issue or bug fix workflow.</route>
    <route intent="Review workflow" reference="references/review.md">Read when asked for code review or second opinion.</route>
    <route intent="Automated code review rubric" reference="references/code-reviewer.md">Read for bug, regression, maintainability, and test findings.</route>
    <route intent="CI/CD debugging" reference="references/ci-cd-debugger.md">Read when builds, tests, or deployments fail in CI.</route>
    <route intent="Dependency maintenance" reference="references/dependency-check.md">Read when auditing outdated or vulnerable dependencies.</route>
    <route intent="Security audit" reference="references/security-audit.md">Read for release or auth/payment security review.</route>
    <route intent="Security scanning" reference="references/security-checker.md">Read for secrets, injection, authz/authn, or insecure patterns.</route>
    <route intent="Performance workflow" reference="references/performance-tune.md">Read when performance budgets are missed or traffic will increase.</route>
    <route intent="Performance analysis" reference="references/performance-analyzer.md">Read when profiling or benchmarking bottlenecks.</route>
    <route intent="Code style and maintainability" reference="references/code-style-enforcer.md">Read for style, naming, DRY, and type-safety checks.</route>
    <route intent="Runtime safety" reference="references/runtime-safety-enforcer.md">Read for dependency isolation, error contracts, and logging policy.</route>
  </routing>

  <workflow>
    <step number="1" name="Classify Intent">
      <instruction>Choose the narrowest matching route from this skill.</instruction>
    </step>
    <step number="2" name="Load One Lane">
      <instruction>Read only the selected reference file before executing specialized steps.</instruction>
    </step>
    <step number="3" name="Use Resources On Demand">
      <instruction>Load scripts, assets, or extra references only when the selected lane requires them.</instruction>
    </step>
    <step number="4" name="Report Route">
      <instruction>State the lane used when it affects auditability, handoff, or recovery.</instruction>
    </step>
  </workflow>

  <best_practices>
    <do>Read the selected lane reference before specialized work.</do>
    <do>Use bundled scripts, assets, or extra references only when the selected lane requires them.</do>
    <do>State the selected route when it affects auditability, handoff, or recovery.</do>
    <dont>Load multiple lane references unless the user request genuinely crosses responsibilities.</dont>
  </best_practices>
  <consolidated_skills>
    <former_skill>analyze</former_skill>
    <former_skill>fix-issue</former_skill>
    <former_skill>review</former_skill>
    <former_skill>code-reviewer</former_skill>
    <former_skill>ci-cd-debugger</former_skill>
    <former_skill>dependency-check</former_skill>
    <former_skill>security-audit</former_skill>
    <former_skill>security-checker</former_skill>
    <former_skill>performance-tune</former_skill>
    <former_skill>performance-analyzer</former_skill>
    <former_skill>code-style-enforcer</former_skill>
    <former_skill>runtime-safety-enforcer</former_skill>
  </consolidated_skills>
  <related_skills>
    <skill>code</skill>
    <skill>archive-manager</skill>
    <skill>research-docs</skill>
  </related_skills>
</skill>
