---
name: canvas-intelligence
description: Design and implement the intelligent canvas layer for the Software Synthesis OS — next-node suggestions, auto-wiring compatible ports, natural language node search, graph explanation in plain English, broken pattern detection, automated repair suggestions, and cost-before-build estimation. This is what makes the canvas productive for non-expert users who do reach it.
triggers: [canvas intelligence, node suggestions, auto-wiring, next node, node search, explain graph, graph explanation, broken graph detection, graph repair, intelligent canvas, smart canvas, node autocomplete, port compatibility]
---

# SKILL: Canvas Intelligence

## Core Principle
The canvas is smart. It always knows what you were trying to build and suggests the next step. It prevents broken connections before they happen. It can describe any graph in plain English. It finds problems before the user discovers them at runtime.

---

## 1. Next-Node Suggestion Engine

When a user drops a node or completes an edge, the canvas immediately suggests valid next nodes.

```typescript
// shell-web/canvas/intelligence/NextNodeSuggester.ts

interface NextNodeSuggestion {
  nodeDefinitionKey: string;
  packageKey: string;
  label: string;
  reason: string;                 // human-readable why this is suggested
  confidence: number;             // 0.0 - 1.0
  estimatedCostUsd?: number;
  autoConnectPort?: string;       // which output port to auto-wire to
}

interface SuggestionContext {
  lastAddedNode: GraphNode;
  allNodes: GraphNode[];
  allEdges: GraphEdge[];
  installedPackages: string[];
  workspaceMode: 'guided' | 'visual' | 'canvas';
  recentPrompt?: string;
}

export class NextNodeSuggester {
  // Pattern-based suggestions (fast, no LLM call)
  suggestFromPatterns(ctx: SuggestionContext): NextNodeSuggestion[] {
    const suggestions: NextNodeSuggestion[] = [];
    const lastNode = ctx.lastAddedNode;

    // After any ingest/extract node → suggest a doc or sheet workspace
    if (lastNode.definition.includes('.ingest') || lastNode.definition.includes('.extract')) {
      if (ctx.installedPackages.includes('engine.document')) {
        suggestions.push({
          nodeDefinitionKey: 'document.workspace',
          packageKey: 'engine.document',
          label: 'Write a Document',
          reason: 'Common next step after extracting content',
          confidence: 0.85,
          autoConnectPort: 'seedContent',
        });
      }
    }

    // After doc workspace → suggest approval or export
    if (lastNode.definition.includes('document.workspace')) {
      suggestions.push({
        nodeDefinitionKey: 'approval.route',
        packageKey: 'engine.approval',
        label: 'Require Approval',
        reason: 'Documents typically need review before export',
        confidence: 0.80,
        autoConnectPort: 'artifactRef',
      });
      suggestions.push({
        nodeDefinitionKey: 'export.bundle',
        packageKey: 'pkg.export.center',
        label: 'Export Bundle',
        reason: 'Package document into a shareable bundle',
        confidence: 0.75,
        autoConnectPort: 'artifactRef',
      });
    }

    // After approval → suggest export or email
    if (lastNode.definition.includes('approval.route')) {
      suggestions.push({
        nodeDefinitionKey: 'email.send',
        packageKey: 'engine.email',
        label: 'Send Email',
        reason: 'Notify stakeholders after approval',
        confidence: 0.88,
        autoConnectPort: 'triggerInput',
      });
    }

    return suggestions.slice(0, 3);  // max 3 suggestions shown
  }

  // LLM-enhanced suggestions (async, for complex graphs)
  async suggestFromLLM(ctx: SuggestionContext): Promise<NextNodeSuggestion[]> {
    const prompt = buildSuggestionPrompt(ctx);
    const response = await openai.chat.completions.create({
      model: 'gpt-4o-mini',
      messages: [{ role: 'user', content: prompt }],
      response_format: { type: 'json_object' },
      max_tokens: 500,
    });

    return parseSuggestions(response.choices[0].message.content ?? '{}');
  }
}

// Debounced suggestion hook for canvas
export function useNextNodeSuggestions(lastAddedNodeId: string | null) {
  const [suggestions, setSuggestions] = useState<NextNodeSuggestion[]>([]);
  const { graph, installedPackages } = useGraphStore();
  const suggester = useRef(new NextNodeSuggester());

  useEffect(() => {
    if (!lastAddedNodeId) return;
    const lastNode = graph.nodes.find(n => n.id === lastAddedNodeId);
    if (!lastNode) return;

    // Fast pattern suggestions immediately
    const patternSuggestions = suggester.current.suggestFromPatterns({
      lastAddedNode: lastNode,
      allNodes: graph.nodes,
      allEdges: graph.edges,
      installedPackages,
      workspaceMode: 'canvas',
    });
    setSuggestions(patternSuggestions);

    // LLM suggestions after short debounce (only for complex graphs)
    if (graph.nodes.length > 3) {
      const timer = setTimeout(async () => {
        const llmSuggestions = await suggester.current.suggestFromLLM({
          lastAddedNode: lastNode,
          allNodes: graph.nodes,
          allEdges: graph.edges,
          installedPackages,
          workspaceMode: 'canvas',
        });
        setSuggestions(prev => mergeSuggestions(prev, llmSuggestions));
      }, 600);
      return () => clearTimeout(timer);
    }
  }, [lastAddedNodeId]);

  return suggestions;
}
```

