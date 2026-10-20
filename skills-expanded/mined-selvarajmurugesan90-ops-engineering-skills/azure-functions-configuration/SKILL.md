---
name: azure-functions-configuration
description: >
  Configures Azure Functions hosting plans (Consumption, Premium,
  Dedicated/App Service), triggers and bindings, and host.json/
  application settings, with explicit cold-start tradeoffs between plans.
  Use when the user asks to "choose an Azure Functions hosting plan," "set
  up a Function App trigger or binding," "reduce Azure Functions cold
  start," "configure Premium plan pre-warmed instances," or "write
  host.json for a Function App."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: serverless-and-alternative-compute
  maturity: stable
---

# Azure Functions Configuration

## Purpose

Azure Functions' behavior is shaped by two largely independent decisions:
which **hosting plan** runs the Function App (Consumption, Premium, or
Dedicated/App Service), and which **triggers and bindings** wire the
function to events and data sources without hand-written integration code.
The hosting plan decision in particular is where most cold-start and cost
problems originate — Consumption is the cheapest at idle but pays for it in
cold-start latency, while Premium trades a always-billed baseline cost for
pre-warmed instances. Picking the wrong plan for the workload's latency
sensitivity is a recurring, avoidable source of production complaints.

## When to use

- Standing up a new Function App and choosing between Consumption,
  Premium, or Dedicated (App Service) hosting plans.
- A Function App on the Consumption plan shows unacceptable latency on
  the first request after idle periods.
- Configuring a trigger (HTTP, Timer, Queue, Blob, Event Grid, Service
  Bus) or an input/output binding to avoid hand-rolled SDK integration
  code.
- Writing or debugging `host.json` (function timeout, extension bundle
  version, batching behavior) or `local.settings.json` vs. Azure
  Application Settings for a given environment.
- Deciding whether a workload needs VNet integration, which constrains
  the hosting plan choice (Premium or Dedicated, not Consumption without
  additional networking features).

## Prerequisites & environment

- Azure CLI (`az`) authenticated against the target subscription, with
  permissions to create Function Apps, App Service Plans, and Storage
  Accounts (every Function App requires a backing storage account for
  triggers/bindings state and deployment packages).
- A `host.json` and function-level `function.json` (or, for newer
  isolated-worker/.NET or Node.js v4 programming models, attribute/
  decorator-based trigger declarations in code) matching the runtime
  stack in use.
- Know the Azure Functions runtime version (`~4` is the current major
  generation) and language worker version pinned for the Function App —
  behavior and supported bindings differ across major runtime versions.

## Step-by-step guidance

1. **Choose the hosting plan based on latency sensitivity and traffic
   shape, not just cost.** Consumption (`Y1` SKU) scales automatically
   from zero and only bills for execution time, but a Function App idle
   for a while pays a cold start on the next invocation while a new
   instance initializes. Premium (`EP1`–`EP3` SKUs) keeps a configurable
   number of pre-warmed instances always ready, eliminating cold starts
   for traffic within that pre-warmed capacity, and supports VNet
   integration; it has an always-on baseline cost even at zero traffic.
   Dedicated (App Service Plan) runs on VMs you already pay for
   continuously — the right choice when the Function App shares
   infrastructure with an existing App Service workload, or needs fully
   predictable, always-on capacity:
   ```bash
   az functionapp plan create \
     --name checkout-functions-premium \
     --resource-group <RESOURCE_GROUP> \
     --sku EP1 \
     --is-linux
   az functionapp create \
     --name checkout-functions \
     --resource-group <RESOURCE_GROUP> \
     --plan checkout-functions-premium \
     --storage-account <STORAGE_ACCOUNT_NAME> \
     --runtime python \
     --runtime-version 3.11 \
     --functions-version 4
   ```

2. **On Premium, set pre-warmed instance count deliberately** — it's the
   knob that directly controls how much traffic is served cold-start-free:
   ```bash
   az functionapp update \
     --name checkout-functions \
     --resource-group <RESOURCE_GROUP> \
     --set siteConfig.preWarmedInstanceCount=2
   ```
   Pre-warmed instances still bill even at zero traffic — size this
   against expected baseline load, not the theoretical maximum.

