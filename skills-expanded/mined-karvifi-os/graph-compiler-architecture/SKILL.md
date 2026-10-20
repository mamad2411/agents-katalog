---
name: graph-compiler-architecture
description: Design and implement the canonical graph compilation pipeline — schema validation, port type checking, edge resolution, patch merge, version diffing, and graph-to-execution planning for the Software Synthesis OS graph-service.
triggers: [graph compiler, graph schema, graph validation, patch merge, graph diff, graph version, port type, edge resolution, graph execution plan, graph-service]
---

# SKILL: Graph Compiler Architecture

## Core Principle
The graph is the single source of truth. Every mutation flows through the compiler. The compiler never executes — it validates, resolves, diffs, and plans. Execution is the runtime's job.

---

## 1. Graph JSON Contract (canonical)

Every graph instance must conform to this structure:

```typescript
interface GraphDocument {
  graphId: string;           // UUID
  version: number;           // monotonic integer
  name: string;
  mode: 'draft' | 'published' | 'archived';
  nodes: NodeDefinition[];
  edges: EdgeDefinition[];
  policies: PolicyRef[];
  createdAt: string;
  updatedAt: string;
}

interface NodeDefinition {
  id: string;                // stable, user-visible
  type: 'primitive' | 'connector' | 'engine' | 'surface' | 'policy' | 'artifact' | 'compound' | 'agent';
  package: string;           // e.g. "engine.document"
  definition: string;        // e.g. "document.workspace"
  position: { x: number; y: number };
  inputs: Record<string, PortBinding>;
  outputs: Record<string, PortSchema>;
  config: Record<string, unknown>;
  surface?: SurfaceHint;
  meta?: Record<string, unknown>;
}

interface EdgeDefinition {
  id: string;
  from: string;              // "nodeId.portName"
  to: string;                // "nodeId.portName"
  transform?: string;        // optional transform expression
}

interface PortBinding {
  binding?: string;          // "artifact:id" | "node:nodeId.output.portName" | "literal:value"
  type?: string;             // expected port type
  optional?: boolean;
}

interface PortSchema {
  type: string;              // "dataset" | "artifactRef" | "text" | "json" | "stream" | etc.
  nullable?: boolean;
}
```

---

## 2. Schema Validation Phase

**Run first, before any other compilation step.**

```typescript
// validation/schema-validator.ts
import Ajv from 'ajv';
import addFormats from 'ajv-formats';

const ajv = new Ajv({ allErrors: true });
addFormats(ajv);

export function validateGraphSchema(graph: unknown): ValidationResult {
  const validate = ajv.compile(GRAPH_JSON_SCHEMA); // import versioned JSON schema
  const valid = validate(graph);
  if (!valid) {
    return {
      valid: false,
      errors: (validate.errors ?? []).map(e => ({
        path: e.instancePath,
        message: e.message ?? 'unknown',
        keyword: e.keyword,
      })),
    };
  }
  return { valid: true, errors: [] };
}
```

**Rules enforced at schema level:**
- All `node.id` values must be unique within the graph
- All `edge.from` and `edge.to` must reference existing node IDs
- `node.package` must be a non-empty string (registry check happens later)
- `position` must be finite numbers
- `mode` must be one of the enum values

---

## 3. Port Type Checking Phase

Port type checking resolves whether an edge connection is type-safe.

