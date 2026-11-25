---
name: log-aggregation
description: Design and implement centralized log aggregation pipelines using ELK Stack, CloudWatch Logs, or Loki. Outputs shipper configuration, parsing rules, retention policies, and search/alerting setup.
argument-hint: [infrastructure type, log sources, volume estimate, alerting requirements]
allowed-tools: Read, Write, Bash
---

# Log Aggregation

Centralize logs from all services into a searchable, structured system. The goal: any engineer can find the root cause of any incident using logs alone, within 5 minutes.

## Process

1. **Inventory log sources** — apps, infra, load balancers, CDN, databases.
2. **Standardize log format** — structured JSON with common fields.
3. **Choose aggregation stack** — ELK, Loki+Grafana, CloudWatch, Datadog.
4. **Deploy log shippers** — Filebeat, Fluentd, or Vector per host/pod.
5. **Configure parsing pipelines** — extract structured fields from log lines.
6. **Set retention policies** — by severity, compliance requirements.
7. **Create index templates** — for efficient storage and querying.
8. **Build dashboards** — error rates, request logs, slow query detection.
9. **Configure alerts** — on error spikes, patterns, and anomalies.

## Output Format

### Structured Log Format (Application)

```python
# logging_config.py
import logging
import json
import sys
import time
import traceback
from datetime import datetime, timezone
from typing import Any

class StructuredFormatter(logging.Formatter):
    """JSON log formatter with standard fields."""
    
    SERVICE_NAME = "order-service"
    ENVIRONMENT = "production"
    
    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            # Standard fields (always present)
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname.lower(),
            "service": self.SERVICE_NAME,
            "environment": self.ENVIRONMENT,
            "message": record.getMessage(),
            
            # Source location
            "logger": record.name,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            
            # Context (set via logging.LoggerAdapter or contextvars)
            "trace_id": getattr(record, "trace_id", None),
            "span_id": getattr(record, "span_id", None),
            "request_id": getattr(record, "request_id", None),
            "user_id": getattr(record, "user_id", None),
        }
        
        # Exception details
        if record.exc_info:
            log_entry["error"] = {
                "type": record.exc_info[0].__name__ if record.exc_info[0] else None,
                "message": str(record.exc_info[1]),
                "stack_trace": traceback.format_exception(*record.exc_info),
            }
        
        # Extra fields from `extra={}` in log call
        for key, value in record.__dict__.items():
            if key not in logging.LogRecord.__dict__ and not key.startswith("_"):
                if key not in log_entry:
                    log_entry[key] = value
        
        # Remove None values to keep logs clean
        log_entry = {k: v for k, v in log_entry.items() if v is not None}
        
        return json.dumps(log_entry, default=str)

def setup_logging(level: str = "INFO"):
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(StructuredFormatter())
    
    root = logging.getLogger()
    root.setLevel(getattr(logging, level.upper()))
    root.handlers = [handler]
    
    # Quiet noisy libraries
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("boto3").setLevel(logging.WARNING)

# Context injection (async)
import contextvars

_trace_id: contextvars.ContextVar[str] = contextvars.ContextVar("trace_id", default="")
_request_id: contextvars.ContextVar[str] = contextvars.ContextVar("request_id", default="")

class ContextLogger(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        extra = kwargs.get("extra", {})
        extra["trace_id"] = _trace_id.get("")
        extra["request_id"] = _request_id.get("")
        kwargs["extra"] = extra
        return msg, kwargs

logger = ContextLogger(logging.getLogger(__name__), {})

# Usage
logger.info("Order created", extra={"order_id": "ord-123", "total_cents": 4999})
logger.error("Payment failed", extra={"order_id": "ord-123", "reason": "insufficient_funds"})
```

### Filebeat Configuration (ELK Stack)

