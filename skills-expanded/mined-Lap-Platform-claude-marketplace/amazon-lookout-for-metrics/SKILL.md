---
name: amazon-lookout-for-metrics
description: "Amazon Lookout for Metrics API skill. Use when working with Amazon Lookout for Metrics for ActivateAnomalyDetector, BackTestAnomalyDetector, CreateAlert. Covers 30 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon Lookout for Metrics
API version: 2017-07-25

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /tags/{resourceArn} -- verify access
3. POST /ActivateAnomalyDetector -- create first ActivateAnomalyDetector

## Endpoints

30 endpoints across 28 groups. See references/api-spec.lap for full details.

### ActivateAnomalyDetector
| Method | Path | Description |
|--------|------|-------------|
| POST | /ActivateAnomalyDetector | Activates an anomaly detector. |

### BackTestAnomalyDetector
| Method | Path | Description |
|--------|------|-------------|
| POST | /BackTestAnomalyDetector | Runs a backtest for anomaly detection for the specified resource. |

### CreateAlert
| Method | Path | Description |
|--------|------|-------------|
| POST | /CreateAlert | Creates an alert for an anomaly detector. |

### CreateAnomalyDetector
| Method | Path | Description |
|--------|------|-------------|
| POST | /CreateAnomalyDetector | Creates an anomaly detector. |

### CreateMetricSet
| Method | Path | Description |
|--------|------|-------------|
| POST | /CreateMetricSet | Creates a dataset. |

### DeactivateAnomalyDetector
| Method | Path | Description |
|--------|------|-------------|
| POST | /DeactivateAnomalyDetector | Deactivates an anomaly detector. |

### DeleteAlert
| Method | Path | Description |
|--------|------|-------------|
| POST | /DeleteAlert | Deletes an alert. |

### DeleteAnomalyDetector
| Method | Path | Description |
|--------|------|-------------|
| POST | /DeleteAnomalyDetector | Deletes a detector. Deleting an anomaly detector will delete all of its corresponding resources including any configured datasets and alerts. |

### DescribeAlert
| Method | Path | Description |
|--------|------|-------------|
| POST | /DescribeAlert | Describes an alert. Amazon Lookout for Metrics API actions are eventually consistent. If you do a read operation on a resource immediately after creating or modifying it, use retries to allow time for the write operation to complete. |

### DescribeAnomalyDetectionExecutions
| Method | Path | Description |
|--------|------|-------------|
| POST | /DescribeAnomalyDetectionExecutions | Returns information about the status of the specified anomaly detection jobs. |

### DescribeAnomalyDetector
| Method | Path | Description |
|--------|------|-------------|
| POST | /DescribeAnomalyDetector | Describes a detector. Amazon Lookout for Metrics API actions are eventually consistent. If you do a read operation on a resource immediately after creating or modifying it, use retries to allow time for the write operation to complete. |

### DescribeMetricSet
| Method | Path | Description |
|--------|------|-------------|
| POST | /DescribeMetricSet | Describes a dataset. Amazon Lookout for Metrics API actions are eventually consistent. If you do a read operation on a resource immediately after creating or modifying it, use retries to allow time for the write operation to complete. |

### DetectMetricSetConfig
| Method | Path | Description |
|--------|------|-------------|
| POST | /DetectMetricSetConfig | Detects an Amazon S3 dataset's file format, interval, and offset. |

### GetAnomalyGroup
| Method | Path | Description |
|--------|------|-------------|
| POST | /GetAnomalyGroup | Returns details about a group of anomalous metrics. |

### GetDataQualityMetrics
| Method | Path | Description |
|--------|------|-------------|
| POST | /GetDataQualityMetrics | Returns details about the requested data quality metrics. |

### GetFeedback
| Method | Path | Description |
|--------|------|-------------|
| POST | /GetFeedback | Get feedback for an anomaly group. |

### GetSampleData
| Method | Path | Description |
|--------|------|-------------|
| POST | /GetSampleData | Returns a selection of sample records from an Amazon S3 datasource. |

### ListAlerts
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListAlerts | Lists the alerts attached to a detector. Amazon Lookout for Metrics API actions are eventually consistent. If you do a read operation on a resource immediately after creating or modifying it, use retries to allow time for the write operation to complete. |

