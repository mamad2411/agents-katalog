---
name: process-excellence
description: Apply Lean Six Sigma methodology for process improvement and operational excellence. Covers the full DMAIC cycle (Define, Measure, Analyze, Improve, Control), value stream mapping, process mining, waste identification, root cause analysis, and sustained performance control. Use when analyzing business processes, identifying inefficiencies, or designing improved workflows.
---

# Process Excellence

Apply Lean Six Sigma methodology to analyze, improve, and control business processes. Lean eliminates waste and improves flow. Six Sigma reduces variation and defects. Together they drive both efficiency and effectiveness.

## DMAIC Methodology

DMAIC (Define, Measure, Analyze, Improve, Control) is the structured approach for improving existing processes. Each phase has specific deliverables and gate criteria before moving to the next.

### Define

Clearly articulate the improvement opportunity before jumping to solutions.

**Problem statement**: Quantify the current problem in terms of cycle time, cost, quality, or customer satisfaction. A vague problem statement produces vague solutions.

**Scope**: Define what's in scope and what's not. Process improvement projects that try to fix everything fix nothing.

**Success criteria**: Establish measurable targets for each key metric. Include current state, target state, and the percentage improvement expected.

**Project charter elements**:
- Problem statement with quantified impact
- Process boundaries (start point, end point)
- Success metrics with baselines and targets
- Timeline for each DMAIC phase
- Team: process owner, sponsor, project lead, team members

**Digital context**: Assess automation potential, current level of process digitization, data availability, and RPA opportunity. This shapes the analysis approach and solution space.

### Measure

Collect baseline data and map the process as it actually operates (not as documentation says it should).

**Process mapping**: Create a SIPOC diagram (Suppliers, Inputs, Process, Outputs, Customers) to establish boundaries, then map the detailed process flow with decision points and handoffs.

**Baseline metrics**: For each key metric, document the measurement method, sample size, current baseline, and sigma level.

**Data collection plan**: Specify each data point, its operational definition, collection method, frequency, and responsible person. Ambiguous definitions produce unreliable data.

**Process capability analysis**:
- Cp/Cpk indices (process capability relative to specifications)
- Process stability assessment (in control vs. out of control)
- Common cause vs. special cause variation

### Analyze

Identify and validate root causes of process variation and waste. This is where discipline matters most. Don't skip to solutions.

**Waste identification (TIMWOODS)**:

| Waste Type | What to Look For |
|------------|-----------------|
| Transportation | Unnecessary movement of materials or information between steps |
| Inventory | Work piling up between process steps, excess WIP |
| Motion | Unnecessary movement of people (extra clicks, walking, searching) |
| Waiting | People or work idle, waiting for approvals, inputs, or capacity |
| Overproduction | Producing more, sooner, or faster than the next step requires |
| Overprocessing | Doing more work than the customer requires or values |
| Defects | Errors requiring rework, correction, or scrapping |
| Skills (underutilized) | People doing work below their capability, untapped expertise |

**Root cause tools**:

5 Whys: Start with the problem statement and ask "why" iteratively until you reach a root cause you can act on. Typically 3-5 iterations. The root cause should be something the team can influence.

Fishbone (Ishikawa) diagram: Organize potential causes into categories (People, Process, Machine, Material, Environment, Measurement). Useful for brainstorming with the team and ensuring you haven't missed a category.

**Hypothesis testing**: For each suspected root cause, define a hypothesis, test method, and acceptance criteria. Validate with data, not intuition.

**Pareto analysis**: Rank root causes by their contribution to the problem. Typically 20% of causes drive 80% of the impact. Address the vital few, not the trivial many.

### Improve

Design and deploy optimized process solutions.

**Solution evaluation matrix**: Score each potential solution on impact, effort, cost, and risk. Separate high-impact/low-effort wins from longer-term structural changes.

**Pilot before rollout**: Test improvements in a controlled setting before full implementation. Measure pilot results against baseline and target. A solution that works in theory but fails in practice isn't a solution.

**Implementation planning**: Phase the rollout with clear activities, owners, timelines, and dependencies. Include training and communication alongside the technical changes.

**Full rollout plan**:
- Training for all affected staff
- Communication to stakeholders
- Phased schedule with go/no-go checkpoints
- Support model during transition

### Control

Ensure improvements are sustained. Without control mechanisms, processes revert to their pre-improvement state within months.

**Control plan**: For each critical process output, define the measurement, control method (control chart, checklist, automated alert), monitoring frequency, and response plan for out-of-control conditions.

**Control charts**: Select the appropriate chart type based on data characteristics:
- X-bar R / X-bar S: variable data, subgroups
- I-MR: variable data, individual measurements
- P-chart: proportion defective
- C-chart: count of defects

Define Upper Control Limit (UCL), Lower Control Limit (LCL), and Center Line (CL).

