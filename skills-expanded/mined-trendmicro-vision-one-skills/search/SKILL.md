---
name: search
description: Query Cloud Provider Rules for Cloud Risk Management (CREM). Use when users ask about security best practices, compliance rules, or configuration checks for AWS, Azure, GCP, Alibaba Cloud, or Oracle/OCI cloud providers. Also handles pricing questions and general best practice queries.
---

# Cloud Security Knowledge Base Search

Query the Trend Micro knowledge base for cloud provider rules, security best practices, and compliance information.

## Instructions

1. **Identify the cloud provider** from the user's query:
   - AWS keywords: EC2, S3, Lambda, IAM, RDS, VPC, CloudFront, etc.
   - Azure keywords: Storage Account, VM, App Service, Key Vault, etc.
   - GCP keywords: Compute Engine, Cloud Storage, BigQuery, GKE, etc.
   - Alibaba keywords: ECS, OSS, ApsaraDB, etc.
   - Oracle/OCI keywords: Compute, Object Storage, Autonomous Database, etc.

2. **Determine the query type** and select the appropriate URL:
   - Specific service/rule check → Provider-specific KB URL
   - General best practices → Base KB URL
   - Pricing questions → AWS Marketplace URL

3. **Fetch the knowledge base page** using WebFetch with the provider URL

4. **Navigate to specific rules** if needed:
   - Service index pages list available rules
   - Individual rule pages contain detailed checks and remediation

5. **Extract and present** the relevant information including:
   - Rule ID and title
   - Risk level (Low, Medium, High, Very High, Extreme)
   - Description of the security issue
   - Remediation steps
   - Compliance framework mappings

## Tools

| Tool | Purpose |
|------|---------|
| `WebFetch` | Fetch knowledge base pages and extract rule information |

## Knowledge Base URLs

Route queries to the appropriate knowledge base:

| Cloud Provider | Knowledge Base URL |
|----------------|-------------------|
| AWS | https://www.trendmicro.com/cloudoneconformity/knowledge-base/aws/ |
| Azure | https://www.trendmicro.com/cloudoneconformity/knowledge-base/azure/ |
| GCP | https://www.trendmicro.com/cloudoneconformity/knowledge-base/gcp/ |
| Alibaba Cloud | https://www.trendmicro.com/cloudoneconformity/knowledge-base/alibaba-cloud/ |
| Oracle/OCI | https://www.trendmicro.com/cloudoneconformity/knowledge-base/oci/ |
| Best Practices | https://www.trendmicro.com/cloudoneconformity/knowledge-base/cloudconformity/ |
| Pricing | https://aws.amazon.com/marketplace/pp/prodview-u2in6sa3igl7c |

## Common Workflows

### Look Up a Specific Rule

1. Identify the cloud provider and service from the query
2. Fetch the provider's knowledge base index: `{provider_url}`
3. Find the service section (e.g., S3, EC2, Storage Account)
4. Fetch the specific rule page if needed
5. Present rule details with remediation steps

### Find All Rules for a Service

1. Identify the cloud provider and service
2. Fetch the service index page: `{provider_url}{service}/`
3. List available rules with risk levels
4. Offer to provide details on specific rules

### General Best Practices Query

1. Fetch the base knowledge base URL
2. Search for relevant categories or topics
3. Summarize applicable best practices

### Pricing Information

1. Fetch the AWS Marketplace URL
2. Extract pricing tiers and features
3. Present pricing information clearly

## Output Format

When presenting rule information:

```
## [Rule ID]: [Rule Title]

**Risk Level**: [Low|Medium|High|Very High|Extreme]
**Service**: [Cloud Service Name]
**Provider**: [AWS|Azure|GCP|Alibaba|OCI]

### Description
[What the rule checks and why it matters]

### Remediation
[Step-by-step instructions to fix the issue]

### Compliance
[Relevant frameworks: CIS, PCI-DSS, SOC2, etc.]
```

## Example Queries

| User Query | Action |
|------------|--------|
| "S3 bucket encryption best practices" | Fetch AWS KB, find S3 encryption rules |
| "Azure storage public access" | Fetch Azure KB, find storage account rules |
| "GCP firewall rules" | Fetch GCP KB, find VPC firewall rules |
| "What does it cost?" | Fetch AWS Marketplace pricing page |
| "Cloud security best practices" | Fetch general KB |

## Security Considerations

- This skill accesses publicly available documentation only
- No authentication or API keys required
- Use alongside `vision-one:cloud-posture` for actual compliance scanning
- Knowledge base content is maintained by Trend Micro security researchers
