---
description: 
globs: 
alwaysApply: true
---
---
name: "Think Pool Rules"
description: "Think Pool 시스템 규칙 정의"
version: "1.0.0"
author: "Cursor IDE"
globs: ["**/*.{js,ts,jsx,tsx,py,java,cpp,cs}"]
priority: high
---

# Think Pool 통합 규칙

## 1. 사고 모드 기본 규칙

### Think 모드 활성화
when: code_complexity_detected
conditions:
  - complexity_score > 8
  - function_length > 50
  - nesting_depth > 3
  - security_critical_section
  - performance_critical_section
then:
  - invoke: "think_mode"
  - analyze_current_approach()
  - evaluate_edge_cases()
  - consider_alternatives()
  - check_architecture_alignment()

### Sequential Thinking 모드 활성화
when: complex_reasoning_needed
conditions:
  - multiple_solution_paths
  - uncertainty_level > "medium"
  - decision_branches > 3
  - incomplete_information
then:
  - invoke: "sequential_thinking_mode"
  - break_down_problem()
  - explore_solution_paths()
  - verify_hypotheses()
  - adapt_thinking_process()

## 2. 통합 분석 규칙

### 알고리즘 분석 통합
when: algorithm_analysis_needed
then:
  - invoke: "sequential_thinking_mode"
  - decompose_problem()
  - invoke: "think_mode"
  - analyze_implementation()
  - apply_rules: "algorithm-rules.mdc"

### 디버깅 통합
when: critical_error_detected
then:
  - invoke: "sequential_thinking_mode"
  - analyze_error_pattern()
  - invoke: "think_mode"
  - design_solution()
  - apply_rules: "debug-rules.mdc"

### 리팩토링 통합
when: code_improvement_needed
then:
  - invoke: "sequential_thinking_mode"
  - plan_refactoring()
  - invoke: "think_mode"
  - analyze_structure()
  - apply_rules: "refactor-rules.mdc"

## 3. MCP 서버 통합 규칙

### Browser Tool 통합
when: browser_analysis_needed
then:
  - invoke: "browser_tool"
  - collect_performance_metrics()
  - analyze_console_logs()
  - check_network_errors()

### Brave Search 통합
when: research_needed
then:
  - invoke: "brave_search"
  - search_latest_patterns()
  - verify_solutions()
  - analyze_trends()

### Sequential Thinking 통합
when: complex_analysis_needed
then:
  - invoke: "sequential_thinking"
  - structure_analysis()
  - evaluate_options()
  - make_decisions()

## 4. 모니터링 및 보고 규칙

### 성능 모니터링
when: monitoring.active
metrics:
  - execution_time
  - memory_usage
  - cpu_utilization
then:
  - collect_metrics()
  - analyze_trends()
  - trigger_alerts()

### 결과 보고
when: analysis.completed
include:
  - thinking_process_summary
  - sequential_analysis_results
  - recommendations
then:
  - generate_report()
  - highlight_priorities()
  - suggest_next_steps()