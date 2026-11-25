---
name: security-access-diagnose
description: 'Diagnose an access refusal while preserving native approval and security boundaries. Use when a task meets a filesystem, credential, provider or approval refusal. RU: отказ в доступе.'
license: MIT
disable-model-invocation: true
---

# Access-boundary diagnosis

Use when an authorized task encounters a filesystem, credential, provider or native approval refusal. Preserve the exact operation, target, native outcome and scope. Distinguish a pre-execution veto from an executed permission error, missing prerequisite, timeout or ordinary application failure; do not infer the reason from a generic error alone.

Stop the denied operation and do not bypass a security or approval veto by substituting another tool, identity, read route or weaker guard. A denied content read does not authorize obtaining that content through a search, hash, historical object or alternate controller. Continue independent authorized work only when the applicable stop scope permits it.

Reuse existing task and operation grants without asking for the same permission again; separately identify any genuinely missing resource access or native action approval. An unanswered approval is not consent. Record what ran, what did not run, partial effects and the narrow unresolved boundary. A fixture test or source inspection establishes only its observed scope, not restored admission to a protected live operation.
