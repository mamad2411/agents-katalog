---
name: ml-feature-store
version: 1.0.0
min_mindforge_version: 10.5.0
status: stable
triggers: ML feature store, feature engineering pipeline, feature serving architecture, offline online feature store, feature reuse pattern, feature registry, feature computation, point-in-time feature, feature freshness, feature monitoring, feature discovery, feature lineage tracking
compose:
---

# ML Feature Store Architecture

## When this skill activates

This skill activates when designing feature stores, implementing feature engineering pipelines, serving features for real-time inference, or managing feature versioning and lineage. It applies to ML systems where features must be computed consistently across training (offline) and inference (online) to avoid training-serving skew.

## Mandatory actions when this skill is active

### Before writing any code

1. **Define feature taxonomy** — Categorize features by computation type: static (user demographics, product attributes), slowly-changing (credit score, updated monthly), fast-changing (session activity, updated per event), and on-demand (real-time aggregations computed at query time). Different types require different storage and serving strategies.
2. **Design offline/online split** — Offline store (data warehouse, S3/GCS, Parquet files) for batch training. Online store (Redis, DynamoDB, Cassandra) for low-latency serving (<10ms). Define synchronization strategy: batch precompute and copy, streaming updates, or hybrid (precompute slow features, compute fast features on-demand).
3. **Establish point-in-time correctness** — Features for training must reflect the state of the world at the time the label was created. Implement temporal joins: match feature values to label timestamps within a tolerance window (e.g., use features from up to 1 hour before the event). Incorrect temporal joins cause label leakage and inflated training accuracy.
4. **Plan for feature versioning** — Features evolve (new aggregations, bug fixes, redefinitions). Version features with semantic versioning (user_clicks_v1, user_clicks_v2). Models must specify which feature versions they depend on. Changing feature definitions without versioning breaks deployed models.

### During implementation

- **Implement feature registry** — Centralized catalog of all features: name, description, data type, computation logic, dependencies, owner, and version. Registry enables feature discovery (find existing features before building new ones) and governance (track who uses which features). Use tools like Feast, Tecton, or build custom with a metadata database.
- **Build batch feature computation pipelines** — Compute features on historical data using batch processing (Spark, Dask, BigQuery). Optimize for cost: materialize expensive aggregations (rolling windows, joins) rather than recomputing on every training run. Schedule pipelines with orchestrators (Airflow, Prefect, Dagster).
- **Implement streaming feature updates** — For fast-changing features (session activity, real-time aggregations), use stream processing (Kafka + Flink, Kinesis, Spark Streaming). Update online store as events arrive. Validate that streaming logic matches batch logic (same SQL query should produce same results on batch and streaming data).
- **Design feature serving API** — Provide low-latency API to fetch features by entity key (user_id, product_id). Batch fetch for efficiency (fetch 100 user features in one call, not 100 individual calls). Return features in consistent schema (names, data types) to avoid model breakage.
- **Handle missing features gracefully** — Features may be missing (new user without history, sensor failure, data pipeline delay). Define default values (zero, mean, median, or a special sentinel value). Document defaults explicitly. Train models with synthetic missing data to ensure robustness.
- **Track feature lineage** — Record dependencies: which raw data sources produce which features, which features are used by which models. Lineage enables impact analysis: if a data source changes, which models are affected? Use metadata graphs or lineage tools (DataHub, Marquez).

### After implementation

- **Validate training-serving consistency** — Compute features offline (for training) and online (for serving) on the same input data. Compare outputs. Divergence >1% indicates a bug in feature logic. Common causes: timezone mismatches, different null handling, floating-point precision differences.
- **Measure feature freshness** — Track lag between event time and feature availability. For streaming features, target <1 minute lag. For batch features, document update frequency (hourly, daily). Stale features degrade model accuracy in production.
- **Benchmark serving latency** — Measure p50, p95, p99 latency for feature retrieval under realistic load. Target: p95 <10ms for online serving. If higher, optimize online store (better indexes, caching, denormalization) or reduce feature count.
- **Monitor feature drift** — Track feature distributions over time. If distributions shift significantly (mean, variance, or cardinality changes), model accuracy may degrade. Set up alerts for distribution drift (Kolmogorov-Smirnov test, Population Stability Index).

## Self-check before task completion

- [ ] Feature taxonomy categorizes features by computation type (static, slowly-changing, fast-changing, on-demand)
- [ ] Offline/online storage split is designed with synchronization strategy documented
- [ ] Point-in-time correctness is implemented with temporal joins (tolerance window defined)
- [ ] Feature versioning uses semantic versioning and models declare feature version dependencies
- [ ] Feature registry catalogs all features with name, description, data type, logic, dependencies, owner, version
- [ ] Batch feature pipelines materialize expensive aggregations and are scheduled with orchestrators
- [ ] Streaming feature updates match batch logic (validated with same SQL queries on batch and streaming data)
- [ ] Feature serving API supports batch fetch and returns consistent schema
- [ ] Missing features are handled with explicit defaults documented per feature
- [ ] Feature lineage tracks raw data sources → features → models for impact analysis
- [ ] Training-serving consistency is validated (offline and online feature outputs differ by <1%)
- [ ] Feature freshness is measured and documented (lag <1 minute for streaming, update frequency for batch)
- [ ] Serving latency p95 is <10ms under realistic load
- [ ] Feature drift monitoring is implemented with distribution tracking and alerts
