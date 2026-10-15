---
name: new-worker
description: Generate a job worker for a Camunda process. Detects language from project config (package.json or pom.xml).
argument-hint: "[worker description]"
---

Generate a job worker. Detect language:
- pom.xml → Java: use `@JobWorker(type = "...")` pattern from `lang-java.md`
- package.json → Node.js: use `zeebe.createWorker()` pattern from `lang-nodejs.md`

The taskType must exactly match the `type` in `<zeebe:taskDefinition>` in the BPMN. Case-sensitive.

$ARGUMENTS
