---
name: agent-framework-workflows
description: 'Design Microsoft Agent Framework workflows in .NET with deterministic orchestration. Use when building routing graphs, agent handoffs, pause/resume checkpoints, multi-step approval flows, human-in-the-loop scenarios, and retry policies for reliable AI-driven processes. Covers workflow state management and recovery.'
---

# Agent Framework Workflows

Design and implement reliable workflow-based orchestration using Microsoft Agent Framework: routing, checkpoints, handoffs, retries, and human-in-the-loop patterns.

## When To Use This Skill

- Multi-step business processes with deterministic control flow and explicit branching.
- Workflows requiring human approval checkpoints or pause/resume semantics.
- Tool orchestration with different handlers per step (e.g., validation tool, then approval tool, then execution tool).
- Scenarios where you need full observability into routing decisions (logs, traces, metrics).
- Systems requiring rollback or compensation patterns (e.g., undo payment if shipping fails).
- Multi-agent handoffs (e.g., research agent → analysis agent → summary agent).

## Initial Workflow

### 1. Define Workflow Input/Output Contract

```csharp
namespace MyApp.Workflows;

/// <summary>
/// Define clear boundaries for workflow state and routing.
/// </summary>
public record WorkflowInput(string UserId, string RequestId, object Payload);

public record WorkflowOutput(
    string RequestId,
    string Status,  // "Pending", "Approved", "Completed", "Failed"
    object? Result = null,
    string? ErrorReason = null);

/// <summary>
/// Intermediate checkpoint state shared across steps.
/// </summary>
public record WorkflowCheckpoint(
    string WorkflowId,
    int CurrentStepIndex,
    string CurrentStepName,
    Dictionary<string, object> ContextData,
    DateTimeOffset CreatedAt,
    DateTimeOffset? LastModifiedAt = null);
```

### 2. Routing Graph with Step Handlers

