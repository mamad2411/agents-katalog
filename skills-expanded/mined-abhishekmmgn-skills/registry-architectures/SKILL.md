---
name: registry-architectures
description: strategies for managing tool and agent assets at scale. Use this to design discovery systems, implement curated lists, and facilitate cross-team reusability through Tool and Agent Registries.
---

# Registry Architectures

## Goal
Design systematic discovery and management layers for agentic assets to prevent redundant development and solve the discovery problem in large-scale ecosystems.

## 1. Tool Registry (The Asset Catalog)
* **Definition:** A centralized system that uses protocols like MCP to catalog every asset, from local functions to enterprise APIs.
* **Usage Patterns:**
    * **Generalist Agents:** Access the full catalog, trading higher latency and lower accuracy for a broader scope of action.
    * **Specialist Agents:** Use predefined, curated subsets of the registry to maintain high performance in specific domains.
    * **Dynamic Agents:** Query the registry at runtime to dynamically adapt to and load new tools as they become available.
* **Benefits:** Facilitates human discovery (preventing duplicate tool builds), enables security auditing, and provides product owners with a clear view of current capabilities.

## 2. Agent Registry (The Expert Network)
* **Definition:** A management layer applied to agents using standardized formats like A2A Agent Cards.
* **Usage:** Helps teams across an organization discover and reuse existing specialized agents built by other departments.
* **Goal:** Lays the technical groundwork for automated agent-to-agent delegation and hierarchical scaling.

## Decision Framework for Registries
Registries offer discovery and governance at the cost of maintenance overhead. Use this framework to decide when to build one:

| Registry Type | Build When... |
| :--- | :--- |
| **Tool Registry** | Manual tool configuration becomes a bottleneck or security requires centralized, auditable access control. |
| **Agent Registry** | Multiple teams need to discover and reuse specialized agents across organizational boundaries without tight coupling. |

## Operationalizing the Mesh
* **Ontology:** Maintain a clear description and ontology of every tool and agent, including their specific requirements and capabilities.
* **Performance Tracking:** Include performance metrics (e.g., success rate, latency) within the registry to allow agents to make data-driven decisions about which peer or tool to utilize.
