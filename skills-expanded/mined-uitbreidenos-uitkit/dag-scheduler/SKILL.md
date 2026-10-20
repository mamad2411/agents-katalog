---
name: "dag-scheduler"
description: "Build, validate, and execute directed acyclic graph (DAG) topologies for multi-agent workflows with automatic parallelization and cycle detection"
---

# DAG Scheduler Skill

## When to activate

- Designing or implementing a multi-agent workflow with complex dependencies (not purely sequential)
- Converting an existing sequential workflow into a DAG to enable parallelization
- Debugging agent coordination issues (deadlocks, circular dependencies, execution order)
- Building resilient workflows that recover from partial failures without restarting
- Optimizing multi-agent latency by identifying parallelizable subtasks

## When NOT to use

- Simple sequential workflows (use saga pattern instead)
- Single-agent tasks or tool loops
- Workflows with circular dependencies (DAGs must be acyclic)
- Real-time streaming workflows (use event-driven architecture instead)

## Instructions

### DAG Definition

Define tasks as a flat list with explicit dependencies:

```json
{
  "dag_id": "my_workflow",
  "tasks": [
    {
      "task_id": "task_1",
      "agent": "agent_name",
      "action": "action_name",
      "dependencies": [],
      "timeout_ms": 30000,
      "retries": 2
    },
    {
      "task_id": "task_2",
      "agent": "agent_name",
      "action": "action_name",
      "dependencies": ["task_1"],
      "timeout_ms": 30000,
      "retries": 2
    }
  ]
}
```

Rules:
- Every task has an explicit `task_id`
- Dependencies list contains only `task_id` values (not agent names)
- Root tasks have `dependencies: []`
- All task IDs referenced in dependencies must exist in the tasks list

### Cycle Detection

Always run cycle detection before executing a DAG:

```python
def has_cycle(dag_tasks):
    """Returns True if the DAG has a cycle, False otherwise."""
    visited = set()
    rec_stack = set()
    task_map = {t['task_id']: t for t in dag_tasks}
    
    def dfs(node):
        visited.add(node)
        rec_stack.add(node)
        for dep in task_map[node]['dependencies']:
            if dep not in visited:
                if dfs(dep):
                    return True
            elif dep in rec_stack:
                return True
        rec_stack.remove(node)
        return False
    
    for task in dag_tasks:
        if task['task_id'] not in visited:
            if dfs(task['task_id']):
                return True
    return False
```

If `has_cycle()` returns True, do not execute. Log the cycle path and escalate to the operator.

### Topological Sort and Parallelization

Convert the DAG into execution lanes (sets of tasks that can run in parallel):

```python
def get_execution_lanes(dag_tasks):
    """
    Returns a list of task lists.
    Each inner list contains tasks with no inter-task dependencies (can run in parallel).
    """
    from collections import defaultdict, deque
    
    in_degree = {t['task_id']: 0 for t in dag_tasks}
    graph = defaultdict(list)
    task_map = {t['task_id']: t for t in dag_tasks}
    
    # Build graph and compute in-degrees
    for task in dag_tasks:
        for dep in task['dependencies']:
            graph[dep].append(task['task_id'])
            in_degree[task['task_id']] += 1
    
    # Kahn's algorithm: process by in-degree level
    lanes = []
    queue = deque([t for t in dag_tasks if in_degree[t['task_id']] == 0])
    
    while queue:
        lane = []
        next_queue = deque()
        
        # All tasks with in-degree 0 can run in the same lane
        while queue:
            task_id = queue.popleft()
            lane.append(task_map[task_id])
            
            # Decrement in-degree for dependent tasks
            for dependent in graph[task_id]:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    next_queue.append(dependent)
        
        lanes.append(lane)
        queue = next_queue
    
    return lanes
```

Each lane represents a set of tasks that must complete before the next lane starts.

### State Persistence

After each lane completes, persist the execution state:

```python
def save_dag_state(dag_state_file, dag_id, execution_id, lane_index, results):
    """
    Append results from completed lane to the DAG state file.
    Use for resumption if the orchestrator crashes.
    """
    import json
    from datetime import datetime
    
    state = {
        "dag_id": dag_id,
        "execution_id": execution_id,
        "completed_lane": lane_index,
        "results": results,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
    with open(dag_state_file, 'a') as f:
        f.write(json.dumps(state) + '\n')
```

Use `.claude/dag-state.json` (append-only JSONL format). On restart, read the last line to find the last completed lane and resume from there.

### Failure Handling

If a task in a lane fails:

1. **Log to dead letter queue:** Record the failed task, its input, and error
2. **Stop the DAG:** Do not proceed to the next lane
3. **Determine recovery action:**
   - Retry if transient error (timeout, rate limit)
   - Escalate if permanent error (validation failure, missing input)
   - Rollback if it's a saga (execute compensations in reverse order)

### Execution Loop

```python
async def execute_dag(dag_spec, execution_id):
    """Execute a DAG to completion or failure."""
    
    # Validate
    if has_cycle(dag_spec['tasks']):
        raise ValueError("DAG contains cycles")
    
    # Compute execution lanes
    lanes = get_execution_lanes(dag_spec['tasks'])
    
    # Initialize state
    dag_state = init_dag_state(dag_spec['dag_id'], execution_id)
    
    # Execute lane by lane
    for lane_index, lane_tasks in enumerate(lanes):
        try:
            # Run all tasks in the lane concurrently
            results = await asyncio.gather(*[
                run_agent_task(task, dag_state)
                for task in lane_tasks
            ])
            
            # Save state
            save_dag_state('.claude/dag-state.json', dag_spec['dag_id'], execution_id, lane_index, results)
            dag_state.update(results)
            
        except Exception as e:
            # Task failed
            log_dead_letter(dag_spec, execution_id, lane_index, e)
            raise
    
    return dag_state
```

## Example

**Order fulfillment DAG:**

```
Input:
{
  "dag_id": "order_fulfillment",
  "tasks": [
    {"task_id": "validate_order", "agent": "order_agent", "action": "validate", "dependencies": []},
    {"task_id": "check_inventory", "agent": "inventory_agent", "action": "check", "dependencies": ["validate_order"]},
    {"task_id": "verify_payment", "agent": "payment_agent", "action": "verify", "dependencies": ["validate_order"]},
    {"task_id": "reserve_items", "agent": "inventory_agent", "action": "reserve", "dependencies": ["check_inventory"]},
    {"task_id": "charge_card", "agent": "payment_agent", "action": "charge", "dependencies": ["verify_payment", "reserve_items"]},
    {"task_id": "send_email", "agent": "notification_agent", "action": "send_confirmation", "dependencies": ["charge_card"]}
  ]
}

Execution lanes (parallelization):
Lane 1: [validate_order]
Lane 2: [check_inventory, verify_payment]  ← Can run in parallel
Lane 3: [reserve_items]
Lane 4: [charge_card]
Lane 5: [send_email]

Latency:
Sequential: 6 steps × 5s = 30s
DAG:       5 lanes × 5s = 25s (25% faster due to parallelization)
```

---
