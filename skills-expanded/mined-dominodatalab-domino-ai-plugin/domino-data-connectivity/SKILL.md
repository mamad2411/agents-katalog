---
name: domino-data-connectivity
description: Connect Domino executions to external data and cloud services. Covers the mechanisms Domino documents (Data Source connectors, External Data Volumes at /domino/edv/<name>, SAML-based AWS credential propagation, IAM-authenticated AWS Data Sources) and the Professional Services blueprints for AWS IRSA through Domsed, EKS Pod Identity, Azure Entra ID user-token propagation, and mounting S3 with the Mountpoint CSI driver as a Generic EDV. Use when a user asks how code in a Workspace or Job should reach S3, ADLS, Azure Blob, Snowflake or another external store, how to propagate a user's cloud identity into a workload, how to mount an NFS, EFS, SMB or S3 volume, or which of these options fits a requirement.
compatibility: Domino 6.3 and Domino Cloud. Data Sources and EDVs apply to both. Cluster-level setup (CSI drivers, Domsed mutations, Keycloak, configuration records) is a self-managed Domino 6.3 procedure; on Domino Cloud request it through Domino Support.
---

# Domino data connectivity

Applies to Domino 6.3 and Domino Cloud.

## Safety rules

The setup guides in this skill are platform-administrator procedures that change cloud IAM and
Kubernetes cluster state.

- **Explain, don't execute.** Show `aws`, `eksctl`, `helm`, `kubectl`, `az` commands and IAM
  policies for the user to review and run. Run one only when the user explicitly asks for that
  command.
- **Least privilege.** Scope every policy to named buckets, roles or resources. Never propose
  `"Resource": "*"` or wildcard actions such as `s3:*`.
- **No secrets in output.** Never print, log or echo access keys, tokens or client secrets, and
  never ask the user to paste one into the chat.
- **Read-only troubleshooting.** Prefer `get`/`describe` over `exec` into running pods.

## Which path applies

Read `GET $DOMINO_API_HOST/version` (no auth) and look at `version`:

- `6.3.x`: self-managed Domino 6.3. Your platform team administers the Kubernetes cluster,
  Keycloak and configuration records, so every mechanism below is available.
- A Domino-hosted deployment (Domino Cloud reports a line newer than 6.3): Domino
  operates the cluster. Use Data Sources and External Data Volumes (EDVs need a remote Data
  Plane on Cloud). IAM authentication, credential propagation, CSI drivers and Domsed mutations
  are requested through Domino Support; the admin pages for them exist only under `/6.3/`.

The real distinction is whether your team administers the cluster; when a self-managed line
newer than 6.3 ships, treat it like 6.3.

## Pick a mechanism

