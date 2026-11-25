---
name: performance
description: Performance testing skill - JMeter, Argo, load profiles, NFR validation
model: sonnet-4-6
token_budget: {input: 8000, output: 4000}
---

# Performance Testing Skill

End-to-end performance testing with JMeter and NFR validation.

## Capabilities

- **NFR Analysis**: Extract and validate non-functional requirements
- **Load Profile Design**: Realistic user load patterns
- **JMeter Script Creation**: Performance test implementation
- **Test Execution**: Argo workflow execution
- **Result Analysis**: Performance bottleneck identification
- **Reporting**: Baseline establishment and improvement tracking

## Load Profiles

- Baseline: Normal expected load
- Peak: Maximum expected load
- Stress: Beyond expected load
- Spike: Sudden load increase
- Soak: Extended duration test

## Performance Metrics

- **Throughput**: Requests per second (RPS)
- **Response Time**: p50, p95, p99 latencies
- **Concurrency**: Simultaneous users supported
- **Error Rate**: Acceptable error percentage
- **Resource Usage**: CPU, memory utilization

## Process Flow

1. Analyze NFR requirements
2. Design test scenarios
3. Create JMeter scripts
4. Execute via Argo
5. Collect results
6. Analyze bottlenecks
7. Report findings

## Skill Triggers

Use this skill when:
- Performance testing needed
- NFR validation required
- Load test scripts needed
- Performance optimization planned
- Baseline establishment required

## Sub-Skills

### PerformanceSTLC
Comprehensive performance testing STLC covering all phases of performance test implementation:
- **Planning & Analysis** - NFR extraction, performance objectives, load profile design
- **Design Phase** - Test scenario design, JMeter script architecture
- **Execution** - Argo workflow orchestration, load generation, monitoring
- **Analysis** - JMeter result analysis, NFR validation, bottleneck identification
- **Reporting** - Baseline establishment, trend analysis, optimization recommendations

## Quality Standards

- Realistic load patterns
- Complete scenario coverage
- Accurate result collection
- Clear bottleneck analysis
- Actionable optimization recommendations
