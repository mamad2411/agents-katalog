---
name: tcc-deploy
description: Deploy TCC (TCE Configuration Center) configurations to PPE environments. Supports two-phase workflow — first review config changes, then confirm and execute deployment. Can create new config items or update existing ones before deploying. Also supports explicit directory creation via command=create_dir. Supports multi-region deployment (China, BOE, Singapore, US-East, US-West, EU-TTP, EU-TTP2, US-EastRed, US-TTP, US-TTP2, and more CN regions).
---

> **session_id 传递**：若本次任务需要在多次 `gdpa-cli run` 之间串联 workflow 状态、日志或上下文，请复用同一个 `session_id`。如果当前 skill / Agent 已经提供了 `session_id`，**请直接复用，不要新建**。
>
> - **已有时优先复用**：不要重复执行 `create-session`。
> - **没有时再创建**：执行 `gdpa-cli create-session`。
> - **后续调用**：可以显式传 `--session-id <session_id>`，例如 `gdpa-cli run <agent> --session-id <session_id> --input '{...}'`。
> - **适用场景**：Base Workflow、BITS Dev Workflow、post-coding-verify 及其他依赖 Session 工作目录的场景需要持续复用；普通单次查询通常可以不传。

# TCC Deploy Agent

Deploy TCC configurations to PPE environments with change review by user, or create a TCC directory explicitly.

> **When to Use**: Deploy TCC configuration changes to PPE environments, review config diffs before deployment, update and deploy config values, or create a TCC directory in a namespace/env.

> **IMPORTANT Safety Rules**:
> 1. **MUST follow two-phase workflow for deploy**: Always run review (without `confirmed`) first, show the result to the user, and wait for explicit user approval before running with `confirmed: true`. NEVER skip the review phase.
> 2. **NEVER change the target region**: Only deploy to the exact region the user requested. If a region fails (timeout, network error, etc.), report the error to the user — do NOT silently switch to a different region.
> 3. **NEVER auto-retry with different parameters**: If a deployment fails, report the failure and let the user decide what to do next.

## Quick Start

```bash
# Step 1: ALWAYS review first (dry run, vregion required)
gdpa-cli run tcc-deploy --session-id "$SESSION_ID" --input '{
  "namespace": "ttarch.gdp.gdpa",
  "conf_name": "test_config_for_script",
  "env": "ppe_test_gdpa",
  "vregion": "China-BOE"
}'
# >>> Show review result to user, wait for user to confirm <<<

# Step 2: ONLY after user confirms, deploy
gdpa-cli run tcc-deploy --session-id "$SESSION_ID" --input '{
  "namespace": "ttarch.gdp.gdpa",
  "conf_name": "test_config_for_script",
  "env": "ppe_test_gdpa",
  "vregion": "China-BOE",
  "confirmed": true
}'

# Create a new config item (config doesn't exist yet)
# Step 1: Review — returns message that config doesn't exist
gdpa-cli run tcc-deploy --session-id "$SESSION_ID" --input '{
  "namespace": "ttarch.gdp.gdpa",
  "conf_name": "new_config_item",
  "env": "ppe_test_gdpa",
  "vregion": "China-BOE"
}'
# >>> Show result to user: "config not found, needs creation". Wait for user to confirm <<<

# Step 2: ONLY after user confirms, create and deploy
gdpa-cli run tcc-deploy --session-id "$SESSION_ID" --input '{
  "namespace": "ttarch.gdp.gdpa",
  "conf_name": "new_config_item",
  "env": "ppe_test_gdpa",
  "vregion": "China-BOE",
  "new_value": "{\"key\": \"value\"}",
  "data_type": "json",
  "confirmed": true
}'

# Create a directory explicitly in the same skill
gdpa-cli run tcc-deploy --session-id "$SESSION_ID" --input '{
  "command": "create_dir",
  "namespace": "desrpc.test.client",
  "env": "ppe_bits_e2e_20260319114538",
  "dir": "/wzzd",
  "owners": ["wanzhizhen"],
  "vregion": "China-BOE"
}'

# dir path aliases are also supported
gdpa-cli run tcc-deploy --session-id "$SESSION_ID" --input '{
  "command": "create_dir",
  "namespace": "desrpc.test.client",
  "env": "ppe_bits_e2e_20260319114538",
  "directory": "wzzd",
  "vregion": "China-BOE"
}'
```

