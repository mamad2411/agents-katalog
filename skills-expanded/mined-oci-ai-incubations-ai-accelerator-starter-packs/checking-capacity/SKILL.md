---
name: checking-capacity
description: Checks hardware capacity and resource quotas across OCI regions for a given starter pack category/size or GPU shape. Audits Terraform code to discover all required resources (GPU, FSS, ADB, customer secret keys), then reports which regions can deploy the pack. Use when the user says "check capacity", "is there GPU availability", "which regions have capacity", or before deploying workloads.
user-invocable: true
allowed-tools: Bash, Read, Grep, Glob, AskUserQuestion
argument-hint: [shape-or-category] [size]
---

# Checking Capacity

Check hardware availability and resource quotas across OCI regions for a starter pack. Reports which regions can actually deploy the requested pack — ALL required resources (GPU, FSS, ADB, etc.) must pass for a region to be marked READY.

## Arguments

- `$0` — GPU shape (e.g., `BM.GPU4.8`) OR pack category (`cuopt`, `vss`, `enterprise_rag`, `enterprise_rag_aiq`, `paas_rag`)
- `$1` — Size (if category given): `poc`, `small`, `medium`

If not provided, ask the user.

**Raw shape mode:** If a raw GPU shape is given (e.g., `BM.GPU4.8`), skip Phase 1 and only check GPU capacity/quota (same as legacy behavior). All phases below apply only to category/size mode.

## Phase 1: Full Repo Audit & Build Resource Manifest

Every invocation starts by auditing the Terraform code to build the resource manifest dynamically. This ensures the manifest stays in sync with the codebase.

### Steps

1. **Discover all OCI resources:** Grep all `*.tf` files in `ai-accelerator-tf/` for `resource "oci_` to find every OCI resource type, its count/for_each condition, and which file it lives in.

2. **Map resources to categories:** For each resource, trace the count condition back to `starter_pack_category`:
   - `local.deploy_app_vss` → `vss` only
   - `local.deploy_app_26ai` / `local.needs_26ai` → check `vars.tf` for which categories are in the `contains()` list
   - `local.deploy_app_rag` → `enterprise_rag`, `enterprise_rag_aiq`
   - `local.deploy_infrastructure` → all categories (infra-layer)
   - `local.deploy_application` → all categories (app-layer)
   - Category-specific conditions like `var.starter_pack_category == "paas_rag"`

3. **Filter to quota-critical resources.** Known OCI resource type → service limit mapping:

   | OCI Resource Type | Service | Limit Name | Scope | Notes |
   |---|---|---|---|---|
   | `oci_file_storage_file_system` | `filesystem` | `file-system-count` | AD | VSS only |
   | `oci_file_storage_mount_target` | `filesystem` | `mount-target-count` | AD | VSS only |
   | `oci_database_autonomous_database` | `database` | `adw-ecpu-count`, `adw-total-storage-tb` (for default LH/DW workload) | Regional (no AD param!) | paas_rag, enterprise_rag |
   | `oci_identity_customer_secret_key` | IAM (per-user) | 2/user hard limit | User | paas_rag only |
   | `oci_objectstorage_bucket` | `objectstorage` | `bucket-count` | Regional | paas_rag only; high limit ~1000, skip check |
   | `oci_containerengine_cluster` | `container-engine` | `cluster-count` | Regional | All packs; high limit, low-priority |
   | `oci_core_vcn` / `oci_core_virtual_network` | `vcn` | `vcn-count` | Regional | All packs; high limit, low-priority |

   Any `oci_*` resource type NOT in this table → flag as **"untracked — verify if quota-gated"** and warn the user.

4. **Get per-category/size config:** Read `vars.tf` `local.starter_pack_configs` to get:
   - `worker_node_shape` and `worker_node_pool_size` (GPU)
   - `database_compute_count` and `database_storage_size_in_tbs` (ADB sizing)

5. **Print the manifest table** for the requested category/size:

```
Resource Manifest for vss/poc:
  GPU:  VM.GPU.A10.2 x 2 nodes
  FSS:  1 file system, 1 mount target
  ADB:  none
  Secret Keys: not needed
```

If any untracked resource types were found, warn:
```
WARNING: Untracked OCI resource types found — verify if quota-gated:
  - oci_some_new_resource (in some_file.tf, count = local.deploy_app_vss ? 1 : 0)
```

## Phase 2: Gather Parameters