---

## 2. Port Compatibility Guard (Auto-wiring + Rejection)

The canvas must never allow connecting incompatible ports. It must suggest auto-wiring when ports are compatible.

```typescript
// shell-web/canvas/intelligence/PortCompatibilityGuard.ts

// Port type compatibility matrix
const PORT_COMPATIBILITY: Record<string, string[]> = {
  'text':        ['text', 'string', 'any'],
  'dataset':     ['dataset', 'json', 'any'],
  'artifactRef': ['artifactRef', 'any'],
  'boolean':     ['boolean', 'any'],
  'number':      ['number', 'integer', 'float', 'any'],
  'email':       ['email', 'text', 'any'],
  'fileRef':     ['fileRef', 'blobRef', 'any'],
  'array':       ['array', 'any'],
  'json':        ['json', 'dataset', 'any'],
  'any':         ['text', 'dataset', 'artifactRef', 'boolean', 'number', 'email', 'fileRef', 'array', 'json', 'any'],
};

export function arePortsCompatible(
  sourcePortType: string,
  targetPortType: string,
): boolean {
  const compatible = PORT_COMPATIBILITY[sourcePortType] ?? ['any'];
  return compatible.includes(targetPortType);
}

// xyflow connection validator — called before any edge is created
export function validateConnection(
  connection: Connection,
  nodes: Node[],
  nodeDefinitions: Map<string, NodeDefinition>,
): ConnectionValidation {
  const sourceNode = nodes.find(n => n.id === connection.source);
  const targetNode = nodes.find(n => n.id === connection.target);
  if (!sourceNode || !targetNode) return { valid: false, reason: 'Node not found' };

  const sourceDef = nodeDefinitions.get(sourceNode.data.definitionKey);
  const targetDef = nodeDefinitions.get(targetNode.data.definitionKey);
  if (!sourceDef || !targetDef) return { valid: true };  // allow if defs not loaded

  const sourcePortType = sourceDef.outputSchema?.properties?.[connection.sourceHandle ?? '']?.type;
  const targetPortType = targetDef.inputSchema?.properties?.[connection.targetHandle ?? '']?.type;

  if (!sourcePortType || !targetPortType) return { valid: true };

  const compatible = arePortsCompatible(sourcePortType, targetPortType);
  return {
    valid: compatible,
    reason: compatible ? undefined : `Cannot connect ${sourcePortType} → ${targetPortType}. Types are incompatible.`,
    suggestedTransform: compatible ? undefined : suggestTransformNode(sourcePortType, targetPortType),
  };
}

// If types are incompatible, suggest a transform node that bridges them
function suggestTransformNode(fromType: string, toType: string): string | undefined {
  const BRIDGES: Record<string, Record<string, string>> = {
    'dataset': { 'text': 'transform.dataset_to_text', 'email': 'transform.dataset_to_email_body' },
    'text': { 'dataset': 'transform.text_to_json', 'email': 'transform.text_to_email_body' },
    'fileRef': { 'text': 'transform.extract_text_from_file', 'dataset': 'transform.parse_file_to_dataset' },
  };
  return BRIDGES[fromType]?.[toType];
}
```

---

## 3. Natural Language Node Search