## Input Parameters

### Deploy mode required

| Parameter | Type | Description |
|-----------|------|-------------|
| `namespace` | string | TCC namespace (PSM), e.g. `ttarch.gdp.gdpa` |
| `conf_name` | string | Configuration item name |
| `env` | string | PPE environment name, e.g. `ppe_test_gdpa` |
| `vregion` | string | **Required.** VRegion for deployment target. Supported: `Singapore-Central`, `US-East`, `US-West`, `China-North`, `China-BOE`, `US-BOE`, `EU-TTP`, `EU-TTP2`, `US-EastRed`, `US-TTP`, `US-TTP2`, `China-North6`, `Aliyun_NC2`, `China-Enterprise`, `China-HKPay`, `ChinaSinf-North`, `China-East`, `China-Pay`, `China-Pay2`. Aliases: `sg`, `us`, `uswest`, `cn`, `boe`, `boei18n`, `euttp`, `euttp2`, `useastred`, `usttp`, `usttp2`, etc. See VRegion table below |

### Create directory required

| Parameter | Type | Description |
|-----------|------|-------------|
| `command` | string | Must be `create_dir` |
| `namespace` | string | TCC namespace (PSM) |
| `env` | string | PPE environment name |
| `dir` / `dir_path` / `directory` | string | Directory path to create. Leading `/` is optional |
| `vregion` | string | Target VRegion |

### Optional

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `remark` | string | - | Deployment remark |
| `enable_review` | bool | `false` | Enable TCC platform review (usually not needed, CLI-side confirmation suffices) |
| `confirmed` | bool | `false` | Set to `true` to execute deployment. Without it, only shows change diff |
| `new_value` | string | - | New config value. If provided, updates config before deploying |
| `data_type` | string | `json` | Data type used when creating a missing config via `new_value`. Supports values accepted by TCC such as `json`, `yaml`, `string` |
| `owners` | []string | current user if available | Directory owners for `command=create_dir` |

## VRegion & Cloud Gateway Mapping

| VRegion               | Aliases              | Gateway (TCCRegion) | JWT  |
|-----------------------|----------------------|---------------------|------|
| `China-North`         | `cn`, `china`        | CN                  | CN   |
| `China-East`          | `chinaeast`          | CN                  | CN   |
| `China-North6`        | `chinanorth6`, `cn6` | CN                  | CN   |
| `China-Pay`           | `chinapay`           | CN                  | CN   |
| `China-Pay2`          | `chinapay2`          | CN                  | CN   |
| `Aliyun_NC2`          | `aliyunnc2`          | CN                  | CN   |
| `China-Enterprise`    | `chinaenterprise`    | CN                  | CN   |
| `China-HKPay`         | `chinahkpay`, `hkpay`| CN                  | CN   |
| `ChinaSinf-North`     | `sinfnorth`          | CN                  | CN   |
| `China-BOE` | `boe`                | BOE                 | CN   |
| `Singapore-Central`   | `sg`                 | Singapore-Central   | i18n |
| `US-East`             | `us`, `i18n`         | US-East             | i18n |
| `US-West`             | `uswest`             | US-East             | i18n |
| `US-BOE`              | `boei18n`            | BOE-I18N            | i18n |
| `EU-TTP`              | `euttp`              | EUTTP               | i18n |
| `EU-TTP2`             | `euttp2`             | EUTTP2              | i18n |
| `US-EastRed`          | `useastred`          | US-EastRed          | i18n |
| `US-TTP`              | `usttp`, `ttp`       | USTTP               | usttp |
| `US-TTP2`             | `usttp2`, `ttp2`     | USTTP               | usttp |