1. Resolve category/size from arguments (or ask the user).
2. Ask for OCI CLI profile if not already known:
   ```bash
   grep '^\[' ~/.oci/config | tr -d '[]'
   ```
3. Get tenancy OCID and user OCID:
   ```bash
   export OCI_CLI_PROFILE=<profile>
   TENANCY_OCID=$(grep -A10 "^\[$PROFILE\]" ~/.oci/config | grep tenancy | head -1 | cut -d= -f2 | tr -d ' ')
   USER_OCID=$(grep -A10 "^\[$PROFILE\]" ~/.oci/config | grep user | head -1 | cut -d= -f2 | tr -d ' ')
   ```
4. List all subscribed regions:
   ```bash
   REGIONS=$(oci iam region-subscription list \
     --tenancy-id $TENANCY_OCID \
     --query 'data[].{"region-name":"region-name"}' \
     --output json | python3 -c "import json,sys; [print(r['region-name']) for r in json.load(sys.stdin)]")
   ```

**For `paas_rag`:** Do NOT exit early. Report "No GPU required" but continue to Phase 3 for ADB and customer secret key checks.

## Phase 3: Check All Resources Per Region

### Pre-flight checks (run once, not per-region)

**Customer secret key check** (if pack needs it — currently only `paas_rag`):
```bash
KEY_COUNT=$(oci iam customer-secret-key list \
  --user-id $USER_OCID \
  --all \
  --query 'data | length(@)' \
  --raw-output 2>/dev/null)
KEY_COUNT=${KEY_COUNT:-0}
```
Hard limit of 2 per user. If `KEY_COUNT >= 2`, warn: all regions will fail the secret key check unless the user pre-provides `aws_access_key_id`. This is a blocker for paas_rag — report it prominently before the region scan.

### Per-region checks

For each subscribed region, get the ADs first:
```bash
ADS=$(oci iam availability-domain list \
  --compartment-id $TENANCY_OCID \
  --region $region \
  --query 'data[].name' --raw-output 2>/dev/null)
```
If no ADs returned, skip the region.

#### GPU capacity + quota (if pack needs GPU)

Same as legacy behavior. For each AD:

```bash
# Hardware capacity
STATUS=$(oci compute compute-capacity-report create \
  --compartment-id $TENANCY_OCID \
  --region $region \
  --availability-domain "$AD" \
  --shape-availabilities "[{\"instanceShape\": \"$SHAPE\", \"faultDomain\": \"FAULT-DOMAIN-1\"}]" \
  --query 'data."shape-availabilities"[0]."availability-status"' \
  --raw-output 2>/dev/null)

# Quota (only if hardware is AVAILABLE)
oci limits resource-availability get \
  --service-name compute \
  --limit-name $GPU_LIMIT_NAME \
  --compartment-id $TENANCY_OCID \
  --availability-domain "$AD" \
  --region $region \
  --query 'data.{available:available,used:used,quota:"effective-quota-value"}' 2>/dev/null
```

**GPU Shape → Limit Name Mapping:**

| Shape | OCI Limit Name |
|---|---|
| `VM.GPU.A10.2` | `gpu-a10-count` |
| `BM.GPU4.8` | `gpu4-count` |
| `BM.GPU.A100-v2.8` | `gpu-a100-v2-8-count` |
| `BM.GPU.L40S-NC.4` | `gpu-l40s-nc-count` |

If the limit name returns empty, discover it:
```bash
oci limits definition list --service-name compute --compartment-id $TENANCY_OCID --region $region --all \
  --query "data[?contains(name, '<keyword>')].name" --output table
```

#### FSS quota (if pack needs FSS — currently only `vss`)

Check per AD (FSS is AD-scoped):
```bash
# Mount targets
oci limits resource-availability get \
  --service-name filesystem \
  --limit-name mount-target-count \
  --compartment-id $TENANCY_OCID \
  --availability-domain "$AD" \
  --region $region \
  --query 'data.{available:available,used:used,quota:"effective-quota-value"}' 2>/dev/null

# File systems
oci limits resource-availability get \
  --service-name filesystem \
  --limit-name file-system-count \
  --compartment-id $TENANCY_OCID \
  --availability-domain "$AD" \
  --region $region \
  --query 'data.{available:available,used:used,quota:"effective-quota-value"}' 2>/dev/null
```

Need: 1 mount target AND 1 file system. Fail if `available < 1` for either.

