---
name: adapter-contract-patterns
description: Design and implement the connector-broker subsystem adapter layer — wrapping n8n, Dify, and ComfyUI with canonical adapter interfaces, capability introspection, job queueing, result mapping, and cost attribution per adapter for the Software Synthesis OS.
triggers: [adapter contract, connector broker, n8n adapter, Dify adapter, ComfyUI adapter, subsystem adapter, capability introspection, job queueing, result mapping, cost attribution, connector-broker, adapter interface]
---

# SKILL: Adapter Contract Patterns

## Core Principle
Subsystems (n8n, Dify, ComfyUI) are wrapped behind the `SubsystemAdapter` interface. The OS never calls n8n's API directly from graph nodes. The connector-broker translates canonical job requests into subsystem-specific calls and maps results back. Adapters are replaceable without changing the graph contract.

---

## 1. Universal Adapter Interface

```typescript
// connector-broker/adapter-interface.ts

export interface SubsystemAdapter {
  /** Unique identifier for this adapter */
  readonly adapterId: string;

  /** Human-readable name */
  readonly adapterName: string;

  /** Subsystem kind */
  readonly kind: AdapterKind;

  /** Introspect what this adapter can do */
  introspect(): Promise<AdapterCapabilities>;

  /** Submit a job to the subsystem */
  submitJob(job: AdapterJob): Promise<AdapterJobHandle>;

  /** Poll for job status */
  getJobStatus(handle: AdapterJobHandle): Promise<AdapterJobStatus>;

  /** Stream results incrementally (optional) */
  streamResults?(handle: AdapterJobHandle): AsyncIterable<AdapterResultChunk>;

  /** Cancel a running job */
  cancelJob(handle: AdapterJobHandle): Promise<void>;

  /** Health check */
  healthCheck(): Promise<AdapterHealth>;
}

export type AdapterKind = 'workflow' | 'ai_workflow' | 'media_generation' | 'durable_task';

export interface AdapterCapabilities {
  supportedJobTypes: string[];
  supportedInputTypes: string[];
  supportedOutputTypes: string[];
  maxConcurrentJobs: number;
  supportsStreaming: boolean;
  supportsWebhooks: boolean;
  estimatedCostUnit?: string;
}

export interface AdapterJob {
  jobId: string;                      // OS-side job ID
  jobType: string;                    // e.g. "run_workflow", "run_chain", "generate_video"
  workspaceId: string;
  runId: string;
  nodeId: string;
  inputs: Record<string, unknown>;
  config: Record<string, unknown>;
  callbackUrl?: string;               // webhook URL for async completion
  timeoutSeconds?: number;
}

export interface AdapterJobHandle {
  adapterId: string;
  externalJobId: string;              // subsystem's own job ID
  submittedAt: string;
}

export interface AdapterJobStatus {
  externalJobId: string;
  status: 'queued' | 'running' | 'completed' | 'failed' | 'cancelled';
  progress?: number;                  // 0-100
  outputs?: Record<string, unknown>;
  error?: string;
  startedAt?: string;
  completedAt?: string;
  costUnits?: number;
}

export interface AdapterHealth {
  healthy: boolean;
  latencyMs?: number;
  message?: string;
}
```

---

## 2. n8n Workflow Adapter