| Need | Mechanism | Set up by | Source |
|---|---|---|---|
| Query a database or read/write an object store from code | **Data Source** connector (Snowflake, Redshift, S3, ADLS, Azure Blob, BigQuery, Databricks, Postgres, MySQL, MSSQL, Oracle, GCS, Pinecone, Qdrant and others). Domino stores the credentials with the Data Source (Individual or Service Account credentials); code never handles them | User, or admin pre-configures and shares | https://docs.domino.ai/cloud/platform-capabilities/core-concepts/data/data-source-connectors |
| AWS stores without stored keys | **IAM authentication** for S3, Redshift, MySQL and PostgreSQL Data Sources: the Data Source uses the user's SAML-propagated AWS role; Workspaces and Jobs only (scheduled Jobs and endpoints need basic auth) | 6.3: admin, after SSO and AWS credential propagation, adds `AWSIAMRole` to `com.cerebro.domino.datasource.<Type>Config.enabledAuthTypes`; Cloud: Domino Support | https://docs.domino.ai/6.3/admin/data-administration/external-data#iam-authentication-for-aws-data-sources |
| Mount NFS, AWS EFS, SMB or any PVC-backed filesystem | **External Data Volume** at `/domino/edv/<name>` | Kubernetes admin labels a PVC; Domino admin registers it; users add it under **Data > External Data Volumes** | [EXTERNAL-DATA-VOLUMES.md](./EXTERNAL-DATA-VOLUMES.md) |
| Each user's own AWS roles, from SSO | **AWS credential propagation** (SAML, `AssumeRoleWithSAML`): a refreshed credentials file at `/var/lib/domino/home/.aws/credentials`, named by `AWS_SHARED_CREDENTIALS_FILE` | Admin: identity-provider settings and mappers plus configuration records on 6.3; not documented for Cloud, ask Domino Support | https://docs.domino.ai/6.3/admin/identity-and-access/authentication/sso/aws-credential-propagation |
| IAM roles for every workload type, per user or service account, cross-account | **IRSA through Domsed** or **EKS Pod Identity** (blueprints) | Platform team with Domino Professional Services | [AWS-IRSA.md](./AWS-IRSA.md) |
| An S3 bucket as a browsable local filesystem | **Mountpoint for Amazon S3 CSI driver** registered as a Generic EDV (blueprint) | Kubernetes and Domino admins | [S3-MOUNTPOINT.md](./S3-MOUNTPOINT.md) |
| Each user's Entra ID identity against Blob, ADLS Gen2, Databricks or Azure SQL | **Azure Entra user-token propagation** through Keycloak token exchange (blueprint) | Keycloak admin with Domino Professional Services | [AZURE-CREDENTIALS.md](./AZURE-CREDENTIALS.md) |
| Anything else | Install the client library, store credentials as Project or user environment variables, fetch in code; not officially supported | User | https://docs.domino.ai/cloud/platform-capabilities/core-concepts/data/access-external-data-directly |

Blueprints are Professional Services guides, indexed at
https://docs.domino.ai/cloud/examples/blueprints with code in
https://github.com/dominodatalab/domino-blueprints. They are not product documentation and change
without release notes; confirm with your Domino contact before adopting one.

Decision rules: prefer a Data Source whenever the store has a connector (shareable, audited,
no credentials in code). Use an EDV when code needs POSIX file semantics on a shared filesystem.
Use credential propagation when access must be attributable to the user in the cloud provider's
own audit log. Use Mountpoint only for S3 and only for read-heavy, large-file workloads.
Data the project produces belongs in a Domino Dataset (domino-datasets), not a new bucket.

## Quick start

Data Source from Python (the domino-data-sdk skill has the full API):

```python
from domino_data.data_sources import DataSourceClient

s3 = DataSourceClient().get_datasource("s3-datalake")
s3.download_file("raw/sales.parquet", "/tmp/sales.parquet")
```

EDV: read it as a directory. The path is listed under **Data > External Data Volumes** in the
Project.

```python
import pandas as pd

df = pd.read_parquet("/domino/edv/finance-share/datasets/sales.parquet")
```

AWS SDK with a propagated identity (SAML credential propagation or IRSA): no keys in code.

```python
import boto3

print(boto3.client("sts").get_caller_identity()["Arn"])   # confirm which identity you hold
objects = boto3.client("s3").list_objects_v2(Bucket="my-bucket", Prefix="raw/")
```

## Reference files

| File | Contents |
|---|---|
| [EXTERNAL-DATA-VOLUMES.md](./EXTERNAL-DATA-VOLUMES.md) | PVC labels and types, registration wizard, mount path, access control, troubleshooting |
| [AWS-IRSA.md](./AWS-IRSA.md) | Documented AWS options, then the IRSA and EKS Pod Identity blueprints with the Domsed mutation |
| [S3-MOUNTPOINT.md](./S3-MOUNTPOINT.md) | Mountpoint CSI driver install, PV/PVC, EDV registration, usage, limits |
| [AZURE-CREDENTIALS.md](./AZURE-CREDENTIALS.md) | Entra app, Keycloak OIDC provider and token exchange, `domino_aad` usage, RBAC |

Related skills: domino-data-sdk (Data API code), domino-datasets (Domino-managed storage),
netapp-volumes (ONTAP-backed volumes), domino-api-intro (authentication to the Domino API).
