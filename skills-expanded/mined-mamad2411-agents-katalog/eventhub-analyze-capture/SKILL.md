---
name: eventhub-analyze-capture
description: Analyze Azure Event Hubs Capture configuration and delivery to Azure Blob Storage or Data Lake Storage, including destination, intervals, file creation, permissions, gaps, and downstream consumption. Use for archival, replay, lake ingestion, or missing-capture investigations.
---

# Analyze Capture

1. Identify event hub, Capture configuration, destination, interval/window, and downstream use.
2. Inspect whether Capture is enabled and events/files are being written as expected.
3. Check destination permissions, storage availability, naming/path behavior, and time-window gaps.
4. Correlate Capture gaps with Event Hubs ingress and storage evidence.
5. Separate Capture failure from producer ingestion failure.
6. Do not delete captured data or alter retention unless explicitly authorized.

## Output
- Capture Configuration
- Delivery Evidence
- Storage/Permission Findings
- Gap Assessment
- Recommended Action
