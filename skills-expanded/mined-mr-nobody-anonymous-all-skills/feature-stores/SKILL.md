---
name: feature-stores
description: "Feature stores (Feast, Hopsworks): dual online/offline storage, point-in-time correctness, feature discovery, and zero training-serving skew"
category: mlops
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/mlops/feature-stores/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Feature Stores for Machine Learning

## Scope
Feature stores provide a single source of truth for machine learning features, guaranteeing point-in-time correctness during training and low-latency feature lookup during serving.

## Dual-Storage Architecture
- **Offline Store (Warehouse/Data Lake)**: S3, BigQuery, Snowflake; stores historical feature values for high-throughput batch training.
- **Online Store (Low-Latency Cache)**: Redis, Cassandra, DynamoDB; stores latest feature values for single-digit millisecond real-time inference lookup.
- **Point-in-Time Joins (Time Travel)**: Prevents data leakage by joining historical entity events with feature values valid precisely at event occurrence time.

## Tools & Platforms
- **Software**: Feast, Hopsworks, Tecton.
