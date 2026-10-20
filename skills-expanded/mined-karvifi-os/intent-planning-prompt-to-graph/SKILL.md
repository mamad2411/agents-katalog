---
name: intent-planning-prompt-to-graph
description: Design and implement the intent-service — LLM-driven graph generation from user prompts, intent classification, package suggestion, graph patch synthesis, missing input detection, cost estimation, and safety validation for the Software Synthesis OS.
triggers: [intent planner, prompt to graph, intent service, intent classification, graph patch synthesis, LLM graph generation, package suggestion, missing input detection, cost estimation, safety validation, intent-service]
---

# SKILL: Intent Planning (Prompt → Graph)

## Core Principle
The intent planner never executes. It produces a plan: a graph patch + surface plan + warnings + questions. The user approves before any graph mutation occurs. The planner is stateless — all context must be supplied as input.

---

## 1. Intent Service I/O Contract

```typescript
// intent-service/types.ts

export interface IntentRequest {
  prompt: string;
  workspaceId: string;
  userId: string;
  context: IntentContext;
}

export interface IntentContext {
  installedPackages: string[];       // ["engine.document", "engine.sheet", ...]
  currentGraph: GraphDocument | null;
  activeArtifacts: ArtifactRef[];
  userRoles: string[];
  previousIntents?: IntentSummary[];  // last 3 intents for continuity
}

export interface IntentResponse {
  classification: IntentClassification;
  graphPatches: GraphPatch[];
  packageSuggestions: PackageSuggestion[];
  surfacePlan?: SurfacePlanHint;
  missingInputs: MissingInput[];
  warnings: IntentWarning[];
  estimatedCost: CostEstimate;
  safetyFlags: SafetyFlag[];
  confidence: number;               // 0.0 - 1.0
  reasoning: string;                // brief explanation for UI
}

export interface IntentClassification {
  intent: 'build' | 'modify' | 'query' | 'execute' | 'install_package' | 'export' | 'ambiguous';
  subIntent?: string;
}

export interface MissingInput {
  field: string;
  description: string;
  required: boolean;
  suggestedType: string;
}

export interface SafetyFlag {
  severity: 'block' | 'warn';
  reason: string;
  affectedNodeIds?: string[];
}

export interface CostEstimate {
  llmTokensEstimate: number;
  executionUnitsEstimate: number;
  storageMbEstimate: number;
  usdEstimate: number;
}
```

---

## 2. Intent Classification

Classify the user's intent before attempting graph patch synthesis.

```typescript
// intent-service/classifier.ts

const CLASSIFICATION_PROMPT = `
You are an intent classifier for a graph-native software OS.
Given a user prompt and workspace context, classify the primary intent.

Intents:
- build: user wants to create a new graph/workflow from scratch
- modify: user wants to change an existing graph
- query: user is asking a question about the workspace or graph
- execute: user wants to trigger a run of an existing graph
- install_package: user wants to add a capability package
- export: user wants to export an artifact
- ambiguous: cannot determine intent

Respond with JSON only:
{"intent": "<intent>", "subIntent": "<optional detail>", "confidence": 0.0-1.0}
`.trim();

export async function classifyIntent(
  prompt: string,
  context: IntentContext,
  llm: LLMClient
): Promise<IntentClassification & { confidence: number }> {
  const response = await llm.complete({
    model: 'gpt-4o-mini',   // cheap classification model
    messages: [
      { role: 'system', content: CLASSIFICATION_PROMPT },
      {
        role: 'user',
        content: JSON.stringify({
          prompt,
          installedPackages: context.installedPackages,
          hasCurrentGraph: context.currentGraph !== null,
          nodeCount: context.currentGraph?.nodes.length ?? 0,
        }),
      },
    ],
    max_tokens: 100,
    response_format: { type: 'json_object' },
  });

  return JSON.parse(response.content);
}
```

---

## 3. Package Suggestion

```typescript
// intent-service/package-suggester.ts

const PACKAGE_SUGGESTION_PROMPT = `
You are a package advisor for a graph-native OS.
Given a user intent and installed packages, suggest any additional packages needed.

Available packages:
- engine.document: rich text document editor
- engine.sheet: spreadsheet engine
- engine.email: email composition and sending
- engine.media: video/audio/image generation
- engine.approval: multi-step approval workflows
- compound.proposal_studio: RFP and proposal workspace
- compound.client_portal: client-facing portal generator
- connector.gmail: Gmail integration
- connector.slack: Slack integration
- connector.stripe: Stripe billing integration

