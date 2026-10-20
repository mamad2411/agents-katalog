# Workflow Runtime Agent Rules

Keep workflow coordination deterministic and provider-neutral. The package may
define shared execution semantics, but native providers and adapters own their
storage or engine details behind `WorkflowRuntimePort`.

Do not persist JavaScript closures, function source, module paths, downloaded
code, raw prompts, credentials, provider URLs, local paths, SQL, or hidden
reasoning as workflow state. Durable providers must use serializable
definitions, stable handler IDs, bounded retries, explicit cancellation,
workspace-scoped history, and idempotency for consequential effects.
