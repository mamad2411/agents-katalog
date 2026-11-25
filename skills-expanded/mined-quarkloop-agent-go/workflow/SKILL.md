# service-workflow

Workflow is the durable orchestration boundary. It exposes Temporal-backed
workflow service functions to agents and runtime, while keeping Temporal SDK
usage out of every other package.

## Agent Rules

1. Use Workflow for long-running, resumable, multi-step work where failure,
   retry, progress visibility, or cancellation matters.
2. Do not ask another service or Workflow to call a domain service. The agent
   executes domain service functions and signals workflow checkpoints.
3. Use `workflow_Start` only with a clear workflow type and concrete work plan.
   For document ingestion, the workflow type is `document_ingestion_indexing`.
4. Use `workflow_Query`, `workflow_Describe`, and `workflow_StreamEvents` to
   explain progress before making assumptions about state.
5. Use `workflow_Cancel` only after approval when cancellation can discard
   progress or leave external work incomplete.
6. Never expose Temporal internals, task queues, worker names, or retry history
   to users unless they are debugging operations.

## Service Functions

- `Start(StartWorkflowRequest) -> StartWorkflowResponse`
  - Generated service function: `workflow_Start`
  - NATS subject: `svc.workflow.v1.start`
  - Starts a durable workflow.

- `Signal(SignalWorkflowRequest) -> SignalWorkflowResponse`
  - Generated service function: `workflow_Signal`
  - NATS subject: `svc.workflow.v1.signal`
  - Sends an asynchronous durable signal.

- `Query(QueryWorkflowRequest) -> QueryWorkflowResponse`
  - Generated service function: `workflow_Query`
  - NATS subject: `svc.workflow.v1.query`
  - Reads workflow state without mutation.

- `Cancel(CancelWorkflowRequest) -> CancelWorkflowResponse`
  - Generated service function: `workflow_Cancel`
  - NATS subject: `svc.workflow.v1.cancel`
  - Cancels a workflow after approval.

- `Describe(DescribeWorkflowRequest) -> DescribeWorkflowResponse`
  - Generated service function: `workflow_Describe`
  - NATS subject: `svc.workflow.v1.describe`
  - Describes one workflow execution.

- `List(ListWorkflowsRequest) -> ListWorkflowsResponse`
  - Generated service function: `workflow_List`
  - NATS subject: `svc.workflow.v1.list`
  - Lists workflow executions.

- `StreamEvents(StreamWorkflowEventsRequest) -> stream WorkflowEvent`
  - Generated service function: `workflow_StreamEvents`
  - NATS subject: `svc.workflow.v1.stream_events`
  - Streams progress events.

## Boundaries

- Workflow owns Temporal client, worker registration, activity retry policy,
  workflow state queries, cancellation, and workflow progress events.
- Workflow accepts checkpoint-completed and checkpoint-failed signals after
  the agent has performed the corresponding work.
- Services remain domain owners and do not call Workflow or each other.
