---
name: azure-monitor-toolkit
description: Consolidated toolkit for azure-monitor. Covers azure-monitor-query-py, azure-monitor-opentelemetry-py, azure-monitor-ingestion-java, azure-monitor-opentelemetry-ts, azure-monitor-opentelemetry-exporter-java, azure-monitor-opentelemetry-exporter-py, azure-monitor-ingestion-py, azure-monitor-query-java
---
# Azure Monitor Toolkit

## Core Capabilities
# Azure Monitor Toolkit

# Azure Monitor Query SDK for Python

Query logs and metrics from Azure Monitor and Log Analytics workspaces.

## Installation

```bash
pip install azure-monitor-query
```

## Environment Variables

```bash
# Log Analytics
AZURE_LOG_ANALYTICS_WORKSPACE_ID=<workspace-id>

# Metrics
AZURE_METRICS_RESOURCE_URI=/subscriptions/<sub>/resourceGroups/<rg>/providers/<provider>/<type>/<name>
```

## Authentication

```python
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
```

## Logs Query Client

### Basic Query

```python
from azure.monitor.query import LogsQueryClient
from datetime import timedelta

client = LogsQueryClient(credential)

query = """
AppRequests
| where TimeGenerated > ago(1h)
| summarize count() by bin(TimeGenerated, 5m), ResultCode
| order by TimeGenerated desc
"""

response = client.query_workspace(
    workspace_id=os.environ["AZURE_LOG_ANALYTICS_WORKSPACE_ID"],
    query=query,
    timespan=timedelta(hours=1)
)

for table in response.tables:
    for row in table.rows:
        print(row)
```

### Query with Time Range

```python
from datetime import datetime, timezone

response = client.query_workspace(
    workspace_id=workspace_id,
    query="AppRequests | take 10",
    timespan=(
        datetime(2024, 1, 1, tzinfo=timezone.utc),
        datetime(2024, 1, 2, tzinfo=timezone.utc)
    )
)
```

### Convert to DataFrame

```python
import pandas as pd

response = client.query_workspace(workspace_id, query, timespan=timedelta(hours=1))

if response.tables:
    table = response.tables[0]
    df = pd.DataFrame(data=table.rows, columns=[col.name for col in table.columns])
    print(df.head())
```

### Batch Query

```python
from azure.monitor.query import LogsBatchQuery

queries = [
    LogsBatchQuery(workspace_id=workspace_id, query="AppRequests | take 5", timespan=timedelta(hours=1)),
    LogsBatchQuery(workspace_id=workspace_id, query="AppExceptions | take 5", timespan=timedelta(hours=1))
]

responses = client.query_batch(queries)

for response in responses:
    if response.tables:
        print(f"Rows: {len(response.tables[0].rows)}")
```

### Handle Partial Results

```python
from azure.monitor.query import LogsQueryStatus

response = client.query_workspace(workspace_id, query, timespan=timedelta(hours=24))

if response.status == LogsQueryStatus.PARTIAL:
    print(f"Partial results: {response.partial_error}")
elif response.status == LogsQueryStatus.FAILURE:
    print(f"Query failed: {response.partial_error}")
```

## Metrics Query Client

### Query Resource Metrics

```python
from azure.monitor.query import MetricsQueryClient
from datetime import timedelta

metrics_client = MetricsQueryClient(credential)

response = metrics_client.query_resource(
    resource_uri=os.environ["AZURE_METRICS_RESOURCE_URI"],
    metric_names=["Percentage CPU", "Network In Total"],
    timespan=timedelta(hours=1),
    granularity=timedelta(minutes=5)
)

for metric in response.metrics:
    print(f"{metric.name}:")
    for time_series in metric.timeseries:
        for data in time_series.data:
            print(f"  {data.timestamp}: {data.average}")
```

### Aggregations

```python
from azure.monitor.query import MetricAggregationType

response = metrics_client.query_resource(
    resource_uri=resource_uri,
    metric_names=["Requests"],
    timespan=timedelta(hours=1),
    aggregations=[
        MetricAggregationType.AVERAGE,
        MetricAggregationType.MAXIMUM,
        MetricAggregationType.MINIMUM,
        MetricAggregationType.COUNT
    ]
)
```

### Filter by Dimension

```python
response = metrics_client.query_resource(
    resource_uri=resource_uri,
    metric_names=["Requests"],
    timespan=timedelta(hours=1),
    filter="ApiName eq 'GetBlob'"
)
```

### List Metric Definitions

```python
definitions = metrics_client.list_metric_definitions(resource_uri)
for definition in definitions:
    print(f"{definition.name}: {definition.unit}")
```

### List Metric Namespaces

```python
namespaces = metrics_client.list_metric_namespaces(resource_uri)
for ns in namespaces:
    print(ns.fully_qualified_namespace)
```

## Async Clients

```python
from azure.monitor.query.aio import LogsQueryClient, MetricsQueryClient
from azure.identity.aio import DefaultAzureCredential

async def query_logs():
    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential)
    
    response = await client.query_workspace(
        workspace_id=workspace_id,
        query="AppRequests | take 10",
        timespan=timedelta(hours=1)
    )
    
    await client.close()
    await credential.close()
    return response
```

## Common Kusto Queries

```kusto
// Requests by status code
AppRequests
| summarize count() by ResultCode
| order by count_ desc

// Exceptions over time
AppExceptions
| summarize count() by bin(TimeGenerated, 1h)

// Slow requests
AppRequests
| where DurationMs > 1000
| project TimeGenerated, Name, DurationMs
| order by DurationMs desc

// Top errors
AppExceptions
| summarize count() by ExceptionType
| top 10 by count_
```

## Client Types

| Client | Purpose |
|--------|---------|
| `LogsQueryClient` | Query Log Analytics workspaces |
| `MetricsQueryClient` | Query Azure Monitor metrics |

## Best Practices

1. **Use timedelta** for relative time ranges
2. **Handle partial results** for large queries
3. **Use batch queries** when running multiple queries
4. **Set appropriate granularity** for metrics to reduce data points
5. **Convert to DataFrame** for easier data analysis
6. **Use aggregations** to summarize metric data
7. **Filter by dimensions** to narrow metric results

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

# Azure Monitor OpenTelemetry Distro for Python

One-line setup for Application Insights with OpenTelemetry auto-instrumentation.

## Installation

```bash
pip install azure-monitor-opentelemetry
```

## Environment Variables

```bash
APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=xxx;IngestionEndpoint=https://xxx.in.applicationinsights.azure.com/
```

## Quick Start

```python
from azure.monitor.opentelemetry import configure_azure_monitor

# One-line setup - reads connection string from environment
configure_azure_monitor()

# Your application code...
```

## Explicit Configuration

```python
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor(
    connection_string="InstrumentationKey=xxx;IngestionEndpoint=https://xxx.in.applicationinsights.azure.com/"
)
```

## With Flask

```python
from flask import Flask
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor()

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

if __name__ == "__main__":
    app.run()
```

## With Django

```python
# settings.py
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor()

# Django settings...
```

## With FastAPI