```yaml
# /etc/filebeat/filebeat.yml
filebeat.inputs:
  # Application logs (JSON)
  - type: filestream
    id: app-logs
    paths:
      - /var/log/app/*.log
      - /var/log/app/*.json
    parsers:
      - ndjson:
          target: ""          # Merge JSON fields to top level
          overwrite_keys: true
          expand_keys: true
    fields:
      log_type: application
    processors:
      - drop_fields:
          fields: ["agent", "ecs", "input", "log.offset"]
  
  # Nginx access logs
  - type: filestream
    id: nginx-access
    paths:
      - /var/log/nginx/access.log
    fields:
      log_type: nginx_access
    processors:
      - dissect:
          tokenizer: '"%{remote_ip} - %{user} [%{timestamp}] \"%{method} %{path} %{protocol}\" %{status} %{bytes} \"%{referrer}\" \"%{user_agent}\""'
          field: message
          target_prefix: ""
  
  # Kubernetes pod logs (when running as DaemonSet)
  - type: filestream
    id: k8s-pods
    paths:
      - /var/log/pods/*/*.log
    parsers:
      - container: {}
    processors:
      - add_kubernetes_metadata:
          host: ${NODE_NAME}
          matchers:
            - logs_path:
                logs_path: "/var/log/pods/"

output.elasticsearch:
  hosts: ["${ELASTICSEARCH_URL:https://elasticsearch:9200}"]
  index: "logs-%{[fields.log_type]}-%{+yyyy.MM.dd}"
  username: "${ELASTICSEARCH_USERNAME}"
  password: "${ELASTICSEARCH_PASSWORD}"
  ssl:
    enabled: true
    ca_file: /etc/ssl/certs/ca.crt

# Retry failed events
queue.mem:
  events: 4096
  flush.min_events: 512
  flush.timeout: 5s

# Internal monitoring
monitoring:
  enabled: true
  elasticsearch:
    hosts: ["${ELASTICSEARCH_URL}"]
```

### Vector Configuration (Modern alternative to Filebeat)

```toml
# vector.toml — lightweight, high-performance log pipeline

[sources.docker_logs]
type = "docker_logs"
include_containers = []  # empty = all containers
auto_partial_merge = true

[sources.file_logs]
type = "file"
include = ["/var/log/app/*.log"]
read_from = "beginning"

# Parse JSON logs
[transforms.parse_json]
type = "remap"
inputs = ["docker_logs", "file_logs"]
source = '''
  . = parse_json!(.message)
  .host = get_hostname!()
  .ingested_at = now()
'''

# Enrich with Kubernetes metadata
[transforms.k8s_enrich]
type = "kubernetes_logs"
inputs = ["parse_json"]

# Route by log level
[transforms.route_by_level]
type = "route"
inputs = ["k8s_enrich"]
route.errors = '.level == "error" || .level == "critical"'
route.info = '.level != "error" && .level != "critical"'

# Send errors to high-priority index
[sinks.elasticsearch_errors]
type = "elasticsearch"
inputs = ["route_by_level.errors"]
endpoint = "${ELASTICSEARCH_URL}"
index = "logs-errors-%Y.%m.%d"
bulk.index = "logs-errors"
auth.strategy = "aws"  # Or "basic"

# Send all logs to main index
[sinks.elasticsearch_all]
type = "elasticsearch"
inputs = ["route_by_level.info", "route_by_level.errors"]
endpoint = "${ELASTICSEARCH_URL}"
index = "logs-all-%Y.%m.%d"

# Send critical errors to PagerDuty
[sinks.pagerduty]
type = "http"
inputs = ["route_by_level.errors"]
uri = "https://events.pagerduty.com/v2/enqueue"
method = "post"
encoding.codec = "json"
```

### Elasticsearch Index Template

```json
// PUT _index_template/logs-template
{
  "index_patterns": ["logs-*"],
  "template": {
    "settings": {
      "number_of_shards": 2,
      "number_of_replicas": 1,
      "index.lifecycle.name": "logs-ilm-policy",
      "index.lifecycle.rollover_alias": "logs",
      "refresh_interval": "5s",
      "codec": "best_compression"
    },
    "mappings": {
      "dynamic_templates": [
        {
          "strings_as_keywords": {
            "match_mapping_type": "string",
            "mapping": { "type": "keyword" }
          }
        }
      ],
      "properties": {
        "timestamp": { "type": "date" },
        "level": { "type": "keyword" },
        "service": { "type": "keyword" },
        "message": { "type": "text", "analyzer": "standard" },
        "trace_id": { "type": "keyword" },
        "request_id": { "type": "keyword" },
        "user_id": { "type": "keyword" },
        "duration_ms": { "type": "long" },
        "status_code": { "type": "short" },
        "error.type": { "type": "keyword" },
        "error.message": { "type": "text" }
      }
    }
  }
}
```

### ILM Policy (Retention)

```json
// PUT _ilm/policy/logs-ilm-policy
{
  "policy": {
    "phases": {
      "hot": {
        "actions": {
          "rollover": {
            "max_size": "50gb",
            "max_age": "1d"
          },
          "set_priority": { "priority": 100 }
        }
      },
      "warm": {
        "min_age": "2d",
        "actions": {
          "shrink": { "number_of_shards": 1 },
          "forcemerge": { "max_num_segments": 1 },
          "set_priority": { "priority": 50 }
        }
      },
      "cold": {
        "min_age": "30d",
        "actions": {
          "freeze": {},
          "set_priority": { "priority": 0 }
        }
      },
      "delete": {
        "min_age": "90d",   // 90-day retention
        "actions": {
          "delete": {}
        }
      }
    }
  }
}
```