```typescript
// connector-broker/adapters/n8n-adapter.ts

export class N8nAdapter implements SubsystemAdapter {
  readonly adapterId = 'n8n';
  readonly adapterName = 'n8n Workflow Engine';
  readonly kind = 'workflow' as const;

  private baseUrl: string;
  private apiKey: string;

  constructor(config: { baseUrl: string; apiKey: string }) {
    this.baseUrl = config.baseUrl;
    this.apiKey = config.apiKey;
  }

  async introspect(): Promise<AdapterCapabilities> {
    const workflows = await this.request<{ data: unknown[] }>('GET', '/workflows');
    return {
      supportedJobTypes: ['run_workflow'],
      supportedInputTypes: ['json', 'text', 'dataset'],
      supportedOutputTypes: ['json', 'text'],
      maxConcurrentJobs: 50,
      supportsStreaming: false,
      supportsWebhooks: true,
      estimatedCostUnit: 'workflow_execution',
    };
  }

  async submitJob(job: AdapterJob): Promise<AdapterJobHandle> {
    // n8n: trigger webhook-based workflow execution
    const workflowId = job.config['workflowId'];
    if (!workflowId) throw new Error('n8n adapter: config.workflowId is required');

    const response = await this.request<{ executionId: string }>(
      'POST',
      `/workflows/${workflowId}/execute`,
      {
        data: job.inputs,
        metadata: { osRunId: job.runId, osNodeId: job.nodeId },
      }
    );

    return {
      adapterId: this.adapterId,
      externalJobId: response.executionId,
      submittedAt: new Date().toISOString(),
    };
  }

  async getJobStatus(handle: AdapterJobHandle): Promise<AdapterJobStatus> {
    const execution = await this.request<N8nExecution>(
      'GET',
      `/executions/${handle.externalJobId}`
    );

    return {
      externalJobId: handle.externalJobId,
      status: mapN8nStatus(execution.status),
      outputs: execution.data?.resultData?.runData
        ? mapN8nOutputs(execution.data.resultData.runData)
        : undefined,
      error: execution.data?.resultData?.error?.message,
      startedAt: execution.startedAt,
      completedAt: execution.stoppedAt,
    };
  }

  async cancelJob(handle: AdapterJobHandle): Promise<void> {
    await this.request('DELETE', `/executions/${handle.externalJobId}`);
  }

  async healthCheck(): Promise<AdapterHealth> {
    const start = Date.now();
    try {
      await this.request('GET', '/healthz');
      return { healthy: true, latencyMs: Date.now() - start };
    } catch (err) {
      return { healthy: false, message: String(err) };
    }
  }

  private async request<T>(method: string, path: string, body?: unknown): Promise<T> {
    const res = await fetch(`${this.baseUrl}${path}`, {
      method,
      headers: {
        'Content-Type': 'application/json',
        'X-N8N-API-KEY': this.apiKey,
      },
      body: body ? JSON.stringify(body) : undefined,
    });

    if (!res.ok) {
      throw new Error(`n8n API error ${res.status}: ${await res.text()}`);
    }

    return res.json() as Promise<T>;
  }
}

function mapN8nStatus(status: string): AdapterJobStatus['status'] {
  const map: Record<string, AdapterJobStatus['status']> = {
    waiting: 'queued',
    running: 'running',
    success: 'completed',
    error: 'failed',
    canceled: 'cancelled',
  };
  return map[status] ?? 'running';
}
```

---

## 3. Dify AI Workflow Adapter