```python
from fastapi import FastAPI
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor()

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

## Custom Traces

```python
from opentelemetry import trace
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor()

tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("my-operation") as span:
    span.set_attribute("custom.attribute", "value")
    # Do work...
```

## Custom Metrics

```python
from opentelemetry import metrics
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor()

meter = metrics.get_meter(__name__)
counter = meter.create_counter("my_counter")

counter.add(1, {"dimension": "value"})
```

## Custom Logs

```python
import logging
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logger.info("This will appear in Application Insights")
logger.error("Errors are captured too", exc_info=True)
```

## Sampling

```python
from azure.monitor.opentelemetry import configure_azure_monitor

# Sample 10% of requests
configure_azure_monitor(
    sampling_ratio=0.1
)
```

## Cloud Role Name

Set cloud role name for Application Map:

```python
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry.sdk.resources import Resource, SERVICE_NAME

configure_azure_monitor(
    resource=Resource.create({SERVICE_NAME: "my-service-name"})
)
```

## Disable Specific Instrumentations

```python
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor(
    instrumentations=["flask", "requests"]  # Only enable these
)
```

## Enable Live Metrics

```python
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor(
    enable_live_metrics=True
)
```

## Azure AD Authentication

```python
from azure.monitor.opentelemetry import configure_azure_monitor
from azure.identity import DefaultAzureCredential

configure_azure_monitor(
    credential=DefaultAzureCredential()
)
```

## Auto-Instrumentations Included

| Library | Telemetry Type |
|---------|---------------|
| Flask | Traces |
| Django | Traces |
| FastAPI | Traces |
| Requests | Traces |
| urllib3 | Traces |
| httpx | Traces |
| aiohttp | Traces |
| psycopg2 | Traces |
| pymysql | Traces |
| pymongo | Traces |
| redis | Traces |

## Configuration Options

| Parameter | Description | Default |
|-----------|-------------|---------|
| `connection_string` | Application Insights connection string | From env var |
| `credential` | Azure credential for AAD auth | None |
| `sampling_ratio` | Sampling rate (0.0 to 1.0) | 1.0 |
| `resource` | OpenTelemetry Resource | Auto-detected |
| `instrumentations` | List of instrumentations to enable | All |
| `enable_live_metrics` | Enable Live Metrics stream | False |

## Best Practices

1. **Call configure_azure_monitor() early** — Before importing instrumented libraries
2. **Use environment variables** for connection string in production
3. **Set cloud role name** for multi-service applications
4. **Enable sampling** in high-traffic applications
5. **Use structured logging** for better log analytics queries
6. **Add custom attributes** to spans for better debugging
7. **Use AAD authentication** for production workloads

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

# Azure Monitor Ingestion SDK for Java

Client library for sending custom logs to Azure Monitor using the Logs Ingestion API via Data Collection Rules.

## Installation

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-monitor-ingestion</artifactId>
    <version>1.2.11</version>
</dependency>
```

Or use Azure SDK BOM:

```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>com.azure</groupId>
            <artifactId>azure-sdk-bom</artifactId>
            <version>{bom_version}</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>

<dependencies>
    <dependency>
        <groupId>com.azure</groupId>
        <artifactId>azure-monitor-ingestion</artifactId>
    </dependency>
</dependencies>
```

## Prerequisites

- Data Collection Endpoint (DCE)
- Data Collection Rule (DCR)
- Log Analytics workspace
- Target table (custom or built-in: CommonSecurityLog, SecurityEvents, Syslog, WindowsEvents)

## Environment Variables

```bash
DATA_COLLECTION_ENDPOINT=https://<dce-name>.<region>.ingest.monitor.azure.com
DATA_COLLECTION_RULE_ID=dcr-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
STREAM_NAME=Custom-MyTable_CL
```

## Client Creation

### Synchronous Client

```java
import com.azure.identity.DefaultAzureCredential;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.azure.monitor.ingestion.LogsIngestionClient;
import com.azure.monitor.ingestion.LogsIngestionClientBuilder;

DefaultAzureCredential credential = new DefaultAzureCredentialBuilder().build();

LogsIngestionClient client = new LogsIngestionClientBuilder()
    .endpoint("<data-collection-endpoint>")
    .credential(credential)
    .buildClient();
```

### Asynchronous Client

```java
import com.azure.monitor.ingestion.LogsIngestionAsyncClient;

LogsIngestionAsyncClient asyncClient = new LogsIngestionClientBuilder()
    .endpoint("<data-collection-endpoint>")
    .credential(new DefaultAzureCredentialBuilder().build())
    .buildAsyncClient();
```

## Key Concepts

| Concept | Description |
|---------|-------------|
| Data Collection Endpoint (DCE) | Ingestion endpoint URL for your region |
| Data Collection Rule (DCR) | Defines data transformation and routing to tables |
| Stream Name | Target stream in the DCR (e.g., `Custom-MyTable_CL`) |
| Log Analytics Workspace | Destination for ingested logs |

## Core Operations

### Upload Custom Logs

```java
import java.util.List;
import java.util.ArrayList;

List<Object> logs = new ArrayList<>();
logs.add(new MyLogEntry("2024-01-15T10:30:00Z", "INFO", "Application started"));
logs.add(new MyLogEntry("2024-01-15T10:30:05Z", "DEBUG", "Processing request"));

client.upload("<data-collection-rule-id>", "<stream-name>", logs);
System.out.println("Logs uploaded successfully");
```

### Upload with Concurrency

For large log collections, enable concurrent uploads:

```java
import com.azure.monitor.ingestion.models.LogsUploadOptions;
import com.azure.core.util.Context;

List<Object> logs = getLargeLogs(); // Large collection

LogsUploadOptions options = new LogsUploadOptions()
    .setMaxConcurrency(3);

client.upload("<data-collection-rule-id>", "<stream-name>", logs, options, Context.NONE);
```

### Upload with Error Handling

Handle partial upload failures gracefully:

```java
LogsUploadOptions options = new LogsUploadOptions()
    .setLogsUploadErrorConsumer(uploadError -> {
        System.err.println("Upload error: " + uploadError.getResponseException().getMessage());
        System.err.println("Failed logs count: " + uploadError.getFailedLogs().size());
        
        // Option 1: Log and continue
        // Option 2: Throw to abort remaining uploads
        // throw uploadError.getResponseException();
    });

client.upload("<data-collection-rule-id>", "<stream-name>", logs, options, Context.NONE);
```

### Async Upload with Reactor

```java
import reactor.core.publisher.Mono;

List<Object> logs = getLogs();

asyncClient.upload("<data-collection-rule-id>", "<stream-name>", logs)
    .doOnSuccess(v -> System.out.println("Upload completed"))
    .doOnError(e -> System.err.println("Upload failed: " + e.getMessage()))
    .subscribe();
```

## Log Entry Model Example

```java
public class MyLogEntry {
    private String timeGenerated;
    private String level;
    private String message;
    
    public MyLogEntry(String timeGenerated, String level, String message) {
        this.timeGenerated = timeGenerated;
        this.level = level;
        this.message = message;
    }
    
    // Getters required for JSON serialization
    public String getTimeGenerated() { return timeGenerated; }
    public String getLevel() { return level; }
    public String getMessage() { return message; }
}
```