```typescript
// shell-web/canvas/intelligence/NodeSearch.ts

interface NodeSearchResult {
  nodeDefinitionKey: string;
  packageKey: string;
  label: string;
  description: string;
  score: number;      // relevance score
  tags: string[];
}

export class NodeSearchEngine {
  private nodeIndex: Map<string, IndexedNode> = new Map();

  // Build search index from installed node definitions
  buildIndex(packages: InstalledPackage[]): void {
    for (const pkg of packages) {
      for (const nodeDef of pkg.nodes) {
        this.nodeIndex.set(nodeDef.key, {
          key: nodeDef.key,
          packageKey: pkg.manifest.packageKey,
          label: nodeDef.ui?.label ?? nodeDef.key,
          description: nodeDef.ui?.description ?? '',
          tags: nodeDef.ui?.tags ?? [],
          searchText: [
            nodeDef.key,
            nodeDef.ui?.label,
            nodeDef.ui?.description,
            ...(nodeDef.ui?.tags ?? []),
          ].filter(Boolean).join(' ').toLowerCase(),
        });
      }
    }
  }

  // Text search — fast, no LLM
  searchText(query: string): NodeSearchResult[] {
    const q = query.toLowerCase();
    const results: NodeSearchResult[] = [];

    for (const node of this.nodeIndex.values()) {
      if (node.searchText.includes(q)) {
        results.push({
          nodeDefinitionKey: node.key,
          packageKey: node.packageKey,
          label: node.label,
          description: node.description,
          tags: node.tags,
          score: node.searchText.indexOf(q) === 0 ? 1.0 : 0.7,  // exact prefix = higher score
        });
      }
    }

    return results.sort((a, b) => b.score - a.score).slice(0, 10);
  }

  // Semantic search — for vague queries ("something that sends messages")
  async searchSemantic(query: string): Promise<NodeSearchResult[]> {
    const allDescriptions = Array.from(this.nodeIndex.values())
      .map(n => `${n.key}: ${n.label} — ${n.description}`);

    const response = await openai.chat.completions.create({
      model: 'gpt-4o-mini',
      messages: [{
        role: 'user',
        content: `Find the most relevant nodes for this query: "${query}"\n\nAvailable nodes:\n${allDescriptions.join('\n')}\n\nReturn top 5 node keys as JSON array.`,
      }],
      max_tokens: 200,
    });

    const keys: string[] = JSON.parse(response.choices[0].message.content ?? '[]');
    return keys
      .map(key => this.nodeIndex.get(key))
      .filter((n): n is IndexedNode => !!n)
      .map(n => ({ ...n, nodeDefinitionKey: n.key, score: 0.9 }));
  }
}
```

---

## 4. "Explain This Graph" — Plain English AI

```typescript
// intent-service/explainer.ts

export async function explainGraph(
  graph: CanonicalGraph,
  audienceLevel: 'technical' | 'business' | 'simple',
): Promise<GraphExplanation> {
  const nodeDescriptions = graph.nodes.map(n => 
    `${n.id} (${n.definition}): inputs [${Object.keys(n.inputs).join(', ')}] → outputs [${Object.keys(n.outputs).join(', ')}]`
  ).join('\n');

  const edgeDescriptions = graph.edges.map(e => 
    `${e.from} → ${e.to}`
  ).join('\n');

  const audiencePrompts = {
    technical: 'Use technical terms. Include data types, port names, and node definitions.',
    business: 'Use business language. Focus on workflow steps and business outcomes.',
    simple: 'Use simple everyday language. Assume the reader knows nothing about software.',
  };

  const response = await openai.chat.completions.create({
    model: 'gpt-4o',
    messages: [{
      role: 'user',
      content: `Explain this graph as a step-by-step workflow.\n\nAudience: ${audiencePrompts[audienceLevel]}\n\nNodes:\n${nodeDescriptions}\n\nConnections:\n${edgeDescriptions}\n\nReturn JSON: { "summary": "one sentence", "steps": ["step 1", "step 2", ...], "outcome": "what the user gets" }`,
    }],
    response_format: { type: 'json_object' },
    max_tokens: 600,
  });

  return JSON.parse(response.choices[0].message.content ?? '{}');
}
```

---

## 5. Graph Health Inspector — Broken Pattern Detection