```typescript
// connector-broker/adapters/dify-adapter.ts

export class DifyAdapter implements SubsystemAdapter {
  readonly adapterId = 'dify';
  readonly adapterName = 'Dify AI Workflow';
  readonly kind = 'ai_workflow' as const;

  constructor(private config: { baseUrl: string; apiKey: string }) {}

  async introspect(): Promise<AdapterCapabilities> {
    return {
      supportedJobTypes: ['run_workflow', 'run_chat', 'run_completion'],
      supportedInputTypes: ['text', 'json', 'files'],
      supportedOutputTypes: ['text', 'json', 'stream'],
      maxConcurrentJobs: 20,
      supportsStreaming: true,
      supportsWebhooks: false,
      estimatedCostUnit: 'llm_token',
    };
  }

  async submitJob(job: AdapterJob): Promise<AdapterJobHandle> {
    const endpoint = job.jobType === 'run_workflow'
      ? '/workflows/run'
      : '/completion-messages';

    const response = await this.request<{ workflow_run_id?: string; task_id?: string }>(
      'POST',
      endpoint,
      {
        inputs: job.inputs,
        response_mode: 'blocking',  // use 'streaming' for stream jobs
        user: job.workspaceId,
      }
    );

    const externalId = response.workflow_run_id ?? response.task_id;
    if (!externalId) throw new Error('Dify did not return a job ID');

    return {
      adapterId: this.adapterId,
      externalJobId: externalId,
      submittedAt: new Date().toISOString(),
    };
  }

  async getJobStatus(handle: AdapterJobHandle): Promise<AdapterJobStatus> {
    const run = await this.request<DifyWorkflowRun>(
      'GET',
      `/workflows/run/${handle.externalJobId}`
    );

    return {
      externalJobId: handle.externalJobId,
      status: mapDifyStatus(run.status),
      outputs: run.outputs,
      error: run.error,
      startedAt: run.created_at,
      completedAt: run.finished_at,
      costUnits: run.total_tokens,
    };
  }

  async *streamResults(handle: AdapterJobHandle): AsyncIterable<AdapterResultChunk> {
    // Dify streaming via SSE
    const res = await fetch(`${this.config.baseUrl}/workflows/run/${handle.externalJobId}/stream`, {
      headers: { Authorization: `Bearer ${this.config.apiKey}` },
    });

    for await (const line of parseSSE(res.body!)) {
      if (line.event === 'workflow_finished') {
        yield { done: true, outputs: line.data?.outputs };
      } else if (line.event === 'text_chunk') {
        yield { done: false, chunk: line.data?.text };
      }
    }
  }

  async cancelJob(): Promise<void> {
    // Dify does not support cancellation in blocking mode
  }

  async healthCheck(): Promise<AdapterHealth> {
    const start = Date.now();
    try {
      await this.request('GET', '/info');
      return { healthy: true, latencyMs: Date.now() - start };
    } catch (err) {
      return { healthy: false, message: String(err) };
    }
  }

  private async request<T>(method: string, path: string, body?: unknown): Promise<T> {
    const res = await fetch(`${this.config.baseUrl}${path}`, {
      method,
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${this.config.apiKey}`,
      },
      body: body ? JSON.stringify(body) : undefined,
    });
    if (!res.ok) throw new Error(`Dify API error ${res.status}: ${await res.text()}`);
    return res.json() as Promise<T>;
  }
}

function mapDifyStatus(status: string): AdapterJobStatus['status'] {
  const map: Record<string, AdapterJobStatus['status']> = {
    running: 'running',
    succeeded: 'completed',
    failed: 'failed',
    stopped: 'cancelled',
  };
  return map[status] ?? 'running';
}
```

---

## 4. ComfyUI Media Generation Adapter

```typescript
// connector-broker/adapters/comfyui-adapter.ts

export class ComfyUIAdapter implements SubsystemAdapter {
  readonly adapterId = 'comfyui';
  readonly adapterName = 'ComfyUI Media Generation';
  readonly kind = 'media_generation' as const;

  constructor(private config: { baseUrl: string; clientId: string }) {}

  async introspect(): Promise<AdapterCapabilities> {
    const objectInfo = await this.request<Record<string, unknown>>('GET', '/object_info');
    return {
      supportedJobTypes: ['generate_image', 'generate_video', 'run_workflow'],
      supportedInputTypes: ['json', 'files', 'text'],
      supportedOutputTypes: ['image', 'video', 'audio'],
      maxConcurrentJobs: 2,  // GPU-bound
      supportsStreaming: false,
      supportsWebhooks: false,
      estimatedCostUnit: 'gpu_second',
    };
  }

  async submitJob(job: AdapterJob): Promise<AdapterJobHandle> {
    const workflow = job.config['workflow'];  // ComfyUI workflow JSON
    if (!workflow) throw new Error('ComfyUI adapter: config.workflow is required');

    // Inject dynamic inputs into workflow nodes
    const patchedWorkflow = injectInputsIntoWorkflow(workflow, job.inputs);

    const response = await this.request<{ prompt_id: string }>(
      'POST',
      '/prompt',
      { prompt: patchedWorkflow, client_id: this.config.clientId }
    );

    return {
      adapterId: this.adapterId,
      externalJobId: response.prompt_id,
      submittedAt: new Date().toISOString(),
    };
  }