#### ADB quota (if pack needs ADB — `paas_rag`, `enterprise_rag`)

ADB limits are **regional** — do NOT pass `--availability-domain` (the API errors with "Parameter 'availabilityDomain' should be null for this limit's scope type").

The default workload type is `LH` (Lakehouse), which falls under ADW (Autonomous Data Warehouse). Check `var.db_workload_type` in `vars.tf` — if it's `LH` or `DW`, use `adw-*` limits. If `OLTP`, use `atp-*`. If `AJD`, use `ajd-*`.

**Workload type → limit name mapping:**

| db_workload_type | ECPU Limit | Storage Limit |
|---|---|---|
| `LH` (default), `DW` | `adw-ecpu-count` | `adw-total-storage-tb` |
| `OLTP` | `atp-ecpu-count` | `atp-total-storage-tb` |
| `AJD` | `ajd-ecpu-count` | `ajd-total-storage-tb` |

```bash
# ECPU availability (no --availability-domain!)
oci limits resource-availability get \
  --service-name database \
  --limit-name adw-ecpu-count \
  --compartment-id $TENANCY_OCID \
  --region $region \
  --query 'data.{available:available,used:used,quota:"effective-quota-value"}' 2>/dev/null

# Storage availability
oci limits resource-availability get \
  --service-name database \
  --limit-name adw-total-storage-tb \
  --compartment-id $TENANCY_OCID \
  --region $region \
  --query 'data.{available:available,used:used,quota:"effective-quota-value"}' 2>/dev/null
```

Need: `database_compute_count` ECPUs (4 for small, 16 for medium) AND `database_storage_size_in_tbs` TB (2 for small, 8 for medium). Fail if `available` is less than required for either.

### Error handling

- If any `oci limits` call fails (permissions, service not available), mark that resource as `UNKNOWN` with the error message. Do NOT mark the region as READY.
- If a region returns no ADs, skip it entirely.

## Phase 4: Report

### Format (example: vss/poc)

```
=== Capacity Report: vss poc ===
GPU Shape: VM.GPU.A10.2 (2 nodes)
Additional Resources: FSS (1 file system, 1 mount target)

Region              GPU HW          GPU Quota  FSS MT   Status
--------------------------------------------------------------
us-sanjose-1        AVAILABLE       4/8        0/2      x NOT READY
  +-- mount-target-count: 0 available (2 used, quota 2) [QUOTA - request increase]
ap-tokyo-1          AVAILABLE       8/8        2/2      v READY
ap-osaka-1          OUT_OF_CAPACITY 0/8        1/2      x NOT READY
  +-- GPU VM.GPU.A10.2: no hardware capacity in AD-1 [CAPACITY - try different region]
uk-london-1         NOT_SUPPORTED   --         --       x NOT READY
  +-- GPU VM.GPU.A10.2: shape not available in region [CAPACITY - try different region]

Recommended: ap-tokyo-1
```

### Format (example: paas_rag/small — no GPU)

```
=== Capacity Report: paas_rag small ===
No GPU required.
Resources: ADB (1 instance, 4 ECPU), Customer Secret Keys (need < 2 used)

Pre-flight: Customer secret keys: 1/2 used — OK

Region              ADB        Status
─────────────────────────────────────
us-sanjose-1        1/2        v READY
ap-tokyo-1          0/1        x NOT READY
  +-- autonomous-database-count: 0 available (1 used, quota 1) [QUOTA - request increase]
ap-osaka-1          2/4        v READY

Recommended: us-sanjose-1
```

### Report rules

- A region is **READY** only if ALL resources in the manifest pass (hardware available AND quota sufficient).
- Failure lines appear indented below the region row showing:
  - Resource name (OCI limit name)
  - Available count, used count, quota
  - Tag: `[QUOTA - request increase]` or `[CAPACITY - try different region]`
- GPU failures distinguish hardware capacity (`OUT_OF_CAPACITY` / `NOT_SUPPORTED`) from quota exhaustion.
- Non-GPU failures show the OCI limit name + available/used/quota numbers.
- **Recommended** = the READY region with the most quota headroom across all resources. If no region is READY, say **"No regions ready"** and the failure breakdown shows what to fix.
- Columns are dynamic — only show columns for resources the pack needs. `paas_rag` omits GPU columns; `cuopt` omits FSS/ADB columns.
- If the pre-flight customer secret key check failed, show it prominently before the region table.