## Error Handling

```java
import com.azure.core.exception.HttpResponseException;

try {
    client.upload(ruleId, streamName, logs);
} catch (HttpResponseException e) {
    System.err.println("HTTP Status: " + e.getResponse().getStatusCode());
    System.err.println("Error: " + e.getMessage());
    
    if (e.getResponse().getStatusCode() == 403) {
        System.err.println("Check DCR permissions and managed identity");
    } else if (e.getResponse().getStatusCode() == 404) {
        System.err.println("Verify DCE endpoint and DCR ID");
    }
}
```

## Best Practices

1. **Batch logs** — Upload in batches rather than one at a time
2. **Use concurrency** — Set `maxConcurrency` for large uploads
3. **Handle partial failures** — Use error consumer to log failed entries
4. **Match DCR schema** — Log entry fields must match DCR transformation expectations
5. **Include TimeGenerated** — Most tables require a timestamp field
6. **Reuse client** — Create once, reuse throughout application
7. **Use async for high throughput** — `LogsIngestionAsyncClient` for reactive patterns

## Querying Uploaded Logs

Use azure-monitor-query to query ingested logs:

```java
// See azure-monitor-query skill for LogsQueryClient usage
String query = "MyTable_CL | where TimeGenerated > ago(1h) | limit 10";
```

## Reference Links

| Resource | URL |
|----------|-----|
| Maven Package | https://central.sonatype.com/artifact/com.azure/azure-monitor-ingestion |
| GitHub | https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/monitor/azure-monitor-ingestion |
| Product Docs | https://learn.microsoft.com/azure/azure-monitor/logs/logs-ingestion-api-overview |
| DCE Overview | https://learn.microsoft.com/azure/azure-monitor/essentials/data-collection-endpoint-overview |
| DCR Overview | https://learn.microsoft.com/azure/azure-monitor/essentials/data-collection-rule-overview |
| Troubleshooting | https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/monitor/azure-monitor-ingestion/TROUBLESHOOTING.md |

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

# Azure Monitor OpenTelemetry SDK for TypeScript

Auto-instrument Node.js applications with distributed tracing, metrics, and logs.

## Installation

```bash
# Distro (recommended - auto-instrumentation)
npm install @azure/monitor-opentelemetry

# Low-level exporters (custom OpenTelemetry setup)
npm install @azure/monitor-opentelemetry-exporter

# Custom logs ingestion
npm install @azure/monitor-ingestion
```

## Environment Variables

```bash
APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=...;IngestionEndpoint=...
```

## Quick Start (Auto-Instrumentation)

**IMPORTANT:** Call `useAzureMonitor()` BEFORE importing other modules.

```typescript
import { useAzureMonitor } from "@azure/monitor-opentelemetry";

useAzureMonitor({
  azureMonitorExporterOptions: {
    connectionString: process.env.APPLICATIONINSIGHTS_CONNECTION_STRING
  }
});

// Now import your application
import express from "express";
const app = express();
```

## ESM Support (Node.js 18.19+)

```bash
node --import @azure/monitor-opentelemetry/loader ./dist/index.js
```

**package.json:**
```json
{
  "scripts": {
    "start": "node --import @azure/monitor-opentelemetry/loader ./dist/index.js"
  }
}
```

## Full Configuration

```typescript
import { useAzureMonitor, AzureMonitorOpenTelemetryOptions } from "@azure/monitor-opentelemetry";
import { resourceFromAttributes } from "@opentelemetry/resources";

const options: AzureMonitorOpenTelemetryOptions = {
  azureMonitorExporterOptions: {
    connectionString: process.env.APPLICATIONINSIGHTS_CONNECTION_STRING,
    storageDirectory: "/path/to/offline/storage",
    disableOfflineStorage: false
  },
  
  // Sampling
  samplingRatio: 1.0,  // 0-1, percentage of traces
  
  // Features
  enableLiveMetrics: true,
  enableStandardMetrics: true,
  enablePerformanceCounters: true,
  
  // Instrumentation libraries
  instrumentationOptions: {
    azureSdk: { enabled: true },
    http: { enabled: true },
    mongoDb: { enabled: true },
    mySql: { enabled: true },
    postgreSql: { enabled: true },
    redis: { enabled: true },
    bunyan: { enabled: false },
    winston: { enabled: false }
  },
  
  // Custom resource
  resource: resourceFromAttributes({ "service.name": "my-service" })
};

useAzureMonitor(options);
```

## Custom Traces

```typescript
import { trace } from "@opentelemetry/api";

const tracer = trace.getTracer("my-tracer");

const span = tracer.startSpan("doWork");
try {
  span.setAttribute("component", "worker");
  span.setAttribute("operation.id", "42");
  span.addEvent("processing started");
  
  // Your work here
  
} catch (error) {
  span.recordException(error as Error);
  span.setStatus({ code: 2, message: (error as Error).message });
} finally {
  span.end();
}
```

## Custom Metrics

```typescript
import { metrics } from "@opentelemetry/api";

const meter = metrics.getMeter("my-meter");

// Counter
const counter = meter.createCounter("requests_total");
counter.add(1, { route: "/api/users", method: "GET" });

// Histogram
const histogram = meter.createHistogram("request_duration_ms");
histogram.record(150, { route: "/api/users" });

// Observable Gauge
const gauge = meter.createObservableGauge("active_connections");
gauge.addCallback((result) => {
  result.observe(getActiveConnections(), { pool: "main" });
});
```

## Manual Exporter Setup

### Trace Exporter

```typescript
import { AzureMonitorTraceExporter } from "@azure/monitor-opentelemetry-exporter";
import { NodeTracerProvider, BatchSpanProcessor } from "@opentelemetry/sdk-trace-node";

const exporter = new AzureMonitorTraceExporter({
  connectionString: process.env.APPLICATIONINSIGHTS_CONNECTION_STRING
});

const provider = new NodeTracerProvider({
  spanProcessors: [new BatchSpanProcessor(exporter)]
});

provider.register();
```

### Metric Exporter

```typescript
import { AzureMonitorMetricExporter } from "@azure/monitor-opentelemetry-exporter";
import { PeriodicExportingMetricReader, MeterProvider } from "@opentelemetry/sdk-metrics";
import { metrics } from "@opentelemetry/api";

const exporter = new AzureMonitorMetricExporter({
  connectionString: process.env.APPLICATIONINSIGHTS_CONNECTION_STRING
});

const meterProvider = new MeterProvider({
  readers: [new PeriodicExportingMetricReader({ exporter })]
});

metrics.setGlobalMeterProvider(meterProvider);
```

### Log Exporter

```typescript
import { AzureMonitorLogExporter } from "@azure/monitor-opentelemetry-exporter";
import { BatchLogRecordProcessor, LoggerProvider } from "@opentelemetry/sdk-logs";
import { logs } from "@opentelemetry/api-logs";

const exporter = new AzureMonitorLogExporter({
  connectionString: process.env.APPLICATIONINSIGHTS_CONNECTION_STRING
});

const loggerProvider = new LoggerProvider();
loggerProvider.addLogRecordProcessor(new BatchLogRecordProcessor(exporter));

logs.setGlobalLoggerProvider(loggerProvider);
```