```csharp
public class OrderApprovalWorkflow
{
    private readonly IChatClient _chatClient;
    private readonly IToolProvider _toolProvider;
    private readonly IWorkflowLogger _logger;

    public OrderApprovalWorkflow(IChatClient chatClient, IToolProvider toolProvider, IWorkflowLogger logger)
    {
        _chatClient = chatClient;
        _toolProvider = toolProvider;
        _logger = logger;
    }

    /// <summary>
    /// Execute workflow steps with explicit routing.
    /// </summary>
    public async Task<WorkflowOutput> ExecuteAsync(WorkflowInput input, CancellationToken cancellationToken = default)
    {
        var checkpoint = new WorkflowCheckpoint(
            WorkflowId: input.RequestId,
            CurrentStepIndex: 0,
            CurrentStepName: "Validate",
            ContextData: new());

        try
        {
            // Step 1: Validation
            checkpoint = await ValidateOrderAsync(input, checkpoint, cancellationToken);
            if (checkpoint.ContextData.ContainsKey("validation_failed"))
                return new(input.RequestId, "Failed", ErrorReason: "Validation failed");

            // Step 2: Risk Assessment (uses AI)
            checkpoint = await AssessRiskAsync(input, checkpoint, cancellationToken);
            var riskLevel = checkpoint.ContextData["risk_level"] as string ?? "unknown";

            // Step 3: Routing based on risk level
            return riskLevel switch
            {
                "low" => await CompleteAsync(input, checkpoint, cancellationToken),
                "medium" => await RequestApprovalAsync(input, checkpoint, cancellationToken),
                "high" => new(input.RequestId, "Failed", ErrorReason: "High risk—manual review required"),
                _ => throw new InvalidOperationException($"Unknown risk level: {riskLevel}")
            };
        }
        catch (Exception ex)
        {
            _logger.LogError("Workflow {WorkflowId} failed at step {StepName}: {Error}",
                checkpoint.WorkflowId, checkpoint.CurrentStepName, ex.Message);
            return new(input.RequestId, "Failed", ErrorReason: ex.Message);
        }
    }

    // Step handlers
    private async Task<WorkflowCheckpoint> ValidateOrderAsync(
        WorkflowInput input,
        WorkflowCheckpoint checkpoint,
        CancellationToken cancellationToken)
    {
        _logger.LogInformation("Step: Validate | WorkflowId={WorkflowId}", checkpoint.WorkflowId);

        // Synchronous validation
        var validationResults = ValidateOrderPayload(input.Payload);
        if (!validationResults.IsValid)
        {
            checkpoint.ContextData["validation_failed"] = true;
            checkpoint.ContextData["validation_errors"] = validationResults.Errors;
        }

        return checkpoint with
        {
            CurrentStepIndex = checkpoint.CurrentStepIndex + 1,
            CurrentStepName = "AssessRisk",
            LastModifiedAt = DateTimeOffset.UtcNow
        };
    }

    private async Task<WorkflowCheckpoint> AssessRiskAsync(
        WorkflowInput input,
        WorkflowCheckpoint checkpoint,
        CancellationToken cancellationToken)
    {
        _logger.LogInformation("Step: AssessRisk | WorkflowId={WorkflowId}", checkpoint.WorkflowId);

        // Use AI to evaluate risk
        var prompt = $@"
Analyze this order for risk:
- Amount: {input.Payload}
- User ID: {input.UserId}

Return ONLY: low, medium, or high";

        var response = await _chatClient.CompleteAsync(
            new List<ChatMessage> { new(ChatRole.User, prompt) },
            cancellationToken: cancellationToken);

        var riskLevel = NormalizeRiskLevel(response.Content[0].Text);
        checkpoint.ContextData["risk_level"] = riskLevel;

        return checkpoint with
        {
            CurrentStepIndex = checkpoint.CurrentStepIndex + 1,
            CurrentStepName = "Route",
            LastModifiedAt = DateTimeOffset.UtcNow
        };
    }

    private async Task<WorkflowOutput> CompleteAsync(
        WorkflowInput input,
        WorkflowCheckpoint checkpoint,
        CancellationToken cancellationToken)
    {
        _logger.LogInformation("Step: Complete (auto-approved) | WorkflowId={WorkflowId}", checkpoint.WorkflowId);

        // Call execution tool
        var tool = _toolProvider.GetTool("execute_order");
        var result = await tool.InvokeAsync(input.Payload, cancellationToken);

        return new(input.RequestId, "Completed", Result: result);
    }

    private async Task<WorkflowOutput> RequestApprovalAsync(
        WorkflowInput input,
        WorkflowCheckpoint checkpoint,
        CancellationToken cancellationToken)
    {
        _logger.LogInformation("Step: RequestApproval | WorkflowId={WorkflowId} Checkpoint={Checkpoint}",
            checkpoint.WorkflowId, System.Text.Json.JsonSerializer.Serialize(checkpoint));

        // Save checkpoint for resume later
        await SaveCheckpointAsync(checkpoint, cancellationToken);

        return new(input.RequestId, "Pending", Result: checkpoint);
    }

    // Helper methods
    private string NormalizeRiskLevel(string text) =>
        text.ToLowerInvariant() switch
        {
            var s when s.Contains("low") => "low",
            var s when s.Contains("medium") => "medium",
            var s when s.Contains("high") => "high",
            _ => "unknown"
        };

    private (bool IsValid, List<string> Errors) ValidateOrderPayload(object payload)
        => (IsValid: true, Errors: new());

    private async Task SaveCheckpointAsync(WorkflowCheckpoint checkpoint, CancellationToken cancellationToken)
    {
        // Persist checkpoint to database/cache for resume later
        _logger.LogInformation("Saved checkpoint for workflow {WorkflowId}", checkpoint.WorkflowId);
    }
}
```

### 3. Human Handoff Pattern

```csharp
public class HumanApprovalHandler
{
    private readonly IApprovalQueue _queue;
    private readonly ILogger<HumanApprovalHandler> _logger;

    public HumanApprovalHandler(IApprovalQueue queue, ILogger<HumanApprovalHandler> logger)
    {
        _queue = queue;
        _logger = logger;
    }

    public async Task<ApprovalDecision> WaitForApprovalAsync(
        WorkflowCheckpoint checkpoint,
        TimeSpan timeout,
        CancellationToken cancellationToken)
    {
        _logger.LogInformation(
            "Enqueued approval request for workflow {WorkflowId} | Timeout={TimeoutSeconds}s",
            checkpoint.WorkflowId, timeout.TotalSeconds);

        // Enqueue approval request
        var approvalTask = _queue.EnqueueAsync(new ApprovalRequest
        {
            WorkflowId = checkpoint.WorkflowId,
            Description = $"Approval needed for: {checkpoint.ContextData}",
            ExpiresAt = DateTimeOffset.UtcNow.Add(timeout)
        }, cancellationToken);

        // Wait for response with timeout
        try
        {
            var decision = await approvalTask.ConfigureAwait(false);
            _logger.LogInformation(
                "Approval decision for {WorkflowId}: {Decision} by {Approver}",
                checkpoint.WorkflowId, decision.IsApproved ? "APPROVED" : "REJECTED", decision.ApprovedBy);
            return decision;
        }
        catch (TimeoutException)
        {
            _logger.LogWarning("Approval request timed out for workflow {WorkflowId}", checkpoint.WorkflowId);
            throw;
        }
    }
}

public record ApprovalRequest(string WorkflowId, string Description, DateTimeOffset ExpiresAt);
public record ApprovalDecision(bool IsApproved, string ApprovedBy, string? Reason = null);
```