```typescript
// graph-service/health/GraphHealthInspector.ts

interface GraphHealthIssue {
  severity: 'error' | 'warning' | 'suggestion';
  nodeId?: string;
  edgeId?: string;
  code: string;
  message: string;         // plain English
  autoFixAvailable: boolean;
  autoFix?: GraphPatch[];  // patches to fix the issue
}

export class GraphHealthInspector {
  inspect(graph: CanonicalGraph): GraphHealthIssue[] {
    const issues: GraphHealthIssue[] = [];

    // 1. Orphaned nodes — nodes with no edges
    for (const node of graph.nodes) {
      const hasConnections = graph.edges.some(e => 
        e.from.startsWith(node.id) || e.to.startsWith(node.id)
      );
      if (!hasConnections && graph.nodes.length > 1) {
        issues.push({
          severity: 'warning',
          nodeId: node.id,
          code: 'ORPHANED_NODE',
          message: `"${node.id}" is not connected to anything. It won't run.`,
          autoFixAvailable: false,
        });
      }
    }

    // 2. Unbound required inputs
    for (const node of graph.nodes) {
      const def = this.getDefinition(node.definition);
      if (!def) continue;
      const requiredInputs = def.requiredInputs ?? [];
      for (const input of requiredInputs) {
        const bound = node.inputs[input];
        const connectedByEdge = graph.edges.some(e => e.to === `${node.id}.${input}`);
        if (!bound && !connectedByEdge) {
          issues.push({
            severity: 'error',
            nodeId: node.id,
            code: 'UNBOUND_REQUIRED_INPUT',
            message: `"${node.id}" is missing required input "${input}". This will fail when run.`,
            autoFixAvailable: false,
          });
        }
      }
    }

    // 3. Cycles — circular dependencies
    if (this.detectCycle(graph)) {
      issues.push({
        severity: 'error',
        code: 'CIRCULAR_DEPENDENCY',
        message: 'This graph has a loop. Execution will never complete.',
        autoFixAvailable: false,
      });
    }

    // 4. Missing approval before dangerous action
    for (const node of graph.nodes) {
      const isDangerous = DANGEROUS_NODE_DEFINITIONS.has(node.definition);
      if (isDangerous) {
        const approvalUpstream = this.hasApprovalUpstream(node.id, graph);
        if (!approvalUpstream) {
          issues.push({
            severity: 'warning',
            nodeId: node.id,
            code: 'DANGEROUS_WITHOUT_APPROVAL',
            message: `"${node.id}" (${node.definition}) performs a dangerous action without an approval gate.`,
            autoFixAvailable: true,
            autoFix: [{
              op: 'add_node',
              node: { id: `approval_before_${node.id}`, definition: 'approval.route', inputs: {}, outputs: {}, config: {} },
            }],
          });
        }
      }
    }

    // 5. Connector nodes with no credential binding
    for (const node of graph.nodes) {
      if (node.type === 'connector' && !node.config.credentialBindingId) {
        issues.push({
          severity: 'error',
          nodeId: node.id,
          code: 'CONNECTOR_NO_CREDENTIALS',
          message: `"${node.id}" needs a connected account to run. Open the node to connect your account.`,
          autoFixAvailable: false,
        });
      }
    }

    return issues;
  }

  private detectCycle(graph: CanonicalGraph): boolean {
    const visited = new Set<string>();
    const inStack = new Set<string>();

    const dfs = (nodeId: string): boolean => {
      visited.add(nodeId);
      inStack.add(nodeId);
      const outgoing = graph.edges
        .filter(e => e.from.startsWith(nodeId))
        .map(e => e.to.split('.')[0]);
      for (const next of outgoing) {
        if (!visited.has(next) && dfs(next)) return true;
        if (inStack.has(next)) return true;
      }
      inStack.delete(nodeId);
      return false;
    };

    for (const node of graph.nodes) {
      if (!visited.has(node.id) && dfs(node.id)) return true;
    }
    return false;
  }
}

const DANGEROUS_NODE_DEFINITIONS = new Set([
  'email.send',
  'connector.stripe.charge',
  'connector.twilio.send_sms',
  'export.publish_external',
  'artifact.delete',
  'graph.delete',
]);
```

---

## 6. Cost-Before-Build Estimator

The canvas shows cost estimate before any run is triggered.

```typescript
// shell-web/canvas/intelligence/CostEstimator.ts

interface CanvasCostEstimate {
  estimatedUsd: number;
  breakdown: CostLineItem[];
  confidence: 'high' | 'medium' | 'low';
  warning?: string;  // e.g. "Includes media render — cost varies by duration"
}

export function estimateGraphRunCost(
  graph: CanonicalGraph,
  installedPackages: InstalledPackage[],
): CanvasCostEstimate {
  const breakdown: CostLineItem[] = [];

  for (const node of graph.nodes) {
    const cost = estimateNodeCost(node, installedPackages);
    if (cost) breakdown.push(cost);
  }

  const total = breakdown.reduce((sum, item) => sum + item.estimatedUsd, 0);
  return {
    estimatedUsd: total,
    breakdown,
    confidence: breakdown.every(b => b.confidence === 'high') ? 'high' : 'medium',
    warning: breakdown.some(b => b.variableCost) ? 'Some costs vary based on content size.' : undefined,
  };
}
```

---

## 7. Checklist

- [ ] Next-node suggestions appear within 100ms of dropping a node (pattern-based)
- [ ] LLM suggestions load asynchronously without blocking canvas interaction
- [ ] Incompatible port connections are rejected before the edge is created
- [ ] Transform node is suggested when types are bridgeable
- [ ] Node search returns results on every keypress (text) + semantic fallback
- [ ] "Explain this graph" is accessible from toolbar and returns in under 3 seconds
- [ ] Graph health inspector runs on every graph save and surfaces issues in the UI
- [ ] Auto-fix patches are offered for fixable issues
- [ ] Cost estimate is visible in canvas toolbar before any run
- [ ] All intelligence features degrade gracefully if LLM service is unavailable