## Custom Logs Ingestion

```typescript
import { DefaultAzureCredential } from "@azure/identity";
import { LogsIngestionClient, isAggregateLogsUploadError } from "@azure/monitor-ingestion";

const endpoint = "https://<dce>.ingest.monitor.azure.com";
const ruleId = "<data-collection-rule-id>";
const streamName = "Custom-MyTable_CL";

const client = new LogsIngestionClient(endpoint, new DefaultAzureCredential());

const logs = [
  {
    Time: new Date().toISOString(),
    Computer: "Server1",
    Message: "Application started",
    Level: "Information"
  }
];

try {
  await client.upload(ruleId, streamName, logs);
} catch (error) {
  if (isAggregateLogsUploadError(error)) {
    for (const uploadError of error.errors) {
      console.error("Failed logs:", uploadError.failedLogs);
    }
  }
}
```

## Custom Span Processor

```typescript
import { SpanProcessor, ReadableSpan } from "@opentelemetry/sdk-trace-base";
import { Span, Context, SpanKind, TraceFlags } from "@opentelemetry/api";
import { useAzureMonitor } from "@azure/monitor-opentelemetry";

class FilteringSpanProcessor implements SpanProcessor {
  forceFlush(): Promise<void> { return Promise.resolve(); }
  shutdown(): Promise<void> { return Promise.resolve(); }
  onStart(span: Span, context: Context): void {}
  
  onEnd(span: ReadableSpan): void {
    // Add custom attributes
    span.attributes["CustomDimension"] = "value";
    
    // Filter out internal spans
    if (span.kind === SpanKind.INTERNAL) {
      span.spanContext().traceFlags = TraceFlags.NONE;
    }
  }
}

useAzureMonitor({
  spanProcessors: [new FilteringSpanProcessor()]
});
```

## Sampling

```typescript
import { ApplicationInsightsSampler } from "@azure/monitor-opentelemetry-exporter";
import { NodeTracerProvider } from "@opentelemetry/sdk-trace-node";

// Sample 75% of traces
const sampler = new ApplicationInsightsSampler(0.75);

const provider = new NodeTracerProvider({ sampler });
```

## Shutdown

```typescript
import { useAzureMonitor, shutdownAzureMonitor } from "@azure/monitor-opentelemetry";

useAzureMonitor();

// On application shutdown
process.on("SIGTERM", async () => {
  await shutdownAzureMonitor();
  process.exit(0);
});
```

## Key Types

```typescript
import {
  useAzureMonitor,
  shutdownAzureMonitor,
  AzureMonitorOpenTelemetryOptions,
  InstrumentationOptions
} from "@azure/monitor-opentelemetry";

import {
  AzureMonitorTraceExporter,
  AzureMonitorMetricExporter,
  AzureMonitorLogExporter,
  ApplicationInsightsSampler,
  AzureMonitorExporterOptions
} from "@azure/monitor-opentelemetry-exporter";

import {
  LogsIngestionClient,
  isAggregateLogsUploadError
} from "@azure/monitor-ingestion";
```

## Best Practices

1. **Call useAzureMonitor() first** - Before importing other modules
2. **Use ESM loader for ESM projects** - `--import @azure/monitor-opentelemetry/loader`
3. **Enable offline storage** - For reliable telemetry in disconnected scenarios
4. **Set sampling ratio** - For high-traffic applications
5. **Add custom dimensions** - Use span processors for enrichment
6. **Graceful shutdown** - Call `shutdownAzureMonitor()` to flush telemetry

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

# Azure Monitor OpenTelemetry Exporter for Java

> **⚠️ DEPRECATION NOTICE**: This package is deprecated. Migrate to `azure-monitor-opentelemetry-autoconfigure`.
>
> See [Migration Guide](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/monitor/azure-monitor-opentelemetry-exporter/MIGRATION.md) for detailed instructions.

Export OpenTelemetry telemetry data to Azure Monitor / Application Insights.

## Installation (Deprecated)

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-monitor-opentelemetry-exporter</artifactId>
    <version>1.0.0-beta.x</version>
</dependency>
```

## Recommended: Use Autoconfigure Instead

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-monitor-opentelemetry-autoconfigure</artifactId>
    <version>LATEST</version>
</dependency>
```

## Environment Variables

```bash
APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=xxx;IngestionEndpoint=https://xxx.in.applicationinsights.azure.com/
```

## Basic Setup with Autoconfigure (Recommended)

### Using Environment Variable

```java
import io.opentelemetry.sdk.autoconfigure.AutoConfiguredOpenTelemetrySdk;
import io.opentelemetry.sdk.autoconfigure.AutoConfiguredOpenTelemetrySdkBuilder;
import io.opentelemetry.api.OpenTelemetry;
import com.azure.monitor.opentelemetry.exporter.AzureMonitorExporter;

// Connection string from APPLICATIONINSIGHTS_CONNECTION_STRING env var
AutoConfiguredOpenTelemetrySdkBuilder sdkBuilder = AutoConfiguredOpenTelemetrySdk.builder();
AzureMonitorExporter.customize(sdkBuilder);
OpenTelemetry openTelemetry = sdkBuilder.build().getOpenTelemetrySdk();
```

### With Explicit Connection String

```java
AutoConfiguredOpenTelemetrySdkBuilder sdkBuilder = AutoConfiguredOpenTelemetrySdk.builder();
AzureMonitorExporter.customize(sdkBuilder, "{connection-string}");
OpenTelemetry openTelemetry = sdkBuilder.build().getOpenTelemetrySdk();
```

## Creating Spans

```java
import io.opentelemetry.api.trace.Tracer;
import io.opentelemetry.api.trace.Span;
import io.opentelemetry.context.Scope;

// Get tracer
Tracer tracer = openTelemetry.getTracer("com.example.myapp");

// Create span
Span span = tracer.spanBuilder("myOperation").startSpan();

try (Scope scope = span.makeCurrent()) {
    // Your application logic
    doWork();
} catch (Throwable t) {
    span.recordException(t);
    throw t;
} finally {
    span.end();
}
```

## Adding Span Attributes

```java
import io.opentelemetry.api.common.AttributeKey;
import io.opentelemetry.api.common.Attributes;

Span span = tracer.spanBuilder("processOrder")
    .setAttribute("order.id", "12345")
    .setAttribute("customer.tier", "premium")
    .startSpan();

try (Scope scope = span.makeCurrent()) {
    // Add attributes during execution
    span.setAttribute("items.count", 3);
    span.setAttribute("total.amount", 99.99);
    
    processOrder();
} finally {
    span.end();
}
```

## Custom Span Processor