## Two-Phase Workflow for Deploy (MANDATORY)

**You MUST always follow both phases for deployment. NEVER skip Phase 1.**

1. **Phase 1 — Review** (without `confirmed`): Queries config and shows diff between online version and latest version. If config doesn't exist, returns a message indicating creation is needed. **Show the result to the user and wait for explicit confirmation before proceeding.**
2. **Phase 2 — Deploy** (`confirmed: true`): ONLY after user explicitly confirms. If config doesn't exist, creates it first (requires `new_value`), then creates deployment order and executes all deployment steps.

## Create Directory Workflow

For `command=create_dir`, the skill does **not** enter the deploy/review chain.

1. Calls `CreateDir`
2. Immediately calls `ListDir`
3. Verifies the target `path` exists in the returned directory list
4. Returns success only after verification passes

## Output Format

### Review Phase

```json
{
  "success": true,
  "action": "review",
  "namespace": "ttarch.gdp.gdpa",
  "conf_name": "test_config_for_script",
  "env": "ppe_test_gdpa",
  "message": "Please review the changes above. Re-run with confirmed=true to execute deployment.",
  "changes": {
    "online_version": 5,
    "latest_version": 6,
    "online_value": "{...}",
    "latest_value": "{...}"
  }
}
```

### Deploy Phase

```json
{
  "success": true,
  "action": "deploy",
  "namespace": "ttarch.gdp.gdpa",
  "conf_name": "test_config_for_script",
  "env": "ppe_test_gdpa",
  "message": "Deployment completed successfully",
  "deployment_id": 123456
}
```

### Create Directory

```json
{
  "success": true,
  "action": "create_dir",
  "namespace": "desrpc.test.client",
  "env": "ppe_bits_e2e_20260319114538",
  "dir": "/wzzd",
  "dir_id": 1703773785832848,
  "owners": ["wanzhizhen"],
  "message": "Directory \"/wzzd\" created successfully"
}
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `namespace parameter is required` | Missing namespace | Add `namespace` parameter |
| `env parameter is required` | Missing env | Add `env` parameter |
| `vregion parameter is required` | Missing vregion | Add `vregion` parameter |
| `conf_name parameter is required` | Missing config name in deploy mode | Add `conf_name` |
| `dir parameter is required when command=create_dir` | Missing directory path in create_dir mode | Add `dir`, `dir_path`, or `directory` |
| `environment not in region` | PPE env doesn't exist in the target region | Check if the namespace has a PPE env in this region on TCC platform |
| `config 'xxx' not found` | Config doesn't exist in this env/region | Re-run with `confirmed=true` and `new_value` to create it |
| `online_version == latest_version` | No new version to deploy | Use `new_value` to create a new version |
| `no deploy strategy found` | PPE env has no deploy strategy | Check env configuration on TCC platform |
| `directory "..." was not found after CreateDir` | Post-create verification failed | Check TCC directory list and retry manually if needed |

## Notes

- **PPE Only**: This agent is designed for PPE environment deployments
- **Two-Phase Safety**: ALWAYS review first, show result to user, then deploy ONLY after user confirms. NEVER skip the review phase or auto-confirm.
- **Create Dir Is Explicit**: Directory creation only happens when `command=create_dir` is provided. Existing deploy behavior stays unchanged.
- **Post-Create Verification**: `CreateDir` success alone is not enough. The skill must confirm the directory exists via `ListDir`.
- **Region Integrity**: NEVER change the target region on your own. If a region fails, report the error — do NOT try a different region.
- **No Auto-Retry with Different Params**: If deployment fails, report to user. Do NOT silently retry with different namespace, env, region, or config name.
- **Multi-Region**: Supports deployment to different regions via `vregion` parameter, each region routes to its corresponding Cloud gateway
- **Config Update**: Use `new_value` to update config content. Always review first before deploying.
- **Config Creation Default**: When `new_value` creates a missing config, `data_type` defaults to `json` unless explicitly provided.
- **Authentication**: Uses JWT token automatically based on vregion