```typescript
// compiler/port-type-checker.ts

export interface PortTypeRegistry {
  getOutputType(nodeId: string, portName: string, graph: GraphDocument): string | null;
  getInputType(nodeId: string, portName: string, graph: GraphDocument): string | null;
}

export function checkPortTypes(
  graph: GraphDocument,
  registry: PortTypeRegistry
): TypeCheckResult[] {
  const errors: TypeCheckResult[] = [];

  for (const edge of graph.edges) {
    const [fromNodeId, fromPort] = edge.from.split('.');
    const [toNodeId, toPort] = edge.to.split('.');

    const outputType = registry.getOutputType(fromNodeId, fromPort, graph);
    const inputType = registry.getInputType(toNodeId, toPort, graph);

    if (!outputType) {
      errors.push({ edgeId: edge.id, error: `Source port "${edge.from}" not found` });
      continue;
    }
    if (!inputType) {
      errors.push({ edgeId: edge.id, error: `Target port "${edge.to}" not found` });
      continue;
    }
    if (!isTypeCompatible(outputType, inputType)) {
      errors.push({
        edgeId: edge.id,
        error: `Type mismatch: "${outputType}" cannot connect to "${inputType}"`,
      });
    }
  }

  return errors;
}

// Type compatibility table
function isTypeCompatible(from: string, to: string): boolean {
  if (from === to) return true;
  const COMPATIBLE: Record<string, string[]> = {
    dataset: ['json', 'any'],
    artifactRef: ['any'],
    text: ['any'],
    json: ['any'],
    stream: ['stream'],
  };
  return COMPATIBLE[from]?.includes(to) ?? false;
}
```

---

## 4. Edge Resolution Phase

Resolve all bindings to their concrete sources before execution.

```typescript
// compiler/edge-resolver.ts

export type ResolvedBinding =
  | { kind: 'artifact'; artifactId: string }
  | { kind: 'node-output'; nodeId: string; portName: string }
  | { kind: 'literal'; value: unknown }
  | { kind: 'unresolved'; reason: string };

export function resolveEdges(graph: GraphDocument): Map<string, ResolvedBinding> {
  const bindings = new Map<string, ResolvedBinding>();

  for (const node of graph.nodes) {
    for (const [portName, portBinding] of Object.entries(node.inputs)) {
      const key = `${node.id}.${portName}`;
      const b = portBinding.binding;

      if (!b) {
        if (!portBinding.optional) {
          bindings.set(key, { kind: 'unresolved', reason: 'No binding and not optional' });
        }
        continue;
      }

      if (b.startsWith('artifact:')) {
        bindings.set(key, { kind: 'artifact', artifactId: b.replace('artifact:', '') });
      } else if (b.startsWith('node:')) {
        // "node:nodeId.output.portName"
        const ref = b.replace('node:', '');
        const parts = ref.split('.');
        bindings.set(key, { kind: 'node-output', nodeId: parts[0], portName: parts.slice(2).join('.') });
      } else if (b.startsWith('literal:')) {
        bindings.set(key, { kind: 'literal', value: b.replace('literal:', '') });
      } else {
        bindings.set(key, { kind: 'unresolved', reason: `Unknown binding prefix: ${b}` });
      }
    }
  }

  return bindings;
}
```

---

## 5. Patch Merge Algorithm

Patches represent incremental changes from the canvas or intent planner.

```typescript
// compiler/patch-merger.ts

export type GraphPatch =
  | { op: 'add_node'; node: NodeDefinition }
  | { op: 'remove_node'; nodeId: string }
  | { op: 'update_node'; nodeId: string; changes: Partial<NodeDefinition> }
  | { op: 'add_edge'; edge: EdgeDefinition }
  | { op: 'remove_edge'; edgeId: string }
  | { op: 'update_config'; nodeId: string; config: Record<string, unknown> }
  | { op: 'set_mode'; mode: GraphDocument['mode'] };

export function applyPatches(
  base: GraphDocument,
  patches: GraphPatch[]
): { graph: GraphDocument; conflicts: string[] } {
  const graph = structuredClone(base);
  const conflicts: string[] = [];

  for (const patch of patches) {
    switch (patch.op) {
      case 'add_node':
        if (graph.nodes.find(n => n.id === patch.node.id)) {
          conflicts.push(`Node "${patch.node.id}" already exists`);
        } else {
          graph.nodes.push(patch.node);
        }
        break;

      case 'remove_node': {
        const before = graph.nodes.length;
        graph.nodes = graph.nodes.filter(n => n.id !== patch.nodeId);
        // Cascade: remove dangling edges
        graph.edges = graph.edges.filter(
          e => !e.from.startsWith(patch.nodeId + '.') && !e.to.startsWith(patch.nodeId + '.')
        );
        if (graph.nodes.length === before) {
          conflicts.push(`Node "${patch.nodeId}" not found for removal`);
        }
        break;
      }

      case 'update_node': {
        const idx = graph.nodes.findIndex(n => n.id === patch.nodeId);
        if (idx === -1) {
          conflicts.push(`Node "${patch.nodeId}" not found for update`);
        } else {
          graph.nodes[idx] = { ...graph.nodes[idx], ...patch.changes, id: patch.nodeId };
        }
        break;
      }

      case 'add_edge':
        if (graph.edges.find(e => e.id === patch.edge.id)) {
          conflicts.push(`Edge "${patch.edge.id}" already exists`);
        } else {
          graph.edges.push(patch.edge);
        }
        break;

      case 'remove_edge':
        graph.edges = graph.edges.filter(e => e.id !== patch.edgeId);
        break;

      case 'update_config': {
        const node = graph.nodes.find(n => n.id === patch.nodeId);
        if (!node) {
          conflicts.push(`Node "${patch.nodeId}" not found for config update`);
        } else {
          node.config = { ...node.config, ...patch.config };
        }
        break;
      }

      case 'set_mode':
        graph.mode = patch.mode;
        break;
    }
  }

  graph.version += 1;
  graph.updatedAt = new Date().toISOString();
  return { graph, conflicts };
}
```