```java
import io.opentelemetry.sdk.trace.SpanProcessor;
import io.opentelemetry.sdk.trace.ReadWriteSpan;
import io.opentelemetry.sdk.trace.ReadableSpan;
import io.opentelemetry.context.Context;

private static final AttributeKey<String> CUSTOM_ATTR = AttributeKey.stringKey("custom.attribute");

SpanProcessor customProcessor = new SpanProcessor() {
    @Override
    public void onStart(Context context, ReadWriteSpan span) {
        // Add custom attribute to every span
        span.setAttribute(CUSTOM_ATTR, "customValue");
    }

    @Override
    public boolean isStartRequired() {
        return true;
    }

    @Override
    public void onEnd(ReadableSpan span) {
        // Post-processing if needed
    }

    @Override
    public boolean isEndRequired() {
        return false;
    }
};

// Register processor
AutoConfiguredOpenTelemetrySdkBuilder sdkBuilder = AutoConfiguredOpenTelemetrySdk.builder();
AzureMonitorExporter.customize(sdkBuilder);

sdkBuilder.addTracerProviderCustomizer(
    (sdkTracerProviderBuilder, configProperties) -> 
        sdkTracerProviderBuilder.addSpanProcessor(customProcessor)
);

OpenTelemetry openTelemetry = sdkBuilder.build().getOpenTelemetrySdk();
```

## Nested Spans

```java
public void parentOperation() {
    Span parentSpan = tracer.spanBuilder("parentOperation").startSpan();
    try (Scope scope = parentSpan.makeCurrent()) {
        childOperation();
    } finally {
        parentSpan.end();
    }
}

public void childOperation() {
    // Automatically links to parent via Context
    Span childSpan = tracer.spanBuilder("childOperation").startSpan();
    try (Scope scope = childSpan.makeCurrent()) {
        // Child work
    } finally {
        childSpan.end();
    }
}
```

## Recording Exceptions

```java
Span span = tracer.spanBuilder("riskyOperation").startSpan();
try (Scope scope = span.makeCurrent()) {
    performRiskyWork();
} catch (Exception e) {
    span.recordException(e);
    span.setStatus(StatusCode.ERROR, e.getMessage());
    throw e;
} finally {
    span.end();
}
```

## Metrics (via OpenTelemetry)

```java
import io.opentelemetry.api.metrics.Meter;
import io.opentelemetry.api.metrics.LongCounter;
import io.opentelemetry.api.metrics.LongHistogram;

Meter meter = openTelemetry.getMeter("com.example.myapp");

// Counter
LongCounter requestCounter = meter.counterBuilder("http.requests")
    .setDescription("Total HTTP requests")
    .setUnit("requests")
    .build();

requestCounter.add(1, Attributes.of(
    AttributeKey.stringKey("http.method"), "GET",
    AttributeKey.longKey("http.status_code"), 200L
));

// Histogram
LongHistogram latencyHistogram = meter.histogramBuilder("http.latency")
    .setDescription("Request latency")
    .setUnit("ms")
    .ofLongs()
    .build();

latencyHistogram.record(150, Attributes.of(
    AttributeKey.stringKey("http.route"), "/api/users"
));
```

## Key Concepts

| Concept | Description |
|---------|-------------|
| Connection String | Application Insights connection string with instrumentation key |
| Tracer | Creates spans for distributed tracing |
| Span | Represents a unit of work with timing and attributes |
| SpanProcessor | Intercepts span lifecycle for customization |
| Exporter | Sends telemetry to Azure Monitor |

## Migration to Autoconfigure

The `azure-monitor-opentelemetry-autoconfigure` package provides:
- Automatic instrumentation of common libraries
- Simplified configuration
- Better integration with OpenTelemetry SDK

### Migration Steps

1. Replace dependency:
   ```xml
   <!-- Remove -->
   <dependency>
       <groupId>com.azure</groupId>
       <artifactId>azure-monitor-opentelemetry-exporter</artifactId>
   </dependency>
   
   <!-- Add -->
   <dependency>
       <groupId>com.azure</groupId>
       <artifactId>azure-monitor-opentelemetry-autoconfigure</artifactId>
   </dependency>
   ```

2. Update initialization code per [Migration Guide](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/monitor/azure-monitor-opentelemetry-exporter/MIGRATION.md)

## Best Practices

1. **Use autoconfigure** — Migrate to `azure-monitor-opentelemetry-autoconfigure`
2. **Set meaningful span names** — Use descriptive operation names
3. **Add relevant attributes** — Include contextual data for debugging
4. **Handle exceptions** — Always record exceptions on spans
5. **Use semantic conventions** — Follow OpenTelemetry semantic conventions
6. **End spans in finally** — Ensure spans are always ended
7. **Use try-with-resources** — Scope management with try-with-resources pattern

## Reference Links

| Resource | URL |
|----------|-----|
| Maven Package | https://central.sonatype.com/artifact/com.azure/azure-monitor-opentelemetry-exporter |
| GitHub | https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/monitor/azure-monitor-opentelemetry-exporter |
| Migration Guide | https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/monitor/azure-monitor-opentelemetry-exporter/MIGRATION.md |
| Autoconfigure Package | https://central.sonatype.com/artifact/com.azure/azure-monitor-opentelemetry-autoconfigure |
| OpenTelemetry Java | https://opentelemetry.io/docs/languages/java/ |
| Application Insights | https://learn.microsoft.com/azure/azure-monitor/app/app-insights-overview |

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

# Azure Monitor OpenTelemetry Exporter for Python

Low-level exporter for sending OpenTelemetry traces, metrics, and logs to Application Insights.

## Installation

```bash
pip install azure-monitor-opentelemetry-exporter
```

## Environment Variables

```bash
APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=xxx;IngestionEndpoint=https://xxx.in.applicationinsights.azure.com/
```

## When to Use

| Scenario | Use |
|----------|-----|
| Quick setup, auto-instrumentation | `azure-monitor-opentelemetry` (distro) |
| Custom OpenTelemetry pipeline | `azure-monitor-opentelemetry-exporter` (this) |
| Fine-grained control over telemetry | `azure-monitor-opentelemetry-exporter` (this) |

## Trace Exporter

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter

# Create exporter
exporter = AzureMonitorTraceExporter(
    connection_string="InstrumentationKey=xxx;..."
)

# Configure tracer provider
trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(exporter)
)

# Use tracer
tracer = trace.get_tracer(__name__)
with tracer.start_as_current_span("my-span"):
    print("Hello, World!")
```

## Metric Exporter

```python
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from azure.monitor.opentelemetry.exporter import AzureMonitorMetricExporter

# Create exporter
exporter = AzureMonitorMetricExporter(
    connection_string="InstrumentationKey=xxx;..."
)

# Configure meter provider
reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
metrics.set_meter_provider(MeterProvider(metric_readers=[reader]))

# Use meter
meter = metrics.get_meter(__name__)
counter = meter.create_counter("requests_total")
counter.add(1, {"route": "/api/users"})
```

## Log Exporter

```python
import logging
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from azure.monitor.opentelemetry.exporter import AzureMonitorLogExporter

# Create exporter
exporter = AzureMonitorLogExporter(
    connection_string="InstrumentationKey=xxx;..."
)

# Configure logger provider
logger_provider = LoggerProvider()
logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
set_logger_provider(logger_provider)