Respond with JSON only:
{"suggestions": [{"packageKey": "...", "reason": "...", "required": true|false}]}
`.trim();

export async function suggestPackages(
  intent: string,
  context: IntentContext,
  llm: LLMClient
): Promise<PackageSuggestion[]> {
  const notInstalled = getAvailablePackages().filter(
    p => !context.installedPackages.includes(p)
  );

  const response = await llm.complete({
    model: 'gpt-4o-mini',
    messages: [
      { role: 'system', content: PACKAGE_SUGGESTION_PROMPT },
      { role: 'user', content: JSON.stringify({ intent, notInstalled }) },
    ],
    max_tokens: 200,
    response_format: { type: 'json_object' },
  });

  return JSON.parse(response.content).suggestions ?? [];
}
```

---

## 4. Graph Patch Synthesis

The core of the planner — produce graph patches from user intent.

```typescript
// intent-service/patch-synthesizer.ts

const PATCH_SYNTHESIS_SYSTEM = `
You are a graph patch synthesizer for a software OS.
Given a user intent, current graph state, and installed packages,
produce a minimal set of graph patches to satisfy the intent.

Patch operations: add_node, remove_node, update_node, add_edge, remove_edge, update_config, set_mode

Node types: primitive, connector, engine, surface, policy, artifact, compound, agent

Rules:
1. Never remove nodes that have downstream edges without also patching those edges.
2. Use installed packages only — suggest missing packages separately.
3. Position new nodes relative to existing nodes (avoid overlaps; use x: existing_max_x + 250).
4. Always include surface hints on engine nodes.
5. Generate stable node IDs: snake_case, descriptive, no UUIDs.

Respond with JSON only:
{
  "patches": [...GraphPatch[]],
  "missingInputs": [...MissingInput[]],
  "reasoning": "brief explanation"
}
`.trim();

export async function synthesizePatches(
  prompt: string,
  classification: IntentClassification,
  context: IntentContext,
  llm: LLMClient
): Promise<{ patches: GraphPatch[]; missingInputs: MissingInput[]; reasoning: string }> {
  const currentGraphSummary = summarizeGraph(context.currentGraph);

  const response = await llm.complete({
    model: 'gpt-4o',
    messages: [
      { role: 'system', content: PATCH_SYNTHESIS_SYSTEM },
      {
        role: 'user',
        content: JSON.stringify({
          prompt,
          intent: classification.intent,
          installedPackages: context.installedPackages,
          currentGraphSummary,
          activeArtifacts: context.activeArtifacts.map(a => a.artifactType),
        }),
      },
    ],
    max_tokens: 2000,
    response_format: { type: 'json_object' },
    temperature: 0.2,   // low temp for deterministic patch generation
  });

  return JSON.parse(response.content);
}

function summarizeGraph(graph: GraphDocument | null): object {
  if (!graph) return { isEmpty: true };
  return {
    nodeCount: graph.nodes.length,
    edgeCount: graph.edges.length,
    nodeTypes: graph.nodes.map(n => ({ id: n.id, type: n.type, package: n.package })),
    maxX: Math.max(...graph.nodes.map(n => n.position.x), 0),
  };
}
```

---

## 5. Missing Input Detection

```typescript
// intent-service/missing-input-detector.ts

export function detectMissingInputs(
  patches: GraphPatch[],
  context: IntentContext
): MissingInput[] {
  const missing: MissingInput[] = [];

  for (const patch of patches) {
    if (patch.op !== 'add_node') continue;

    const { node } = patch;
    for (const [portName, portBinding] of Object.entries(node.inputs)) {
      if (!portBinding.binding && !portBinding.optional) {
        missing.push({
          field: `${node.id}.inputs.${portName}`,
          description: `Node "${node.id}" requires input "${portName}" (type: ${portBinding.type ?? 'unknown'})`,
          required: true,
          suggestedType: portBinding.type ?? 'unknown',
        });
      }
    }

    // Check if required packages are installed
    if (!context.installedPackages.includes(node.package)) {
      missing.push({
        field: `${node.id}.package`,
        description: `Package "${node.package}" is not installed`,
        required: true,
        suggestedType: 'package_install',
      });
    }
  }

  return missing;
}
```

---

## 6. Cost Estimation