---

## 6. Version Diffing

Produce a structured diff between two graph versions for audit and undo.

```typescript
// compiler/graph-differ.ts

export interface GraphDiff {
  fromVersion: number;
  toVersion: number;
  addedNodes: string[];
  removedNodes: string[];
  updatedNodes: Array<{ id: string; changes: string[] }>;
  addedEdges: string[];
  removedEdges: string[];
  modeChanged?: { from: string; to: string };
}

export function diffGraphs(from: GraphDocument, to: GraphDocument): GraphDiff {
  const fromNodeMap = new Map(from.nodes.map(n => [n.id, n]));
  const toNodeMap = new Map(to.nodes.map(n => [n.id, n]));
  const fromEdgeSet = new Set(from.edges.map(e => e.id));
  const toEdgeSet = new Set(to.edges.map(e => e.id));

  const addedNodes = [...toNodeMap.keys()].filter(id => !fromNodeMap.has(id));
  const removedNodes = [...fromNodeMap.keys()].filter(id => !toNodeMap.has(id));
  const updatedNodes: Array<{ id: string; changes: string[] }> = [];

  for (const [id, toNode] of toNodeMap) {
    const fromNode = fromNodeMap.get(id);
    if (!fromNode) continue;
    const changes: string[] = [];
    if (JSON.stringify(fromNode.config) !== JSON.stringify(toNode.config)) changes.push('config');
    if (JSON.stringify(fromNode.inputs) !== JSON.stringify(toNode.inputs)) changes.push('inputs');
    if (JSON.stringify(fromNode.position) !== JSON.stringify(toNode.position)) changes.push('position');
    if (fromNode.definition !== toNode.definition) changes.push('definition');
    if (changes.length > 0) updatedNodes.push({ id, changes });
  }

  return {
    fromVersion: from.version,
    toVersion: to.version,
    addedNodes,
    removedNodes,
    updatedNodes,
    addedEdges: [...toEdgeSet].filter(id => !fromEdgeSet.has(id)),
    removedEdges: [...fromEdgeSet].filter(id => !toEdgeSet.has(id)),
    modeChanged: from.mode !== to.mode ? { from: from.mode, to: to.mode } : undefined,
  };
}
```

---

## 7. Graph-to-Execution Plan

Convert a validated graph into an ordered execution plan for the runtime-service.