# Add handler to Python logging
handler = LoggingHandler(level=logging.INFO, logger_provider=logger_provider)
logging.getLogger().addHandler(handler)

# Use logging
logger = logging.getLogger(__name__)
logger.info("This will be sent to Application Insights")
```

## From Environment Variable

Exporters read `APPLICATIONINSIGHTS_CONNECTION_STRING` automatically:

```python
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter

# Connection string from environment
exporter = AzureMonitorTraceExporter()
```

## Azure AD Authentication

```python
from azure.identity import DefaultAzureCredential
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter

exporter = AzureMonitorTraceExporter(
    credential=DefaultAzureCredential()
)
```

## Sampling

Use `ApplicationInsightsSampler` for consistent sampling:

```python
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.sampling import ParentBasedTraceIdRatio
from azure.monitor.opentelemetry.exporter import ApplicationInsightsSampler

# Sample 10% of traces
sampler = ApplicationInsightsSampler(sampling_ratio=0.1)

trace.set_tracer_provider(TracerProvider(sampler=sampler))
```

## Offline Storage

Configure offline storage for retry:

```python
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter

exporter = AzureMonitorTraceExporter(
    connection_string="...",
    storage_directory="/path/to/storage",  # Custom storage path
    disable_offline_storage=False  # Enable retry (default)
)
```

## Disable Offline Storage

```python
exporter = AzureMonitorTraceExporter(
    connection_string="...",
    disable_offline_storage=True  # No retry on failure
)
```

## Sovereign Clouds

```python
from azure.identity import AzureAuthorityHosts, DefaultAzureCredential
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter

# Azure Government
credential = DefaultAzureCredential(authority=AzureAuthorityHosts.AZURE_GOVERNMENT)
exporter = AzureMonitorTraceExporter(
    connection_string="InstrumentationKey=xxx;IngestionEndpoint=https://xxx.in.applicationinsights.azure.us/",
    credential=credential
)
```

## Exporter Types

| Exporter | Telemetry Type | Application Insights Table |
|----------|---------------|---------------------------|
| `AzureMonitorTraceExporter` | Traces/Spans | requests, dependencies, exceptions |
| `AzureMonitorMetricExporter` | Metrics | customMetrics, performanceCounters |
| `AzureMonitorLogExporter` | Logs | traces, customEvents |

## Configuration Options

| Parameter | Description | Default |
|-----------|-------------|---------|
| `connection_string` | Application Insights connection string | From env var |
| `credential` | Azure credential for AAD auth | None |
| `disable_offline_storage` | Disable retry storage | False |
| `storage_directory` | Custom storage path | Temp directory |

## Best Practices

1. **Use BatchSpanProcessor** for production (not SimpleSpanProcessor)
2. **Use ApplicationInsightsSampler** for consistent sampling across services
3. **Enable offline storage** for reliability in production
4. **Use AAD authentication** instead of instrumentation keys
5. **Set export intervals** appropriate for your workload
6. **Use the distro** (`azure-monitor-opentelemetry`) unless you need custom pipelines

---

# Azure Monitor Ingestion SDK for Python

Send custom logs to Azure Monitor Log Analytics workspace using the Logs Ingestion API.

## Installation

```bash
pip install azure-monitor-ingestion
pip install azure-identity
```

## Environment Variables

```bash
# Data Collection Endpoint (DCE)
AZURE_DCE_ENDPOINT=https://<dce-name>.<region>.ingest.monitor.azure.com

# Data Collection Rule (DCR) immutable ID
AZURE_DCR_RULE_ID=dcr-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Stream name from DCR
AZURE_DCR_STREAM_NAME=Custom-MyTable_CL
```

## Prerequisites

Before using this SDK, you need:

1. **Log Analytics Workspace** — Target for your logs
2. **Data Collection Endpoint (DCE)** — Ingestion endpoint
3. **Data Collection Rule (DCR)** — Defines schema and destination
4. **Custom Table** — In Log Analytics (created via DCR or manually)

## Authentication

```python
from azure.monitor.ingestion import LogsIngestionClient
from azure.identity import DefaultAzureCredential
import os

client = LogsIngestionClient(
    endpoint=os.environ["AZURE_DCE_ENDPOINT"],
    credential=DefaultAzureCredential()
)
```

## Upload Custom Logs

```python
from azure.monitor.ingestion import LogsIngestionClient
from azure.identity import DefaultAzureCredential
import os

client = LogsIngestionClient(
    endpoint=os.environ["AZURE_DCE_ENDPOINT"],
    credential=DefaultAzureCredential()
)

rule_id = os.environ["AZURE_DCR_RULE_ID"]
stream_name = os.environ["AZURE_DCR_STREAM_NAME"]

logs = [
    {"TimeGenerated": "2024-01-15T10:00:00Z", "Computer": "server1", "Message": "Application started"},
    {"TimeGenerated": "2024-01-15T10:01:00Z", "Computer": "server1", "Message": "Processing request"},
    {"TimeGenerated": "2024-01-15T10:02:00Z", "Computer": "server2", "Message": "Connection established"}
]

client.upload(rule_id=rule_id, stream_name=stream_name, logs=logs)
```

## Upload from JSON File

```python
import json

with open("logs.json", "r") as f:
    logs = json.load(f)

client.upload(rule_id=rule_id, stream_name=stream_name, logs=logs)
```

## Custom Error Handling

Handle partial failures with a callback:

```python
failed_logs = []

def on_error(error):
    print(f"Upload failed: {error.error}")
    failed_logs.extend(error.failed_logs)

client.upload(
    rule_id=rule_id,
    stream_name=stream_name,
    logs=logs,
    on_error=on_error
)

# Retry failed logs
if failed_logs:
    print(f"Retrying {len(failed_logs)} failed logs...")
    client.upload(rule_id=rule_id, stream_name=stream_name, logs=failed_logs)
```

## Ignore Errors

```python
def ignore_errors(error):
    pass  # Silently ignore upload failures

client.upload(
    rule_id=rule_id,
    stream_name=stream_name,
    logs=logs,
    on_error=ignore_errors
)
```

## Async Client

```python
import asyncio
from azure.monitor.ingestion.aio import LogsIngestionClient
from azure.identity.aio import DefaultAzureCredential

async def upload_logs():
    async with LogsIngestionClient(
        endpoint=endpoint,
        credential=DefaultAzureCredential()
    ) as client:
        await client.upload(
            rule_id=rule_id,
            stream_name=stream_name,
            logs=logs
        )

asyncio.run(upload_logs())
```

## Sovereign Clouds

```python
from azure.identity import AzureAuthorityHosts, DefaultAzureCredential
from azure.monitor.ingestion import LogsIngestionClient