```typescript
// intent-service/cost-estimator.ts

const COST_PER_GPT4O_TOKEN = 0.000005;  // $5 per 1M tokens input
const COST_PER_EXECUTION_UNIT = 0.0001;

export function estimateCost(
  patches: GraphPatch[],
  classification: IntentClassification
): CostEstimate {
  const addedNodes = patches.filter(p => p.op === 'add_node').length;
  const engineNodes = patches
    .filter(p => p.op === 'add_node')
    .filter(p => (p as any).node?.type === 'engine').length;

  // Estimate LLM tokens based on graph complexity
  const llmTokensEstimate = 500 + addedNodes * 200;

  // Estimate execution units (engine nodes cost more)
  const executionUnitsEstimate = addedNodes * 1 + engineNodes * 5;

  // Storage estimate (engine nodes produce artifacts)
  const storageMbEstimate = engineNodes * 2;

  return {
    llmTokensEstimate,
    executionUnitsEstimate,
    storageMbEstimate,
    usdEstimate:
      llmTokensEstimate * COST_PER_GPT4O_TOKEN +
      executionUnitsEstimate * COST_PER_EXECUTION_UNIT,
  };
}
```

---

## 7. Safety Validation

```typescript
// intent-service/safety-validator.ts

const DANGEROUS_DEFINITIONS = new Set([
  'email.send_bulk',
  'export.publish_external',
  'data.delete_all',
  'connector.execute_arbitrary_code',
]);

export function validateSafety(
  patches: GraphPatch[],
  context: IntentContext
): SafetyFlag[] {
  const flags: SafetyFlag[] = [];

  for (const patch of patches) {
    if (patch.op !== 'add_node') continue;
    const { node } = patch;

    // Block known dangerous operations for non-owners
    if (DANGEROUS_DEFINITIONS.has(node.definition) && !context.userRoles.includes('owner')) {
      flags.push({
        severity: 'block',
        reason: `Node "${node.definition}" requires owner role. Current roles: ${context.userRoles.join(', ')}`,
        affectedNodeIds: [node.id],
      });
    }

    // Warn on bulk data operations
    if (node.definition.includes('bulk') || node.definition.includes('delete')) {
      flags.push({
        severity: 'warn',
        reason: `Node "${node.id}" performs bulk or destructive operations. Review before running.`,
        affectedNodeIds: [node.id],
      });
    }
  }

  return flags;
}
```

---

## 8. Intent Service Orchestrator

```typescript
// intent-service/index.ts

export async function planIntent(
  request: IntentRequest,
  llm: LLMClient
): Promise<IntentResponse> {
  const { prompt, context } = request;

  // Step 1: Classify (cheap model)
  const classification = await classifyIntent(prompt, context, llm);

  // Step 2: If query intent, skip patch synthesis
  if (classification.intent === 'query') {
    return buildQueryResponse(prompt, context, llm);
  }

  // Step 3: Synthesize patches + suggest packages (parallel)
  const [patchResult, packageSuggestions] = await Promise.all([
    synthesizePatches(prompt, classification, context, llm),
    suggestPackages(prompt, context, llm),
  ]);

  const { patches, missingInputs: llmMissingInputs, reasoning } = patchResult;

  // Step 4: Detect missing inputs from patch analysis
  const missingInputs = [
    ...llmMissingInputs,
    ...detectMissingInputs(patches, context),
  ];

  // Step 5: Safety validation
  const safetyFlags = validateSafety(patches, context);

  // Step 6: Cost estimation
  const estimatedCost = estimateCost(patches, classification);

  // Step 7: Block if safety flags contain blockers
  const hasBlocker = safetyFlags.some(f => f.severity === 'block');

  return {
    classification,
    graphPatches: hasBlocker ? [] : patches,
    packageSuggestions,
    missingInputs,
    warnings: hasBlocker
      ? [{ level: 'error', message: 'Blocked by safety policy. Review safety flags.' }]
      : [],
    estimatedCost,
    safetyFlags,
    confidence: classification.confidence,
    reasoning,
  };
}
```

---

## 9. Checklist

Before shipping intent-service changes:
- [ ] Classification uses a cheap model (gpt-4o-mini) — never gpt-4o for classification alone
- [ ] Patch synthesis prompt enforces stable node IDs (no random UUIDs)
- [ ] All LLM calls set `max_tokens` — no unbounded completions
- [ ] Safety validator blocks dangerous definitions for non-owners before returning patches
- [ ] Missing input detection runs AFTER LLM synthesis (LLM misses some; code catches the rest)
- [ ] Cost estimates are shown in the UI before user confirms the plan
- [ ] Intent responses with `missingInputs` are returned to the user as questions — not errors
- [ ] No graph mutations happen inside intent-service — it only produces plans
- [ ] Rate limit intent endpoint: max 20 requests per user per minute
