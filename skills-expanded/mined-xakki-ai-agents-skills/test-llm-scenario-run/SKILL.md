---
name: test-llm-scenario-run
description: 'Design and run bounded, reproducible scenario evaluations for LLM applications. Use when comparing prompts, models or agent behaviors on fixed scenarios. RU: оценка LLM, сценарии.'
disable-model-invocation: true
---

# LLM scenario evaluation

Trace the real application entrypoint, model and transport interfaces, relevant fixtures and actual test runner. Exercise the existing application core rather than a parallel implementation that can drift. Separate ordinary deterministic offline tests from explicit model-backed evaluation; neither a fake model nor a retrieval-only check proves answer quality.

Use synthetic, non-sensitive scenarios with versioned inputs and unique output locations. Record the code and scenario revisions, evaluated model/configuration, cases, observable outputs, rubric and actual results. Check the model boundary's effective network, mounts, credentials and data access; never expose real user content, secrets or a live channel merely to make a fixture realistic. An offline container does not prove a local socket bridge works without an actual handshake.

Agree on quality criteria and cost/call limits appropriate to the task. Preserve a human-reviewed baseline when useful; do not invent a numeric threshold or treat an uncalibrated model judge as ground truth. Check source grounding, unsupported claims and relevant failure cases. Do not use byte-identical prose as a general quality oracle for variable generation.

Run actual model calls only when authorized; keep them outside ordinary unit/build checks unless requested. Report deterministic test results separately from model-run observations, and report unavailable or unrun scenarios. Preserve evidence before cleaning disposable runs. If evaluation is a dependency of delivery, record the prerequisite in both directions without blocking unrelated authorized work.