3. **Declare triggers and bindings instead of writing manual SDK calls**
   for the event source and any output destination. HTTP trigger example
   (`function.json`, classic model):
   ```json
   {
     "bindings": [
       { "authLevel": "function", "type": "httpTrigger", "direction": "in", "name": "req", "methods": ["post"] },
       { "type": "http", "direction": "out", "name": "$return" },
       { "type": "queue", "direction": "out", "name": "outputQueueItem", "queueName": "order-events", "connection": "AzureWebJobsStorage" }
     ]
   }
   ```
   A Queue-triggered function that writes to Cosmos DB:
   ```json
   {
     "bindings": [
       { "type": "queueTrigger", "direction": "in", "name": "msg", "queueName": "order-events", "connection": "AzureWebJobsStorage" },
       { "type": "cosmosDB", "direction": "out", "name": "output", "databaseName": "orders", "collectionName": "processed", "connection": "CosmosDBConnection" }
     ]
   }
   ```
   The binding handles polling/connection management; application code
   only reads the input parameter and returns/assigns the output
   parameter.

4. **Configure `host.json`** for function-level timeout, extension bundle
   version, and (for queue/event-based triggers) batching behavior:
   ```json
   {
     "version": "2.0",
     "extensionBundle": { "id": "Microsoft.Azure.Functions.ExtensionBundle", "version": "[4.*, 5.0.0)" },
     "functionTimeout": "00:05:00",
     "extensions": {
       "queues": { "batchSize": 16, "maxDequeueCount": 5, "visibilityTimeout": "00:00:30" }
     }
   }
   ```
   `functionTimeout` on Consumption defaults to a plan-specific ceiling
   and cannot exceed it; Premium/Dedicated support longer or unbounded
   execution — check the current documented ceiling for the plan in use
   rather than assuming Consumption's default applies everywhere.

5. **Separate local development config from deployed Application
   Settings.** `local.settings.json` is for local `func start` only and
   must never be deployed or committed with real connection strings; in
   Azure, the equivalent values live in Application Settings (or
   Key Vault references) on the Function App:
   ```bash
   az functionapp config appsettings set \
     --name checkout-functions \
     --resource-group <RESOURCE_GROUP> \
     --settings "CosmosDBConnection=@Microsoft.KeyVault(SecretUri=<KEY_VAULT_SECRET_URI>)"
   ```

6. **Add VNet integration only on plans that support it** (Premium or
   Dedicated) when the function needs to reach private resources (a
   VNet-restricted database, an internal API) — Consumption does not
   support regional VNet integration for outbound calls in the same way,
   so this constrains the plan choice made in step 1, not something to
   retrofit later.

## Best practices

- Treat the hosting plan choice as a per-Function-App decision driven by
  the specific workload's latency and traffic profile — don't default an
  entire org to one plan type regardless of use case.
- Pin the extension bundle version range in `host.json` (`[4.*, 5.0.0)`
  style) rather than leaving it fully open, so a major bundle version
  bump doesn't silently change binding behavior on the next deploy.
- Store secrets and connection strings as Key Vault references in
  Application Settings, not as plaintext values, even though Application
  Settings are already encrypted at rest — Key Vault references add
  centralized rotation and access auditing.
- Size Premium plan instance count and pre-warmed count from observed
  traffic (Application Insights request rate), not a guess, and revisit
  after the workload has run for a real traffic cycle.
- Use deployment slots (where supported) to validate a new Function App
  version against production-like traffic before swapping it into the
  live slot, mirroring blue/green deploy practice elsewhere in this repo.

## Common pitfalls

- **Symptom:** A Consumption-plan HTTP-triggered function times out or
  responds very slowly on the first request after a period of no traffic,
  then responds quickly afterward.
  **Fix:** This is a cold start on Consumption — if the workload has a
  latency SLA that a cold start would violate, move it to Premium with a
  pre-warmed instance count sized to expected baseline traffic, rather
  than trying to eliminate cold starts on Consumption itself.

