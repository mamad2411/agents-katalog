---
name: review-evidence-schema
description: Shared schema for evidence-backed Google review findings and remediation requirements.
tags:
  - evidence
  - schema
  - audit
---

# Review Evidence Schema

所有审计输出都应基于证据，避免泛化建议。

## Evidence IDs

推荐 ID：

- `URL-...`：页面证据。
- `LINK-...`：断链证据。
- `SIM-...`：相似度证据。
- `ADS-...`：广告库存证据。
- `TRUST-...`：信任页证据。
- `TECH-...`：robots/sitemap/ads.txt/canonical/hreflang。
- `SRC-...`：源码、模板、数据文件证据。

如果证据来自 `site-profile.json`，可以引用字段路径：

```text
profile.summary.thinPages[3]
profile.duplicatePairs[0]
profile.crossSiteSimilarPages[2]
profile.staticFiles.adsTxt
profile.brokenLinks[10]
```

## Finding Schema

```markdown
| evidence_id | severity | url_or_file | issue | why_it_matters | recommended_fix |
|-------------|----------|-------------|-------|----------------|-----------------|
```

Severity：

- `P0`：不修不建议提交审核。
- `P1`：高概率影响审核或信任。
- `P2`：应修但不一定阻塞。
- `P3`：增强建议。

## Requirement Schema

每条整改需求必须包含：

- `source_agents`
- `rejection_mapping`
- `evidence`
- `affected_urls`
- `affected_files`
- `current_risk`
- `remediation`
- `acceptance_criteria`
- `verification`
- `re_review_risk`

## Readiness Schema

最终 QA 必须输出：

```text
submit_ready: true/false
confidence: 1-10
remaining_p0: N
remaining_p1: N
evidence_profile: path
```

## 原则

- 没有证据的问题只能列为“待验证假设”。
- 多个专家发现同一问题时，合并成一个根因。
- 证据不足时，下一步是采集证据，不是猜测结论。