```typescript
// compiler/execution-planner.ts

export interface ExecutionStep {
  stepIndex: number;
  nodeId: string;
  nodeType: NodeDefinition['type'];
  package: string;
  definition: string;
  resolvedInputs: Map<string, ResolvedBinding>;
  dependsOn: string[];         // nodeIds this step depends on
  parallelGroup: number;       // same group = can run in parallel
}

export function planExecution(
  graph: GraphDocument,
  resolvedBindings: Map<string, ResolvedBinding>
): ExecutionStep[] {
  // Build dependency graph (topological sort)
  const deps = buildDependencyMap(graph);
  const ordered = topologicalSort(graph.nodes.map(n => n.id), deps);

  // Assign parallel groups using level-based BFS
  const levels = assignLevels(ordered, deps);

  return ordered.map((nodeId, idx) => {
    const node = graph.nodes.find(n => n.id === nodeId)!;
    const nodeBindings = new Map<string, ResolvedBinding>();
    for (const portName of Object.keys(node.inputs)) {
      const key = `${nodeId}.${portName}`;
      const b = resolvedBindings.get(key);
      if (b) nodeBindings.set(portName, b);
    }

    return {
      stepIndex: idx,
      nodeId,
      nodeType: node.type,
      package: node.package,
      definition: node.definition,
      resolvedInputs: nodeBindings,
      dependsOn: [...(deps.get(nodeId) ?? [])],
      parallelGroup: levels.get(nodeId) ?? 0,
    };
  });
}

function buildDependencyMap(graph: GraphDocument): Map<string, Set<string>> {
  const deps = new Map<string, Set<string>>(graph.nodes.map(n => [n.id, new Set()]));
  for (const edge of graph.edges) {
    const toNodeId = edge.to.split('.')[0];
    const fromNodeId = edge.from.split('.')[0];
    deps.get(toNodeId)?.add(fromNodeId);
  }
  return deps;
}

function topologicalSort(nodeIds: string[], deps: Map<string, Set<string>>): string[] {
  const visited = new Set<string>();
  const result: string[] = [];

  function visit(id: string) {
    if (visited.has(id)) return;
    visited.add(id);
    for (const dep of deps.get(id) ?? []) visit(dep);
    result.push(id);
  }

  nodeIds.forEach(visit);
  return result;
}

function assignLevels(ordered: string[], deps: Map<string, Set<string>>): Map<string, number> {
  const levels = new Map<string, number>();
  for (const id of ordered) {
    const depLevels = [...(deps.get(id) ?? [])].map(d => levels.get(d) ?? 0);
    levels.set(id, depLevels.length > 0 ? Math.max(...depLevels) + 1 : 0);
  }
  return levels;
}
```

---

## 8. Compiler Pipeline (compose all phases)

```typescript
// compiler/index.ts

export async function compileGraph(
  raw: unknown,
  registry: PortTypeRegistry
): Promise<CompileResult> {
  // Phase 1: schema
  const schemaResult = validateGraphSchema(raw);
  if (!schemaResult.valid) return { ok: false, phase: 'schema', errors: schemaResult.errors };

  const graph = raw as GraphDocument;

  // Phase 2: port types
  const typeErrors = checkPortTypes(graph, registry);
  if (typeErrors.length > 0) return { ok: false, phase: 'type-check', errors: typeErrors };

  // Phase 3: edge resolution
  const bindings = resolveEdges(graph);
  const unresolvedBindings = [...bindings.entries()]
    .filter(([, b]) => b.kind === 'unresolved')
    .map(([key, b]) => ({ path: key, message: (b as any).reason }));
  if (unresolvedBindings.length > 0) return { ok: false, phase: 'edge-resolution', errors: unresolvedBindings };

  // Phase 4: execution plan
  const plan = planExecution(graph, bindings);

  return { ok: true, graph, bindings, plan };
}
```

---

## 9. Checklist

Before merging any graph-service change:
- [ ] Schema validator has a JSON schema file versioned in `/schemas/`
- [ ] Port type registry is loaded from installed package manifests, not hardcoded
- [ ] Topological sort detects cycles and returns a `CyclicDependencyError`
- [ ] Patches are idempotent — applying same patch twice returns one conflict, not corruption
- [ ] Graph diff is stored as `patch_json` in `graph_instance_versions` table
- [ ] Execution plan is never cached across graph version changes
- [ ] All compiler phases are unit-tested with invalid inputs