### ListAnomalyDetectors
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListAnomalyDetectors | Lists the detectors in the current AWS Region. Amazon Lookout for Metrics API actions are eventually consistent. If you do a read operation on a resource immediately after creating or modifying it, use retries to allow time for the write operation to complete. |

### ListAnomalyGroupRelatedMetrics
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListAnomalyGroupRelatedMetrics | Returns a list of measures that are potential causes or effects of an anomaly group. |

### ListAnomalyGroupSummaries
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListAnomalyGroupSummaries | Returns a list of anomaly groups. |

### ListAnomalyGroupTimeSeries
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListAnomalyGroupTimeSeries | Gets a list of anomalous metrics for a measure in an anomaly group. |

### ListMetricSets
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListMetricSets | Lists the datasets in the current AWS Region. Amazon Lookout for Metrics API actions are eventually consistent. If you do a read operation on a resource immediately after creating or modifying it, use retries to allow time for the write operation to complete. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{resourceArn} | Gets a list of tags for a detector, dataset, or alert. |
| POST | /tags/{resourceArn} | Adds tags to a detector, dataset, or alert. |
| DELETE | /tags/{resourceArn} | Removes tags from a detector, dataset, or alert. |

### PutFeedback
| Method | Path | Description |
|--------|------|-------------|
| POST | /PutFeedback | Add feedback for an anomalous metric. |

### UpdateAlert
| Method | Path | Description |
|--------|------|-------------|
| POST | /UpdateAlert | Make changes to an existing alert. |

### UpdateAnomalyDetector
| Method | Path | Description |
|--------|------|-------------|
| POST | /UpdateAnomalyDetector | Updates a detector. After activation, you can only change a detector's ingestion delay and description. |

### UpdateMetricSet
| Method | Path | Description |
|--------|------|-------------|
| POST | /UpdateMetricSet | Updates a dataset. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a ActivateAnomalyDetector?" -> POST /ActivateAnomalyDetector
- "Create a BackTestAnomalyDetector?" -> POST /BackTestAnomalyDetector
- "Create a CreateAlert?" -> POST /CreateAlert
- "Create a CreateAnomalyDetector?" -> POST /CreateAnomalyDetector
- "Create a CreateMetricSet?" -> POST /CreateMetricSet
- "Create a DeactivateAnomalyDetector?" -> POST /DeactivateAnomalyDetector
- "Create a DeleteAlert?" -> POST /DeleteAlert
- "Create a DeleteAnomalyDetector?" -> POST /DeleteAnomalyDetector
- "Create a DescribeAlert?" -> POST /DescribeAlert
- "Create a DescribeAnomalyDetectionExecution?" -> POST /DescribeAnomalyDetectionExecutions
- "Create a DescribeAnomalyDetector?" -> POST /DescribeAnomalyDetector
- "Create a DescribeMetricSet?" -> POST /DescribeMetricSet
- "Create a DetectMetricSetConfig?" -> POST /DetectMetricSetConfig
- "Create a GetAnomalyGroup?" -> POST /GetAnomalyGroup
- "Create a GetDataQualityMetric?" -> POST /GetDataQualityMetrics
- "Create a GetFeedback?" -> POST /GetFeedback
- "Create a GetSampleData?" -> POST /GetSampleData
- "Create a ListAlert?" -> POST /ListAlerts
- "Create a ListAnomalyDetector?" -> POST /ListAnomalyDetectors
- "Create a ListAnomalyGroupRelatedMetric?" -> POST /ListAnomalyGroupRelatedMetrics
- "Create a ListAnomalyGroupSummary?" -> POST /ListAnomalyGroupSummaries
- "Create a ListAnomalyGroupTimeSery?" -> POST /ListAnomalyGroupTimeSeries
- "Create a ListMetricSet?" -> POST /ListMetricSets
- "Get tag details?" -> GET /tags/{resourceArn}
- "Create a PutFeedback?" -> POST /PutFeedback
- "Delete a tag?" -> DELETE /tags/{resourceArn}
- "Create a UpdateAlert?" -> POST /UpdateAlert
- "Create a UpdateAnomalyDetector?" -> POST /UpdateAnomalyDetector
- "Create a UpdateMetricSet?" -> POST /UpdateMetricSet
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
