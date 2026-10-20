---
name: database-replication
description: "When to activate: replication, leader-follower, CDC, Debezium, read replica, failover, logical replication, multi-master"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: databases
  language: sql
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---
# Database Replication Patterns

## PostgreSQL Logical Replication

```sql
-- Primary: enable logical replication
-- postgresql.conf: wal_level = logical

-- Create publication
CREATE PUBLICATION my_pub FOR TABLE users, orders, products;
-- Or all tables:
CREATE PUBLICATION my_pub FOR ALL TABLES;

-- Replica: create subscription
CREATE SUBSCRIPTION my_sub
  CONNECTION 'host=primary-host port=5432 dbname=app user=replicator password=secret'
  PUBLICATION my_pub;

-- Monitor replication lag
SELECT client_addr, state, sent_lsn, write_lsn, flush_lsn, replay_lsn,
  (sent_lsn - replay_lsn) AS lag_bytes
FROM pg_stat_replication;

-- On replica: check replication delay
SELECT NOW() - pg_last_xact_replay_timestamp() AS replication_lag;
```

## Change Data Capture with Debezium

```json
// Debezium connector config (Kafka Connect)
{
  "name": "postgres-cdc",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "postgres",
    "database.port": "5432",
    "database.user": "debezium",
    "database.password": "secret",
    "database.dbname": "myapp",
    "database.server.name": "myapp",
    "plugin.name": "pgoutput",
    "table.include.list": "public.users,public.orders",
    "topic.prefix": "cdc",
    "transforms": "route",
    "transforms.route.type": "org.apache.kafka.connect.transforms.ReplaceField$Value",
    "snapshot.mode": "initial"
  }
}
```

```python
# Consume CDC events from Kafka
from confluent_kafka import Consumer

consumer = Consumer({'bootstrap.servers': 'kafka:9092', 'group.id': 'cdc-consumer'})
consumer.subscribe(['cdc.public.orders'])

for msg in consumer:
    event = json.loads(msg.value())
    op = event['payload']['op']   # 'c'=create, 'u'=update, 'd'=delete, 'r'=read(snapshot)
    before = event['payload']['before']
    after  = event['payload']['after']
    if op == 'u' and after['status'] == 'completed':
        trigger_fulfillment(after['id'])
```

## MySQL Replication with GTID

```sql
-- primary my.cnf
-- server-id=1, log_bin=ON, gtid_mode=ON, enforce_gtid_consistency=ON, binlog_format=ROW

-- replica
CHANGE REPLICATION SOURCE TO
  SOURCE_HOST='primary',
  SOURCE_USER='replication_user',
  SOURCE_PASSWORD='secret',
  SOURCE_AUTO_POSITION=1,
  SOURCE_SSL=1;
START REPLICA;

-- Monitor
SHOW REPLICA STATUS\G
-- Key fields: Seconds_Behind_Source, Replica_SQL_Running, Replica_IO_Running

-- Promote replica (planned failover)
STOP REPLICA;
RESET REPLICA ALL;
-- Point app to new primary
```

## Multi-Master with CockroachDB / Galera

```sql
-- CockroachDB: distributed SQL, multi-active, geo-partitioning
-- No config needed — all nodes are equal primaries
-- Use RETURNING NOTHING for fire-and-forget writes
-- Follow-the-workload: pin rows to region
ALTER TABLE users ADD COLUMN region crdb_internal_region NOT NULL DEFAULT 'us-east1';
ALTER TABLE users SET LOCALITY REGIONAL BY ROW;  -- row-level geo partitioning

-- Galera (MySQL multi-master)
-- wsrep_provider, wsrep_cluster_address, wsrep_node_address in my.cnf
-- Writes replicated synchronously to all nodes (SST for new nodes)
-- Avoid large transactions (> 128MB) — they block cluster
```

## Replication Lag Handling

```python
# Application-level: sticky reads after write
class DBSession:
    def __init__(self, primary_url, replica_url):
        self.primary = create_engine(primary_url)
        self.replica = create_engine(replica_url)
        self._wrote_at = None

    def write(self, *args, **kwargs):
        result = self.primary.execute(*args, **kwargs)
        self._wrote_at = time.time()
        return result

    def read(self, *args, **kwargs):
        # Read from primary for 2s after write (replication window)
        if self._wrote_at and time.time() - self._wrote_at < 2.0:
            return self.primary.execute(*args, **kwargs)
        return self.replica.execute(*args, **kwargs)
```

## Monitoring Checklist

- [ ] Replication lag alert: > 30s triggers page
- [ ] Replication slot size monitored (unbounded growth fills disk)
- [ ] Failover tested in staging (automated with Patroni/ProxySQL)
- [ ] Read/write split verified (writes never hit replica)
- [ ] GTID/LSN tracked for point-in-time recovery
