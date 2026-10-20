# Copilot Instructions: Agentic Ai System Design
Description: A comprehensive skill for designing robust agentic AI systems that avoid common failure modes like infinite loops, hallucinated planning, and unsafe tool use.

# Agentic AI System Design Skill

## Overview
This skill enables you to design robust agentic AI systems that avoid common failure modes while maintaining effective functionality. Key concepts are covered in [Core Concepts](references/core_concepts.md).

## Step-by-Step Workflow
1. **System Requirements Analysis**
   - Identify all required capabilities
   - Map necessary tools and APIs
   - Define success criteria and constraints

2. **Failure Mode Prevention Design**
   - Implement safeguards against [common failure modes](references/failure_modes.md)
   - Apply [mitigation strategies](references/mitigation_strategies.md) for each potential failure

3. **Implementation**
   ```python
   # Example: Safe search agent with termination conditions
   class SafeSearchAgent:
       def __init__(self, max_retries=5, timeout=300):
           self.max_retries = max_retries
           self.timeout = timeout  # seconds
           self.attempts = 0
           self.start_time = time.time()
       
       def search(self, query):
           while (self.attempts < self.max_retries and 
                  time.time() - self.start_time < self.timeout):
               self.attempts += 1
               results = execute_search(query)
               if validate_results(results):
                   return results
               query = refine_query(query, results)
           raise Exception("Maximum attempts or timeout reached")
   ```

4. **Validation Layer Implementation**
   ```python
   # Example: Plan verification decorator
   def verify_plan(required_tools):
       def decorator(func):
           def wrapper(plan, *args, **kwargs):
               missing_tools = [t for t in plan['tools'] 
                               if t not in required_tools]
               if missing_tools:
                   raise Exception(f"Unavailable tools: {missing_tools}")
               return func(plan, *args, **kwargs)
           return wrapper
       return decorator
   ```

5. **Monitoring System Setup**
   - Track action history
   - Measure progress metrics
   - Log tool usage

## Best Practices
1. **Always implement termination conditions** for iterative processes
2. **Separate planning and execution** with validation layers
3. **Adopt principle of least privilege** for tool access
4. **Maintain comprehensive logs** for debugging and analysis

## Common Pitfalls
1. **Assuming model failures** when system design is actually the issue
2. **Overlooking action tracking** leading to ineffective retries
3. **Inadequate tool documentation** causing capability assumptions
4. **Missing approval workflows** for high-risk operations

## Validation Steps
1. **Stress Testing**: Simulate edge cases and failure scenarios
2. **Progress Monitoring**: Verify measurable improvement in iterative processes
3. **Permission Auditing**: Confirm least-privilege access for all tools
4. **Plan Validation Checks**: Ensure all plans pass feasibility verification

By following this comprehensive approach, you can build reliable agentic AI systems that avoid common failure modes while delivering consistent results.

## Reference Guides

### Core Concepts

# Core Concepts of Agentic AI System Design

Agentic AI systems are complex architectures that go beyond simple chatbot applications. They operate in cyclical or iterative formats to drive consistent results through observation, planning, and execution cycles. Unlike traditional AI models where failures were often attributed to model hallucinations, modern agentic system failures typically stem from design flaws rather than model capabilities.

Key characteristics of agentic systems include:
1. **Iterative Operation**: Agents perform tasks through repeated observe-plan-act cycles
2. **Tool Integration**: Systems incorporate external tools and APIs to extend functionality
3. **Autonomous Decision Making**: Agents make independent decisions within defined constraints

Common failure modes include:
- **Infinite Loops**: Agents repetitively perform similar tasks without meaningful progress
- **Hallucinated Planning**: Creating plausible but impossible execution plans
- **Unsafe Tool Use**: Executing technically valid but risky or destructive actions

Understanding these core concepts is essential for designing robust agentic systems that avoid common pitfalls while maintaining effective functionality.

### Failure Modes

# Detailed Analysis of Agentic AI Failure Modes

## Infinite Loops
Occur when agents repetitively perform similar tasks without making progress toward goal completion. Primary causes:
1. **Missing Termination Conditions**: No defined limits on retries or runtime
2. **Lack of Action Tracking**: Not monitoring if actions change between iterations
3. **No Progress Measurement**: Failing to track whether results improve with retries

Example: An agent searching for a non-existent document keeps retrying with similar search terms without realizing the document doesn't exist.

## Hallucinated Planning
Happens when agents create plausible but impossible execution plans due to:
1. **Undefined Tool Capabilities**: Agents assume unavailable functionality
2. **Missing Plan Validation**: Executing without verifying feasibility
3. **Unclear Constraints**: Agents make assumptions instead of checking limitations

Example: An agent plans to book flights using a non-existent travel API.

## Unsafe Tool Use
Occurs when technically valid actions have unintended consequences:
1. **Overprivileged Tools**: Excessive permissions granted
2. **Missing Approval Workflows**: No review for high-risk actions
3. **Undefined Access Tiers**: No separation between read/write/delete operations

Example: A database cleanup agent accidentally deletes active records instead of archived ones.

### Mitigation Strategies

# Comprehensive Mitigation Strategies for Agentic AI Failures

## Infinite Loop Prevention
1. **Set Termination Conditions**:
   - Maximum retry counts (e.g., 5 attempts)
   - Time limits (e.g., 5 minute timeout)
   - Computational budget limits
2. **Implement Action Tracking**:
   - Compare current actions with previous attempts
   - Require significant variation between retries
3. **Progress Monitoring**:
   - Quantify result quality improvements
   - Establish minimum improvement thresholds

## Hallucinated Planning Prevention
1. **Clear Tool Documentation**:
   - Explicitly define capabilities and limitations
   - Provide detailed tool schemas
2. **Plan Verification**:
   - Implement multi-agent architectures with verifier agents
   - Human-in-the-loop for high-risk plans
3. **Constraint Specification**:
   - Explicitly list available tools and permissions
   - Require confirmation before assuming capabilities

## Unsafe Tool Use Prevention
1. **Principle of Least Privilege**:
   - Grant minimum necessary permissions
   - Separate read/write/delete access
2. **Approval Workflows**:
   - Human review for high-risk actions
   - Multi-step confirmation processes
3. **Tool Tiering**:
   - Classify tools by risk level
   - Implement graduated access controls

Implementation of these strategies significantly reduces failure rates while maintaining system effectiveness.

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[Why Agentic AI Fails: Infinite Loops, Planning Errors, and More](https://www.youtube.com/watch?v=D37Ijn2o5U0)** by IBM Technology