  async getJobStatus(handle: AdapterJobHandle): Promise<AdapterJobStatus> {
    const history = await this.request<Record<string, ComfyUIHistoryEntry>>(
      'GET',
      `/history/${handle.externalJobId}`
    );

    const entry = history[handle.externalJobId];
    if (!entry) return { externalJobId: handle.externalJobId, status: 'queued' };

    const outputs = entry.status.completed
      ? await this.collectOutputs(entry.outputs)
      : undefined;

    return {
      externalJobId: handle.externalJobId,
      status: entry.status.completed ? 'completed' : 'running',
      outputs,
    };
  }

  private async collectOutputs(
    outputs: Record<string, ComfyUIOutput>
  ): Promise<Record<string, string>> {
    // Download generated images/videos and upload to blob storage
    const result: Record<string, string> = {};
    for (const [nodeId, output] of Object.entries(outputs)) {
      if (output.images) {
        for (const img of output.images) {
          const imageData = await this.request<Blob>(
            'GET',
            `/view?filename=${img.filename}&subfolder=${img.subfolder}&type=${img.type}`
          );
          // Return filename as key — upload to blob storage separately
          result[`${nodeId}_${img.filename}`] = img.filename;
        }
      }
    }
    return result;
  }

  async cancelJob(handle: AdapterJobHandle): Promise<void> {
    await this.request('POST', '/interrupt');
  }

  async healthCheck(): Promise<AdapterHealth> {
    const start = Date.now();
    try {
      await this.request('GET', '/system_stats');
      return { healthy: true, latencyMs: Date.now() - start };
    } catch (err) {
      return { healthy: false, message: String(err) };
    }
  }

  private async request<T>(method: string, path: string, body?: unknown): Promise<T> {
    const res = await fetch(`${this.config.baseUrl}${path}`, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: body ? JSON.stringify(body) : undefined,
    });
    if (!res.ok) throw new Error(`ComfyUI API error ${res.status}`);
    return res.json() as Promise<T>;
  }
}
```

---

## 5. Job Queue and Cost Attribution

```typescript
// connector-broker/job-queue.ts

export class AdapterJobQueue {
  private adapters = new Map<string, SubsystemAdapter>();

  register(adapter: SubsystemAdapter) {
    this.adapters.set(adapter.adapterId, adapter);
  }

  async dispatch(
    adapterId: string,
    job: AdapterJob,
    db: DatabaseClient
  ): Promise<AdapterJobHandle> {
    const adapter = this.adapters.get(adapterId);
    if (!adapter) throw new Error(`Adapter not found: "${adapterId}"`);

    // Record job in DB before dispatching
    await db.execute(
      `INSERT INTO adapter_jobs (job_id, run_id, node_id, adapter_id, external_job_id, status, submitted_at)
       VALUES ($1, $2, $3, $4, '', 'queued', now())`,
      [job.jobId, job.runId, job.nodeId, adapterId]
    );

    const handle = await adapter.submitJob(job);

    // Update with external ID
    await db.execute(
      `UPDATE adapter_jobs SET external_job_id = $1, status = 'running' WHERE job_id = $2`,
      [handle.externalJobId, job.jobId]
    );

    return handle;
  }

  async poll(
    handle: AdapterJobHandle,
    jobId: string,
    db: DatabaseClient
  ): Promise<AdapterJobStatus> {
    const adapter = this.adapters.get(handle.adapterId);
    if (!adapter) throw new Error(`Adapter not found: "${handle.adapterId}"`);

    const status = await adapter.getJobStatus(handle);

    // Update DB and record cost attribution
    await db.execute(
      `UPDATE adapter_jobs
       SET status = $1, completed_at = $2, cost_units = $3
       WHERE job_id = $4`,
      [
        status.status,
        status.completedAt ?? null,
        status.costUnits ?? null,
        jobId,
      ]
    );

    // Emit cost to telemetry-service
    if (status.costUnits) {
      await emitCostEvent({
        adapterId: handle.adapterId,
        runId: jobId,
        costUnits: status.costUnits,
        timestamp: new Date().toISOString(),
      });
    }

    return status;
  }
}
```

---

## 6. Result Mapping

```typescript
// connector-broker/result-mapper.ts