- **Symptom:** A Function App on Consumption fails to reach a database
  that's only reachable from inside a VNet.
  **Fix:** Consumption doesn't support the same regional VNet integration
  model as Premium/Dedicated for this — migrate the Function App to a
  Premium plan (or Dedicated) and configure VNet integration there, rather
  than trying to open the database to the public internet as a
  workaround.

- **Symptom:** `local.settings.json` (containing a real storage account
  connection string) gets committed to source control or accidentally
  included in a deployment package.
  **Fix:** Add `local.settings.json` to `.gitignore` by default in every
  new Function App project, and rely on Application Settings / Key Vault
  references for any deployed environment — never deploy this file.

- **Symptom:** A queue-triggered function processes the same message
  repeatedly and eventually stops entirely.
  **Fix:** The function is throwing on a specific message and exhausting
  `maxDequeueCount` in `host.json`'s queues extension config; the message
  then moves to the poison queue — inspect the poison queue
  (`<queue-name>-poison`) for the actual failing payload instead of only
  watching the main queue's retry behavior.

- **Symptom:** Premium plan cost is far higher than expected even with
  low traffic.
  **Fix:** Pre-warmed instance count and the plan's minimum instance
  count both bill continuously regardless of traffic — right-size these
  against real baseline load (Application Insights metrics) rather than
  leaving a default or conservatively-high value in place indefinitely.

## Worked example

**Scenario:** A checkout notification service needs a low-latency HTTP
endpoint (called synchronously from a web frontend) plus an async
queue-triggered function that writes processed events to Cosmos DB. The
HTTP path has a strict latency requirement; the queue path does not.

Because of the HTTP path's latency requirement, the whole Function App is
placed on a Premium plan rather than Consumption:
```bash
az functionapp plan create --name checkout-notify-premium --resource-group <RESOURCE_GROUP> --sku EP1 --is-linux
az functionapp create --name checkout-notify --resource-group <RESOURCE_GROUP> \
  --plan checkout-notify-premium --storage-account <STORAGE_ACCOUNT_NAME> \
  --runtime node --runtime-version 20 --functions-version 4
az functionapp update --name checkout-notify --resource-group <RESOURCE_GROUP> \
  --set siteConfig.preWarmedInstanceCount=2
```
`host.json` pins the extension bundle and sets a generous queue batch
size for the async path, which doesn't need low latency:
```json
{
  "version": "2.0",
  "extensionBundle": { "id": "Microsoft.Azure.Functions.ExtensionBundle", "version": "[4.*, 5.0.0)" },
  "extensions": { "queues": { "batchSize": 32, "maxDequeueCount": 3 } }
}
```
The Cosmos DB connection string is stored as a Key Vault reference in
Application Settings rather than a plaintext value. Before this ships,
the trigger/binding declarations and `host.json` are reviewed against the
general pre-deploy discipline described in
[aws-lambda-configuration-validation](../aws-lambda-configuration-validation/SKILL.md)'s
approach (adapted to Azure equivalents: App Settings secret scanning,
VNet integration correctness), since this domain doesn't yet have an
Azure-specific validation skill of its own.

## Cross-references

- [aws-lambda-packaging-and-configuration](../aws-lambda-packaging-and-configuration/SKILL.md) — the equivalent packaging/tuning/cold-start decisions on AWS Lambda, useful when comparing platforms or migrating.
- [google-cloud-functions-configuration](../google-cloud-functions-configuration/SKILL.md) — the equivalent hosting/scaling configuration on Google Cloud Functions Gen1/Gen2.
- [dapr-distributed-runtime-configuration](../dapr-distributed-runtime-configuration/SKILL.md) — Azure Functions' Dapr extension lets triggers/bindings target Dapr state stores and pub/sub components instead of native Azure services, useful for polyglot or multi-cloud portability.
