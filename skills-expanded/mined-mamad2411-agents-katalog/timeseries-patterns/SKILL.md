---
name: timeseries-patterns
description: "When to activate: TimescaleDB, InfluxDB, time series, time-bucketing, continuous aggregates, retention, metrics storage"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: databases
  language: sql
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---
# Time-Series Patterns

## TimescaleDB (PostgreSQL extension)

```sql
-- Enable and create hypertable
CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE metrics (
  time        TIMESTAMPTZ NOT NULL,
  device_id   TEXT NOT NULL,
  metric_name TEXT NOT NULL,
  value       DOUBLE PRECISION NOT NULL
);

SELECT create_hypertable('metrics', 'time', chunk_time_interval => INTERVAL '1 day');

-- Compression (after 7 days)
ALTER TABLE metrics SET (
  timescaledb.compress,
  timescaledb.compress_segmentby = 'device_id,metric_name',
  timescaledb.compress_orderby = 'time DESC'
);
SELECT add_compression_policy('metrics', INTERVAL '7 days');

-- Retention policy
SELECT add_retention_policy('metrics', INTERVAL '90 days');
```

## Time-Bucketing Queries

```sql
-- Downsample to 5-minute buckets
SELECT
  time_bucket('5 minutes', time) AS bucket,
  device_id,
  avg(value)   AS avg_val,
  max(value)   AS max_val,
  min(value)   AS min_val,
  count(*)     AS sample_count
FROM metrics
WHERE time > NOW() - INTERVAL '24 hours'
  AND device_id = 'sensor-01'
  AND metric_name = 'temperature'
GROUP BY bucket, device_id
ORDER BY bucket DESC;

-- Gap-filling (include missing buckets)
SELECT
  time_bucket_gapfill('1 hour', time) AS hour,
  device_id,
  locf(avg(value)) AS value_filled  -- last-observation-carried-forward
FROM metrics
WHERE time BETWEEN '2024-01-01' AND '2024-01-07'
GROUP BY hour, device_id
ORDER BY hour;
```

## Continuous Aggregates

```sql
-- Pre-compute hourly rollups automatically
CREATE MATERIALIZED VIEW metrics_hourly
WITH (timescaledb.continuous) AS
SELECT
  time_bucket('1 hour', time) AS hour,
  device_id,
  metric_name,
  avg(value) AS avg_val,
  max(value) AS max_val,
  min(value) AS min_val
FROM metrics
GROUP BY hour, device_id, metric_name
WITH NO DATA;

-- Refresh policy
SELECT add_continuous_aggregate_policy('metrics_hourly',
  start_offset => INTERVAL '3 hours',
  end_offset   => INTERVAL '1 hour',
  schedule_interval => INTERVAL '1 hour');

-- Query the aggregate (transparent routing)
SELECT * FROM metrics_hourly WHERE hour > NOW() - INTERVAL '7 days';
```

## InfluxDB Line Protocol

```
# measurement,tag_key=tag_val field_key=field_val timestamp_ns
temperature,device=sensor-01,location=room-A value=22.5 1700000000000000000
cpu,host=server-01 usage_idle=80.1,usage_user=15.2 1700000000000000000
```

```python
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

client = InfluxDBClient(url="http://localhost:8086", token="TOKEN", org="myorg")
write_api = client.write_api(write_options=SYNCHRONOUS)

point = (Point("temperature")
         .tag("device", "sensor-01")
         .field("value", 22.5)
         .time(datetime.utcnow()))
write_api.write(bucket="sensors", record=point)

# Flux query
query_api = client.query_api()
result = query_api.query('''
  from(bucket:"sensors")
    |> range(start: -1h)
    |> filter(fn: (r) => r._measurement == "temperature")
    |> aggregateWindow(every: 5m, fn: mean, createEmpty: false)
    |> yield(name: "mean")
''')
```

## Design Principles

- Always include `time` as first column / partition key
- Tag columns = low cardinality (device_id, region) → indexed
- Field columns = high cardinality measurements → not indexed
- Batch writes: 100–10k points per request
- Use continuous aggregates/rollups for dashboard queries (never raw data)
- Partition by time interval matching your retention: daily chunks for 30-90 day retention