export function mapAdapterOutputsToPortValues(
  outputs: Record<string, unknown>,
  nodeOutputSchema: Record<string, NodePortSpec>
): Record<string, unknown> {
  const mapped: Record<string, unknown> = {};

  for (const [portName, spec] of Object.entries(nodeOutputSchema)) {
    // Try exact key match first
    if (outputs[portName] !== undefined) {
      mapped[portName] = coerceType(outputs[portName], spec.type);
      continue;
    }

    // Try case-insensitive match
    const key = Object.keys(outputs).find(
      k => k.toLowerCase() === portName.toLowerCase()
    );
    if (key) {
      mapped[portName] = coerceType(outputs[key], spec.type);
    }
  }

  return mapped;
}

function coerceType(value: unknown, targetType: string): unknown {
  if (targetType === 'text' && typeof value !== 'string') return JSON.stringify(value);
  if (targetType === 'json' && typeof value === 'string') {
    try { return JSON.parse(value); } catch { return value; }
  }
  return value;
}
```

---

## 7. Adapter Registry

```typescript
// connector-broker/adapter-registry.ts

export class AdapterRegistry {
  private adapters = new Map<string, SubsystemAdapter>();

  register(adapter: SubsystemAdapter) {
    if (this.adapters.has(adapter.adapterId)) {
      throw new Error(`Adapter "${adapter.adapterId}" already registered`);
    }
    this.adapters.set(adapter.adapterId, adapter);
  }

  get(adapterId: string): SubsystemAdapter {
    const a = this.adapters.get(adapterId);
    if (!a) throw new Error(`Adapter not registered: "${adapterId}"`);
    return a;
  }

  async getAllCapabilities(): Promise<Record<string, AdapterCapabilities>> {
    const result: Record<string, AdapterCapabilities> = {};
    for (const [id, adapter] of this.adapters) {
      try {
        result[id] = await adapter.introspect();
      } catch {
        result[id] = { supportedJobTypes: [], supportedInputTypes: [], supportedOutputTypes: [], maxConcurrentJobs: 0, supportsStreaming: false, supportsWebhooks: false };
      }
    }
    return result;
  }
}

// Bootstrap
export function createAdapterRegistry(): AdapterRegistry {
  const registry = new AdapterRegistry();

  registry.register(new N8nAdapter({
    baseUrl: process.env.N8N_BASE_URL!,
    apiKey: process.env.N8N_API_KEY!,
  }));

  registry.register(new DifyAdapter({
    baseUrl: process.env.DIFY_BASE_URL!,
    apiKey: process.env.DIFY_API_KEY!,
  }));

  registry.register(new ComfyUIAdapter({
    baseUrl: process.env.COMFYUI_BASE_URL!,
    clientId: process.env.COMFYUI_CLIENT_ID!,
  }));

  return registry;
}
```

---

## 8. Checklist

Before shipping connector-broker changes:
- [ ] All adapter credentials come from environment variables — never hardcoded
- [ ] Each adapter implements `healthCheck()` — connector-broker health endpoint calls all adapters
- [ ] Job records are written to DB BEFORE dispatching to subsystem (prevent orphan jobs)
- [ ] Cost units are recorded on every completed job — `null` if subsystem doesn't report
- [ ] `mapAdapterOutputsToPortValues` handles missing keys gracefully (logs warn, not throw)
- [ ] ComfyUI GPU-bound concurrency limit is enforced with a semaphore (max 2 parallel)
- [ ] Dify streaming uses SSE — never buffer full response for large completions
- [ ] Adapter `request()` methods set a fetch timeout (default 30s, configurable per adapter)
- [ ] All adapter errors are wrapped with adapterId context before re-throwing
- [ ] `introspect()` is cached per adapter instance (TTL: 5 minutes) — not called on every job