# Azure Government
credential = DefaultAzureCredential(authority=AzureAuthorityHosts.AZURE_GOVERNMENT)
client = LogsIngestionClient(
    endpoint="https://example.ingest.monitor.azure.us",
    credential=credential,
    credential_scopes=["https://monitor.azure.us/.default"]
)
```

## Batching Behavior

The SDK automatically:
- Splits logs into chunks of 1MB or less
- Compresses each chunk with gzip
- Uploads chunks in parallel

No manual batching needed for large log sets.

## Client Types

| Client | Purpose |
|--------|---------|
| `LogsIngestionClient` | Sync client for uploading logs |
| `LogsIngestionClient` (aio) | Async client for uploading logs |

## Key Concepts

| Concept | Description |
|---------|-------------|
| **DCE** | Data Collection Endpoint — ingestion URL |
| **DCR** | Data Collection Rule — defines schema, transformations, destination |
| **Stream** | Named data flow within a DCR |
| **Custom Table** | Target table in Log Analytics (ends with `_CL`) |

## DCR Stream Name Format

Stream names follow patterns:
- `Custom-<TableName>_CL` — For custom tables
- `Microsoft-<TableName>` — For built-in tables

## Best Practices

1. **Use DefaultAzureCredential** for authentication
2. **Handle errors gracefully** — use `on_error` callback for partial failures
3. **Include TimeGenerated** — Required field for all logs
4. **Match DCR schema** — Log fields must match DCR column definitions
5. **Use async client** for high-throughput scenarios
6. **Batch uploads** — SDK handles batching, but send reasonable chunks
7. **Monitor ingestion** — Check Log Analytics for ingestion status
8. **Use context manager** — Ensures proper client cleanup

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

# Azure Monitor Query SDK for Java

> **DEPRECATION NOTICE**: This package is deprecated in favor of:
> - `azure-monitor-query-logs` — For Log Analytics queries
> - `azure-monitor-query-metrics` — For metrics queries
>
> See migration guides: [Logs Migration](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/monitor/azure-monitor-query-logs/migration-guide.md) | [Metrics Migration](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/monitor/azure-monitor-query-metrics/migration-guide.md)

Client library for querying Azure Monitor Logs and Metrics.

## Installation

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-monitor-query</artifactId>
    <version>1.5.9</version>
</dependency>
```

Or use Azure SDK BOM:

```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>com.azure</groupId>
            <artifactId>azure-sdk-bom</artifactId>
            <version>{bom_version}</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>

<dependencies>
    <dependency>
        <groupId>com.azure</groupId>
        <artifactId>azure-monitor-query</artifactId>
    </dependency>
</dependencies>
```

## Prerequisites

- Log Analytics workspace (for logs queries)
- Azure resource (for metrics queries)
- TokenCredential with appropriate permissions

## Environment Variables

```bash
LOG_ANALYTICS_WORKSPACE_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
AZURE_RESOURCE_ID=/subscriptions/{sub}/resourceGroups/{rg}/providers/{provider}/{resource}
```

## Client Creation

### LogsQueryClient (Sync)

```java
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.azure.monitor.query.LogsQueryClient;
import com.azure.monitor.query.LogsQueryClientBuilder;

LogsQueryClient logsClient = new LogsQueryClientBuilder()
    .credential(new DefaultAzureCredentialBuilder().build())
    .buildClient();
```

### LogsQueryAsyncClient

```java
import com.azure.monitor.query.LogsQueryAsyncClient;

LogsQueryAsyncClient logsAsyncClient = new LogsQueryClientBuilder()
    .credential(new DefaultAzureCredentialBuilder().build())
    .buildAsyncClient();
```

### MetricsQueryClient (Sync)

```java
import com.azure.monitor.query.MetricsQueryClient;
import com.azure.monitor.query.MetricsQueryClientBuilder;

MetricsQueryClient metricsClient = new MetricsQueryClientBuilder()
    .credential(new DefaultAzureCredentialBuilder().build())
    .buildClient();
```

### MetricsQueryAsyncClient

```java
import com.azure.monitor.query.MetricsQueryAsyncClient;

MetricsQueryAsyncClient metricsAsyncClient = new MetricsQueryClientBuilder()
    .credential(new DefaultAzureCredentialBuilder().build())
    .buildAsyncClient();
```

### Sovereign Cloud Configuration

```java
// Azure China Cloud - Logs
LogsQueryClient logsClient = new LogsQueryClientBuilder()
    .credential(new DefaultAzureCredentialBuilder().build())
    .endpoint("https://api.loganalytics.azure.cn/v1")
    .buildClient();

// Azure China Cloud - Metrics
MetricsQueryClient metricsClient = new MetricsQueryClientBuilder()
    .credential(new DefaultAzureCredentialBuilder().build())
    .endpoint("https://management.chinacloudapi.cn")
    .buildClient();
```

## Key Concepts

| Concept | Description |
|---------|-------------|
| Logs | Log and performance data from Azure resources via Kusto Query Language |
| Metrics | Numeric time-series data collected at regular intervals |
| Workspace ID | Log Analytics workspace identifier |
| Resource ID | Azure resource URI for metrics queries |
| QueryTimeInterval | Time range for the query |

## Logs Query Operations

### Basic Query

```java
import com.azure.monitor.query.models.LogsQueryResult;
import com.azure.monitor.query.models.LogsTableRow;
import com.azure.monitor.query.models.QueryTimeInterval;
import java.time.Duration;

LogsQueryResult result = logsClient.queryWorkspace(
    "{workspace-id}",
    "AzureActivity | summarize count() by ResourceGroup | top 10 by count_",
    new QueryTimeInterval(Duration.ofDays(7))
);

for (LogsTableRow row : result.getTable().getRows()) {
    System.out.println(row.getColumnValue("ResourceGroup") + ": " + row.getColumnValue("count_"));
}
```

### Query by Resource ID

```java
LogsQueryResult result = logsClient.queryResource(
    "{resource-id}",
    "AzureMetrics | where TimeGenerated > ago(1h)",
    new QueryTimeInterval(Duration.ofDays(1))
);

for (LogsTableRow row : result.getTable().getRows()) {
    System.out.println(row.getColumnValue("MetricName") + " " + row.getColumnValue("Average"));
}
```

### Map Results to Custom Model

```java
// Define model class
public class ActivityLog {
    private String resourceGroup;
    private String operationName;
    
    public String getResourceGroup() { return resourceGroup; }
    public String getOperationName() { return operationName; }
}

// Query with model mapping
List<ActivityLog> logs = logsClient.queryWorkspace(
    "{workspace-id}",
    "AzureActivity | project ResourceGroup, OperationName | take 100",
    new QueryTimeInterval(Duration.ofDays(2)),
    ActivityLog.class
);

for (ActivityLog log : logs) {
    System.out.println(log.getOperationName() + " - " + log.getResourceGroup());
}
```

### Batch Query

```java
import com.azure.monitor.query.models.LogsBatchQuery;
import com.azure.monitor.query.models.LogsBatchQueryResult;
import com.azure.monitor.query.models.LogsBatchQueryResultCollection;
import com.azure.core.util.Context;

LogsBatchQuery batchQuery = new LogsBatchQuery();
String q1 = batchQuery.addWorkspaceQuery("{workspace-id}", "AzureActivity | count", new QueryTimeInterval(Duration.ofDays(1)));
String q2 = batchQuery.addWorkspaceQuery("{workspace-id}", "Heartbeat | count", new QueryTimeInterval(Duration.ofDays(1)));
String q3 = batchQuery.addWorkspaceQuery("{workspace-id}", "Perf | count", new QueryTimeInterval(Duration.ofDays(1)));

LogsBatchQueryResultCollection results = logsClient
    .queryBatchWithResponse(batchQuery, Context.NONE)
    .getValue();

LogsBatchQueryResult result1 = results.getResult(q1);
LogsBatchQueryResult result2 = results.getResult(q2);
LogsBatchQueryResult result3 = results.getResult(q3);

// Check for failures
if (result3.getQueryResultStatus() == LogsQueryResultStatus.FAILURE) {
    System.err.println("Query failed: " + result3.getError().getMessage());
}
```

