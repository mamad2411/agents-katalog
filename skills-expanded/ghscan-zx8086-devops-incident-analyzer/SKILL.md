---
name: cite-sources
description: Require every factual claim in an analysis to be traceable to a specific tool output -- name the tool and datasource, include the concrete supporting data point, and mark inferences explicitly as hypotheses rather than findings. Applies to the orchestrator and every sub-agent on every turn that states a finding.
---

# Skill: Cite Sources

## Purpose
Every factual claim in an analysis must be traceable to a specific tool output.
This shared skill applies to the orchestrator and every sub-agent.

## Procedure
1. When you state a finding, name the tool that produced it and the datasource
   it came from (e.g. "per `elasticsearch_search` on the prod deployment").
2. Include the concrete data point that supports the claim: a timestamp, a metric
   value, a count, an error string, or a document/record id.
3. When correlating across datasources, cite each contributing source separately
   so a reviewer can audit which evidence supports which leg of the correlation.
4. If a claim cannot be tied to a tool output, mark it explicitly as an inference
   or hypothesis, not a finding.

## Rules
- No uncited findings. An assertion without a tool-output citation is a defect.
- Prefer the narrowest citation that supports the claim (one tool call, one
  record) over a vague "the logs show".
- Never fabricate a citation. If you did not run the tool, do not cite it.