### 4. Checkpoint & Resume Pattern

```csharp
public class CheckpointRecovery
{
    private readonly ICheckpointStore _store;
    private readonly ILogger<CheckpointRecovery> _logger;

    public CheckpointRecovery(ICheckpointStore store, ILogger<CheckpointRecovery> logger)
    {
        _store = store;
        _logger = logger;
    }

    public async Task<WorkflowCheckpoint?> LoadCheckpointAsync(string workflowId, CancellationToken cancellationToken)
    {
        var checkpoint = await _store.GetAsync(workflowId, cancellationToken);
        if (checkpoint != null)
        {
            _logger.LogInformation(
                "Recovered checkpoint for workflow {WorkflowId} at step {StepName}",
                workflowId, checkpoint.CurrentStepName);
        }
        return checkpoint;
    }

    public async Task SaveCheckpointAsync(WorkflowCheckpoint checkpoint, CancellationToken cancellationToken)
    {
        await _store.SaveAsync(checkpoint, cancellationToken);
        _logger.LogInformation(
            "Checkpoint saved for workflow {WorkflowId} at step {StepName}",
            checkpoint.WorkflowId, checkpoint.CurrentStepName);
    }

    public async Task ResumeWorkflowAsync(
        string workflowId,
        Func<WorkflowCheckpoint, Task<WorkflowOutput>> resumeHandler,
        CancellationToken cancellationToken)
    {
        var checkpoint = await LoadCheckpointAsync(workflowId, cancellationToken);
        if (checkpoint == null)
            throw new InvalidOperationException($"No checkpoint found for workflow {workflowId}");

        _logger.LogInformation("Resuming workflow {WorkflowId} from step {StepIndex}",
            checkpoint.WorkflowId, checkpoint.CurrentStepIndex);

        await resumeHandler(checkpoint);
    }
}
```

## Troubleshooting Matrix

| Symptom | Likely Cause | Debug Steps |
|---------|--------------|-------------|
| **Workflow hangs at step** | Checkpoint not saved; async task awaits indefinitely | Check log timestamps; verify `SaveCheckpointAsync()` completed; add timeout to all waits |
| **Routing takes wrong branch** | Risk assessment AI prompt ambiguous or model hallucinates | Log full model response; add explicit parsing validation; test with multiple models |
| **Human approval times out** | Approval queue not persisted across restarts; timeout too short | Verify `IApprovalQueue` persistence; increase timeout; add monitoring for stuck approvals |
| **Workflow fails on resume** | Checkpoint context data lost or corrupted | Validate checkpoint schema before resume; add version field to checkpoint; test serialization |
| **Tool invocation fails midway** | External API rate-limited or down; no fallback defined | Add retry policy to tool calls; implement circuit breaker; log full error details |
| **Duplicate workflow execution** | Request ID collision or no idempotency check | Enforce unique `RequestId`; check for retried requests; use `RequestId` as deduplication key |

## Gotchas

- **Prompts Inside Routing Logic**: Never embed critical routing decisions only in AI prompts (e.g., "decide if approved"). Always validate model output explicitly; use structured extraction (e.g., regex, JSON parsing).
- **Unhandled Branches**: Every conditional path must have explicit error handling. Use exhaustive pattern matching or throw `InvalidOperationException` for unexpected states.
- **Checkpoint Versioning**: If you refactor workflow steps, old checkpoints may fail on resume. Add a `version` field to `WorkflowCheckpoint` and implement migration logic.
- **Async Deadlocks**: When using `Wait()` or `.Result` on async code, you risk deadlock in certain contexts. Always use `await` or `ConfigureAwait(false)`.
- **Tool Dependency Ordering**: Ensure tools are registered before workflow execution; missing tools cause late runtime failures instead of fast startup errors.
- **Large Context Data**: Checkpoint `ContextData` can grow large across steps. Use separate data store for large blobs; checkpoint should only reference keys/IDs.

## References

- **Agent Framework Workflows Docs**: <https://learn.microsoft.com/agent-framework/workflows/>
- **Workflow Routing & Handoffs**: <https://learn.microsoft.com/agent-framework/workflows/routing/>
- **Checkpoint & Recovery**: <https://learn.microsoft.com/agent-framework/workflows/checkpoints/>
- **Tool Registration**: <https://learn.microsoft.com/agent-framework/tools/>
- **Structured Extraction**: <https://learn.microsoft.com/agent-framework/models/structured-output/>
