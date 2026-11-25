---
name: data-to-ai-governance-10
description: The ten pairs from a Sivasankar Natarajan infographic "The Evolution of Governance - From Data to AI Systems", each mapping a data-governance practice to its AI-governance counterpart (data quality to reliable AI, lineage to bias tracking, access control to ethical use, catalog to model registry, compliance to AI regulations, ownership to model accountability, standards to training standards, version control to drift monitoring, security to AI defense, metrics to explainability), with the bridging line and an evidence question for each. Use when extending an existing data-governance programme to AI, explaining why data governance comes first, or checking a programme for gaps. Complements ai-governance-15-concepts.
---

# From data governance to AI governance: ten pairs

Source: a 12-second video of an infographic by Sivasankar Natarajan (@shiva.bytes), "The Evolution of Governance: From Data to AI Systems". Text in the first four columns is the infographic's; the evidence question is mine. The graphic's bridge lines are quoted in the third column.

| # | Data governance | Bridge line (as printed) | AI governance | Evidence to ask for [mine] |
|---|---|---|---|---|
| 1 | Data Quality: ensure data is accurate and consistent | Clean data reduces errors and model drift | Reliable AI: better data means fewer AI errors and hallucinations | Data quality checks and their results |
| 2 | Data Lineage: track where data comes from | You can't fix what you can't track | Bias Tracking: identify and reduce bias in AI decisions | Lineage from source to model input; a bias test |
| 3 | Access Control: control who can use sensitive data | Role-based access prevents wrong learning | Ethical AI Use: prevent misuse of protected information | Role list and review date |
| 4 | Data Catalog: organise and find data easily | Same concepts apply, just used differently | Model Registry: track AI models, versions and use cases | A register with owners and versions |
| 5 | Compliance: follow laws like GDPR and HIPAA | Compliance skills carry over, just on a larger scale | AI Regulations: extend to AI laws and accountability rules | A list of applicable rules and who confirmed them |
| 6 | Data Ownership: assign owners for datasets | Clear ownership avoids blame when systems fail | Model Accountability: assign responsibility for AI models and outcomes | A named owner per dataset and per model |
| 7 | Data Standards: define formats and rules for data | Standard formats ensure consistent model behavior | Training Standards: ensure consistent and valid AI training | Written training and data rules |
| 8 | Version Control: track changes in data over time | Tracking data versions explains model changes | Drift Monitoring: monitor when AI performance drops | Dataset versions linked to model versions; a drift alert |
| 9 | Security: protect data with encryption | Secure pipelines protect training data from attacks | AI Defense: defend against attacks like data poisoning | Pipeline access controls; a poisoning review |
| 10 | Metrics: measure data quality | Measuring performance helps turn data into better decisions | Explainability: ensure AI decisions are transparent and understandable | Metrics reported on a schedule; sample explanations |

## Reading it well

- **The message is sequence:** if data governance is weak, AI governance has nothing to stand on. Fix rows 1 to 4 before building rows 5 to 10.
- **Limits:** like the 15-concepts graphic it names no regulation and sets no thresholds. Row 5 says "AI laws" without naming any; find the rules that apply to you before claiming alignment. [Certain]
- **Row 2 is a stretch:** lineage helps trace where bias entered but does not itself find or reduce bias. [Likely]
- Use `ai-governance-15-concepts` for the completeness list and `/ai-governance` for the six-layer audit.
