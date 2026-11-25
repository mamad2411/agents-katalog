# OSINT-NEXUS

An “all-source” real-time conflict monitoring platform: ingests RSS/news + Telegram + ADS-B flight tracking + maritime AIS + civil defense alerts, fuses events into a Neo4j temporal knowledge graph, and uses LLM reasoning to produce SITREPs, causal chains, contradiction detection, and “priority action” rankings. Surfaces confidence/corroboration/freshness scoring, includes a disinfo/coordinated-emergence detector (sliding ~45-min window), and ships with a fairly complete stack (FastAPI + Postgres/PostGIS + Neo4j + Redis + Next.js, docker-compose). Mentions MGRS coordinate outputs and an analyst-centric “explain why ranked #1” UI.

## Triggers
- "osint nexus"
- "conflict monitoring"
- "real time osint"
- "sitreps generation"
- "priority action ranking"
- "disinfo detection"

## Description
OSINT-NEXUS is a comprehensive real-time conflict monitoring platform that ingests multiple data sources (RSS/news, Telegram, ADS-B flight tracking, maritime AIS, civil defense alerts) and fuses them into a temporal knowledge graph using Neo4j. It leverages LLM reasoning to generate Situation Reports (SITREPs), identify causal chains, detect contradictions, and rank priority actions. The system includes confidence scoring, a disinformation detector, and a full technology stack for deployment.

## Features
- Multi-source ingestion: RSS/news, Telegram, ADS-B, maritime AIS, civil defense alerts
- Neo4j temporal knowledge graph for event fusion
- LLM reasoning for SITREP generation
- Causal chain analysis
- Contradiction detection
- Priority action ranking
- Confidence, corroboration, and freshness scoring
- Disinformation/coordinated-emergence detector (sliding 45-minute window)
- MGRS coordinate outputs
- Analyst-centric "explain why ranked #1" UI
- Full stack: FastAPI + Postgres/PostGIS + Neo4j + Redis + Next.js
- Docker-compose deployment

## Usage
Use when you need to monitor real-time conflicts or crises from multiple open-source intelligence feeds and produce actionable intelligence products.

## Example
```
/osint-nexus start monitoring ukraine conflict
/osint-nexus generate sitrep for middle east tensions
/osint-nexus check disinformation on viral claim
/osint-nexus show priority actions for taiwan strait
/osint-nexus explain why action #1 is ranked highest
```
