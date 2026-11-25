---
name: fabric-graph
description: Builds a step graph from plain Fabric programs. In-session graphs are ordinary code; resumable graphs are a durable actor that checkpoints each node in the mesh, schedules its next step, and parks human nodes on decisions. Use for multi-step flows that must survive restarts or wait for a person.
disable-model-invocation: true
---

# Fabric Graph

A graph is program code, not a framework. Pick the smallest form that fits:

- **In-session graph**: one Python `fabric_exec` program. Nodes are calls; edges are `if`, loops, bounded `asyncio.gather`, and budgets. Use it when the whole graph finishes in this turn.
- **Resumable graph**: a durable actor that runs one node per mailbox message, checkpoints each node with `mesh.put` CAS, and wakes itself for the next node. Use it when a node waits on a person or a schedule, or the run must survive Main and resident-host restarts.

Nodes that are reviewed, reusable steps can be saved programs: `await programs.run(ref=ref, input=data, requirePromoted=True)` runs one nested with the caller's capabilities.

## In-session graph

```python
import asyncio
target = π.target
types, tests = await asyncio.gather(
    pi.bash(command="bun run typecheck", settle=True),
    pi.bash(command="bunx vitest run " + target, settle=True),
)
if not types["ok"] or not tests["ok"]:
    return {"status": "failed", "node": "checks", "types": types["ok"], "tests": tests["ok"]}
review = await agents.run(task="Review the change to " + target + " for correctness. Reply APPROVE or a list of blockers.", name="graph review")
text = review.get("text") or ""
return {"status": "success" if review.get("status") == "completed" and text.startswith("APPROVE") else "partial", "review": text}
```

Pass the test target as `payloads.target`. A failed node returns its evidence; do not rerun passing nodes.

## Resumable graph

Seed the run once, then create a durable actor that owns it. The state record is the single source of truth: `runs/<run>/graph` holds `{node, status, results, decisionId?}` with its mesh version.

```python
run = π.run
key = "runs/" + run + "/graph"
await mesh.put(key=key, value={"node": "fetch", "status": "ready", "results": {}}, ifVersion=0)
instructions = "\n".join([
    "You own the resumable graph " + key + ". Nodes in order: fetch, test, approve, release.",
    "On every message, run exactly one fabric_exec program that:",
    "1. reads " + key + " with mesh.get and stops if status is done or failed;",
    "2. runs the current node only, writes its result and the next node with mesh.put(ifVersion=<the version you read>), and stops on a CAS conflict;",
    "3. for approve, raises tools.call(ref='decisions.raise', args={'title': ..., 'input': 'confirm'}) once, stores decisionId in the record, and waits with decisions.wait(id=..., timeoutMs=60000); while still open, schedules mesh.publish(topic=..., kind='graph.tick', afterMs=600000, key=...) and stops;",
    "4. after a successful node, wakes itself with agents.tell to its own id from mesh.self().",
    "Every node must be idempotent: before acting, check the recorded result; an interrupted spawn or shell run is indeterminate, so verify its effect before repeating it.",
])
actor = await agents.create(name="graph-" + run, runner="pi", residency="durable", topics=["graph." + run], instructions=instructions)
await agents.tell(id=actor["id"], message="Start graph " + key + ".")
return {"run": run, "key": key, "actor": actor["id"], "topic": "graph." + run}
```

Pass the run key as `payloads.run`. The actor's node program follows this shape:

```python
run = π.run
key = "runs/" + run + "/graph"
entry = await mesh.get(key=key)
if entry is None or entry["value"]["status"] in ("done", "failed"):
    return {"status": entry["value"]["status"] if entry else "missing"}
graph = entry["value"]
order = {"fetch": "test", "test": "approve", "approve": "release", "release": "done"}

async def advance(node, result, status):
    results = dict(graph["results"])
    results[graph["node"]] = result
    await mesh.put(key=key, value={"node": node, "status": status, "results": results}, ifVersion=entry["version"])
    if status == "ready":
        me = await mesh.self()
        await agents.tell(id=me["id"], message="Continue " + key + ".")

if graph["node"] == "approve":
    decision_id = graph.get("decisionId")
    if not decision_id:
        # `raise` is a Python keyword, so call the action by ref.
        raised = await tools.call(ref="decisions.raise", args={"title": "Release " + run + "?", "input": "confirm"})
        waiting = dict(graph)
        waiting["decisionId"] = raised["id"]
        await mesh.put(key=key, value=waiting, ifVersion=entry["version"])
        return {"status": "waiting", "decisionId": raised["id"]}
    decision = await decisions.wait(id=decision_id, timeoutMs=60000)
    if decision["status"] == "open":
        await mesh.publish(topic="graph." + run, kind="graph.tick", afterMs=600000, key="graph-" + run)
        return {"status": "waiting", "decisionId": decision_id}
    approved = decision["status"] == "answered" and (decision.get("answer") or {}).get("optionId") == "yes"
    await advance("release" if approved else "approve", decision["status"], "ready" if approved else "failed")
    return {"status": "approved" if approved else "rejected"}
result = await programs.run(ref="graph-" + graph["node"], input={"run": run}, requirePromoted=True)
nxt = order[graph["node"]]
await advance(nxt, result, "done" if nxt == "done" else "ready")
return {"status": "advanced", "from": graph["node"]}
```

Here each work node is a promoted saved program named `graph-<node>`; plain inline code works the same way.

## Rules

- One node per wake. The mesh record decides what runs next; mailbox text never does.
- Every write is `mesh.put` with the version you read. A conflict means another wake advanced the graph: stop.
- Human nodes park on `decisions.raise` (through `tools.call`) and `decisions.wait`, and recheck through a scheduled `mesh.publish` with a stable `key`, so a restart never raises a second decision.
- Nodes are idempotent. Interrupted spawns are indeterminate after a restart: verify effects (files, commits, tickets) before repeating a node, and record the evidence in `results`.
- Mesh events never run programs by themselves. An event may carry `data["fabricProgram"] = {"ref": ..., "input": ...}`; the subscribed actor decides to call `programs.run`.

## Completion criterion

Complete when the in-session program returns `success`, `partial`, or `failed` with per-node evidence, or when the resumable graph is seeded, its durable actor is created and told to start, and you report the run key, state key, actor id, and topic.