### Query with Options

```java
import com.azure.monitor.query.models.LogsQueryOptions;
import com.azure.core.http.rest.Response;

LogsQueryOptions options = new LogsQueryOptions()
    .setServerTimeout(Duration.ofMinutes(10))
    .setIncludeStatistics(true)
    .setIncludeVisualization(true);

Response<LogsQueryResult> response = logsClient.queryWorkspaceWithResponse(
    "{workspace-id}",
    "AzureActivity | summarize count() by bin(TimeGenerated, 1h)",
    new QueryTimeInterval(Duration.ofDays(7)),
    options,
    Context.NONE
);

LogsQueryResult result = response.getValue();

// Access statistics
BinaryData statistics = result.getStatistics();
// Access visualization data
BinaryData visualization = result.getVisualization();
```

### Query Multiple Workspaces

```java
import java.util.Arrays;

LogsQueryOptions options = new LogsQueryOptions()
    .setAdditionalWorkspaces(Arrays.asList("{workspace-id-2}", "{workspace-id-3}"));

Response<LogsQueryResult> response = logsClient.queryWorkspaceWithResponse(
    "{workspace-id-1}",
    "AzureActivity | summarize count() by TenantId",
    new QueryTimeInterval(Duration.ofDays(1)),
    options,
    Context.NONE
);
```

## Metrics Query Operations

### Basic Metrics Query

```java
import com.azure.monitor.query.models.MetricsQueryResult;
import com.azure.monitor.query.models.MetricResult;
import com.azure.monitor.query.models.TimeSeriesElement;
import com.azure.monitor.query.models.MetricValue;
import java.util.Arrays;

MetricsQueryResult result = metricsClient.queryResource(
    "{resource-uri}",
    Arrays.asList("SuccessfulCalls", "TotalCalls")
);

for (MetricResult metric : result.getMetrics()) {
    System.out.println("Metric: " + metric.getMetricName());
    for (TimeSeriesElement ts : metric.getTimeSeries()) {
        System.out.println("  Dimensions: " + ts.getMetadata());
        for (MetricValue value : ts.getValues()) {
            System.out.println("    " + value.getTimeStamp() + ": " + value.getTotal());
        }
    }
}
```

### Metrics with Aggregations

```java
import com.azure.monitor.query.models.MetricsQueryOptions;
import com.azure.monitor.query.models.AggregationType;

Response<MetricsQueryResult> response = metricsClient.queryResourceWithResponse(
    "{resource-id}",
    Arrays.asList("SuccessfulCalls", "TotalCalls"),
    new MetricsQueryOptions()
        .setGranularity(Duration.ofHours(1))
        .setAggregations(Arrays.asList(AggregationType.AVERAGE, AggregationType.COUNT)),
    Context.NONE
);

MetricsQueryResult result = response.getValue();
```

### Query Multiple Resources (MetricsClient)

```java
import com.azure.monitor.query.MetricsClient;
import com.azure.monitor.query.MetricsClientBuilder;
import com.azure.monitor.query.models.MetricsQueryResourcesResult;

MetricsClient metricsClient = new MetricsClientBuilder()
    .credential(new DefaultAzureCredentialBuilder().build())
    .endpoint("{endpoint}")
    .buildClient();

MetricsQueryResourcesResult result = metricsClient.queryResources(
    Arrays.asList("{resourceId1}", "{resourceId2}"),
    Arrays.asList("{metric1}", "{metric2}"),
    "{metricNamespace}"
);

for (MetricsQueryResult queryResult : result.getMetricsQueryResults()) {
    for (MetricResult metric : queryResult.getMetrics()) {
        System.out.println(metric.getMetricName());
        metric.getTimeSeries().stream()
            .flatMap(ts -> ts.getValues().stream())
            .forEach(mv -> System.out.println(
                mv.getTimeStamp() + " Count=" + mv.getCount() + " Avg=" + mv.getAverage()));
    }
}
```

## Response Structure

### Logs Response Hierarchy

```
LogsQueryResult
├── statistics (BinaryData)
├── visualization (BinaryData)
├── error
└── tables (List<LogsTable>)
    ├── name
    ├── columns (List<LogsTableColumn>)
    │   ├── name
    │   └── type
    └── rows (List<LogsTableRow>)
        ├── rowIndex
        └── rowCells (List<LogsTableCell>)
```

### Metrics Response Hierarchy

```
MetricsQueryResult
├── granularity
├── timeInterval
├── namespace
├── resourceRegion
└── metrics (List<MetricResult>)
    ├── id, name, type, unit
    └── timeSeries (List<TimeSeriesElement>)
        ├── metadata (dimensions)
        └── values (List<MetricValue>)
            ├── timeStamp
            ├── count, average, total
            ├── maximum, minimum
```

## Error Handling

```java
import com.azure.core.exception.HttpResponseException;
import com.azure.monitor.query.models.LogsQueryResultStatus;

try {
    LogsQueryResult result = logsClient.queryWorkspace(workspaceId, query, timeInterval);
    
    // Check partial failure
    if (result.getStatus() == LogsQueryResultStatus.PARTIAL_FAILURE) {
        System.err.println("Partial failure: " + result.getError().getMessage());
    }
} catch (HttpResponseException e) {
    System.err.println("Query failed: " + e.getMessage());
    System.err.println("Status: " + e.getResponse().getStatusCode());
}
```

## Best Practices

1. **Use batch queries** — Combine multiple queries into a single request
2. **Set appropriate timeouts** — Long queries may need extended server timeout
3. **Limit result size** — Use `top` or `take` in Kusto queries
4. **Use projections** — Select only needed columns with `project`
5. **Check query status** — Handle PARTIAL_FAILURE results gracefully
6. **Cache results** — Metrics don't change frequently; cache when appropriate
7. **Migrate to new packages** — Plan migration to `azure-monitor-query-logs` and `azure-monitor-query-metrics`

## Reference Links

| Resource | URL |
|----------|-----|
| Maven Package | https://central.sonatype.com/artifact/com.azure/azure-monitor-query |
| GitHub | https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/monitor/azure-monitor-query |
| API Reference | https://learn.microsoft.com/java/api/com.azure.monitor.query |
| Kusto Query Language | https://learn.microsoft.com/azure/data-explorer/kusto/query/ |
| Log Analytics Limits | https://learn.microsoft.com/azure/azure-monitor/service-limits#la-query-api |
| Troubleshooting | https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/monitor/azure-monitor-query/TROUBLESHOOTING.md |

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---