**Standard work documentation**: Update process flows, work instructions, SOPs, and training materials to reflect the improved process. If it's not documented, it will drift.

**Response protocol**: Define specific triggers and their required responses. When metric X exceeds threshold Y, person Z takes action A within timeframe T.

**Handover checklist**:
- Control charts deployed and understood
- Response plan documented and tested
- Process owner trained on monitoring
- SOPs updated and accessible
- Training completed for all operators
- Dashboard live and accurate
- Lessons learned documented

## Value Stream Mapping

### Building a Value Stream Map

Value stream mapping visualizes the end-to-end flow of materials and information required to deliver a product or service.

**Steps to map current state**:
1. Walk the process from customer back to supplier
2. Record cycle time, changeover time, and WIP at each step
3. Separate value-added from non-value-added time
4. Identify bottlenecks (highest cycle time relative to takt time)
5. Mark inventory accumulation points
6. Calculate total lead time vs. value-added time ratio

**Key metrics per step**: Cycle time (C/T), work in progress (WIP), changeover time, uptime, batch size.

**Summary metrics**: Total lead time, total value-added time, percentage value-added. In most service processes, value-added time is less than 5% of total lead time. The gap is the improvement opportunity.

**Future state design**: Design for continuous flow where possible. Eliminate steps that don't add value. Pull work through the system rather than pushing it. The future state should show reduced lead time, lower WIP, and higher value-added percentage.

## Process Mining

Process mining uses event log data from IT systems to discover, monitor, and improve actual processes.

### When to Use Process Mining

- Large-scale processes with many variants and exceptions
- ERP or workflow system logs available for extraction
- Need to discover actual process behavior vs. documented process
- Conformance checking against regulatory or policy requirements
- Identifying automation candidates from high-volume, low-variation paths

### Process Mining Analysis

**Discovery metrics**: Number of process path variants discovered, average case duration, deviation points where the process diverges from the intended flow.

**Conformance analysis**: Compliance rate, number and percentage of deviating cases, root causes of deviation (are deviations intentional workarounds or genuine errors?).

**Process intelligence findings**: Identify bottlenecks (where cases spend the most time), rework loops (where cases go backwards), and excessive wait times (where cases sit idle).

## SIPOC Analysis

SIPOC establishes process boundaries before detailed mapping. It answers: Who supplies what, through which high-level steps, producing what outputs, for whom?

| Element | Question |
|---------|----------|
| **S**uppliers | Who provides inputs to this process? |
| **I**nputs | What enters the process (materials, information, triggers)? |
| **P**rocess | What are the 5-7 high-level steps? |
| **O**utputs | What does the process produce? |
| **C**ustomers | Who receives the outputs? |

Use SIPOC in the Define phase to align the team on process scope. It prevents scope creep and ensures you're mapping the right process.

## Standard Work

Standard work documents the current best method for performing a process. It is the baseline for improvement, not the ceiling.

**Standard work elements**:
- Takt time: customer demand rate (available time / customer demand)
- Cycle time: time to complete one unit (must be less than or equal to takt time)
- WIP limit: maximum work in progress allowed
- Work sequence: steps in order with time and quality checks at each step

**Principles**:
- Takt time sets the pace. If cycle time exceeds takt time at any station, that station is a bottleneck
- WIP limits prevent overburden and expose bottlenecks. If you limit WIP and work piles up, you've found the constraint
- Document the current best method, then improve from there. You can only improve what is standardized

## Process Performance Dashboard

Track three categories of metrics to monitor process health.

**Efficiency metrics**: Cycle time, throughput, utilization. These tell you how fast and how productively the process operates.

**Quality metrics**: Defect rate, first pass yield (FPY), customer complaints. These tell you whether the process produces acceptable output.

**Cost metrics**: Cost per unit, scrap cost, rework cost. These translate process performance into financial impact.

Use RAG status (Green = on target, Yellow = at risk, Red = off target) and track baseline, current, and target values to show direction of travel.

## Financial Impact

Every process improvement should be translated into financial terms.

| Category | How to Calculate |
|----------|-----------------|
| Cost savings (annual) | Reduction in labor, materials, rework, waste |
| Revenue impact | Increased throughput, reduced lead time enabling more sales |
| One-time implementation cost | Training, systems, consulting, pilot costs |
| ROI | (Annual savings - Implementation cost) / Implementation cost |
| Payback period | Implementation cost / Monthly savings |

## Principles

- Start with data. Never assume. Measure current state before proposing improvements
- Value is defined by the customer, not by internal convenience
- Eliminate waste first, then optimize what remains
- Standardize before improving. You can only improve what is standardized
- Changes in one part of a process affect other parts. Think systemically
- Engage the people doing the work. They know the process best and they'll be implementing the changes
- Pilot before rollout. Test improvements before full implementation
- Control to sustain. Improvements without control mechanisms revert within months
- If you're not measuring, you're not improving. And if your measurements are wrong, you're improving the wrong thing