### Loki + Grafana (Kubernetes-native)

```yaml
# loki-config.yaml
auth_enabled: false

server:
  http_listen_port: 3100
  grpc_listen_port: 9096

ingester:
  wal:
    enabled: true
    dir: /loki/wal
  lifecycler:
    ring:
      kvstore:
        store: inmemory
      replication_factor: 1
  chunk_idle_period: 5m
  chunk_retain_period: 30s

schema_config:
  configs:
    - from: 2024-01-01
      store: boltdb-shipper
      object_store: s3
      schema: v12
      index:
        prefix: index_
        period: 24h

storage_config:
  boltdb_shipper:
    active_index_directory: /loki/index
    cache_location: /loki/cache
    shared_store: s3
  aws:
    s3: s3://my-loki-bucket
    region: us-east-1

limits_config:
  retention_period: 2160h  # 90 days
  ingestion_rate_mb: 16
  ingestion_burst_size_mb: 32

---
# promtail-config.yaml (Loki shipper)
server:
  http_listen_port: 9080

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  - job_name: kubernetes-pods
    kubernetes_sd_configs:
      - role: pod
    pipeline_stages:
      - docker: {}
      - json:
          expressions:
            level: level
            message: message
            trace_id: trace_id
      - labels:
          level:
          app:
          namespace:
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_label_app]
        target_label: app
      - source_labels: [__meta_kubernetes_namespace]
        target_label: namespace
```

### CloudWatch Logs (AWS)

```python
# cloudwatch_logs.py — structured logging for Lambda/ECS
import boto3
import json
import time

def create_log_group_and_retention(log_group: str, retention_days: int = 90):
    client = boto3.client("logs")
    
    try:
        client.create_log_group(logGroupName=log_group)
    except client.exceptions.ResourceAlreadyExistsException:
        pass
    
    client.put_retention_policy(
        logGroupName=log_group,
        retentionInDays=retention_days
    )

# CloudWatch Logs Insights query examples
COMMON_QUERIES = {
    "error_rate": """
        filter level = "error"
        | stats count(*) as errors by bin(5m)
        | sort @timestamp desc
    """,
    
    "slow_requests": """
        filter duration_ms > 1000
        | fields @timestamp, service, path, duration_ms, user_id
        | sort duration_ms desc
        | limit 100
    """,
    
    "user_activity": """
        filter user_id = "{user_id}"
        | fields @timestamp, level, message, request_id
        | sort @timestamp desc
        | limit 200
    """,
    
    "trace_lookup": """
        filter trace_id = "{trace_id}"
        | fields @timestamp, service, level, message
        | sort @timestamp asc
    """
}
```

### Alerting Rules

```yaml
# ElastAlert2 config for error spike detection
name: Error Rate Spike
type: spike
index: logs-*
threshold_ref: 10
threshold_cur: 50        # 5x spike triggers alert
timeframe:
  minutes: 5
spike_height: 5
spike_type: up
filter:
  - term:
      level: error

alert: pagerduty
pagerduty_service_key: ${PAGERDUTY_KEY}
alert_text: "Error rate spike: {num_matches} errors in last 5 minutes"

---
# Grafana alert for log volume
apiVersion: 1
groups:
  - orgId: 1
    name: log-alerts
    folder: Log Monitoring
    interval: 1m
    rules:
      - uid: log-error-spike
        title: Log Error Rate High
        condition: error_count
        data:
          - refId: error_count
            queryType: range
            relativeTimeRange:
              from: 300
              to: 0
            model:
              expr: 'sum(rate({app="order-service"} |= "level=\"error\"" [5m]))'
        noDataState: OK
        execErrState: Alerting
        for: 2m
        annotations:
          summary: "High error rate in order-service"
        labels:
          severity: warning
```

## Rules

- **Structured JSON from day one** — unstructured logs are unsearchable at scale.
- **Common fields across all services** — `timestamp`, `level`, `service`, `trace_id`, `request_id`.
- **Never log PII** — no passwords, tokens, SSNs, credit card numbers in logs.
- **Use log levels correctly** — ERROR for actionable failures, WARN for degraded state, INFO for important events, DEBUG never in production.
- **Set retention policies** — unbounded log storage becomes expensive fast.
- **Correlate with traces** — `trace_id` links logs to distributed traces.
- **Test log parsing** — a misconfigured pipeline silently drops logs.
- **Monitor the pipeline itself** — alert on shipper errors, dropped events, lag.
- **Index only searchable fields** — full-text indexing of everything is expensive.
- **Separate high-volume from low-volume** — DEBUG/access logs vs. errors in different indices with different retention.
