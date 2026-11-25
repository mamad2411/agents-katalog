---
name: managing-lambda-labs
description: |
  Use when working with Lambda Labs — lambda Labs GPU cloud management covering
  instance inventory, GPU type availability, SSH key management, filesystem
  status, instance pricing, and capacity analysis. Use for comprehensive Lambda
  Labs workspace assessment and GPU instance optimization.
connection_type: lambda-labs
preload: false
---

# Lambda Labs Management

Analyze Lambda Labs GPU instances, availability, filesystems, and pricing.

## Phase 1: Discovery

```bash
#!/bin/bash
TOKEN="${LAMBDA_API_KEY}"
BASE="https://cloud.lambdalabs.com/api/v1"
AUTH=(-H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json")

echo "=== Running Instances ==="
curl -s "${BASE}/instances" "${AUTH[@]}" \
  | jq -r '.data[] | "\(.name // .id[0:12])\t\(.id[0:12])\t\(.status)\t\(.instance_type.name)\t\(.region.name)\t\(.ip)"' \
  | column -t | head -20

echo ""
echo "=== Instance Types & Pricing ==="
curl -s "${BASE}/instance-types" "${AUTH[@]}" \
  | jq -r '.data | to_entries[] | "\(.key)\t\(.value.instance_type.description)\tGPUs:\(.value.instance_type.specs.gpus)\tRAM:\(.value.instance_type.specs.ram)GB\t$\(.value.instance_type.price_cents_per_hour / 100)/hr"' \
  | column -t | head -15

echo ""
echo "=== GPU Availability by Region ==="
curl -s "${BASE}/instance-types" "${AUTH[@]}" \
  | jq -r '.data | to_entries[] | .key as $type | .value.regions_with_capacity_available[]? | "\($type)\t\(.name)\t\(.description)"' \
  | column -t | head -20

echo ""
echo "=== SSH Keys ==="
curl -s "${BASE}/ssh-keys" "${AUTH[@]}" \
  | jq -r '.data[] | "\(.name)\t\(.id[0:12])\t\(.public_key[0:40])..."' \
  | column -t | head -10
```

## Phase 2: Analysis

```bash
#!/bin/bash
TOKEN="${LAMBDA_API_KEY}"
BASE="https://cloud.lambdalabs.com/api/v1"
AUTH=(-H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json")

echo "=== Instance Details ==="
for INST in $(curl -s "${BASE}/instances" "${AUTH[@]}" | jq -r '.data[].id'); do
  curl -s "${BASE}/instances/${INST}" "${AUTH[@]}" \
    | jq -r '.data | "\(.name // .id[0:12])\t\(.instance_type.name)\t\(.status)\tGPUs:\(.instance_type.specs.gpus)\tVCPUs:\(.instance_type.specs.vcpus)\tRAM:\(.instance_type.specs.ram)GB\tStorage:\(.instance_type.specs.storage_in_gb)GB"' 2>/dev/null
done | column -t | head -15

echo ""
echo "=== Filesystem Attachments ==="
for INST in $(curl -s "${BASE}/instances" "${AUTH[@]}" | jq -r '.data[].id'); do
  NAME=$(curl -s "${BASE}/instances/${INST}" "${AUTH[@]}" | jq -r '.data.name // .data.id[0:12]')
  curl -s "${BASE}/instances/${INST}" "${AUTH[@]}" \
    | jq -r ".data.file_system_names[]? | \"${NAME}\t\(.)\"" 2>/dev/null
done | column -t | head -10

echo ""
echo "=== Filesystems ==="
curl -s "${BASE}/file-systems" "${AUTH[@]}" \
  | jq -r '.data[]? | "\(.name)\t\(.id[0:12])\t\(.region.name)\t\(.mount_point // "N/A")"' \
  | column -t | head -10

echo ""
echo "=== Cost Estimate ==="
INSTANCES=$(curl -s "${BASE}/instances" "${AUTH[@]}")
echo "$INSTANCES" | jq '{
  running_instances: [.data[] | select(.status == "active")] | length,
  total_hourly_cost: [.data[] | select(.status == "active") | .instance_type.price_cents_per_hour] | (add // 0) / 100,
  total_daily_est: (([.data[] | select(.status == "active") | .instance_type.price_cents_per_hour] | (add // 0) / 100) * 24),
  gpu_summary: [.data[] | .instance_type.name] | group_by(.) | map({type: .[0], count: length})
}'

echo ""
echo "=== Availability Summary ==="
curl -s "${BASE}/instance-types" "${AUTH[@]}" \
  | jq '{available_types: [.data | to_entries[] | select(.value.regions_with_capacity_available | length > 0) | .key], unavailable_types: [.data | to_entries[] | select(.value.regions_with_capacity_available | length == 0) | .key]}'
```

## Output Format

```
LAMBDA LABS ANALYSIS
======================
Instance         Type           GPUs   Region     IP              Status
──────────────────────────────────────────────────────────────────────────
ml-train-1       gpu_8x_a100    8xA100 us-tx-3    192.168.1.10    active
dev-box          gpu_1x_a10     1xA10  us-az-1    192.168.1.11    active

Running: 2 instances | GPUs: A100(8) A10(1)
Hourly Cost: $12.49 | Daily Est: $299.76
SSH Keys: 3 configured | Filesystems: 1 attached
Available Types: gpu_1x_a10, gpu_8x_a100 | Sold Out: gpu_8x_h100
```

## Safety Rules

- **Read-only**: Only use GET endpoints against the Lambda Labs API
- **Never launch or terminate** instances without confirmation
- **API keys**: Never output API key values
- **Cost awareness**: Always highlight running cost estimates for active instances

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

